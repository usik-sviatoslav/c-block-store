from django.db import models


class CurrencyChoices(models.TextChoices):
    ETH = "ETH", "Ethereum"
    BTC = "BTC", "Bitcoin"
