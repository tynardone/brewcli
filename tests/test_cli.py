import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from brewcli import cli
from brewcli.models import Brewery

# In order to test CLI have to mock the BreweryAPI client and responses.
# Mock it  as "brewcli.cli.BreweryAPI"
# Then use CLIRunner to invoke the cli commands with arguments and options
# Use tmp_path fixture for files


# CLI Testing
# ------------------------------
# Test incorrect arguement values
# Test missing arguements
# Test datatypes
# Test Null values
# Check typing errors
# Test exceptions


@pytest.fixture(name="cli_runner")
def runner():
    """Provides a  CliRunner instance for CLI tepysts."""
    return CliRunner()


def test_random_success(mocker: MockerFixture, cli_runner: CliRunner) -> None:
    """Test the CLI correctly fetches and displays random breweries."""

    mock_client = mocker.MagicMock(spec=cli.BreweryAPI)
    mock_client.get_random_breweries.return_value = [
        {
            "id": "1",
            "name": "Test Brewery",
            "brewery_type": "micro",
            "address_1": "123 Main St",
            "city": "Sample City",
            "state": "CA",
            "postal_code": "12345",
            "country": "USA",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "phone": "555-1234",
            "website_url": "http://testbrewery.com",
        },
        {
            "id": "2",
            "name": "Another Brewery",
            "brewery_type": "nano",
            "address_1": "456 Another St",
            "city": "Another City",
            "state": "NY",
            "postal_code": "67890",
            "country": "USA",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "phone": "555-5678",
            "website_url": "http://anotherbrewery.com",
        },
    ]

    # Explicitly define __enter__ and __exit__ for context manager
    mock_api = mocker.MagicMock()
    mock_api.__enter__.return_value = mock_client
    mock_api.__exit__.return_value = None

    # Patch BreweryAPI with the explicitly defined mock
    mocker.patch("brewcli.cli.BreweryAPI", return_value=mock_api)

    # Use the real from_dict method but still track its calls
    mock_from_dict = mocker.patch.object(
        Brewery, "from_dict", side_effect=Brewery.from_dict
    )

    result = cli_runner.invoke(cli.random, ["2"])

    assert result.exit_code == 0

    mock_client.get_random_breweries.assert_called_once_with(number=2)

    print(mock_from_dict.call_args_list)

    assert mock_from_dict.call_count == 2

    assert "Test Brewery" in result.output
    assert "Another Brewery" in result.output


def test_random_api_fail(mock_brewery_api, cli_runner):
    pass


# Test by_id
def test_by_id_success(mock_brewery_api, clirunner):
    pass


def test_by_id_not_found(mock_brewery_api, clirunner):
    pass


def test_by_id_api_fail(mock_brewery_api, clirunner):
    pass


# Test search
def test_search_success(mock_brewery_api, clirunner):
    pass


def test_search_no_results(mock_brewery_api, clirunner):
    pass


def test_search_api_fail(mock_brewery_api, clirunner):
    pass
