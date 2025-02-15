from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask  # type: ignore

from .models import Provider
from .signals import TASK_NAME


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "display_api_key", "cron_job_status")
    fields = ("name", "api_key")

    @admin.display(description=_("api key"))
    def display_api_key(self, obj: Provider) -> str:
        return f"{'*' * len(obj.api_key)}"

    def get_readonly_fields(self, request: HttpRequest, obj: Provider | None = None) -> tuple[str, ...]:
        return ("name",) if obj else ()

    @admin.display(description=_("Cron job active"), boolean=True)
    def cron_job_status(self, obj: Provider) -> bool:
        task = PeriodicTask.objects.filter(name=TASK_NAME % obj.name).first()
        return task.enabled if task else False
