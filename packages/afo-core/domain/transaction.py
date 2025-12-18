# packages/afo-core/domain/transaction.py
from datetime import datetime

from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    amount: float
    description: str
    date: datetime
    category: str | None = None
    source: str = "manual"

    @classmethod
    def mock(cls):
        return cls(
            id="mock-tx-1",
            amount=15000.0,
            description="점심 식사 (Mock)",
            date=datetime.now(),
            category="식비",
            source="dry_run",
        )

    @classmethod
    def from_raw(cls, data: dict):
        return cls(**data)
