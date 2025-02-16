from datetime import datetime
from uuid import UUID

from .base import BaseModelSchema
from .currency import CurrencyReadSchema
from .provider import ProviderReadSchema


class BlockReadSchema(BaseModelSchema):
    id: UUID  # noqa: VNE003
    stored_at: datetime
    created_at: datetime
    block_number: int
    currency: CurrencyReadSchema
    provider: ProviderReadSchema
