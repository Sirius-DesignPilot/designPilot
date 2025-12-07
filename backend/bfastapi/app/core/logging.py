import logging
import logging.config
import sys

from .config import settings  # ← DÜZELTİLDİ


def setup_logging():
    # Default log level (settings içinde varsa onu kullan)
    LOG_LEVEL = getattr(settings, "LOG_LEVEL", "INFO")

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "format": "%(asctime)s - %(levelname)s - [%(name)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,  # ← düzeltildi
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "formatter": "access",
                "propagate": False,  # ← düzeltildi
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,  # ← düzeltildi
            },
        },
    }

    logging.config.dictConfig(logging_config)
