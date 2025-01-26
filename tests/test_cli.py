import pytest
from click.testing import CliRunner

# Need to mock return data for all the CLI tests


@pytest.fixture
def runner():
    """
    Provides a shared CliRunner instance for CLI tests.
    """
    return CliRunner()
