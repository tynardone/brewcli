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

    Provide a number specifying how many results you would like!
    """


@cli.command()
@click.argument("number")
def random(number):
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
        click.echo(f"HTTP Exception for {exc.request.url} - {exc}")
        return

    for result in breweries:
        click.echo(result)
