import logging
import sys
import json
from pathlib import Path
from types import FrameType
from typing import cast, Optional

from loguru import logger


class InterceptHandler(logging.Handler):

    loglevel_mapping = {
            50: 'CRITICAL',
            40: 'ERROR',
            30: 'WARNING',
            20: 'INFO',
            10: 'DEBUG',
            0: 'NOTSET',
        }

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = self.loglevel_mapping[record.levelno]

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )

class CustomizeLogger:

    loggers = ["uvicorn"]

    @classmethod
    def make_logger(cls,config_path: Path):

        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')

        logger = cls.customize_logging(
            filepath=logging_config.get('path'),
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            format=logging_config.get('format')
        )
        return logger

    @classmethod
    def customize_logging(
        cls,
        level: str,
        format: str,
        filepath: Optional[Path] = None,
        rotation: Optional[str] = None,
        retention: Optional[str] = None
    ):

        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )

        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in CustomizeLogger.loggers:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger


    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config

config_path = Path(__file__).parent.parent.with_name("logging_config.json")

# ? Single log instance -- to be used everywhere
LOG = CustomizeLogger.make_logger(config_path=config_path)