import click

from brewery import random_brewery
from models import Brewery


@click.group()
def cli() -> None:
    """
    A simple CLI that retrieves random breweries and displays their name, location,
    and a link to their website.

    Provide a number specifying how many results you would like!
    """
    pass


@cli.command()
@click.argument("number")
def random(number):
    breweries = [
        Brewery.from_dict(brewery) for brewery in random_brewery(number=number)
    ]

    for result in breweries:
        click.echo(result)


if __name__ == "__main__":
    cli()
