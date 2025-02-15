import importlib
import logging.config
from typing import Any

from celery import shared_task  # type: ignore

from apps.block.handlers import BaseBlockDataHandler

logger = logging.getLogger("celery.worker")


@shared_task
def fetch_block_data(**kwargs: Any) -> None:
    """Calls a handler to retrieve blockchain data"""
    module = importlib.import_module("apps.block.handlers")

    provider_name = kwargs["provider_name"]
    handler_class_name = provider_name + "Handler"
    handler_class: type[BaseBlockDataHandler] | None = getattr(module, handler_class_name, None)

    if handler_class:
        logger.debug("Fetching block data for provider: %s", provider_name)
        handler_class(kwargs["provider_id"], kwargs["api_key"], kwargs["currency_id"])()
        logger.debug("Fetching block data complete for provider: %s\n", provider_name)
