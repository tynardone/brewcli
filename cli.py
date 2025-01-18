import click
from dataclasses import dataclass
from brewery import random_brewery


@dataclass
class Coordinate:
    longitude: int
    latitude: int


@dataclass
class Address:
    address_one: str
    address_two: str | None
    address_three: str | None
    street: str
    city: str
    state: str
    posta_code: str
    country: str
    coordinate: Coordinate


@dataclass
class Brewery:
    id: str
    name: str
    address: Address
    phone: str
    website_url: str


@click.command()
@click.argument("number")
def main(number) -> None:
    """
    A simple CLI that retrieves random breweries and displays their name, location,
    and a link to their website.

    Provide a number specifying how many results you would like!
    """
    response: list[dict] = random_brewery(number=number)
    for result in response:
        click.echo(
            f"{result.get("name")} located in {result.get("city")}, {result.get("state")}. Learn more at {result.get("website_url")}"
        )


if __name__ == "__main__":
    main()
