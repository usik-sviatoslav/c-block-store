from typing import Any

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Currency


@receiver(post_migrate)
def sync_currencies_after_migrations(sender: Any, **kwargs: Any) -> None:  # noqa: F841
    Currency.sync_with_choices()
