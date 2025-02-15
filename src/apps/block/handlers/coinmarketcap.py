from typing import Any

from .base import BaseBlockDataHandler


class CoinMarketCapHandler(BaseBlockDataHandler):
    def fetch_data(self) -> dict[str, Any]:
        url = "https://pro-api.coinmarketcap.com/v1/blockchain/statistics/latest"
        headers = {"X-CMC_PRO_API_KEY": self.api_key}
        return self.fetch_json(url, headers=headers)

    def parse_data(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        data = raw_data["data"]["BTC"]
        return {
            "block_number": int(data["total_blocks"]),
            "created_at": self.parse_datetime(data["first_block_timestamp"]),
            "currency_id": self.currency_id,
            "provider_id": self.provider_id,
        }
