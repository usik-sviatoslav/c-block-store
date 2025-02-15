from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import ProviderChoices, ProviderCurrencies


class Provider(models.Model):
    class Meta:
        db_table = "provider"
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")

    name = models.CharField(max_length=32, unique=True, choices=ProviderChoices.choices)
    api_key = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name

    @property
    def currency_symbol(self) -> str:
        return str(getattr(ProviderCurrencies, self.name.upper()).value)
