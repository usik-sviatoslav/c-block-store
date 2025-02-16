from .base import BaseModelSchema


class CurrencyReadSchema(BaseModelSchema):
    name: str
    symbol: str
