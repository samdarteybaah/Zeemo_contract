import logging
import sys
from pythonjsonlogger import jsonlogger


def configure_logger() -> logging.Logger:
    """
    Configures and returns a structured JSON logger.
    """

    logger = logging.getLogger("zeemo")
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.propagate = False

    return logger


# Global logger instance
logger = configure_logger()