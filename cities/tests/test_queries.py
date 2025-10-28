from unittest.mock import patch
import pytest

import cities.queries as qry

@pytest.fixture(scope='function')
def temp_city():
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    yield new_rec_id
    try:
        qry.delete(new_rec_id)
        print(f"[DEBUG] Successfully deleted temp city ID: {new_rec_id}")
    except ValueError as e:
        print(f"[WARN] Cleanup skipped: {e}")
        
@pytest.fixture
def reset_cache():
    original_cache = qry.city_cache.copy()
    yield
    qry.city_cache.clear()
    qry.city_cache.update(original_cache)
    
def test_reset_cache():
    original_cache = qry.num_cities()
    test_id = qry.create({'name': 'city', 'state_code': 'state'})
    assert qry.num_cities() == original_cache + 1
    assert test_id in qry.city_cache

def test_create_db_failure():
    with patch('cities.queries.dbc.create', side_effect=RuntimeError("DB error")):
        with pytest.raises(RuntimeError):
            qry.create(qry.SAMPLE_CITY)

@pytest.mark.skip('This is an example of a bad test!')
def test_bad_test_from_num_cities():
    assert qry.num_cities() == len(qry.city_cache)

@pytest.mark.skip('Feature pending full implementation rollout') 
def test_num_cities(temp_city):
    # get the count
    old_count = qry.num_cities()
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    assert qry.is_valid_id(new_rec_id)
    assert qry.num_cities() == old_count + 1
    
def test_good_cities():
    old_count = qry.num_cities()
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    assert qry.is_valid_id(new_rec_id)
    assert qry.num_cities() == old_count + 1
    
def test_create_bad_name():
    with pytest.raises(ValueError):
        qry.create({})
    
def test_create_bad_param_type():
    with pytest.raises(ValueError):
        qry.create(17)

@pytest.mark.skip('Feature pending full implementation rollout')
def test_read():
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    cities = qry.read()
    assert isinstance(cities, dict)
    assert len(cities) > 1
    
@pytest.mark.skip('Feature pending full implementation rollout')
def test_read_connection():
    with pytest.raises(ConnectionError):
        cities = qry.read()

@pytest.mark.skip('Feature pending full implementation rollout')
def test_delete(temp_city):
    qry.delete(temp_city)
    assert temp_city not in qry.read()

def test_delete_not_there():
    with pytest.raises(ValueError):
        qry.delete('Some value that is not there')

@pytest.mark.skip(reason="Feature pending full implementation.")
def test_is_valid_id_whitespace():
    assert qry.is_valid_id(" ") is False

