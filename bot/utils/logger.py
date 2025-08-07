import logging

def get_logger(name: str = "Tg Logger") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s() - %(message)s'
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
