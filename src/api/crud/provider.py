from typing import Any

from apps.provider.models import Provider

from .base import CRUDBase

__all__ = ["crud"]


class CRUDProvider(CRUDBase[Provider, Any, Any]):
    pass


crud = CRUDProvider(Provider)
