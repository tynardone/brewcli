import click
from httpx import HTTPError

from .brewery import BreweryAPI
from .models import Brewery

brewery_client = BreweryAPI()


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
    Retrieve a random set of breweries

    Args:
        number (int):
    """
    try:
        breweries = [
            Brewery.from_dict(brewery)
            for brewery in brewery_client.get_random_breweries(number=number)
        ]
    except HTTPError as exc:
        click.echo(f"HTTP Exception for {exc.request.url} - {exc}", err=True)
        return

    for brewery in breweries:
        click.echo(brewery)


@cli.command()
@click.argument("id")
def by_id():
    """Retrieve a brewery by ID"""


@cli.command()
@click.argument()
def search():
    """Retrieve a set of breweries using search."""


cli.add_command(random)
cli.add_command(by_id, "id")
cli.add_command(search)
