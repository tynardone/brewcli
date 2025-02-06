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
@click.argument("number", type=click.INT)
def random(number: int) -> None:
    """
    Retrieve a random set of breweries.

    Args:
        number (int): The number of random breweries to retrieve.
    """
    with BreweryAPI() as client:
        try:
            breweries: list[Brewery] = [
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
@click.argument("brewery_id", type=click.STRING)
def by_id(brewery_id: str) -> None:
    """Retrieve a brewery by ID"""
    with BreweryAPI() as client:
        try:
            data: dict = client.get_brewery_by_id(brewery_id=brewery_id)
            brewery: Brewery = Brewery.from_dict(data)
        except (KeyError, TypeError) as exc:
            click.echo(f"Error occurred creating Brewery from response data: {exc}")
        except HTTPError as exc:
            click.echo(f"HTTP Exception for {exc.request.url} - {exc}", err=True)

    click.echo(brewery)


@cli.command()
@click.option("--by-city", type=click.STRING)
@click.option("--by-country", type=click.STRING)
@click.option("--by-dist", type=click.STRING)
@click.option("--by-name", type=click.STRING)
@click.option("--by-postal", type=click.INT)
@click.option("--by-type", type=click.Choice(BREWERY_TYPES, case_sensitive=False))
def search(
    by_city: str | None,
    by_country: str | None,
    by_dist: str | None,
    by_postal: int | None,
    by_type: str | None,
    by_name: str | None,
):
    """Retrieve a set of breweries using search."""
    click.echo(type(by_country))


cli.add_command(random)
cli.add_command(by_id)
cli.add_command(search)
