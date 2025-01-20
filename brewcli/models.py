from dataclasses import dataclass, fields


@dataclass
class Coordinate:
    longitude: float | None
    latitude: float | None

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if value is not None:
                try:
                    setattr(self, field.name, float(value))
                except ValueError:
                    raise ValueError(f"Cannot convert {field.name}={value!r} to float")


@dataclass
class Address:
    address_one: str
    address_two: str | None
    address_three: str | None
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    coordinate: Coordinate

    @classmethod
    def from_dict(cls, data: dict) -> "Address":
        coordinate = Coordinate(
            longitude=data.get("longitude"), latitude=data.get("latitude")
        )
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
    id: str
    name: str
    address: Address
    phone: str
    website_url: str

    @classmethod
    def from_dict(cls, data: dict) -> "Brewery":
        address = Address.from_dict(data)
        return cls(
            id=data["id"],
            name=data["name"],
            address=address,
            phone=data["phone"],
            website_url=data["website_url"],
        )
