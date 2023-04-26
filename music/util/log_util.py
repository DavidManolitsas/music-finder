"""
Logging utility functions.
"""
import logging
import sys
from logging import Logger


def __create_logger() -> Logger:
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(module)s: %(message)s"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    api_registration_logger = logging.getLogger("music_finder_logger")
    api_registration_logger.setLevel(logging.INFO)
    api_registration_logger.addHandler(handler)
    return api_registration_logger


logger = __create_logger()


def get_logger() -> Logger:
    """
    Get logger.

    :return: Logger
    """
    return logger
