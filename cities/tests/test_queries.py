from copy import deepcopy
from unittest.mock import patch
import pytest

import cities.queries as qry


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
        qry.delete(temp_rec[qry.NAME], temp_rec[qry.STATE_CODE])
        print(f"[DEBUG] Successfully deleted temp city ID: {new_rec_id}")
    except ValueError as e:
        print(f"[WARN] Cleanup skipped: {e}")


# @pytest.fixture
# def reset_cache():
#     original_cache = qry.city_cache.copy()
#     yield
#     qry.city_cache.clear()
#     qry.city_cache.update(original_cache)


# def test_reset_cache():
#     original_cache = qry.num_cities()
#     test_id = qry.create({'name': 'city', 'state_code': 'state'})
#     assert qry.num_cities() == original_cache + 1


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
    new_rec_id = qry.create(get_temp_rec())
    assert qry.is_valid_id(new_rec_id)
    assert qry.num_cities() == old_count + 1


# def test_good_cities():
#     old_count = qry.num_cities()
#     new_rec_id = qry.create(get_temp_rec())
#     assert qry.is_valid_id(new_rec_id)
#     assert qry.num_cities() == old_count + 1


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
    ret = qry.delete(temp_city_no_del[qry.NAME], temp_city_no_del[qry.STATE_CODE])
    assert ret == 1


# def test_delete_not_there():
#     with pytest.raises(ValueError):
#         qry.delete('Some city name that is not there', 'not a state')


@pytest.mark.skip(reason="Feature pending full implementation.")
def test_is_valid_id_whitespace():
    assert qry.is_valid_id(" ") is False


def test_get_cities_by_state():
    result = qry.get_cities_by_state('NY')
    assert all(city['state_code'] == 'NY' for city in result.values())
