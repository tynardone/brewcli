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

    def test_to_str(self):
        """Test to_str method output"""
        coordinate = Coordinate(longitude=45.1234, latitude=-93.4567)
        assert coordinate.to_str() == "-93.4567,45.1234"


class TestAddress:
    def test_from_dict_full(self, valid_brewery_response):
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

    def test_from_dict_optional_none(self, valid_brewery_response):
        """Test creating Address without optional parameters."""
        valid_brewery_response["address_2"] = None
        valid_brewery_response["address_3"] = None
        valid_brewery_response["longitude"] = None
        valid_brewery_response["latitude"] = None

        address = Address.from_dict(valid_brewery_response)

        assert address.address_one == "123 Main St"
        assert address.city == "Sample City"
        assert address.address_two is None
        assert address.address_three is None
        assert address.state == "Sample State"
        assert address.postal_code == "12345"
        assert address.country == "Sample Country"
        assert address.coordinate is None

    @pytest.mark.parametrize(
        "lat,long",
        [("abc", "100"), ("100", "abc"), ("abc", "abc")],
    )
    def test_from_dict_invalid_coordinates(self, lat, long, valid_brewery_response):
        """
        Test Address is created with Coordinate None if bad latitude or longitude
        supplied.
        """
        valid_brewery_response["latitude"] = lat
        valid_brewery_response["longitude"] = long
        address = Address.from_dict(valid_brewery_response)
        assert address.coordinate is None

    @pytest.mark.parametrize(
        "data, expected_exception",
        [
            # ValueError: Non-float-compatible string for latitude or longitude
            ({"latitude": "abc", "longitude": "100"}, ValueError),
            ({"latitude": "100", "longitude": "abc"}, ValueError),
            ({"latitude": "abc", "longitude": "abc"}, ValueError),
            # TypeError: NoneType for latitude or longitude
            ({"latitude": None, "longitude": "100"}, TypeError),
            ({"latitude": "100", "longitude": None}, TypeError),
            ({"latitude": None, "longitude": None}, TypeError),
        ],
    )
    def test_address_from_dict_with_invalid_coordinates(
        self, data, expected_exception, valid_brewery_response
    ):
        """
        Test Address is created with coordinate as None if Coordinate initialization
        fails due to ValueError, TypeError, or KeyError.
        """
        # Update valid_brewery_response with test-specific data
        valid_brewery_response.update(data)

        # Create the Address object
        address = Address.from_dict(valid_brewery_response)

        # Assert that coordinate is None
        assert address.coordinate is None, (
            f"Expected coordinate to be None when {expected_exception.__name__}"
            "is raised, but got a non-None value."
        )

    def test_address_from_dict_missing_lat_long_keys(self, valid_brewery_response):
        """
        When data does not have latitude and/or longitude key, KeyError is caught
        and address.coordinate is None.
        """
        # Remove latitude and longitude keys using del
        missing_lat_long = valid_brewery_response.copy()
        del missing_lat_long["latitude"]
        del missing_lat_long["longitude"]

        # After raising KeyError, verify that coordinate is None
        address = Address.from_dict(missing_lat_long)
        assert address.coordinate is None


class TestBrewery:
    def test_brewery_from_dict_valid(self, valid_brewery_response):
        """
        Test creating a Brewery from valid dictionary data
        """
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


class TestQuerySet:
    pass
