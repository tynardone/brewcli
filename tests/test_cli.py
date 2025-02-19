import httpx
import pytest
from click.testing import CliRunner

from brewcli.cli import cli

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


def test_random_success(mocker, cli_runner, brewery_reponse_single):
    """
    Tests that the 'random' command correctly retrieves and displays a brewery
    by mocking an API request and verifying the expected output and request parameters.
    """

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = brewery_reponse_single

    mock_client = mocker.Mock(spec=httpx.Client)
    mock_client.get.return_value = mock_response
    mocker.patch("httpx.Client", return_value=mock_client)

    result = cli_runner.invoke(cli, ["random", "1"])
    assert result.exit_code == 0
    assert "Osgood Brewing" in result.output
    assert "Grandville" in result.output
    assert "http://www.osgoodbrewing.com" in result.output

    mock_client.get.assert_called_once_with(
        "https://api.openbrewerydb.org/v1/breweries/random", params={"size": 1}
    )


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
