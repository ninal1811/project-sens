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

@pytest.mark.skip('This is an example of a bad test!')
def test_bad_test_from_num_cities():
    assert qry.num_cities() == len(qry.city_cache)
    
def test_num_cities():
    # get the count
    old_count = qry.num_cities()
    print(f"[DEBUG] old_count={old_count}")

    # add a record
    qry.create(qry.SAMPLE_CITY)
    assert qry.is_valid_id(new_id), "[ERROR] Invalid ID returned from create()"
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

@patch('cities.queries.db_connect', return_value=True, autospec=True)
def test_read(mock_db_connect):
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    cities = qry.read()
    assert isinstance(cities, dict)
    assert len(cities) > 1
    
@patch('cities.queries.db_connect', return_value=False, autospec=True)
def test_read_connection(mock_db_connect):
    with pytest.raises(ConnectionError):
        cities = qry.read()

@patch('cities.queries.db_connect', return_value=True, autospec=True)
def test_delete(mock_db_connect, temp_city):
    qry.delete(temp_city)
    assert temp_city not in qry.read()