import click
from httpx import HTTPError

from .brewery import BreweryAPI
from .models import BREWERY_TYPES, Brewery


@click.group()
def cli() -> None:
    """
    A simple CLI that retrieves random breweries and displays their name, location,
    and a link to their website.

    Provide a number specifying how many brewerys you would like!
    """


@cli.command()
@click.argument("number", type=int)
def random(number: int) -> None:
    """
    Retrieve a random set of breweries.

    Args:
        number (int): The number of random breweries to retrieve.
    """
    with BreweryAPI() as client:
        try:
            breweries = [
                Brewery.from_dict(brewery)
                for brewery in client.get_random_breweries(number=number)
            ]
        except HTTPError as exc:
            click.echo(f"HTTP Exception for {exc.request.url} - {exc}", err=True)
            return

    for brewery in breweries:
        click.echo(brewery)
        click.echo()


@cli.command()
@click.argument("id")
def by_id(id: int):
    """Retrieve a brewery by ID"""


@cli.command()
@click.argument("search")
@click.option("--by-city", type=str)
@click.option("--by-country", type=str)
@click.option("--by-dist", type=str)
@click.option("--by-name", type=str)
@click.option("--by-postal", type=int)
@click.option("--by-type", type=click.Choice(BREWERY_TYPES, case_sensitive=False))
def search(by_city: str, by_country: str, by_dist: str, by_postal: int, by_type: str):
    """Retrieve a set of breweries using search."""


cli.add_command(random)
cli.add_command(by_id)
cli.add_command(search)
