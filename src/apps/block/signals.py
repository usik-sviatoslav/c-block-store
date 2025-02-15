import logging
from typing import Any

from django.dispatch import Signal, receiver
from django_celery_beat.models import PeriodicTask  # type: ignore

from apps.provider.models import Provider
from apps.provider.signals import TASK_NAME

logger = logging.getLogger("celery.worker")
provider_auth_failed = Signal()


@receiver(provider_auth_failed)
def delete_periodic_task_on_auth_fail(sender: Any, instance_id: int, reason: str, **kwargs: Any) -> None:  # noqa: F841
    """Signal handler that deletes a periodic Celery task when a provider fails authentication."""
    instance = Provider.objects.get(pk=instance_id)

    PeriodicTask.objects.filter(name=TASK_NAME % instance.name).update(enabled=False)
    logger.warning("Periodic task was disabled. Reason - %s. Task name - `%s`", reason, TASK_NAME % instance.name)
