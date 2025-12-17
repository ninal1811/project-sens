import pytest
from countries.country_queries import get_country, num_countries, read_all


def test_get_country_valid():
    country = get_country(1)
    assert country["name"] == "United States"
    assert country["capital"] == "Washington, DC"


def test_get_country_invalid():
    with pytest.raises(ValueError):
        get_country(999)


def test_num_countries():
    assert num_countries() == len(read_all())

def test_read_all_structure():
    data = read_all()
    assert isinstance(data, dict)
    assert all(isinstance(cid, int) for cid in data.keys())
    assert all(isinstance(info, dict) for info in data.values())
