from pydantic import BaseModel as AnySchema

from api.schemas.provider import ProviderReadSchema as ReadSchema
from apps.provider.models import Provider

from .base import CRUDBase

__all__ = ["CRUDProvider"]


class CRUDProvider(CRUDBase[Provider, ReadSchema, AnySchema, AnySchema, AnySchema]):
    def __init__(self) -> None:
        super().__init__(Provider, ReadSchema)
