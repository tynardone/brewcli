"""Tests for classes from models.py"""

import pytest

from brewcli.models import Address, Brewery, BreweryType, Coordinate, SearchQuery


class TestCoordinate:
    def test_init_valid_input(self, brewery_data):
        """Test creating a Coordinate with valid inputs."""
        coord = Coordinate(
            longitude=brewery_data["longitude"],
            latitude=brewery_data["latitude"],
        )

        assert coord.longitude == -85.76493039
        assert coord.latitude == 42.90907804
        assert isinstance(coord.longitude, float)
        assert isinstance(coord.latitude, float)

    def test_init_invalid_string_input(self):
        """Test creating a Coordinate with invalid inputs."""
        with pytest.raises(ValueError):
            Coordinate(longitude="abc", latitude="56.78")

    @pytest.mark.parametrize(
        "latitude,longitude", [(181, 100), (-181, -100), (100, -181), (100, 181)]
    )
    def test_init_invalid_range_input(self, latitude, longitude):
        """Test checking valid coordinate range -180 to 180"""
        with pytest.raises(ValueError):
            Coordinate(longitude=longitude, latitude=latitude)

    @pytest.mark.parametrize("latitude,longitude", [(None, "123"), ("123", None)])
    def test_init_none_fail(self, latitude, longitude):
        """Test that a Coordinate fails when initialized with None values."""
        with pytest.raises(TypeError):
            Coordinate(longitude=longitude, latitude=latitude)

    def test_to_str(self):
        """Test to_str method output '<latitude>,<longitude>.'"""
        coordinate = Coordinate(longitude=45.1234, latitude=-93.4567)
        assert coordinate.to_str() == "-93.4567,45.1234"


class TestAddress:
    def test_from_dict_full(self, brewery_data):
        """Test creating an Address from valid dictionary data."""
        address = Address.from_dict(brewery_data)
        assert address.address_one == "4051 Chicago Dr SW"
        assert address.city == "Grandville"
        assert address.address_two == "Bldg 1"
        assert address.address_three == "Unit 1"
        assert address.state == "Michigan"
        assert address.postal_code == "12345"
        assert address.country == "United States"
        assert address.coordinate.longitude == -85.76493039
        assert address.coordinate.latitude == 42.90907804

    def test_from_dict_optional_none(self, brewery_data):
        """Test creating Address without optional parameters."""
        brewery_data["address_2"] = None
        brewery_data["address_3"] = None
        brewery_data["longitude"] = None
        brewery_data["latitude"] = None

        address = Address.from_dict(brewery_data)

        assert address.address_one == "4051 Chicago Dr SW"
        assert address.city == "Grandville"
        assert address.address_two is None
        assert address.address_three is None
        assert address.state == "Michigan"
        assert address.postal_code == "12345"
        assert address.country == "United States"
        assert address.coordinate is None

    @pytest.mark.parametrize(
        "latitude,longitude",
        [("abc", "100"), ("100", "abc"), ("abc", "abc")],
    )
    def test_from_dict_invalid_coordinates(self, latitude, longitude, brewery_data):
        """
        Test Address is created with Coordinate None if bad latitude or longitude
        supplied.
        """
        brewery_data["latitude"] = latitude
        brewery_data["longitude"] = longitude
        address = Address.from_dict(brewery_data)
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
        self, data, expected_exception, brewery_data
    ):
        """
        Test Address is created with coordinate as None if Coordinate initialization
        fails due to ValueError, TypeError, or KeyError.
        """
        # Update brewery_data with test-specific data
        brewery_data.update(data)

        # Create the Address object
        address = Address.from_dict(brewery_data)

        # Assert that coordinate is None
        assert address.coordinate is None, (
            f"Expected coordinate to be None when {expected_exception.__name__}"
            "is raised, but got a non-None value."
        )

    def test_address_from_dict_missing_lat_long_keys(self, brewery_data):
        """
        When data does not have latitude and/or longitude key, KeyError is caught
        and address.coordinate is None.
        """
        # Remove latitude and longitude keys using del
        missing_lat_long = brewery_data.copy()
        del missing_lat_long["latitude"]
        del missing_lat_long["longitude"]

        # After raising KeyError, verify that coordinate is None
        address = Address.from_dict(missing_lat_long)
        assert address.coordinate is None


class TestBrewery:
    def test_brewery_from_dict_valid(self, brewery_data):
        """
        Test creating a Brewery from valid dictionary data
        """
        brewery = Brewery.from_dict(brewery_data)
        assert brewery.id == "b9c27692-5db5-44dd-aa88-b8b66b944f3c"
        assert brewery.name == "Osgood Brewing"
        assert brewery.brewery_type == "brewpub"
        assert brewery.address.city == "Grandville"
        assert brewery.address.coordinate.longitude == -85.76493039
        assert brewery.address.coordinate.latitude == 42.90907804
        assert brewery.phone == "111-111-1111"
        assert brewery.website_url == "http://www.osgoodbrewing.com"

    def test_brewery_from_dict_invalid_coordinates(self, brewery_data):
        """
        Test that coordinate is None if invalid latitude or longitude are supplied.
        """
        # Update brewery_data with invalid coordinates
        brewery_data["latitude"] = "invalid_latitude"
        brewery_data["longitude"] = "invalid_longitude"

        # Create the Brewery object
        brewery = Brewery.from_dict(brewery_data)

        # Assert that coordinate is None
        assert brewery.address.coordinate is None

    def test_to_flat_dict(self):
        # TODO: implement test
        pass


