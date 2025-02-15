from contextlib import suppress

from django.db import models
from django.db.utils import OperationalError, ProgrammingError
from django.utils.translation import gettext_lazy as _

from .choices import CurrencyChoices
from .utils import log_added_currencies


class Currency(models.Model):
    class Meta:
        db_table = "currency"
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.symbol} - {self.name}"

    @classmethod
    def sync_with_choices(cls) -> None:
        """Synchronizes the database with CurrencyChoices"""
        with suppress(OperationalError, ProgrammingError):
            currencies = set(CurrencyChoices.choices)
            db_currencies = set(cls.objects.values_list("symbol", "name"))

            if to_add := currencies - db_currencies:
                currencies_list = [cls(symbol=symbol, name=name) for symbol, name in to_add]
                Currency.objects.bulk_create(currencies_list)

                log_added_currencies(to_add)
