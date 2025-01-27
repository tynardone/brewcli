"""Fixtures and other shared test resources"""

import pytest


@pytest.fixture
def valid_brewery_response():
    """Represents a valid response from brewery api with all fields present."""
    return {
        "id": "brewery_1",
        "name": "Sample Brewery",
        "phone": "123-456-7890",
        "website_url": "http://samplebrewery.com",
        "address_1": "123 Main St",
        "address_2": "Bldg 1",
        "address_3": "Apt 1",
        "street": "Main St",
        "city": "Sample City",
        "state": "Sample State",
        "postal_code": "12345",
        "country": "Sample Country",
        "longitude": "123.123",
        "latitude": "-123.123",
    }


@pytest.fixture
def valid_query_set():
    """Represents a full and valid set of query parameters."""
    return {
        "by_city": "Grand Rapids",
        "by_country": "USA",
        "by_dist": "100,100",
        "by_name": "Brewery",
        "by_state": "Michigan",
        "by_postal": "11111",
        "by_type": "micro",
        "sort_order": "asc",
        "by_ids": ["123", "456", "789"],
        "page": 2,
        "per_page": 100,
    }
