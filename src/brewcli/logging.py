import json
import logging
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "logging_config.json"
LOG_FILE_PATH = BASE_DIR / "brewcli.log"


def setup_logging():
    """Setup logging from a JSON config file."""
    with CONFIG_PATH.open("r") as f:
        config = json.load(f)

    # Ensures the log file directory exists
    LOG_FILE_PATH.touch(exist_ok=True)

    # Set up Queues for async logging

    logging.config.dictConfig(config)
