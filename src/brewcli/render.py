"""Rich-based rendering helpers for displaying breweries in the terminal."""

from rich.box import ROUNDED, SIMPLE_HEAVY
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .models import Brewery

console = Console()

# Shown in place of a missing value.
PLACEHOLDER = "—"


def _website_text(url: str | None) -> Text:
    """Render a website as a compact, clickable link where the terminal allows."""
    if not url:
        return Text(PLACEHOLDER, style="dim")
    display = (
        url.removeprefix("https://")
        .removeprefix("http://")
        .removeprefix("www.")
        .rstrip("/")
    )
    return Text(display, style=Style(link=url, color="blue", underline=True))


def _location(brewery: Brewery) -> str:
    """Human-readable "City, State" string, falling back gracefully."""
    address = brewery.address
    parts = [p for p in (address.city, address.state) if p]
    return ", ".join(parts) if parts else PLACEHOLDER


def render_breweries(breweries: list[Brewery], out: Console = console) -> None:
    """Print a list of breweries as a table."""
    table = Table(box=SIMPLE_HEAVY, header_style="bold magenta", expand=False)
    table.add_column("Name", style="bold cyan")
    table.add_column("Type", style="green")
    table.add_column("Location")
    table.add_column("Phone")
    table.add_column("Website")

    for brewery in breweries:
        table.add_row(
            brewery.name,
            brewery.brewery_type or PLACEHOLDER,
            _location(brewery),
            brewery.phone or PLACEHOLDER,
            _website_text(brewery.website_url),
        )

    out.print(table)


def render_brewery(brewery: Brewery, out: Console = console) -> None:
    """Print a single brewery as a detailed panel."""
    address = brewery.address
    body = Text()

    street = address.address_one or address.street
    if street:
        body.append(f"{street}\n")
    body.append(f"{_location(brewery)} {address.postal_code or ''}".rstrip() + "\n")
    if address.country:
        body.append(f"{address.country}\n")

    body.append("\n")
    body.append("☎  ", style="bold")
    body.append(f"{brewery.phone or PLACEHOLDER}\n")
    body.append("🌐 ", style="bold")
    body.append_text(_website_text(brewery.website_url))

    title = Text(brewery.name, style="bold cyan")
    title.append(f"  ({brewery.brewery_type})", style="green")

    out.print(Panel(body, title=title, title_align="left", box=ROUNDED, expand=False))
