import sys
import csv

from states.queries import (
    COUNTRY_CODE,
    create,
)

CURR_COUNTRY = 'USA'

def main():
    exit(1)
    state_list = extract(sys.argv[1])
    rev_list = transform(state_list)
    load(rev_list)