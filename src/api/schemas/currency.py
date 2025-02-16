from pydantic import BaseModel


class CurrencyRetrieve(BaseModel):
    class Config:
        from_attributes = True

    name: str
    symbol: str
