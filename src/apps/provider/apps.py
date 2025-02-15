from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProviderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Provider")
    name = "apps.provider"

    def ready(self) -> None:
        import apps.provider.signals  # noqa: F401
