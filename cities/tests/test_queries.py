from copy import deepcopy
from unittest.mock import patch
import pytest
from data.db_connect import is_valid_id
import cities.cities_queries as qry


def get_temp_rec():
    return deepcopy(qry.SAMPLE_CITY)


@pytest.fixture(scope='function')
def temp_city_no_del():
    temp_rec = get_temp_rec()
    qry.create(get_temp_rec())
    return temp_rec


@pytest.fixture(scope='function')
def temp_city():
    temp_rec = get_temp_rec()
    new_rec_id = qry.create(get_temp_rec())
    yield new_rec_id
    try:
        qry.delete_city(temp_rec[qry.CITY], temp_rec[qry.STATE_CODE], temp_rec[qry.COUNTRY_CODE])
        print(f"[DEBUG] Successfully deleted temp city ID: {new_rec_id}")
    except ValueError as e:
        print(f"[WARN] Cleanup skipped: {e}")


@pytest.fixture
def reset_cache():
    original_cache = qry.cache.copy() if qry.cache else {}
    yield
    qry.cache = original_cache.copy() if original_cache else None


def test_reset_cache():
    original_count = qry.count()
    
    test_city = {
        qry.CITY: 'ZZTEST_ResetCache_99999',
        qry.STATE_CODE: 'NY',
        qry.COUNTRY_CODE: 'US',
        qry.REC_RESTAURANT: 'Test Restaurant'
    }
    
    test_id = qry.create(test_city)
    
    assert qry.count() == original_count + 1
    
    qry.delete_city(
        test_city[qry.CITY],
        test_city[qry.STATE_CODE],
        test_city[qry.COUNTRY_CODE]
    )
    
    assert qry.count() == original_count


def test_create_db_failure():
    with patch('cities.cities_queries.dbc.create', side_effect=RuntimeError("DB error")):
        with pytest.raises(RuntimeError):
            qry.create(qry.SAMPLE_CITY)


@pytest.mark.skip('This is an example of a bad test!')
def test_bad_test_from_num_cities():
    assert qry.num_cities() == len(qry.city_cache)


@pytest.mark.skip('Feature pending full implementation rollout')
def test_num_cities(temp_city):
    # get the count
    old_count = qry.num_cities()
    new_rec_id = qry.create(get_temp_rec())
    assert qry.is_valid_id(new_rec_id)
    assert qry.num_cities() == old_count + 1


def test_good_cities():
    old_count = qry.count()
    
    temp_rec = get_temp_rec()
    temp_rec[qry.CITY] = "ZZTEST_GoodCities_12345"
    
    new_rec_id = qry.create(temp_rec)
    
    assert is_valid_id(new_rec_id)
    
    assert qry.count() == old_count + 1
    
    qry.delete_city(
        temp_rec[qry.CITY], 
        temp_rec[qry.STATE_CODE], 
        temp_rec[qry.COUNTRY_CODE]
    )
    
    # Verify cleanup worked
    assert qry.count() == old_count


def test_create_bad_name():
    with pytest.raises(ValueError):
        qry.create({})


def test_create_bad_param_type():
    with pytest.raises(ValueError):
        qry.create(17)


@pytest.mark.skip('Feature pending full implementation rollout')
def test_read():
    cities = qry.read()  # Fixed: defined cities variable
    assert isinstance(cities, list)
    assert get_temp_rec() in cities


@pytest.mark.skip('Feature pending full implementation rollout')
def test_delete(temp_city_no_del):
    ret = qry.delete(temp_city_no_del[qry.CITY], temp_city_no_del[qry.STATE_CODE], temp_city_no_del[qry.COUNTRY_CODE])
    assert ret == 1


def test_delete_not_there():
    with pytest.raises(ValueError):
        qry.delete('Some city name that is not there')

@pytest.mark.skip(reason="Feature pending full implementation.")
def test_is_valid_id_whitespace():
    assert qry.is_valid_id(" ") is False


def test_get_cities_by_state():
    result = qry.get_cities_by_state('NY')
    assert all(city['state_code'] == 'NY' for city in result.values())
