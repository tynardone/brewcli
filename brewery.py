import httpx
from typing import Any


def random_brewery(number: int = 1) -> Any:
    url = "https://api.openbrewerydb.org/v1/breweries/random"

    params = {"size": number}
    response = httpx.get(url=url, params=params)

    return response.json()
