from functools import wraps

import data.db_connect as dbc

CITY_COLLECTION = 'cities'

CITY = 'city'
STATE_CODE = 'state_code'
COUNTRY_CODE = 'country_code'
REC_RESTAURANT = 'rec_restaurant'

cache = None


def needs_cache(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global cache
        if not cache:
            load_cache()
        return fn(*args, **kwargs)
    return wrapper

@needs_cache
def count() -> int:
    return len(cache)

@needs_cache
def read() -> dict:
    return {city_name: doc for (city_name, _st, _cc), doc in cache.items()}

def load_cache():
    global cache
    cache = {}
    cities = dbc.read(CITY_COLLECTION)
    for city_doc in cities:
        cache[(city_doc[CITY], city_doc[STATE_CODE], city_doc[COUNTRY_CODE])] = city_doc

@needs_cache
def add_city(country_code: str, state_code: str, city_name: str, rec_restaurant: str, **extra_fields) -> None:
    doc = {
        CITY: city_name,
        STATE_CODE: state_code,
        COUNTRY_CODE: country_code,
        REC_RESTAURANT: rec_restaurant,
        **extra_fields,
    }

    result = dbc.update(
        CITY_COLLECTION,
        {CITY: city_name, STATE_CODE: state_code, COUNTRY_CODE: country_code},
        doc
    )
    if result.matched_count == 0:
        dbc.create(CITY_COLLECTION, doc)

    load_cache()

@needs_cache
def get_city(city_name: str, state_code: str, country_code: str) -> dict:
    """Retrieve a city record by ID."""
    key = (city_name, state_code, country_code)
    doc = cache.get(key)
    if doc is None:
        query = {CITY: city_name, STATE_CODE: state_code, COUNTRY_CODE: country_code}
        doc = dbc.read_one(CITY_COLLECTION, query)
        if doc is None:
            raise ValueError(f"City not found: {city_name}, {state_code}, {country_code}")
        cache[key] = doc
    return doc

@needs_cache
def get_cities_by_state(state_code: str) -> dict:
    sc = state_code.strip().upper()
    return {city_name: doc for (city_name, st, _cc), doc in cache.items() if st == sc}


@needs_cache
def get_city_by_name(city_name: str) -> dict:
    matches = [doc for (nm, _, _), doc in cache.items() if nm == city_name]
    if not matches:
        raise ValueError(f"City not found: {city_name}")
    if len(matches) > 1:
        raise ValueError(f"Ambiguous city name: {city_name}")
    return matches[0]

def create(name: str, details: dict) -> str:
    doc = {CITY: name, **(details or {})}
    doc.setdefault(STATE_CODE, "N/A")
    doc.setdefault(COUNTRY_CODE, "N/A")
    doc.setdefault(REC_RESTAURANT, "N/A")
    return create_doc(doc)


def delete_city(city_name: str, state_code: str, country_code: str) -> bool:
    """Delete a city"""
    ret = dbc.delete(CITY_COLLECTION, {CITY: city_name, STATE_CODE: state_code, COUNTRY_CODE: country_code})
    if ret < 1:
        raise ValueError(f"City not found: {city_name}, {state_code}, {country_code}")
    load_cache()
    return True

def delete_city_by_name(city_name: str) -> bool:
    ret = dbc.delete(CITY_COLLECTION, {CITY: city_name})
    if ret < 1:
        raise ValueError(f"City not found: {city_name}")
    load_cache()
    return True

def delete(city_name: str) -> bool:
    return delete_city_by_name(city_name)

def update_city(city_name: str, state_code: str, country_code: str, new_data: dict) -> bool:
    """Update an existing city record."""
    if not new_data:
        raise ValueError("No update data provided")
    query = {CITY: city_name, STATE_CODE: state_code, COUNTRY_CODE: country_code}
    ret = dbc.update(CITY_COLLECTION, query, new_data)
    if ret.modified_count < 1:
        raise ValueError(
            f"City not found: {city_name}, {state_code}, {country_code}"
        )
    load_cache()
    return ret.modified_count


def create_doc(data: dict) -> str:
    print(f'{data=}')
    if not isinstance(data, dict):
        raise ValueError(f'Bad type for {type(data)=}')
    if not data.get(CITY):
        raise ValueError(f'Bad type for {data.get(CITY)=}')
    new_id = dbc.create(CITY_COLLECTION, data)
    print(f'{new_id=}')
    load_cache()
    return str(new_id.inserted_id)

@needs_cache
def read_one(city_name: str, state_code: str, country_code: str) -> dict:
    key = (city_name, state_code, country_code)
    if key not in cache:
        raise ValueError(f"City not found: {city_name}, {state_code}, {country_code}")
    return cache[key]

def main():
    load_cache()
    print(f"Loaded {len(cache)} cities into cache")


if __name__ == '__main__':
    main()
