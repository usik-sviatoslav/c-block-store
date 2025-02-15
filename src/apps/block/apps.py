from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlockConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Block")
    name = "apps.block"

    def ready(self) -> None:
        import apps.block.signals  # noqa: F401
