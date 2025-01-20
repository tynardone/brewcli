import pytest

from ..models import Address, Brewery, Coordinate


def test_coordinate_valid():
    """Test creating a Coordinate with valid inputs."""
    coord = Coordinate(longitude="12.34", latitude="56.78")
    assert coord.longitude == 12.34
    assert coord.latitude == 56.78


def test_coordinate_invalid():
    """Test creating a Coordinate with invalid inputs."""
    with pytest.raises(ValueError, match="Cannot convert longitude='abc' to float"):
        Coordinate(longitude="abc", latitude="56.78")


def test_coordinate_none():
    """Test creating a Coordinate with None values."""
    coord = Coordinate(longitude=None, latitude=None)
    assert coord.longitude is None
    assert coord.latitude is None


def test_address_from_dict_valid():
    """Test creating an Address from valid dictionary data."""
    data = {
        "address_1": "123 Main St",
        "address_2": None,
        "address_3": None,
        "street": "Main St",
        "city": "Sample City",
        "state": "Sample State",
        "postal_code": "12345",
        "country": "Sample Country",
        "longitude": "12.34",
        "latitude": "56.78",
    }
    address = Address.from_dict(data)
    assert address.address_one == "123 Main St"
    assert address.city == "Sample City"
    assert address.state == "Sample State"
    assert address.postal_code == "12345"
    assert address.country == "Sample Country"
    assert address.coordinate.longitude == 12.34
    assert address.coordinate.latitude == 56.78


def test_address_from_dict_missing_fields():
    """Test creating an Address with missing fields."""
    data = {
        "address_1": "123 Main St",
        "street": "Main St",
        "city": "Sample City",
        "state": "Sample State",
        "postal_code": "12345",
        "country": "Sample Country",
        # "longitude" and "latitude" intentionally omitted
    }
    with pytest.raises(KeyError, match="'address_2'"):
        Address.from_dict(data)


def test_brewery_from_dict_valid():
    """Test creating a Brewery from valid dictionary data."""
    data = {
        "id": "brewery_1",
        "name": "Sample Brewery",
        "address_1": "123 Main St",
        "address_2": None,
        "address_3": None,
        "street": "Main St",
        "city": "Sample City",
        "state": "Sample State",
        "postal_code": "12345",
        "country": "Sample Country",
        "longitude": "12.34",
        "latitude": "56.78",
        "phone": "123-456-7890",
        "website_url": "http://samplebrewery.com",
    }
    brewery = Brewery.from_dict(data)
    assert brewery.id == "brewery_1"
    assert brewery.name == "Sample Brewery"
    assert brewery.address.city == "Sample City"
    assert brewery.address.coordinate.longitude == 12.34
    assert brewery.phone == "123-456-7890"
    assert brewery.website_url == "http://samplebrewery.com"


def test_brewery_from_dict_missing_fields():
    """Test creating a Brewery with missing fields."""
    data = {
        "id": "brewery_1",
        "name": "Sample Brewery",
        "address_1": "123 Main St",
        "address_2": None,
        "address_3": None,
        "street": "Main St",
        "city": "Sample City",
        "state": "Sample State",
        "postal_code": "12345",
        "country": "Sample Country",
        # Missing "longitude", "latitude", "phone", and "website_url"
    }
    with pytest.raises(KeyError, match="'longitude'"):
        Brewery.from_dict(data)
