# Need to mock httpx.get for testing the request functions
import httpx
import pytest

from brewcli.brewery import BreweryAPI


def test_brewery_api_initialization():
    """Test that the BreweryAPI initializes correctly."""
    with BreweryAPI() as client:
        assert isinstance(client.client, httpx.Client)
        assert client.base_url == "https://api.openbrewerydb.org/v1/breweries"
        assert client.headers == {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/html;q=0.9, */*;q=0.8",
        }


def test_get_random_breweries(httpx_mock, api_client: BreweryAPI):
    """Test `get_random_breweries` method."""
    mock_response = [{"id": "abc123", "name": "Random Brewery"}]
    httpx_mock.add_response(json=mock_response)

    response = api_client.get_random_breweries(1)
    assert response == mock_response


def test_client_closes_after_context():
    """Test that the HTTP client is closed after exiting the context manager."""

    with BreweryAPI() as client:
        assert client.client.is_closed is False

    assert client.client.is_closed is True


def test_context_manager_closes_client():
    """Test that client context manager is working."""
    with BreweryAPI() as client:
        assert client.client.is_closed is False
    assert client.client.is_closed is True


def test_client_handles_invalid_json(httpx_mock, api_client):
    """Test that API methods raise `ValueError` when JSON parsing fails."""
    httpx_mock.add_response(
        url="https://api.openbrewerydb.org/v1/breweries/random?size=1",
        content="Not a JSON response",
    )

    with pytest.raises(ValueError):
        api_client.get_random_breweries()
