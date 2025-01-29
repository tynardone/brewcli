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
- Search breweries by city, state, or brewery type.
- Retrieve detailed information about a specific brewery.
- Output data in a user-friendly format.

## Installation

Install `brewcli` using pip:

```sh
pip install brewcli
```

## Usage example

Here are some examples of how to use brewcli:

Get a Random Brewery

```sh
brewcli random
```

Search Breweries by City

```sh
brewcli search --city "Cincinnati"
```

Search Breweries by State and Type

```sh
brewcli search --state "California" --type "micro"
```

*For more examples and usage instructions, please refer to the documentation.*

## Development setup

To set up a development environment for brewcli, follow these steps:

Clone the repository:

```sh
git clone https://github.com/yourname/brewcli.git
cd brewcli
```

Set up a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Run tests:

```sh
pytest
```

## Release History

- 0.0.1
  - Work in progress

## Meta

Tyler Nardone – <tynardone@gmail.com> - [LinkedIn](https://www.linkedin.com/in/tynardone/)

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/tynardone/brewcli](https://github.com/tynardone/brewcli)

<!-- Markdown link & img dfn's -->
[python-versions]: https://img.shields.io/pypi/pyversions/brewcli
[license]: https://img.shields.io/github/license/yourname/brewcli
[downloads]: https://img.shields.io/pypi/dm/brewcli
[ruff-style]:https://img.shields.io/badge/code%20style-ruff-000000?style=flat&logo=python
[mypy-check]:https://img.shields.io/badge/type%20checked-mypy-blue?style=flat&logo=python
