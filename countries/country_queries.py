from functools import wraps

import data.db_connect as dbc
import logging
logging.basicConfig(level=logging.INFO)

MIN_ID_LEN = 1
COUNTRY_COLLECTION = "countries"

ID = "_id"
NAME = "name"
CAPITAL = "capital"

country_cache = None


def needs_cache(fn, *args, **kwargs):
    """
    Ensure the country cache is loaded before calling fn.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if country_cache is None:
            load_cache()
        return fn(*args, **kwargs)
    return wrapper


def load_cache() -> None:
    """
    Load all countries from database into memory cache, keyed by ID.
    """
    global country_cache
    country_cache = {}
    docs = dbc.read(COUNTRY_COLLECTION)
    for doc in docs:
        cid = doc.get(ID)
        if cid is not None:
            country_cache[cid] = doc


def add_country(country_id: int, name: str, capital: str) -> None:
    doc = {
        ID: country_id,
        NAME: name,
        CAPITAL: capital,
    }
    result = dbc.update(COUNTRY_COLLECTION, {ID: country_id}, doc)
    if result.matched_count == 0:
        dbc.create(COUNTRY_COLLECTION, doc)
    load_cache()


@needs_cache
def get_country(country_id: int) -> dict:
    """Retrieve a country by ID."""
    logging.info(f"Fetching country with ID: {country_id}")
    doc = country_cache.get(country_id)

    if doc is None:
        # Optional: fall back to DB in case cache is somehow stale
        doc = dbc.read_one(COUNTRY_COLLECTION, {ID: country_id})
        if doc is None:
            raise ValueError(f"No such country with id {country_id}.")
        country_cache[country_id] = doc

    return doc


@needs_cache
def search_country(keyword: str) -> dict:
    if not keyword:
        raise ValueError("Keyword must not be empty.")
    keyword_lower = keyword.lower()

    return {
        cid: c
        for cid, c in country_cache.items()
        if isinstance(c.get(NAME), str) and keyword_lower in c[NAME].lower()
    }


def delete_country(country_id: int) -> bool:
    result = dbc.delete(COUNTRY_COLLECTION, {ID: country_id})
    if result < 1:
        raise ValueError(f"Country with id {country_id} not found.")
    load_cache()
    return True


@needs_cache
def get_capital_by_name(name: str) -> str:
    for doc in country_cache.values():
        if doc.get(NAME) == name:
            return doc[CAPITAL]
    raise ValueError(f"No country found with name {name}")


@needs_cache
def num_countries() -> int:
    return len(country_cache)


@needs_cache
def country_exists(name: str) -> bool:
    if not isinstance(name, str):
        return False
    return any(doc.get(NAME) == name for doc in country_cache.values())


@needs_cache
def read_all() -> dict:
    return country_cache


def is_valid_capital(capital: str) -> bool:
    if not isinstance(capital, str):
        logging.error("Invalid type for capital. Capital should be a string.")
        return False


def is_valid_id(_id: str) -> bool:
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True
