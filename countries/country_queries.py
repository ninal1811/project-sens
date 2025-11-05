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
    """Add a country to the cache."""
    country_cache[country_id] = {NAME: name, CAPITAL: capital}


def get_country(country_id: int) -> dict:
    """Retrieve a country by ID."""
    logging.info(f"Fetching country with ID: {country_id}")
    if country_id not in country_cache:
        raise ValueError(f"No such country with id {country_id}.")
    return country_cache[country_id]


def num_countries() -> int:
    return len(country_cache)


def read_all() -> dict:
    return country_cache
