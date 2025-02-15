from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CurrencyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Currency")
    name = "apps.currency"

    def ready(self) -> None:
        import apps.currency.signals  # noqa: F401
