import pytest
from click.testing import CliRunner

# In order to test CLI have to mock the BreweryAPI client and responses.
# Mock it  as "cli.BreweryAPI"
# Then use CLIRunner to invoke the cli commands with arguments and options
# Use tmp_path fixture for files


@pytest.fixture
def clirunner():
    """
    Provides a  CliRunner instance for CLI tests.
    """
    return CliRunner()


@pytest.fixture(autouse=True)
def setup_mocks(self, mocker):
    """Automatically apply mocks before each test."""
    self.mock_api = mocker.patch("cli.BreweryAPI")
    self.mock_client = self.mock_api.return_value.__enter__.return_value


# Test random
def test_random_success(mocker, clirunner):
    pass


def test_random_api_fail(mocker, clirunner):
    pass


# Test by_id
def test_by_id_success(mocker, clirunner):
    pass


def test_by_id_not_found(mocker, clirunner):
    pass


def test_by_id_api_fail(mocker, clirunner):
    pass


# Test search
def test_search_success(mocker, clirunner):
    pass


def test_search_no_results(mocker, clirunner):
    pass


def test_search_api_fail(mocker, clirunner):
    pass
