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

def create(data, dict):
    if not isinstance(data, dict):
        raise ValueError(f'Bad type for {type(data)=}')
    if not data.get(NAME):
        raise ValueError(f'Bad type for {data.get(NAME)=}')
    new_id = str(len(city_cache) + 1)
    city_cache[new_id] = data
    return new_id

def num_cities():
    return len(city_cache)

