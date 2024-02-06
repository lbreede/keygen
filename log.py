import json
import logging.config
import pathlib


def setup_logging() -> None:
    config_file = pathlib.Path("logging_configs/config.json")
    with open(config_file) as fp:
        config = json.load(fp)
    logging.config.dictConfig(config)
