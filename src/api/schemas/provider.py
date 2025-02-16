from pydantic import BaseModel


class Provider(BaseModel):
    name: str
    api_key: str


class ProviderRetrieve(BaseModel):
    class Config:
        from_attributes = True

    name: str
