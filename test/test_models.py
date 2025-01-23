import pytest

from brewcli.models import Address, Brewery, Coordinate


# --- Fixtures ---
@pytest.fixture
def valid_coordinate_data():
    return {"longitude": "12.34", "latitude": "56.78"}


@pytest.fixture
def valid_address_data(valid_coordinate_data):
    return {
        "address_1": "123 Main St",
        "address_2": None,
        "address_3": None,
        "street": "Main St",
        "city": "Sample City",
        "state": "Sample State",
        "postal_code": "12345",
        "country": "Sample Country",
        **valid_coordinate_data,
    }


@pytest.fixture
def valid_brewery_data(valid_address_data):
    return {
        "id": "brewery_1",
        "name": "Sample Brewery",
        "address": valid_address_data,
        "phone": "123-456-7890",
        "website_url": "http://samplebrewery.com",
    }


# --- Tests ---


class TestCoordinate:
    def test_coordinate_valid(self, valid_coordinate_data):
        """Test creating a Coordinate with valid inputs."""
        coord = Coordinate(**valid_coordinate_data)
        assert coord.longitude == 12.34
        assert coord.latitude == 56.78

    def test_valid_coordinate(self):
        coordinate = Coordinate(longitude=45.1234, latitude=-93.4567)
        assert coordinate.to_str() == "-93.4567,45.1234"

    def test_coordinate_invalid(self):
        """Test creating a Coordinate with invalid inputs."""
        with pytest.raises(ValueError, match="Cannot convert longitude='abc' to float"):
            Coordinate(longitude="abc", latitude="56.78")

    def test_coordinate_none(self):
        """Test creating a Coordinate with None values."""
        coord = Coordinate(longitude=None, latitude=None)
        assert coord.longitude is None
        assert coord.latitude is None


class TestAddress:
    def test_address_from_dict_valid(self, valid_address_data):
        """Test creating an Address from valid dictionary data."""
        address = Address.from_dict(valid_address_data)
        assert address.address_one == "123 Main St"
        assert address.city == "Sample City"
        assert address.state == "Sample State"
        assert address.postal_code == "12345"
        assert address.country == "Sample Country"
        assert address.coordinate.longitude == 12.34
        assert address.coordinate.latitude == 56.78

    def test_address_from_dict_missing_fields(self, valid_address_data):
        """Test creating an Address with missing fields."""
        data = valid_address_data.copy()
        del data["address_2"]  # Simulating missing field
        with pytest.raises(KeyError, match="'address_2'"):
            Address.from_dict(data)


class TestBrewery:
    def test_brewery_from_dict_valid(self, valid_brewery_data):
        """Test creating a Brewery from valid dictionary data."""
        brewery = Brewery.from_dict(valid_brewery_data)
        assert brewery.id == "brewery_1"
        assert brewery.name == "Sample Brewery"
        assert brewery.address.city == "Sample City"
        assert brewery.address.coordinate.longitude == 12.34
        assert brewery.phone == "123-456-7890"
        assert brewery.website_url == "http://samplebrewery.com"

    def test_brewery_from_dict_missing_fields(self, valid_brewery_data):
        """Test creating a Brewery with missing fields."""
        data = valid_brewery_data.copy()
        del data["phone"]  # Simulating missing field
        with pytest.raises(KeyError):
            Brewery.from_dict(data)
