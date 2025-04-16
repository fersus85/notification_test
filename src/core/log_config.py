import json
import logging.config
import pathlib


def setup_logging() -> None:
    config_file = pathlib.Path(__file__).resolve().parent / "log_config.json"

    with open(config_file) as f_in:
        config = json.load(f_in)
        try:
            logging.config.dictConfig(config)
        except ValueError as ex:
            logging.error("Error setting up logging: %s", ex)
