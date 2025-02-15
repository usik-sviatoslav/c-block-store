from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString
from django.utils.translation import gettext_lazy as _

from .models import Block


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("block_number", "display_provider", "currency", "created_at", "stored_at")

    @admin.display(description=_("Provider"))
    def display_provider(self, obj: Block) -> SafeString:
        reverse_path = "admin:provider_provider_change"
        format_string = '<a href="{}">{}</a>'

        args = (reverse(reverse_path, args=[obj.pk]), obj.provider.name)
        return format_html(format_string, *args)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Block]:
        return super().get_queryset(request).select_related("currency", "provider")
