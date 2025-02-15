from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.currency.models import Currency
from apps.provider.models import Provider
from core.django.db.models import UUIDv7Model


class Block(UUIDv7Model):
    class Meta:
        db_table = "block"
        verbose_name = _("Block")
        verbose_name_plural = _("Blocks")

    block_number = models.BigIntegerField()
    created_at = models.DateTimeField()
    stored_at = models.DateTimeField(auto_now_add=True)

    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    def __str__(self) -> str:
        args = (self.block_number, self.provider.name, self.currency.name, self.created_at)
        return " | ".join(str(arg) for arg in args)
