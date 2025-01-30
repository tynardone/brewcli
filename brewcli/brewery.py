"""This module contains functions for calling Open Brewery DB API"""

from typing import Any

import httpx

from brewcli.models import SearchQuery


class BreweryAPI:
    """
    A class to interact with the Open Brewery DB API using httpx.

    This class provides methods to perform API requests, such as fetching
    random breweries and getting details for a specific brewery by ID.
    """

    BASE_URL = "https://api.openbrewerydb.org/v1/breweries"
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/html;q=0.9, */*;q=0.8",
    }

    def __init__(self, base_url: str = BASE_URL):
        """
        Initializes the BreweryAPI object with the base URL.

        Args:
            base_url (str): The base URL for the API. Defaults to Open Brewery DB URL.
        """
        self.base_url = base_url

        self.client = httpx.Client(headers=self.HEADERS)

    def _handle_request(
        self, endpoint: str | None = None, params: dict | None = None
    ) -> Any:
        """
        Internal method to handle GET requests to the API.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict): Any query parameters to include in the request.

        Returns:
            Any: The JSON response from the API.

        Raises:
            httpx.HTTPError: If the request fails.
            ValueError: If the response cannot be parsed as JSON.
        """
        if endpoint:
            url = f"{self.base_url}/{endpoint}"
        else:
            url = self.base_url

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            print(f"Error while requesting {exc.request.url!r}.")  # pylint: disable=no-member
            raise exc
        try:
            return response.json()
        except ValueError as exc:
            raise ValueError(f"Failed to parse response from {url}") from exc

    def get_random_breweries(self, number: int = 1) -> Any:
        """
        Fetches a specified number of random breweries from the Open Brewery DB API.

        Args:
            number (int): The number of random brewery results to return. Defaults to 1.

        Returns:
            list[dict]: A list of brewery details as dictionaries.
        """
        return self._handle_request("random", {"size": number})

    def get_brewery_by_id(self, brewery_id: str) -> Any:
        """
        Fetches a single brewery by its ID.

        Args:
            brewery_id (str): The ID of the brewery to fetch.

        Returns:
            dict: The brewery details.
        """
        return self._handle_request(brewery_id)

    def get_brewery_filters(self, search_query: SearchQuery) -> Any:
        """
        Fetches a list of breweries based on the specified search query filters.

        This method constructs the necessary query parameters from the provided
        `SearchQuery` object and sends a request to the Open Brewery DB API to
        retrieve breweries that match the search criteria.

        Args:
            search_query (SearchQuery): An object containing search filters to be
                                        applied to the brewery search.

        Returns:
            Any: The JSON response from the API, typically a list of breweries
                that match the search query.

        Raises:
            httpx.HTTPError: If the request to the API fails.
            ValueError: If the response cannot be parsed as JSON.
        """
        params = search_query.to_params()
        return self._handle_request(params=params)


if __name__ == "__main__":
    client = BreweryAPI()
    r = client.get_random_breweries(5)
    print(r)
