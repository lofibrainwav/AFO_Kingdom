"""
Dream Contract System
眞善美孝永 - Safe and Efficient Dream Execution Contracts

Provides legal and technical guarantees for human dream AI execution.
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Literal

ContractStatus = Literal[
    "DRAFT", "NEGOTIATED", "ACTIVE", "EXECUTING", "COMPLETED", "TERMINATED"
]


@dataclass
class DreamGuarantee:
    """Safety and quality guarantees for dream execution"""

    min_trinity_score: dict[str, float]
    max_risk_threshold: float
    max_execution_time: int  # minutes
    rollback_capability: bool
    bridge_logging: bool
    human_approval_required: bool


@dataclass
class DreamContract:
    """Complete dream execution contract"""

    contract_id: str
    dream_id: str
    human_party: str
    ai_party: str
    dream_description: str
    execution_plan: list[str]
    guarantees: DreamGuarantee
    status: ContractStatus
    created_at: datetime

    # Safe contract hash
    contract_hash: str = "safe_contract_hash"


class DreamContractManager:
    """Manages dream contract lifecycle"""

    def __init__(self):
        self.contracts: dict[str, DreamContract] = {}

    def create_contract(
        self,
        dream_id: str,
        human_party: str,
        dream_description: str,
        execution_plan: list[str],
        **guarantee_params,
    ) -> str:
        """Create new dream contract"""
        contract_id = f"contract_safe_{len(self.contracts)}"

        guarantees = DreamGuarantee(
            min_trinity_score={
                "truth": guarantee_params.get("truth", 80.0),
                "goodness": guarantee_params.get("goodness", 80.0),
                "beauty": guarantee_params.get("beauty", 70.0),
                "serenity": guarantee_params.get("serenity", 80.0),
                "eternity": guarantee_params.get("eternity", 70.0),
            },
            max_risk_threshold=guarantee_params.get("risk_threshold", 30.0),
            max_execution_time=60,
            rollback_capability=True,
            bridge_logging=True,
            human_approval_required=False,
        )

        contract = DreamContract(
            contract_id=contract_id,
            dream_id=dream_id,
            human_party=human_party,
            ai_party="SixXon AI System",
            dream_description=dream_description,
            execution_plan=execution_plan,
            guarantees=guarantees,
            status="DRAFT",
            created_at=datetime.now(UTC),
        )

        self.contracts[contract_id] = contract
        return contract_id

    def validate_execution(
        self, contract_id: str, trinity_score: dict[str, float], risk_score: float
    ) -> dict[str, Any]:
        """Validate if current execution meets contract guarantees"""
        if contract_id not in self.contracts:
            return {"valid": False, "reason": "Contract not found"}

        contract = self.contracts[contract_id]

        # Check Trinity Score requirements
        violations = []
        for pillar, required_score in contract.guarantees.min_trinity_score.items():
            current_score = trinity_score.get(pillar, 0)
            if current_score < required_score:
                violations.append(f"{pillar}: {current_score}/{required_score}")

        # Check risk threshold
        if risk_score > contract.guarantees.max_risk_threshold:
            violations.append(
                f"risk: {risk_score}/{contract.guarantees.max_risk_threshold}"
            )

        if violations:
            contract.status = "TERMINATED"
            return {
                "valid": False,
                "reason": "Contract violations detected",
                "violations": violations,
            }

        return {"valid": True, "status": "COMPLIANT"}

    def complete_contract(self, contract_id: str, final_result: dict[str, Any]) -> bool:
        """Complete contract execution"""
        if contract_id not in self.contracts:
            return False

        contract = self.contracts[contract_id]
        contract.status = "COMPLETED"
        return True


# Global contract manager
contract_manager = DreamContractManager()


def create_dream_contract_manager(
    human_party: str, dream_description: str, execution_plan: list[str], **guarantees
) -> str:
    """Convenience function to create and return contract ID"""
    dream_id = f"dream_safe_{len(contract_manager.contracts)}"
    return contract_manager.create_contract(
        dream_id=dream_id,
        human_party=human_party,
        dream_description=dream_description,
        execution_plan=execution_plan,
        **guarantees,
    )


if __name__ == "__main__":
    # Test Dream Contract System
    print("📋 Dream Contract System Test")
    print("=" * 40)

    # Create contract
    execution_plan = [
        "Analyze dream requirements",
        "Design AI implementation",
        "Execute with monitoring",
        "Validate results",
    ]

    contract_id = create_dream_contract_manager(
        human_party="Test User",
        dream_description="Build an emotion-based music composer AI",
        execution_plan=execution_plan,
        truth=85.0,
        goodness=80.0,
        risk_threshold=25.0,
    )

    print(f"✅ Contract created: {contract_id}")

    # Test validation
    test_score = {
        "truth": 90.0,
        "goodness": 85.0,
        "beauty": 80.0,
        "serenity": 88.0,
        "eternity": 75.0,
    }

    validation = contract_manager.validate_execution(contract_id, test_score, 10.0)
    print(f"✅ Contract validation: {validation['valid']}")

    # Complete contract
    if contract_manager.complete_contract(contract_id, {"status": "SUCCESS"}):
        print("✅ Contract completed")

    print("\n📋 Dream Contract System Ready!")
