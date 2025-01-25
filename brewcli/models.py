"""Module providing data objects"""

from dataclasses import dataclass, fields
from enum import Enum


@dataclass
class Coordinate:
    """
    Represents a geographic coordinate with latitude and longitude values.

    This class ensures that both latitude and longitude values are float-compatible and
    within the valid range of -180 to 180.

    Attributes:
        latitude (float): The latitude of the coordinate, a float value in the range [-180, 180].
        longitude (float): The longitude of the coordinate, a float value in the range [-180, 180].

    Methods:
        to_str() -> str: Returns a string representation of the coordinate in the
        format "<latitude>,<longitude>".

    Raises:
        ValueError: If the latitude or longitude is not convertible to a float or is
                    out of the valid range.
        TypeError: If the latitude or longitude is of type `None`.
    """

    latitude: float
    longitude: float

    def __post_init__(self):
        for f in fields(self):
            value = getattr(self, f.name)
            try:
                value = float(value)
                setattr(self, f.name, value)
            except ValueError as exc:
                raise ValueError(f"Cannot convert {f.name}={value!r} to float") from exc
            except TypeError as exc:
                raise TypeError(f"Cannot accept NoneType {f.name}={value!r}") from exc
            if abs(value) > 180:
                raise ValueError(
                    "Coordinate values must be within interval [-180, 180]"
                )

    def to_str(self) -> str:
        """
        Returns a string representation of the coordinate.

        Returns:
            str: A string in the format "<latitude>,<longitude>".

        Example:
            >>> coord = Coordinate(latitude=45.0, longitude=-93.0)
            >>> coord.to_str()
            '45.0,-93.0'
        """
        return f"{self.latitude},{self.longitude}"


