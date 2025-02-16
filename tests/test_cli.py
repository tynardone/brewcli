import pytest
from click.testing import CliRunner

# In order to test CLI have to mock the BreweryAPI client and responses.
# Mock it  as "cli.BreweryAPI"
# Then use CLIRunner to invoke the cli commands with arguments and options
# Use tmp_path fixture for files


@pytest.fixture(name="runner")
def clirunner():
    """Provides a  CliRunner instance for CLI tepysts."""
    return CliRunner()


@pytest.fixture(autouse=True, name="breweryapi")
def mock_brewery_api(mocker):
    """Automatically mock BreweryAPI before each test."""
    mock_api = mocker.patch("brewcli.cli.BreweryAPI")
    mock_client = mock_api.return_value.__enter__.return_value
    return mock_client  # This will be used as a shared mock across tests


# Test random
def test_random_success(breweryapi, runner, brewery_data: dict):
    pass


def test_random_api_fail(mock_brewery_api, clirunner):
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
