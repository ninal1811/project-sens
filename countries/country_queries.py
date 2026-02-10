from functools import wraps

import data.db_connect as dbc
import logging
logging.basicConfig(level=logging.INFO)

MIN_ID_LEN = 3  # ISO-3 Country Code
COUNTRY_COLLECTION = "countries"

ID = "_id"
NAME = "name"
CAPITAL = "capital"
NATIONAL_DISH = "nat_dish"
POP_DISH_1 = "pop_dish_1"
POP_DISH_2 = "pop_dish_2"

country_cache = None


def needs_cache(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if country_cache is None:
            load_cache()
        return fn(*args, **kwargs)
    return wrapper


def load_cache() -> None:
    global country_cache
    country_cache = {}

    try:
        docs = dbc.read(COUNTRY_COLLECTION, no_id=False)
    except Exception:
        docs = []

    for doc in docs:
        cid = doc.get(ID)
        if cid is not None:
            country_cache[cid] = doc


@needs_cache
def get_country(country_id) -> dict:
    """
    Retrieve a country by ID.

    Note: Unit tests use integer IDs (e.g., 1), so we accept any hashable ID.
    """
    doc = country_cache.get(country_id)
    if doc is not None:
        return doc

    try:
        doc = dbc.read_one(COUNTRY_COLLECTION, {ID: country_id})
    except Exception:
        doc = None

    if doc is None:
        raise ValueError(f"No such country with id {country_id}.")

    country_cache[country_id] = doc
    return doc


def add_country(country_id: str, name: str, capital: str, **extra_fields) -> None:
    """
    Add or update a country with all its fields.
    extra_fields can include: nat_dish, pop_dish_1, pop_dish_2, etc.
    """
    doc = {
        ID: country_id,
        NAME: name,
        CAPITAL: capital,
        **extra_fields  # This adds any additional fields like nat_dish, pop_dish_1, etc.
    }
    result = dbc.update(COUNTRY_COLLECTION, {ID: country_id}, doc)
    if result.matched_count == 0:
        dbc.create(COUNTRY_COLLECTION, doc)
    load_cache()


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


def delete_country(country_id: str) -> bool:
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
def get_national_dish_by_name(name: str) -> str:
    for doc in country_cache.values():
        if doc.get(NAME) == name:
            return doc.get(NATIONAL_DISH, "")
    raise ValueError(f"No country found with name {name}")


@needs_cache
def get_popular_dishes_by_name(name: str) -> list:
    for doc in country_cache.values():
        if doc.get(NAME) == name:
            dishes = []
            if doc.get(POP_DISH_1):
                dishes.append(doc[POP_DISH_1])
            if doc.get(POP_DISH_2):
                dishes.append(doc[POP_DISH_2])
            return dishes
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
    if not capital.strip():
        return False
    return True


def is_valid_id(_id: str) -> bool:
    if not isinstance(_id, str):
        return False
    _id = _id.strip().upper()
    if len(_id) != MIN_ID_LEN:
        return False
    if not _id.isalpha():
        return False
    return True
