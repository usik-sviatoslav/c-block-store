import logging
import os
from typing import Literal

__all__ = [
    "LOGGING",
    "LOGGING_LEVEL_CONSOLE",
    "LOGGING_LEVEL_FILE",
]

LOGGING_LEVEL_CONSOLE = os.getenv("LOGGING_LEVEL_CONSOLE", logging.INFO)
LOGGING_LEVEL_FILE = os.getenv("LOGGING_LEVEL_FILE", logging.WARNING)

Mb = 1024**2
LOG_FILE_MAX_BYTES = int(os.getenv("LOG_FILE_MAX_BYTES", 10 * Mb))
LOG_FILE_BACKUP_COUNT = int(os.getenv("LOG_FILE_BACKUP_COUNT", 5))


DEFAULT_HANDLERS = Literal[
    "console",
    "access",
    "file_access",
    "file_celery_beat",
    "file_celery_worker",
    "file_fastapi_errors",
    "file_django_errors",
]


def to_handlers(handlers: list[DEFAULT_HANDLERS] | None = None) -> dict:
    return {"handlers": handlers if handlers else [], "propagate": False}


def file_handler(file_name: str, level: int | str) -> dict:
    return {
        "formatter": "file",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"/var/log/backend/{file_name}",
        "backupCount": LOG_FILE_BACKUP_COUNT,
        "maxBytes": LOG_FILE_MAX_BYTES,
        "level": level,
    }


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": True,
        },
        "file": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s %(levelprefix)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            "use_colors": True,
        },
    },
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOGGING_LEVEL_CONSOLE,
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": LOGGING_LEVEL_CONSOLE,
        },
        "file_access": file_handler("access/access.log", logging.INFO),
        "file_celery_beat": file_handler("celery/beat.log", LOGGING_LEVEL_FILE),
        "file_celery_worker": file_handler("celery/worker.log", LOGGING_LEVEL_FILE),
        "file_fastapi_errors": file_handler("fastapi/errors.log", LOGGING_LEVEL_FILE),
        "file_django_errors": file_handler("django/errors.log", LOGGING_LEVEL_FILE),
    },
    "loggers": {
        "uvicorn": to_handlers(["console"]),
        "uvicorn.access": to_handlers(["access", "file_access"]),
        "uvicorn.error": to_handlers(["console", "file_fastapi_errors"]),
        # ---------------------------------------------------------------------
        "django": to_handlers(["console", "file_django_errors"]),
        "django.request": to_handlers(["console", "file_django_errors"]),
        "django.db.backends": to_handlers(["console", "file_django_errors"]),
        "django.security.csrf": to_handlers(["console", "file_django_errors"]),
        # ---------------------------------------------------------------------
        "celery": to_handlers(["console"]),
        "celery.beat": to_handlers(["console", "file_celery_beat"]),
        "celery.worker": to_handlers(["console", "file_celery_worker"]),
        # ---------------------------------------------------------------------
        "healthcheck": to_handlers(["console"]),
    },
}
