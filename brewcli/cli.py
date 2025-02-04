import json

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
@click.argument("number")
@click.option(
    "--save",
    type=click.Path(writable=True),
    default=None,
    help="File path to save the retreived breweries data as JSON.",
)
def random(number: int, save: str | None) -> None:
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

    for brewery in breweries:
        click.echo(brewery)

    if save:
        try:
            with open(save, "w", encoding="utf-8") as f:
                json.dump([brewery.__dict__ for brewery in breweries], f, indent=4)
                click.echo(f"Data successfully saved to {save}.")
        except IOError as e:
            click.echo(f"Failed to save data: {e}")


@cli.command()
@click.argument("id")
def by_id():
    """Retrieve a brewery by ID"""
    pass


@cli.command()
@click.argument()
def search():
    """Retrieve a set of breweries using search."""
    pass


cli.add_command(random)
cli.add_command(by_id, "id")
cli.add_command(search)
