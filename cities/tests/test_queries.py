from unittest.mock import patch
import pytest

from cities.queries as qry

@pytest.mark.skip('This is an example of a bad test!')
def test_bad_test_from_num_cities():
    assert qry.num_cities() == len(qry.city_cache)
    
def test_num_cities():
    old_count = qry.num_cities()
    qry.create(qry.SAMPLE_CITY)
    assert qry.num_cities() == old_count + 1
    
def test_good_cities():
    old_count = qry.num_cities()
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    assert qry.is_valid_id(new_rec_id)
    assert qry.num_cities() == old_count + 1
    
def test_create_bad_name():
    with pytest.raise(ValueError):
    qry.create({})
    
def test_create_bad_param_type():
    with pytest.raise(ValueError):
    qry.create(17)
