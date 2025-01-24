"""Module providing data objects"""

from dataclasses import dataclass, field, fields
from enum import Enum


@dataclass
class Coordinate:
    """
    Coordinate object in signed coordinate form.
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
            if abs(value) > 180:
                raise ValueError(
                    "Coordinate values must be within interval [-180, 180]"
                )

    def to_str(self) -> str:
        """
        Returns a string of format "<latitude>,<longitude>"
        """
        return f"{self.latitude},{self.longitude}"


@dataclass
class Address:
    """
    Brewery address
    """

    address_one: str
    address_two: str | None
    address_three: str | None
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    coordinate: Coordinate | None

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create and Address object from dictionary.
        """
        try:
            coordinate = Coordinate(
                longitude=data["longitude"], latitude=data["latitude"]
            )
        except (ValueError, TypeError):
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
    Class for brewery data recieved from API.
    """

    id: str
    name: str
    address: Address
    phone: str
    website_url: str

    @classmethod
    def from_dict(cls, data: dict) -> "Brewery":
        """
        Create a Brewery object from a dictionary.
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
    """
    Allowable options for brewery type.
    """

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
    Class for capturing and validating search parameters from users.
    """

    by_city: str | None
    by_country: str | None
    by_dist: str | None  # Format: "latitude,longitude"
    by_name: str | None
    by_state: str | None
    by_postal: str | None
    by_type: BreweryType | None
    sort_order: str | None
    by_ids: list[str] | None = field(default_factory=list)
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
