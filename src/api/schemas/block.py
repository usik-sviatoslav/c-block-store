from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from api.schemas.currency import CurrencyRetrieve
from api.schemas.provider import ProviderRetrieve


class Block(BaseModel):
    class Config:
        from_attributes = True

    id: UUID  # noqa: VNE003
    stored_at: datetime
    created_at: datetime
    block_number: int
    currency: CurrencyRetrieve
    provider: ProviderRetrieve
