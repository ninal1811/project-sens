import data.db_connect as dbc
import logging
logging.basicConfig(level=logging.INFO)

MIN_ID_LEN = 1
COUNTRY_COLLECTION = "countries"

ID = "id"
NAME = "name"
CAPITAL = "capital"

country_cache = {
    1: {
        NAME: "United States",
        CAPITAL: "Washington, DC",
    },
    2: {
        NAME: "France",
        CAPITAL: "Paris",
    },
}

def add_country(country_id: int, name: str, capital: str) -> None:
    doc = {
        ID: country_id,
        NAME: name,
        CAPITAL: capital,
    }
    result = dbc.update(COUNTRY_COLLECTION, {ID: country_id}, doc)
    if result.matched_count == 0:
        dbc.create(COUNTRY_COLLECTION, doc)


def get_country(country_id: int) -> dict:
    """Retrieve a country by ID."""
    logging.info(f"Fetching country with ID: {country_id}")
    doc = dbc.read_one(COUNTRY_COLLECTION, {ID: country_id})
    if doc is None:
        raise ValueError(f"No such country with id {country_id}.")
    return doc

def search_country(keyword: str) -> dict:
    if not keyword:
        raise ValueError("Keyword must not be empty.")
    keyword_lower = keyword.lower()
    all_countries = read_all()  # dict keyed by ID

    return {
        cid: c
        for cid, c in all_countries.items()
        if isinstance(c.get(NAME), str)
        and keyword_lower in c[NAME].lower()
    }

def delete_country(country_id: int) -> bool:
    result = dbc.delete(COUNTRY_COLLECTION, {ID: country_id})
    if result < 1:
        raise ValueError(f"Country with id {country_id} not found.")
    return True

def get_capital_by_name(name: str) -> str:
    docs = dbc.read_one(COUNTRY_COLLECTION, {NAME: name})
    if docs is None:
        raise ValueError(f"No country found with name {name}")
    return docs[CAPITAL]

def num_countries() -> int:
    return len(read_all())

def country_exists(name: str) -> bool:
    if not isinstance(name, str):
        return False
    doc = dbc.read_one(COUNTRY_COLLECTION, {NAME: name})
    return doc is not None

def read_all() -> dict:
    docs = dbc.read(COUNTRY_COLLECTION)
    countries_by_id = {}
    for doc in docs:
        cid = doc.get(ID)
        if cid is not None:
            countries_by_id[cid] = doc
    return countries_by_id

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

