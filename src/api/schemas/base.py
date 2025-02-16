from fastapi import Query

from apps.currency.choices import CurrencyChoices
from apps.provider.choices import ProviderChoices


class PaginationRequestQuery:
    def __init__(
        self,
        skip: int | None = Query(default=0, ge=0),
        limit: int | None = Query(default=100, ge=0),
    ) -> None:
        self.skip = skip
        self.limit = limit


class FilterByCurrencyProviderRequestQuery:
    def __init__(
        self,
        currency: CurrencyChoices | None = Query(None),
        provider: ProviderChoices | None = Query(None),
    ) -> None:
        self.currency = currency
        self.provider = provider
