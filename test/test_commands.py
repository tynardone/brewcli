import pytest


@pytest.fixture
def brewery_all_fields_present():
    return {
        "id": "b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0",
        "name": "MadTree Brewing 2.0",
        "brewery_type": "regional",
        "address_1": "5164 Kennedy Ave",
        "address_2": "Apt 1",
        "address_3": "Room 1",
        "city": "Cincinnati",
        "state_province": "Ohio",
        "postal_code": "45213",
        "country": "United States",
        "longitude": "-84.4137736",
        "latitude": "39.1885752",
        "phone": "5138368733",
        "website_url": "http://www.madtreebrewing.com",
        "state": "Ohio",
        "street": "5164 Kennedy Ave",
    }


@pytest.fixture
def brewery_all_fields_none():
    return {
        "id": None,
        "name": None,
        "brewery_type": None,
        "address_1": None,
        "address_2": None,
        "address_3": None,
        "city": None,
        "state_province": None,
        "postal_code": None,
        "country": None,
        "longitude": None,
        "latitude": None,
        "phone": None,
        "website_url": None,
        "state": None,
        "street": None,
    }
