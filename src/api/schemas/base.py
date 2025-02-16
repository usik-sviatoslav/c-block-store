from fastapi import Query
from pydantic import BaseModel, ConfigDict

from apps.currency.choices import CurrencyChoices
from apps.provider.choices import ProviderChoices


class BaseModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PaginationRequestQuery:
    def __init__(
        self,
        skip: int | None = Query(default=0, ge=0),
        limit: int | None = Query(default=100, ge=0),
    ) -> None:
        self.skip = skip or 0
        self.limit = limit or 100


class FilterByCurrencyProviderRequestQuery:
    def __init__(
        self,
        currency: CurrencyChoices | None = Query(None),
        provider: ProviderChoices | None = Query(None),
    ) -> None:
        self.currency = currency
        self.provider = provider
