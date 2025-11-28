"""import logging
from types import FrameType
from typing import cast
from loguru import logger

class InterceptHandler(logging.Handler):
    def emit(self,record:logging.LogRecord)->None:
        try:
            level=logger.level(record.levelname).name
        except ValueError:
            level=str(record.levelno)

        
        frame,depth=logging.currentframe(),2
        while frame.f_code.co_filename==logging.__file__:
            frame=cast(FrameType,frame.f_back)
            depth+=1

        logger.opt(depth=depth,exception=record.exc_info).log(
            level,
            record.getMessage(),

        )"""


import logging 
import logging.config
import sys

from app.config import settings


def setup_logging():
    LOG_FORMAT="INFO"

    logging_config={
        "version":1,
        "disable_existing_loggers":False,
        "formatters":{
            "default":{
                "format":LOG_FORMAT,
                "datefmt":"%Y-%m-%d %H:%M:%S",
            },
            "access":{
                "format":"%(asctime)s-%(levelname)s-[%(name)s]-%(message)s",
                "datefmt":"%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers":{
            "console":{
                "formatter":"default",
                "class":"logging.StreamHandler",
                "stream":sys.stdout,
            },
        },
        "loggers":{
            "app":{"handlers":["console"],"level":LOG_LEVEL,"propagate":False},
            "uvicorn":{"handlers":["console"],"level":"INFO","propogate":False},
            "uvicorn.access":{"handlers":["console"],"level":"INFO","formatter":"access","propogate":False},
            "sqlalchemy.engine":{"handlers":["console"],"level":"WARN","propogate":False}
        },
    }

    logging.config.dictConfig(logging_config)