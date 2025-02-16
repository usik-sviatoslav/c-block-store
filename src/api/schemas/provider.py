from .base import BaseModelSchema


class ProviderReadSchema(BaseModelSchema):
    name: str


class Provider(ProviderReadSchema):
    api_key: str
