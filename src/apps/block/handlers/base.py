import logging.config
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, cast

import redis
import requests
from dateutil import parser
from django.conf import settings
from django.utils import timezone
from requests import HTTPError, Response

from apps.block.signals import provider_auth_failed

logger = logging.getLogger("celery.worker")


class AbstractBlockHandler(ABC):
    @abstractmethod
    def fetch_data(self) -> dict[str, Any]:
        """Fetch data from the provider"""
        pass

    @abstractmethod
    def parse_data(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Parse the data received from the provider"""
        pass


class BaseBlockDataHandler(AbstractBlockHandler):
    def __init__(self, provider_id: int, provider_api_key: str, currency_id: int) -> None:
        self.redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)
        self.api_key = provider_api_key
        self.provider_id = provider_id
        self.currency_id = currency_id
        self.data: dict[str, Any] = {}

    @staticmethod
    def parse_datetime(dt_str: str) -> datetime:
        """Convert date to timezone-aware format"""
        dt = parser.parse(dt_str)
        return timezone.make_aware(dt) if dt.tzinfo is None else dt

    def process_data(self) -> None:
        self.data = self.parse_data(self.fetch_data())

        if not self.is_duplicate():
            self.save_data()

    def is_duplicate(self) -> bool:
        """Fetches last block number and returns True if block is duplicate"""
        key = f"provider-{self.provider_id}:currency-{self.currency_id}::last-block-number"
        is_duplicate = False

        last_block_number = cast(bytes | None, self.redis_client.get(key))
        current_block_number = self.data["block_number"]

        if last_block_number:
            if int(last_block_number.decode()) >= current_block_number:
                is_duplicate = True

        if not is_duplicate:
            self.redis_client.set(key, current_block_number)

        logger.debug(f"Block data is duplicate: {is_duplicate}")
        return is_duplicate

    def save_data(self) -> None:
        from apps.block.models import Block

        block = Block.objects.create(**self.data)
        logger.info(f"New block created: {block}")

    def response_status_check(self, response: Response) -> None:
        default_message = f"Response status: {response.status_code} {response.reason}"
        detail_message = f"{default_message}\n{response.text}"

        match response.status_code:
            case 200:
                logger.debug(default_message)
            case 401 | 403:
                logger.error(detail_message)
                provider_auth_failed.send(
                    sender=self.__class__,
                    instance_id=self.provider_id,
                    reason=response.reason,
                )
                raise HTTPError
            case _:
                logger.warning(detail_message)
                raise HTTPError

    def fetch_json(self, url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
        response = requests.get(url, headers=headers)
        self.response_status_check(response)
        data: dict[str, Any] = response.json()
        return data

    def fetch_data(self) -> dict[str, Any]:
        raise NotImplementedError("Subclasses should implement this method")

    def parse_data(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Subclasses should implement this method")

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.process_data()
