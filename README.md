# brewcli

> A command-line interface (CLI) for exploring breweries via the [Open Brewery DB API](https://www.openbrewerydb.org/).

![Code Style: Ruff][ruff-style]
![Type Checked: Mypy][mypy-check]
![Python Versions][python-versions]
![License][license]
![Downloads][downloads]

`brewcli` is a Python-based CLI tool designed to interact with the [Open Brewery DB API](https://www.openbrewerydb.org/). With `brewcli`, you can fetch random breweries, search breweries by city, state, or type, and more—all from the command line.

## Features

- Fetch a list of random breweries.
- Search breweries by city, country, name, postal code, state, type, or distance from a coordinate.
- Retrieve detailed information about a specific brewery by its ID.
- Output data in a user-friendly format.

## Installation

Install `brewcli` using pip:

```sh
pip install brewcli
```

## Usage example

Here are some examples of how to use brewcli:

Lists of breweries are rendered as a color table, and single-brewery lookups as a
detail panel. Website URLs are shown as clickable links in terminals that support them.

Get a number of random breweries (the count is required):

```sh
brewcli random 3
```

```text
  Name                 Type       Location            Phone        Website
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MadTree Brewing      regional   Cincinnati, Ohio    5138368733   madtreebrewing.com
  Rhinegeist Brewery   micro      Cincinnati, Ohio    —            rhinegeist.com
  Fifty West Brewing   brewpub    Cincinnati, Ohio    5138916996   fiftywestbrew.com
```

Look up a specific brewery by its ID:

```sh
brewcli by-id b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0
```

```text
╭─ MadTree Brewing  (regional) ─╮
│ 5164 Kennedy Ave              │
│ Cincinnati, Ohio 45213        │
│ United States                 │
│                               │
│ ☎  5138368733                 │
│ 🌐 madtreebrewing.com         │
╰───────────────────────────────╯
```

Search breweries by city:

```sh
brewcli search --by-city "Cincinnati"
```

Search breweries by state and type:

```sh
brewcli search --by-state "California" --by-type "micro"
```

Available `search` filters: `--by-city`, `--by-country`, `--by-dist` (coordinates as
`'lat,lon'`), `--by-name`, `--by-postal`, `--by-state`, and `--by-type` (one of:
`micro`, `nano`, `regional`, `brewpub`, `planning`, `contract`, `proprietor`, `closed`).

Run `brewcli --help` or `brewcli <command> --help` for full usage details.

## Development setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and is
pinned to Python 3.12 (see `.python-version`).

Clone the repository:

```sh
git clone https://github.com/tynardone/brewcli.git
cd brewcli
```

Create the virtual environment and install all dependencies (runtime + dev) from the
lockfile:

```sh
uv sync
```

Run the CLI:

```sh
uv run brewcli --help
```

Run tests:

```sh
uv run pytest
```

## Release History

- 0.2.1
  - Fix a crash when the API returned an HTTP error (`random`/`by-id` now show a
    friendly message instead of a traceback).
  - Fix an invalid PyPI classifier that broke the package build.
  - Ship `py.typed` so downstream type checkers use the bundled annotations.
  - Expand the test suite (CLI commands, error paths, and output rendering).
- 0.2.0
  - Rich terminal output: brewery lists render as a color table and single
    lookups as a detail panel, with clickable website links.
- 0.1.0
  - Initial release: `random`, `by-id`, and `search` commands.

## Meta

Tyler Nardone – <tynardone@gmail.com> - [LinkedIn](https://www.linkedin.com/in/tynardone/)

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/tynardone/brewcli](https://github.com/tynardone/brewcli)

<!-- Markdown link & img dfn's -->
[python-versions]: https://img.shields.io/pypi/pyversions/brewcli
[license]: https://img.shields.io/github/license/tynardone/brewcli
[downloads]: https://img.shields.io/pypi/dm/brewcli
[ruff-style]:https://img.shields.io/badge/code%20style-ruff-000000?style=flat&logo=python
[mypy-check]:https://img.shields.io/badge/type%20checked-mypy-blue?style=flat&logo=python
