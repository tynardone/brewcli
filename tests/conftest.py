"""Fixtures and other shared test resources"""

import pytest
from click.testing import CliRunner

from brewcli.brewery import BreweryAPI
from brewcli.models import Coordinate


@pytest.fixture
def valid_query_inputs():
    """Represents a full and valid set of query parameters."""
    return {
        "city": "Grand Rapids",
        "country": "USA",
        "coord": Coordinate(100, 100),
        "name": "Brewery",
        "state": "Michigan",
        "postal": "11111",
        "type": "micro",
        "sort_order": "asc",
        "ids": ["123", "456", "789"],
        "page": 2,
        "per_page": 100,
    }


@pytest.fixture
def api_client():
    """Fixture to provide an instance of BreweryAPI in a context manager."""
    with BreweryAPI() as client:
        yield client


@pytest.fixture
def brewery_data():
    """Fixture to provide mock brewery data."""
    return {
        "id": "b9c27692-5db5-44dd-aa88-b8b66b944f3c",
        "name": "Osgood Brewing",
        "brewery_type": "brewpub",
        "address_1": "4051 Chicago Dr SW",
        "address_2": "Bldg 1",
        "address_3": "Unit 1",
        "city": "Grandville",
        "state_province": "Michigan",
        "postal_code": "12345",
        "country": "United States",
        "longitude": "-85.76493039",
        "latitude": "42.90907804",
        "phone": "111-111-1111",
        "website_url": "http://www.osgoodbrewing.com",
        "state": "Michigan",
        "street": "4051 Chicago Dr SW",
    }


@pytest.fixture
def clirunner():
    """
    Provides a  CliRunner instance for CLI tests.
    """
    return CliRunner()
