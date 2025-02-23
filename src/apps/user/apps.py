from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("User")
    name = "apps.user"
