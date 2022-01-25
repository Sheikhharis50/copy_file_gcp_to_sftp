import logging

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


def log(message: str, level: str = "info"):
    logger = dict(
        error=logging.error,
        info=logging.info,
        warn=logging.warn,
    )

    logger[level](message)
