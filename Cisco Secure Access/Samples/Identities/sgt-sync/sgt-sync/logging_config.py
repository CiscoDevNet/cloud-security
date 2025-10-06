# sgt_sync/logging_config.py
import logging
from logging.config import dictConfig

def setup_logging():
    """Configures logging for the application and returns the main logger."""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - [%(name)s:%(lineno)d]: %(levelname)s: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "default": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "sgt_sync": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
            "root": {"level": "INFO", "handlers": ["default"]},
        }
    )
    return logging.getLogger("sgt_sync")