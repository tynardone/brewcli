"""Tests for the rich-based output rendering in render.py."""

import io

import pytest
from rich.console import Console

from brewcli.models import Brewery
from brewcli.render import PLACEHOLDER, render_breweries, render_brewery


@pytest.fixture
def capture_console():
    """A rich Console writing to an in-memory buffer at a fixed width.

    Width is set wide enough that the table columns never wrap/truncate, so
    substring assertions on names and values are reliable.
    """
    buffer = io.StringIO()
    console = Console(file=buffer, width=200, force_terminal=False)
    return console, buffer


@pytest.fixture
def brewery(brewery_data):
    return Brewery.from_dict(brewery_data)


class TestRenderBrewery:
    def test_panel_includes_core_fields(self, brewery, capture_console):
        console, buffer = capture_console
        render_brewery(brewery, out=console)
        output = buffer.getvalue()

        assert "Osgood Brewing" in output
        assert "brewpub" in output
        assert "Grandville" in output
        assert "Michigan" in output
        assert "111-111-1111" in output
        # Website is shown without the scheme.
        assert "osgoodbrewing.com" in output

    def test_panel_placeholder_for_missing_contact(self, brewery_data, capture_console):
        brewery_data["phone"] = None
        brewery_data["website_url"] = None
        brewery = Brewery.from_dict(brewery_data)

        console, buffer = capture_console
        render_brewery(brewery, out=console)
        output = buffer.getvalue()

        assert PLACEHOLDER in output
        assert "Osgood Brewing" in output


class TestRenderBreweries:
    def test_table_lists_all_breweries(self, brewery_data, capture_console):
        second = dict(brewery_data, id="2", name="Second Brewery", city="Ann Arbor")
        breweries = [Brewery.from_dict(brewery_data), Brewery.from_dict(second)]

        console, buffer = capture_console
        render_breweries(breweries, out=console)
        output = buffer.getvalue()

        assert "Osgood Brewing" in output
        assert "Second Brewery" in output
        assert "Grandville" in output
        assert "Ann Arbor" in output
        # Column headers.
        assert "Name" in output
        assert "Website" in output

    def test_table_placeholder_for_missing_values(self, brewery_data, capture_console):
        brewery_data["phone"] = None
        brewery_data["website_url"] = None
        breweries = [Brewery.from_dict(brewery_data)]

        console, buffer = capture_console
        render_breweries(breweries, out=console)
        output = buffer.getvalue()

        assert PLACEHOLDER in output
