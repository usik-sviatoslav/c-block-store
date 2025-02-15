from typing import Any

from .base import BaseBlockDataHandler


class BlockchairHandler(BaseBlockDataHandler):
    def fetch_data(self) -> dict[str, Any]:
        url = "https://api.blockchair.com/ethereum/stats"
        return self.fetch_json(url)

    def parse_data(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        data = raw_data["data"]
        return {
            "block_number": int(data["best_block_height"]),
            "created_at": self.parse_datetime(data["best_block_time"]),
            "currency_id": self.currency_id,
            "provider_id": self.provider_id,
        }
