import json
import logging.config
from pathlib import Path


def setup_logging() -> None:
    config_file = Path("logging_configs/config.json")
    with open(config_file) as fp:
        config = json.load(fp)
    logging.config.dictConfig(config)
