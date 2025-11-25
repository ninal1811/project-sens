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

def main():
    create(SAMPLE_STATE)
    print(read())
    
if __name__ == '__main__':
    main()
