import httpx
import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from brewcli import cli
from brewcli.models import SearchQuery


@pytest.fixture(name="cli_runner")
def runner():
    """Provides a CliRunner instance for CLI tests."""
    return CliRunner()


@pytest.fixture
def mock_client(mocker: MockerFixture):
    """Patch BreweryAPI and yield the inner client mock returned by the
    context manager, so tests can set return values / side effects on it.
    """
    client = mocker.MagicMock(spec=cli.BreweryAPI)
    api = mocker.MagicMock()
    api.__enter__.return_value = client
    api.__exit__.return_value = None
    mocker.patch("brewcli.cli.BreweryAPI", return_value=api, autospec=True)
    return client


@pytest.fixture
def response_data():
    return [
        {
            "id": "1",
            "name": "Test Brewery",
            "brewery_type": "micro",
            "address_1": "123 Main St",
            "street": "Sample Ave",
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
            "street": "Sample Ave",
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


# ---------------------------------------------------------------------------
# random
# ---------------------------------------------------------------------------
class TestRandom:
    def test_success(self, mock_client, cli_runner, response_data):
        mock_client.get_random_breweries.return_value = response_data

        result = cli_runner.invoke(cli.random, ["2"])

        assert result.exit_code == 0
        mock_client.get_random_breweries.assert_called_once_with(number=2)
        assert "Test Brewery" in result.output
        assert "Another Brewery" in result.output

    def test_invalid_number_rejected(self, cli_runner):
        """IntRange(min=1) should reject 0 and negatives at the Click layer."""
        result = cli_runner.invoke(cli.random, ["0"])
        assert result.exit_code != 0

    def test_http_error(self, mock_client, cli_runner):
        mock_client.get_random_breweries.side_effect = httpx.HTTPError("boom")

        result = cli_runner.invoke(cli.random, ["2"])

        assert result.exit_code == 0  # handled gracefully, not a crash
        assert result.exception is None
        assert "HTTP error" in result.output

    def test_parse_error(self, mock_client, cli_runner):
        """Malformed response data surfaces a friendly message, not a traceback."""
        mock_client.get_random_breweries.return_value = [{"id": "1"}]  # missing keys

        result = cli_runner.invoke(cli.random, ["1"])

        assert result.exit_code == 0
        assert result.exception is None
        assert "Error occurred" in result.output


# ---------------------------------------------------------------------------
# by-id
# ---------------------------------------------------------------------------
class TestById:
    def test_success(self, mock_client, cli_runner, response_data):
        mock_client.get_brewery_by_id.return_value = response_data[0]

        result = cli_runner.invoke(cli.by_id, ["1"])

        assert result.exit_code == 0
        mock_client.get_brewery_by_id.assert_called_once_with(brewery_id="1")
        assert "Test Brewery" in result.output

    def test_parse_error(self, mock_client, cli_runner):
        mock_client.get_brewery_by_id.return_value = {"id": "1"}  # missing keys

        result = cli_runner.invoke(cli.by_id, ["1"])

        assert result.exit_code == 0
        assert result.exception is None
        assert "Error occurred creating Brewery" in result.output

    def test_http_error(self, mock_client, cli_runner):
        mock_client.get_brewery_by_id.side_effect = httpx.HTTPError("boom")

        result = cli_runner.invoke(cli.by_id, ["123"])

        assert result.exit_code == 0
        assert result.exception is None
        assert "HTTP error" in result.output


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------
class TestSearch:
    def test_success(self, mock_client, cli_runner, response_data):
        mock_client.get_brewery_filters.return_value = response_data

        result = cli_runner.invoke(cli.search, ["--by-city", "Cincinnati"])

        assert result.exit_code == 0
        assert "Test Brewery" in result.output
        assert "Another Brewery" in result.output

    def test_filters_mapped_to_query(self, mock_client, cli_runner, response_data):
        """The --by-* options must map onto the right SearchQuery fields."""
        mock_client.get_brewery_filters.return_value = response_data

        result = cli_runner.invoke(
            cli.search, ["--by-city", "Denver", "--by-type", "micro"]
        )

        assert result.exit_code == 0
        query = mock_client.get_brewery_filters.call_args.args[0]
        assert isinstance(query, SearchQuery)
        assert query.city == "Denver"
        assert query.type == "micro"
        assert query.state is None

    def test_no_results(self, mock_client, cli_runner):
        mock_client.get_brewery_filters.return_value = []

        result = cli_runner.invoke(cli.search, ["--by-city", "Nowhere"])

        assert result.exit_code == 0
        assert "No breweries found." in result.output

    def test_http_error(self, mock_client, cli_runner):
        mock_client.get_brewery_filters.side_effect = httpx.HTTPError("boom")

        result = cli_runner.invoke(cli.search, ["--by-city", "Cincinnati"])

        assert result.exit_code == 0
        assert result.exception is None
        assert "HTTP Exception" in result.output

    def test_invalid_by_dist(self, mock_client, cli_runner):
        """A malformed --by-dist coordinate is reported and no request is made."""
        result = cli_runner.invoke(cli.search, ["--by-dist", "not-a-coord"])

        assert result.exit_code == 0
        assert "Invalid --by-dist value" in result.output
        mock_client.get_brewery_filters.assert_not_called()

    def test_invalid_by_type_rejected(self, cli_runner):
        """Click.Choice should reject an unknown brewery type."""
        result = cli_runner.invoke(cli.search, ["--by-type", "gigantic"])
        assert result.exit_code != 0

    def test_skips_unparseable_results(self, mock_client, cli_runner, response_data):
        """A malformed brewery in the results is skipped; valid ones still render."""
        mock_client.get_brewery_filters.return_value = [
            {"id": "bad"},  # missing required keys
            response_data[0],
        ]

        result = cli_runner.invoke(cli.search, ["--by-city", "Cincinnati"])

        assert result.exit_code == 0
        assert result.exception is None
        assert "Error parsing brewery" in result.output
        assert "Test Brewery" in result.output
