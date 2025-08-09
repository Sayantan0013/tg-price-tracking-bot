from bot.utils.constants import LOG_FILE
import logging
import os

def get_logger(name: str = "Tg Logger") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # file handler
    ch = logging.FileHandler(LOG_FILE)
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s() - %(message)s'
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
