import csv
import json
from pathlib import Path

import click
from httpx import HTTPError

from .brewery import BreweryAPI
from .models import Brewery

brewery_client = BreweryAPI()


class UnsupportedFileFormatError(Exception):
    """Custom exceptoin for unsupported file formats."""


def save_option(func):
    return click.option(
        "--save",
        type=click.File(mode="w", encoding="utf-8"),
        default=None,
        help="File path to save the retreived breweries data as JSON.",
    )(func)


def save_data(data: list[Brewery], file_obj) -> None:
    """Function to handle saving json"""
    suffix = Path(file_obj.name).suffix.lower()
    if suffix == ".json":
        json.dump(data, file_obj, indent=4)
    elif suffix == ".csv":
        # write to csv
        fieldnames: set[str] = set(data[0].to_flat_dict().keys())
        writer = csv.DictWriter(
            file_obj,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        for brewery in data:
            writer.writerow(brewery.to_flat_dict())
    else:
        raise UnsupportedFileFormatError(f"Unsupported file format: {suffix}")


@click.group()
def cli() -> None:
    """
    A simple CLI that retrieves random breweries and displays their name, location,
    and a link to their website.

    Provide a number specifying how many brewerys you would like!
    """


@cli.command()
@click.argument("number", type=int)
@save_option
def random(number: int, save) -> None:
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

    if save:
        try:
            save_data(breweries, file_obj=save)
            click.echo(f"Data saved to {save.name}")
        except UnsupportedFileFormatError as exc:
            click.echo(f"Error: {exc}", err=True)
            raise click.Abort()


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
