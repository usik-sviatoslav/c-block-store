"""
ASGI config for `c-block-store` project.

It exposes the ASGI callable as a module-level variable named `app`.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from core.django.utils import settings_module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = get_asgi_application()
