from copy import deepcopy
from unittest.mock import patch
import pytest

import states.queries as qry

@pytest.fixture(scope='function')
def temp_state_no_del():
    temp_rec = get_temp_rec()
    qry.create(get_temp_rec())
    return temp_rec
    
@pytest.fixture(scope='function')
def temp_state():
    temp_rec = get_temp_rec()
    new_rec_id = qry.create(get_temp_rec())
    yield new_rec_id
    try:
        qry.delete(temp_rec[qry.CODE], temp_rec[qry.COUNTRY_CODE])
    except ValueError:
        print('The record was already deleted.')

def get_temp_rec():
    return deepcopy(qry.SAMPLE_STATE)
    
def test_count():
    old_count = qry.count()
    qry.create(get_temp_rec())
    assert qry.count() == old_count + 1
    qry.delete(qry.SAMPLE_CODE, qry.SAMPLE_COUNTRY)
    
def test_good_create():
    old_count = qry.count()
    new_rec_id = qry.create(get_temp_rec())
    assert qry.is_valid_id(new_rec_id)
    assert qry.count() == old_count + 1
    qry.delete(qry.SAMPLE_CODE, qry.SAMPLE_COUNTRY)
