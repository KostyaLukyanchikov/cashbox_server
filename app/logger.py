import logging

import logging.config



MEGABYTE = 1024 * 1024


filebeat_handler = {
    "filebeat": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": "/var/log/filebeat.log",
        "backupCount": 1,
        "maxBytes": 3 * MEGABYTE,
        "filters": ["request_id", "headers"],
    },
}


LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": (
                "%(levelname)s::%(asctime)s:%(name)s.%(funcName)s : [%(message)s]"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "filelog": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "cashbox_server.log",
            "formatter": "default",
            "backupCount": 1,
            "maxBytes": 3 * MEGABYTE,
        },
    },
    "loggers": {
            "default": {
                "level": "INFO",
                "handlers": ["filelog"],
                "propagate": False,
            },
        },
    "disable_existing_loggers": True,
}


def init_logging():
    logging.config.dictConfig(LOGGING_CONFIG)


logger = logging.getLogger("default")
