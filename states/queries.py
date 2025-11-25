from functools import wraps

import data.db_connect as dbc
from data.db_connect import is_valid_id

STATE_COLLECTION = 'states'
ID = 'id'
NAME = 'name'
CODE = 'code'
COUNTRY_CODE = 'country_code'

SAMPLE_CODE = 'NY'
SAMPLE_COUNTRY = 'USA'
SAMPLE_KEY = (SAMPLE_CODE, SAMPLE_COUNTRY)
SAMPLE_STATE = {
    NAME: 'New York',
    CODE: SAMPLE_CODE,
    COUNTRY_CODE: SAMPLE_COUNTRY
}

cache = None

def needs_cache(fn, *args, **kwargs):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not cache:
            load_cache()
        return fn(*args, **kwargs)
    return wrapper
    
@needs_cache
def count():
    return len(cache)
    
@needs_cache
def read():
    return cache
    
def load_cache():
    global cache
    cache = {}
    states = dbc.read(STATE_COLLECTION)
    for state in states:
        cache[(state[CODE], state[COUNTRY_CODE])] = state

def main():
    create(SAMPLE_STATE)
    print(read())
    
if __name__ == '__main__':
    main()