class TestSearchQuery:
    def test_init_all_fields(self, valid_query_inputs):
        """Test initialization of SearchQuery from valid data where all fields
        are present."""
        query_set = SearchQuery(**valid_query_inputs)
        assert query_set.city == "Grand Rapids"
        assert query_set.country == "USA"
        assert query_set.coord == Coordinate(100, 100)
        assert query_set.name == "Brewery"
        assert query_set.state == "Michigan"
        assert query_set.type == "micro"
        assert query_set.postal == "11111"
        assert query_set.sort_order == "asc"
        assert query_set.ids == ["123", "456", "789"]
        assert query_set.page == 2
        assert query_set.per_page == 100

    def test_init_defaults(self):
        """
        Test for expected default parameters.
        """
        query_set = SearchQuery()
        assert query_set.city is None
        assert query_set.country is None
        assert query_set.coord is None
        assert query_set.name is None
        assert query_set.type is None
        assert query_set.state is None
        assert query_set.postal is None
        assert query_set.sort_order is None
        assert query_set.ids is None
        assert query_set.page == 1
        assert query_set.per_page == 50

    @pytest.mark.parametrize("sort", ["asc", "desc", None])
    def test_sort_order_validation_valid(self, sort):
        """
        Test successful creation when sort_order is valid option of 'asc', 'desc',
        or None
        """
        query_set = SearchQuery(sort_order=sort)
        assert query_set.sort_order == sort

    @pytest.mark.parametrize("sort", ["ascending", "descending", 1])
    def test_sort_order_validation_invalid(self, sort):
        """Test that a ValueError is raised when sort_order is not 'asc' or 'desc'."""
        with pytest.raises(
            ValueError,
            match=f"Invalid sort_order '{sort}'. Must be 'asc', 'desc', or None.",
        ):
            SearchQuery(sort_order=sort)

    @pytest.mark.parametrize("per_page", [1, 50, 200, None])
    def test_per_page_validation_valid(self, per_page):
        """
        Test that `per_page` accepts valid values within range 1 to 200, or None.
        """
        query_set = SearchQuery(per_page=per_page)
        if per_page:
            assert query_set.per_page == per_page
        else:
            assert query_set.per_page is None

    @pytest.mark.parametrize("per_page", [-10, 0, 201, 12.5, "invalid"])
    def test_per_page_validation_invalid(self, per_page):
        """
        Test that `per_page` raises exception with invalid arguments:
         - Outside of range [1, 200]
         - float e.g 12.5
         - str
        """
        with pytest.raises(
            ValueError,
            match=f"Invalid per_page: {per_page}. Must be an integer from 1 to 200.",
        ):
            SearchQuery(per_page=per_page)

    @pytest.mark.parametrize("page", [1, 10, 100, None])
    def test_page_validation_valid(self, page):
        """
        Test that `page` accepts vaild values of integers equal to or greater than 1,
        or None.
        """
        query_set = SearchQuery(page=page)
        if page:
            assert query_set.page == page
        else:
            assert query_set.page is None

    @pytest.mark.parametrize("page", [0, -10, 12.5, "invalid"])
    def test_page_validation_invalid(self, page):
        """
        Test that an exception is raised with invalid  `page` arguments:
        - Outside range
        - float
        - str
        """
        with pytest.raises(
            ValueError,
            match=f"Invalid page: {page}. Must be an integer greater "
            "than or equal to 1.",
        ):
            SearchQuery(page=page)

    @pytest.mark.parametrize("brew_type", [t.value for t in BreweryType] + [None])
    def test_by_type_validation(self, brew_type):
        """
        Test by_type validation works for all members of BreweryType enum.
        """
        query_set = SearchQuery(type=brew_type)
        assert query_set.type == brew_type

    @pytest.mark.parametrize("brew_type", ["Micro", "invalid", 100, ""])
    def test_by_type_validation_invalid(self, brew_type: str):
        """
        Test that an exception is raised with invalid `by_type` arguments, to
        ensure only excepts options defined in BreweryType.
        """
        with pytest.raises(
            ValueError,
            match=f"Invalid value for type: {brew_type}. Must be one of "
            f"{', '.join([t.value for t in BreweryType])}",
        ):
            SearchQuery(
                type=brew_type,
            )

    def test_to_params_all_fields(self, valid_query_inputs):
        """
        Test that to_params creates expecte key-value pairs with proper formatting
        of ids and coordinates.
        """
        query_set = SearchQuery(**valid_query_inputs)
        params = query_set.to_params()
        assert params == {
            "by_city": "Grand Rapids",
            "by_country": "USA",
            "by_dist": "100.0,100.0",
            "by_ids": "123,456,789",
            "by_name": "Brewery",
            "by_state": "Michigan",
            "by_postal": "11111",
            "by_type": "micro",
            "page": 2,
            "per_page": 100,
            "sort_order": "asc",
        }
