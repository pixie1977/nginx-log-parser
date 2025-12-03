import logging
import sys
from typing import Final

DEFAULT_LOG_FORMAT: Final[str] = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"


def configure_logging(level: str = "INFO") -> None:
    """Configure basic logging for the application.

    Parameters
    ----------
    level:
        Logging level as a string, e.g. 'DEBUG', 'INFO', 'WARNING'.
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format=DEFAULT_LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
    )
