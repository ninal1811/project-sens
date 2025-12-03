import sys
import csv

from states.queries import (
    COUNTRY_CODE,
    create,
)

CURR_COUNTRY = 'USA'

def extract(flnm: str) -> list:
    state_list = []

def transform(state_list: list) -> list:
    rev_list = []
    col_names = state_list.pop(0)
    for state in state_list:
        state_dict = {}
        for i, fld in enumerate(col_names):
            state_dict[fld] = state[i]
        state_dict[COUNTRY_CODE] = CURR_COUNTRY
        rev_list.append(state_dict)
    return rev_list


def load(rev_list: list):
    for state in rev_list:
        create(state, reload=False)

def main():
    exit(1)
    state_list = extract(sys.argv[1])
    rev_list = transform(state_list)
    load(rev_list)