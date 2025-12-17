import pytest
from countries.country_queries import get_country, num_countries, read_all


def test_get_country_valid():
    country = get_country(1)
    assert country["name"] == "United States"
    assert country["capital"] == "Washington D.C."


def test_get_country_invalid():
    with pytest.raises(ValueError):
        get_country(999)


def test_num_countries():
    assert num_countries() == len(read_all())

def test_read_all_structure():
    data = read_all()
    assert isinstance(data, dict)
    for key in data.keys():
        assert isinstance(key, (int, str))
