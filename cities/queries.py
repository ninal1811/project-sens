import data.db_connect as dbc

MIN_ID_LEN = 1
CITY_COLLECTION = 'cities'

ID = 'id'
NAME = 'name'
STATE_CODE = 'state_code'

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

def get_city(city_id: str) -> dict:
    """Retrieve a city record by ID."""
    if city_id not in city_cache:
        raise ValueError(f'City with ID {city_id} not found.')
    return city_cache[city_id]

def delete(name: str, state_code: str) -> bool:
    ret = dbc.delete(CITY_COLLECTION, {NAME: name, STATE_CODE: state_code})
    if ret < 1:
        raise ValueError(f'City not found: {name}, {state_code}')
    return ret

def create(data: dict) -> str:
    print(f'{data=}')
    if not isinstance(data, dict):
        raise ValueError(f'Bad type for {type(data)=}')
    if not data.get(NAME):
        raise ValueError(f'Bad type for {data.get(NAME)=}')
    new_id = dbc.create(CITY_COLLECTION, data)
    print(f'{new_id=}')
    return new_id


def num_cities() -> int:
    return len(read())
    
def is_valid_id(_id: str) -> bool:
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True

def read() -> dict:
    return dbc.read(CITY_COLLECTION)

def main():
    print(read())
    try:
        city = get_city('1')
        print(f"Retrieved city: {city}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__=='__main__':
    main()

