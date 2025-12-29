# Trinity Score: 90.0 (Established by Chancellor)
from .trinity import TrinityInputs, TrinityMetrics


class TrinityManager:
    """
    [TrinityManager]
    The Keeper of the Kingdom's Balance.
    Manages the dynamic state of Trinity Scores (Base + Delta).

    Architecture (PDF Page 3):
    - Base Scores: Initialize at 100%.
    - Delta Logic: Apply real-time +/- based on actions.
    - Clamping: Ensure 0 <= Score <= 100.
    """

    # Trigger Definitions (SSOT Goodness)
    TRIGGERS = {
        "VERIFICATION_SUCCESS": {"truth": 5.0, "goodness": 2.0},
        "VERIFICATION_FAIL": {"truth": -10.0, "risk": 5.0},  # Risk increases
        "DRY_RUN_ACTIVE": {"goodness": 10.0, "risk": -5.0},
        "AUTO_RUN_ACTION": {"filial_serenity": 10.0, "beauty": 5.0},
        "MANUAL_INTERVENTION": {"filial_serenity": -5.0},  # Friction
        "ELEGANT_RESPONSE": {"beauty": 8.0},
        "PERSISTENCE_SAVE": {"eternity": 5.0},  # Checking point
    }

    def __init__(self) -> None:
        # Initial State: Perfect Harmony
        self.base_inputs = TrinityInputs(
            truth=1.0, goodness=1.0, beauty=1.0, filial_serenity=1.0
        )  # 100%
        self.eternity = 1.0

        # Accumulators for Deltas (reset periodically or decay?)
        # For V1, we just accumulate until reset.
        self.deltas: dict[str, float] = {
            "truth": 0.0,
            "goodness": 0.0,
            "beauty": 0.0,
            "filial_serenity": 0.0,
            "eternity": 0.0,
        }

    def apply_trigger(self, trigger_name: str) -> TrinityMetrics:
        """Apply a predefined trigger event to modify scores."""
        delta_map = self.TRIGGERS.get(trigger_name, {})
        for key, value in delta_map.items():
            if key == "risk":
                # Risk reduces Goodness (Goodness = 100 - Risk)
                # Or we can track risk separately.
                # For simplified Trinity model, Risk penalty is Goodness penalty.
                self.deltas["goodness"] -= value
            elif key in self.deltas:
                self.deltas[key] += value

        return self.get_current_metrics()

    def get_current_metrics(self) -> TrinityMetrics:
        """Calculate current metrics with clamping."""
        # Apply Deltas to Base (100 scale logic mapped to 0-1)
        # Delta of 10 points = 0.1

        new_inputs = TrinityInputs(
            truth=self.base_inputs.truth + (self.deltas["truth"] / 100.0),
            goodness=self.base_inputs.goodness + (self.deltas["goodness"] / 100.0),
            beauty=self.base_inputs.beauty + (self.deltas["beauty"] / 100.0),
            filial_serenity=self.base_inputs.filial_serenity
            + (self.deltas["filial_serenity"] / 100.0),
        )

        new_eternity = self.eternity + (self.deltas["eternity"] / 100.0)

        # Create metrics (Clamping happens inside from_inputs)
        return TrinityMetrics.from_inputs(new_inputs, eternity=new_eternity)


# Singleton Instance
trinity_manager = TrinityManager()
