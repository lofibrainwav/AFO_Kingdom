from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FinancialRecord:
    id: str
    description: str
    amount: float
    category: str
    risk_score: int  # 0-100 (Sima Yi Filter)
    status: str      # 'PENDING', 'APPROVED', 'REJECTED'

class JulieService:
    """
    Julie CPA Service (Financial Autonomous Driving)
    Strategy: Input -> Labeling -> Queue
    """
    
    def __init__(self):
        self.queue: List[FinancialRecord] = []

    async def ingest_record(self, description: str, amount: float) -> FinancialRecord:
        """Step 1: Input (Data Collection)"""
        # TODO: Integrate with grok_engine for real ingestion
        record = FinancialRecord(
            id="temp-id",
            description=description,
            amount=amount,
            category="UNCATEGORIZED",
            risk_score=0,
            status="PENDING"
        )
        return await self.assess_risk(record)

    async def assess_risk(self, record: FinancialRecord) -> FinancialRecord:
        """Step 2: Labeling (Sima Yi Risk Filter)"""
        # Simple logic for now: High amount = High risk
        if record.amount > 1000:
            record.risk_score = 80
        else:
            record.risk_score = 10
            
        record.category = "Auto-Classified"
        self.queue.append(record)
        return record

    async def get_approval_queue(self) -> List[FinancialRecord]:
        """Step 3: Queue (Approval Mechanism)"""
        return [r for r in self.queue if r.status == "PENDING"]

