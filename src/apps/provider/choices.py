import enum

from django.db import models

from apps.currency.choices import CurrencyChoices as Currency


class ProviderChoices(models.TextChoices):
    COINMARKETCAP = "CoinMarketCap", "CoinMarketCap"
    BLOCKCHAIR = "Blockchair", "Blockchair"


class ProviderCurrencies(enum.Enum):
    COINMARKETCAP = Currency.BTC
    BLOCKCHAIR = Currency.ETH
