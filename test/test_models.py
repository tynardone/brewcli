"""Tests for classes from models.py"""

import pytest

from brewcli.models import Address, Brewery, Coordinate


class TestCoordinate:
    def test_init_valid_input(self, valid_brewery_response):
        """Test creating a Coordinate with valid inputs."""
        coord = Coordinate(
            longitude=valid_brewery_response["longitude"],
            latitude=valid_brewery_response["latitude"],
        )
        assert coord.longitude == 123.123
        assert coord.latitude == -123.123
        assert isinstance(coord.longitude, float)
        assert isinstance(coord.latitude, float)

    def test_init_invalid_string_input(self):
        """Test creating a Coordinate with invalid inputs."""
        with pytest.raises(ValueError):
            Coordinate(longitude="abc", latitude="56.78")

    def test_init_invalid_range_input(self):
        """Test checking valid coordinate range"""
        with pytest.raises(ValueError):
            Coordinate(longitude=100, latitude=999)

    @pytest.mark.parametrize("long,lat", [(None, "123"), ("123", None)])
    def test_init_none_fail(self, long, lat):
        """Test that a Coordinate fails when initialized with None values."""
        with pytest.raises(TypeError):
            Coordinate(longitude=long, latitude=lat)

    def test_to_str_success(self):
        """Test to_str method output"""
        coordinate = Coordinate(longitude=45.1234, latitude=-93.4567)
        assert coordinate.to_str() == "-93.4567,45.1234"


class TestAddress:
    def test_from_dict_valid(self, valid_brewery_response):
        """Test creating an Address from valid dictionary data."""
        address = Address.from_dict(valid_brewery_response)
        assert address.address_one == "123 Main St"
        assert address.city == "Sample City"
        assert address.address_two == "Bldg 1"
        assert address.address_three == "Apt 1"
        assert address.state == "Sample State"
        assert address.postal_code == "12345"
        assert address.country == "Sample Country"
        assert address.coordinate.longitude == 123.123
        assert address.coordinate.latitude == -123.123


class TestBrewery:
    def test_brewery_from_dict_valid(self, valid_brewery_response):
        """Test creating a Brewery from valid dictionary data."""
        brewery = Brewery.from_dict(valid_brewery_response)
        assert brewery.id == "brewery_1"
        assert brewery.name == "Sample Brewery"
        assert brewery.address.city == "Sample City"
        assert brewery.address.coordinate.longitude == 123.123
        assert brewery.address.coordinate.latitude == -123.123
        assert brewery.phone == "123-456-7890"
        assert brewery.website_url == "http://samplebrewery.com"

    def test_brewery_from_dict_missing_fields(self, valid_brewery_response):
        """Test creating a Brewery with missing fields."""
        data = valid_brewery_response.copy()
        del data["phone"]  # Simulating missing field
        with pytest.raises(KeyError):
            Brewery.from_dict(data)
