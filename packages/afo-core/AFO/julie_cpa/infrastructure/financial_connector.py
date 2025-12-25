# Trinity Score: 90.0 (Established by Chancellor)
import asyncio
import random
from typing import Any

from AFO.julie_cpa.config import julie_config


class FinancialConnector:
    """
    [Three Kingdoms #14 & #21]
    Resilient Connector for External Financial APIs (Mocked).
    Implements Retry (Three Visits) and Circuit Breaker (Bitter Meat).
    """

    def __init__(self) -> None:
        self._circuit_open = False
        self._failure_count = 0
        self._threshold = julie_config.MAX_RETRIES

    async def fetch_bank_data(self, account_id: str) -> dict[str, Any]:
        """
        [Three Kingdoms #14: Three Visits]
        Retries up to 3 times before giving up.
        """
        if self._circuit_open:
            print("⚡ [Circuit Breaker] Open! Skipping request to protect system.")
            return {"error": "Circuit Open"}

        for attempt in range(1, julie_config.MAX_RETRIES + 1):
            try:
                print(
                    f"🔄 [Attempt {attempt}/{julie_config.MAX_RETRIES}] Connecting to Bank for {account_id}..."
                )
                data = await self._mock_api_call(account_id)
                self._success()
                return data
            except Exception as e:
                print(f"⚠️ Connection Failed: {e}")
                await asyncio.sleep(
                    julie_config.RETRY_BACKOFF_FACTOR * attempt
                )  # Exponential Backoff

        self._record_failure()
        return {"error": "Max Retries Exceeded"}

    async def _mock_api_call(self, account_id: str) -> dict[str, Any]:
        # Simulate Network Flakiness (Fog of War) - Reduced failure rate for stability
        if random.random() < 0.05:  # Reduced from 30% to 5% for better stability
            raise ConnectionError("Network Glitch")

        # Add small delay to simulate network latency
        await asyncio.sleep(0.1)

        return {
            "account_id": account_id,
            "balance": 1000000,
            "currency": "KRW",
            "status": "ACTIVE",
        }

    def _record_failure(self) -> None:
        self._failure_count += 1
        if self._failure_count >= self._threshold:
            self._circuit_open = True
            print("💥 [Circuit Breaker] Threshold reached. Opening Circuit.")

    def _success(self) -> None:
        self._failure_count = 0
        self._circuit_open = False
