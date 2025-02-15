import logging.config
import os

from celery import Celery  # type: ignore

from core.config.log import LOGGING, LOGGING_LEVEL_CONSOLE
from core.django.utils import settings_module

logging.config.dictConfig(LOGGING)

logger = logging.getLogger("celery")
logger.setLevel(LOGGING_LEVEL_CONSOLE)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("c-block-store")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    broker_connection_retry_on_startup=True,
    beat_max_loop_interval=10,
    accept_content=["json"],
    task_serializer="json",
    timezone="UTC",
)

app.autodiscover_tasks()
