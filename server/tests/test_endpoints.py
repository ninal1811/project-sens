from http.client import (  # noqa: F401
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


@pytest.fixture(scope="module")
def client():
    """Flask test client for all tests in this module."""
    return ep.app.test_client()


# Test that /hello returns correct status + JSON format
def test_hello_ok(client):
    resp = client.get(ep.HELLO_EP)
    assert resp.status_code == 200
    assert resp.get_json() == {ep.HELLO_RESP: "world"}


# Test helper function: invalid values should raise ValueError
def test_parse_limit_raises_on_invalid():
    # invalid strings should raise
    with pytest.raises(ValueError):
        ep.parse_limit("abc")
    # zero/negative should raise
    with pytest.raises(ValueError):
        ep.parse_limit("0")
    with pytest.raises(ValueError):
        ep.parse_limit("-5")


# Test valid inputs for parse_limit helper
def test_parse_limit_valid_cases():
    assert ep.parse_limit(None) is None
    assert ep.parse_limit("") is None
    assert ep.parse_limit("3") == 3


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json

# Mock the DB/read function so we don't touch real data during the test


@patch("cities.queries.read", return_value=[{"name": "NYC"}] * 10)
def test_cities_bad_limit_ignored_returns_200(mock_read, client):
    # Endpoint ignores bad ?limit= and still returns 200 with the full list.
    resp = client.get(f"{ep.CITIES_EPS}/{ep.READ}?limit=notanint")
    assert resp.status_code == 200
    body = resp.get_json()
    assert ep.CITY_RESP in body
    assert len(body[ep.CITY_RESP]) == 10  # unchanged
    mock_read.assert_called_once()


@patch("cities.queries.read", return_value=[{"name": "NYC"}, {"name": "LA"}])
def test_cities_success(mock_read, client):
    resp = client.get(f"{ep.CITIES_EPS}/{ep.READ}")
    assert resp.status_code == 200
    body = resp.get_json()
    assert ep.CITY_RESP in body
    assert body[ep.CITY_RESP] == [{"name": "NYC"}, {"name": "LA"}]
    mock_read.assert_called_once()


@pytest.mark.skip(reason="Integration placeholder")
def test_endpoints_listing(client):
    resp = client.get(ep.ENDPOINT_EP)
    assert resp.status_code == 200