@dataclass
class Address:
    """
    Represents a physical address and its associated geographic coordinate.

    This class contains attributes to define a complete address and an optional
    geographic coordinate (latitude and longitude).

    Attributes:
        address_one (str): The primary address line.
        address_two (str | None): The secondary address line, if any.
        address_three (str | None): The tertiary address line, if any.
        street (str): The street name.
        city (str): The city where the address is located.
        state (str): The state or province of the address.
        postal_code (str): The postal or ZIP code.
        country (str): The country of the address.
        coordinate (Coordinate | None): The geographic coordinate of the address,
            represented as a `Coordinate` object. Can be `None` if not provided.

    Methods:
        from_dict(data: dict) -> Address:
            Creates an `Address` object from a dictionary of attributes.
    """

    address_one: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    address_two: str | None = None
    address_three: str | None = None
    coordinate: Coordinate | None = None

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create and Address object from dictionary.
        """
        try:
            coordinate = Coordinate(
                longitude=data["longitude"], latitude=data["latitude"]
            )
        except (ValueError, KeyError, TypeError) as exc:
            print(f"Error: {exc}")
            coordinate = None
        return cls(
            address_one=data["address_1"],
            address_two=data["address_2"],
            address_three=data["address_3"],
            street=data["street"],
            city=data["city"],
            state=data["state"],
            postal_code=data["postal_code"],
            country=data["country"],
            coordinate=coordinate,
        )


@dataclass
class Brewery:
    """
    Represents a brewery and its associated details.

    This class encapsulates information about a brewery, including its ID, name,
    address, contact details, and website URL.

    Attributes:
        id (str): The unique identifier of the brewery.
        name (str): The name of the brewery.
        address (Address): The address of the brewery, represented as an `Address` object.
        phone (str): The phone number of the brewery.
        website_url (str): The website URL of the brewery.

    Methods:
        from_dict(data: dict) -> Brewery:
            Creates a `Brewery` object from a dictionary of attributes.
    """

    id: str
    name: str
    address: Address
    phone: str
    website_url: str

    @classmethod
    def from_dict(cls, data: dict) -> "Brewery":
        """
        Creates a `Brewery` object from a dictionary.

        Args:
            data (dict): A dictionary containing the brewery data. Expected keys include:
                - "id" (str): The brewery's unique identifier.
                - "name" (str): The brewery's name.
                - "address_1", "address_2", "address_3", "street", "city", "state",
                    "postal_code", "country": Address details passed to `Address.from_dict`.
                - "latitude", "longitude" (float): Geographic coordinates of the brewery.
                - "phone" (str): The brewery's phone number.
                - "website_url" (str): The brewery's website URL.

        Returns:
            Brewery: An instance of the `Brewery` class.

        Raises:
            KeyError: If required fields are missing in the input data.
            TypeError: If the input data is not a dictionary or contains incorrect types.

        Example:
            >>> data = {
            ...     "id": "b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0",
            ...     "name": "MadTree Brewing 2.0",
            ...     "address_1": "5164 Kennedy Ave",
            ...     "city": "Cincinnati",
            ...     "state": "Ohio",
            ...     "postal_code": "45213",
            ...     "country": "United States",
            ...     "latitude": 39.1885752,
            ...     "longitude": -84.4137736,
            ...     "phone": "5138368733",
            ...     "website_url": "http://www.madtreebrewing.com",
            ... }
            >>> brewery = Brewery.from_dict(data)
            >>> brewery.phones
            '5138368733'
        """
        address = Address.from_dict(data)
        return cls(
            id=data["id"],
            name=data["name"],
            address=address,
            phone=data["phone"],
            website_url=data["website_url"],
        )


class BreweryType(Enum):
    MICRO = "micro"
    NANO = "nano"
    REGIONAL = "regional"
    BREWPUB = "brewpub"
    PLANNING = "planning"
    CONTRACT = "contract"
    PROPRIETOR = "proprietor"
    CLOSED = "closed"


@dataclass
class SearchQuery:
    """
    Represents a set of search parameters for querying the OD Brewery API in a form it excpects.

    This class captures user input, validates certain parameters, and provides
    a method to convert the data into a dictionary suitable for use as query
    parameters in API requests.

    Attributes:
        by_city (str | None): The city to filter the search results by.
        by_country (str | None): The country to filter the search results by.
        by_dist (str | None): A string representing distance in the format
            "latitude,longitude".
        by_name (str | None): The name of the brewery to search for.
        by_state (str | None): The state to filter the search results by.
        by_postal (str | None): The postal code to filter the search results by.
        by_type (BreweryType | None): The type of brewery to filter results by.
        sort_order (str | None): The sorting order for the results, either 'asc' or 'desc'.
        by_ids (list[str] | None): A list of brewery IDs to filter the search results by.
        page (int | None): The page number for paginated results. Defaults to 1.
        per_page (int | None): The number of results per page. Defaults to 50, with
            a maximum value of 200.

    Methods:
        __post_init__(): Validates the parameters, ensuring sort_order is either
            'asc' or 'desc', page is 1 or greater, and per_page is between 1 and 200.
        to_params() -> dict: Converts the dataclass fields into a dictionary of
            query parameters, excluding any fields with a value of `None`.
    """

    by_city: str | None = None
    by_country: str | None = None
    by_dist: str | None = None  # Format: "latitude,longitude"
    by_name: str | None = None
    by_state: str | None = None
    by_postal: str | None = None
    by_type: BreweryType | None = None
    sort_order: str | None = None
    by_ids: list[str] | None = None
    page: int | None = 1
    per_page: int | None = 50  # Default 50, max 200

    def __post_init__(self):
        if self.sort_order is not None and self.sort_order not in ["asc", "desc"]:
            raise ValueError(
                f"Invalid sort_order '{self.sort_order}'. Must be 'asc' or 'desc'."
            )
        if self.page is not None and self.page < 1:
            raise ValueError("page must be 1 or greater")
        if self.per_page is not None and not 1 <= self.per_page <= 200:
            raise ValueError("per_page must be between 1 and 200")

    def to_params(self) -> dict:
        """
        Convert the dataclass into a dictionary of query parameters.
        """
        params = {
            "by_city": self.by_city,
            "by_country": self.by_country,
            "by_dist": self.by_dist,
            "by_ids": ",".join(self.by_ids) if self.by_ids else None,
            "by_name": self.by_name,
            "by_state": self.by_state,
            "by_postal": self.by_postal,
            "by_type": self.by_type.value if self.by_type else None,
            "page": self.page,
            "per_page": self.per_page,
            "sort_order": self.sort_order,
        }
        # Remove keys with `None` values
        return {k: v for k, v in params.items() if v is not None}
