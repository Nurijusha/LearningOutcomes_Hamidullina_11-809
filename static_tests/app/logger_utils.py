import os
import logging
import sys

LOG_DIR = "logs"
APP_LOGGER_NAME = 'main'


def setup_applevel_logger(logger_name=APP_LOGGER_NAME):
    """ Main logger for app. """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    fh = logging.FileHandler(f"{LOG_DIR}/all.log")
    fh.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger


def get_logger(module_name) -> logging.Logger:
    """ Return child logger with module name (e.g. main.test). """
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)
