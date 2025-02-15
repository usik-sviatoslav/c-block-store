import json
import logging
from typing import Any

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask  # type: ignore

from apps.currency.models import Currency

from .models import Provider

logger = logging.getLogger("django.db.backends")
TASK_NAME = "Fetch block data from provider: %s"


@receiver(post_save, sender=Provider)
async def create_periodic_task(sender: Any, instance: Provider, created: bool, **kwargs: Any) -> None:  # noqa: F841
    """Creates a cron job when adding a provider"""
    task_name = TASK_NAME % instance.name

    currency = await Currency.objects.aget(symbol=instance.currency_symbol)
    schedule, _ = await CrontabSchedule.objects.aget_or_create(minute="*", hour="*")

    task_kwargs = {
        "provider_name": instance.name,
        "provider_id": instance.pk,
        "currency_id": currency.pk,
        "api_key": instance.api_key,
    }

    task_obj, task_created = await PeriodicTask.objects.aupdate_or_create(
        task="apps.block.tasks.fetch_block_data",
        name=task_name,
        crontab=schedule,
        defaults={"kwargs": json.dumps(task_kwargs)},
    )
    logger.info(f"Periodic task was {'created' if task_created else 'updated'}. Task name: `%s`", task_name)


@receiver(post_delete, sender=Provider)
async def delete_periodic_task(sender: Any, instance: Provider, **kwargs: Any) -> None:  # noqa: F841
    """Deletes the cron job when the provider is removed"""
    await PeriodicTask.objects.filter(name=TASK_NAME % instance.name).adelete()
    logger.info("Periodic task deleted. Task name: `%s`", TASK_NAME % instance.name)
