from functools import wraps

import data.db_connect as dbc

MIN_ID_LEN = 1
CITY_COLLECTION = 'cities'

ID = '_id'
NAME = 'name'
STATE_CODE = 'state_code'

cache = None


def needs_cache(fn, *args, **kwargs):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if cache is None:
            load_cache()
        return fn(*args, **kwargs)
    return wrapper


def load_cache():
    global cache
    cache = {}
    docs = dbc.read(CITY_COLLECTION)
    for doc in docs:
        cid = doc.get(ID)
        if cid is not None:
            cache[cid] = doc


SAMPLE_CITY = {
    NAME: 'New York City',
    STATE_CODE: 'NY',
}


# using the ID as the key
city_cache = {
    1: SAMPLE_CITY,
    2: {
        NAME: 'New Orleans',
        STATE_CODE: 'LA',
    },
}


@needs_cache
def get_city(city_id: str) -> dict:
    """Retrieve a city record by ID."""
    if not is_valid_id(city_id):
        raise ValueError(f"Invalid ID: {city_id}")
    doc = cache.get(city_id)
    if doc is None:
        doc = dbc.read_one(CITY_COLLECTION, {ID: city_id})
        if doc is None:
            raise ValueError(f'City with ID {city_id} not found.')
        cache[city_id] = doc
    return doc


@needs_cache
def get_cities_by_state(state_code: str) -> dict:
    """Retrieve all cities that match the given state code"""
    if not isinstance(state_code, str) or not state_code:
        raise ValueError(f'Bad state code: {state_code}')
    cities = dbc.read(CITY_COLLECTION, no_id=False)  # returns a list of docs
    return {
        city[ID]: city
        for city in cities
        if city.get(STATE_CODE) == state_code
    }


def delete(name: str, state_code: str) -> bool:
    ret = dbc.delete(CITY_COLLECTION, {NAME: name, STATE_CODE: state_code})
    if ret < 1:
        raise ValueError(f'City not found: {name}, {state_code}')
    load_cache()
    return ret


def update_city(city_id: str, new_data: dict) -> bool:
    if not is_valid_id(city_id):
        raise ValueError(f"Invalid ID: {city_id}")
    if not new_data:
        raise ValueError("No update data provided.")
    ret = dbc.update(CITY_COLLECTION, {ID: city_id}, new_data)
    if ret < 1:
        raise ValueError(f"No city found to update: {city_id}")
    load_cache()
    return True


def create(data: dict) -> str:
    print(f'{data=}')
    if not isinstance(data, dict):
        raise ValueError(f'Bad type for {type(data)=}')
    if not data.get(NAME):
        raise ValueError(f'Bad type for {data.get(NAME)=}')
    new_id = dbc.create(CITY_COLLECTION, data)
    print(f'{new_id=}')
    load_cache()
    return str(new_id.inserted_id)


@needs_cache
def num_cities() -> int:
    return len(read())


def is_valid_id(_id: str) -> bool:
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True


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
