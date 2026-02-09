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
        if cache is None:
            load_cache()
        return fn(*args, **kwargs)
    return wrapper


def load_cache():
    global cache
    cache = {}
    cities = dbc.read(CITY_COLLECTION)
    for city in cities:
        key = (city[CITY], city[STATE_CODE], city[COUNTRY_CODE])
        cache[key] = city


SAMPLE_CITY = {
    CITY: 'New York City',
    STATE_CODE: 'NY',
}


# using the ID as the key
city_cache = {
    1: SAMPLE_CITY,
    2: {
        CITY: 'New Orleans',
        STATE_CODE: 'LA',
    },
}


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
    """Retrieve all cities that match the given state code"""
    if not isinstance(state_code, str) or not state_code:
        raise ValueError(f"Bad state code: {state_code}")
    return {key: city for key, city in cache.items() if key[1] == state_code}


def delete_city(city_name: str, state_code: str, country_code: str) -> bool:
    """Delete a city"""
    ret = dbc.delete(CITY_COLLECTION, {CITY: city_name, STATE_CODE: state_code, COUNTRY_CODE: country_code})
    if ret < 1:
        raise ValueError(f"City not found: {city_name}, {state_code}, {country_code}")
    load_cache()
    return True


def update_city(city_name: str, state_code: str, country_code: str, new_data: dict) -> bool:
    """Update an existing city record."""
    if not new_data:
        raise ValueError("No update data provided")
    query = {CITY: city_name, STATE_CODE: state_code, COUNTRY_CODE: country_code}
    ret = dbc.update(CITY_COLLECTION, query, new_data)
    if ret.modified_count < 1:
        raise ValueError(
            f"No city found to update: {city_name}, {state_code}, {country_code}"
        )
    load_cache()
    return True


def create(data: dict) -> str:
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
def num_cities() -> int:
    return len(read())


@needs_cache
def read() -> dict:
    return dbc.read(CITY_COLLECTION)


def main():
    print(read())
    try:
        city = get_city('1')
        print(f"Retrieved city: {city}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
