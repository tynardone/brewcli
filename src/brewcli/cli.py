import click
from httpx import HTTPError

from .brewery import BreweryAPI
from .models import BREWERY_TYPES, Brewery, Coordinate, SearchQuery
from .render import render_breweries, render_brewery


@click.group()
def cli() -> None:
    """
    A simple CLI that retrieves random breweries and displays their name, location,
    and a link to their website.

    Provide a number specifying how many breweries you would like!
    """


@cli.command()
@click.argument("number", type=click.IntRange(min=1))
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
            click.echo(f"HTTP error: {exc}", err=True)
            return
        except (KeyError, TypeError) as exc:
            click.echo(
                f"Error occurred while instantiating Brewery from response data: {exc}",
                err=True,
            )
            return

    render_breweries(breweries)


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
            return
        except HTTPError as exc:
            click.echo(f"HTTP error: {exc}", err=True)
            return

    render_brewery(brewery)


@cli.command()
@click.option("--by-city", type=click.STRING)
@click.option("--by-country", type=click.STRING)
@click.option("--by-dist", type=click.STRING, help="Coordinates as 'lat,lon'")
@click.option("--by-name", type=click.STRING)
@click.option("--by-postal", type=click.STRING)
@click.option("--by-state", type=click.STRING)
@click.option("--by-type", type=click.Choice(BREWERY_TYPES, case_sensitive=False))
def search(**filters: str | None) -> None:
    """Retrieve a set of breweries using one or more search terms."""
    by_dist = filters.pop("by_dist")
    coord = None
    if by_dist:
        try:
            coord = Coordinate.from_str(by_dist)
        except ValueError as exc:
            click.echo(f"Invalid --by-dist value: {exc}", err=True)
            return

    query = SearchQuery(
        coord=coord,
        city=filters["by_city"],
        country=filters["by_country"],
        name=filters["by_name"],
        postal=filters["by_postal"],
        state=filters["by_state"],
        type=filters["by_type"],
    )

    with BreweryAPI() as client:
        try:
            results = client.get_brewery_filters(query)
        except HTTPError as exc:
            click.echo(f"HTTP Exception: {exc}", err=True)
            return

    if not results:
        click.echo("No breweries found.")
        return

    breweries: list[Brewery] = []
    for data in results:
        try:
            breweries.append(Brewery.from_dict(data))
        except (KeyError, TypeError) as exc:
            click.echo(f"Error parsing brewery: {exc}", err=True)
            continue

    if breweries:
        render_breweries(breweries)


cli.add_command(random)
cli.add_command(by_id)
cli.add_command(search)
