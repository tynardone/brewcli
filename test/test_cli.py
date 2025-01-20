import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    """
    Provides a shared CliRunner instance for CLI tests.
    """
    return CliRunner()
