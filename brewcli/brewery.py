"""This module contains functions for calling Open Brewery DB API"""

from typing import Any

import httpx


def random_brewery(number: int = 1) -> Any:
    """
    Fetches a specified number of random breweries from the Open Brewery DB API.

    Args:
        number (int): The number of random brewery results to return. Defaults to 1.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains details
        about a brewery. Each dictionary has the following structure:

        {
            "id": str,
            "name": str,
            "brewery_type": str,
            "address_1": str,
            "address_2": str | None,
            "address_3": str | None,
            "city": str,
            "state_province": str,
            "postal_code": str,
            "country": str,
            "longitude": str,
            "latitude": str,
            "phone": str,
            "website_url": str,
            "state": str,
            "street": str
        }

    Raises:
        httpx.HTTPError: If the HTTP request to the Open Brewery DB API fails.
        ValueError: If the response from the API cannot be parsed as JSON.
    """

    url = "https://api.openbrewerydb.org/v1/breweries/random"

    params = {"size": number}
    response = httpx.get(url=url, params=params)
    response.raise_for_status()

    return response.json()


def get_brewery() -> Any:
    pass
