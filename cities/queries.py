from random import randint

MIN_ID_LEN = 1

ID = 'id'
NAME = 'name'
STATE_CODE = 'state_code'

SAMPLE_CITY_1 = {
    NAME: 'New York City',
    STATE_CODE: 'NY',
}

SAMPLE_CITY_2 = { 
    NAME: 'New Orleans',
    STATE_CODE: 'LA',
}

# using the ID as the key
city_cache = {
    1: SAMPLE_CITY_1,
    2: SAMPLE_CITY_2,
}

def get_city(city_id: str) -> dict:
    """Retrieve a city record by ID."""
    if city_id not in city_cache:
        raise ValueError(f'City with ID {city_id} not found.')
    return city_cache[city_id]

def db_connect(success_ratio: int) -> bool:
    # returns True if connected to the DB, False otherwise
    return randint(1, success_ratio) % success_ratio

def delete(city_id: str) -> bool:
    if city_id not in city_cache:
        raise ValueError(f'No such city: {city_id}')
    del city_cache[city_id]
    return True

def create(data: dict) -> str:
    if not isinstance(data, dict):
        raise ValueError(f'Bad type for {type(data)=}')
    if not data.get(NAME):
        raise ValueError(f'Bad type for {data.get(NAME)=}')
    new_id = str(len(city_cache) + 1)
    city_cache[new_id] = data
    return new_id


def num_cities() -> int:
    return len(city_cache)
    
def is_valid_id(_id: str) -> bool:
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True

def read() -> dict:
    if not db_connect(3):
        raise ConnectionError('Could not connect to DB.')
    return city_cache

def main():
    print(read())
    try:
        city = get_city('1')
        print(f"Retrieved city: {city}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__=='__main__':
    main()

