# Need to mock httpx.get for testing the request functions
import pytest


@pytest.mark.parametrize("num_breweries", [1, 3, 5])
def test_get_random_breweries(httpx_mock, brewery_api, brewery_data, num_breweries):
    """Test fetching a variable number of random breweries."""
    httpx_mock.add_response(json=[brewery_data] * num_breweries)
    response = brewery_api.get_random_breweries(num_breweries)
    assert isinstance(response, list)
    assert len(response) == num_breweries
    assert all(brewery["name"] == brewery_data["name"] for brewery in response)
    assert all(brewery["city"] == brewery_data["city"] for brewery in response)


def test_get_brewery_by_id(httpx_mock, brewery_api, brewery_data):
    """Test fetching a brewery by ID."""
    httpx_mock.add_response(json=brewery_data)
    response = brewery_api.get_brewery_by_id(brewery_data["id"])
    assert isinstance(response, dict)
    assert response["id"] == brewery_data["id"]
    assert response["name"] == brewery_data["name"]
    assert response["city"] == brewery_data["city"]


def test_invalid_brewery_id(httpx_mock, brewery_api):
    """Test handling of invalid brewery ID."""
    httpx_mock.add_response(status_code=404, json={"message": "Not Found"})
    with pytest.raises(Exception):
        brewery_api.get_brewery_by_id("invalid_id")
