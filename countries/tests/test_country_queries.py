import pytest
from unittest.mock import patch
import country_queries


def test_get_country_valid():
    test_country = {'_id': 1, 'name': 'United States', 'capital': 'Washington D.C.'}
    
    with patch('country_queries.country_cache', {1: test_country}):
        with patch('country_queries.load_cache'):
            country = country_queries.get_country(1)
            assert country['_id'] == 1
            assert country["name"] == "United States"
            assert country["capital"] == "Washington D.C."


def test_get_country_invalid():
    with pytest.raises(ValueError):
        country_queries.get_country(999)


def test_num_countries():
    assert country_queries.num_countries() == len(country_queries.read_all())

def test_read_all_structure():
    data = country_queries.read_all()
    assert isinstance(data, dict)
    for key in data.keys():
        assert isinstance(key, (int, str))
