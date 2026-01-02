"""
DSPy MIPROv2 Optimizer Module for AFO Kingdom.
Combines AFO Philosophy (Trinity Score) with DSPy's automated optimization.
Robust implementation with Strict Mode for CI/CD gates.
"""

from pathlib import Path

from AFO.config.antigravity import antigravity
from AFO.services.trinity_calculator import calculate_trinity_score

try:
    from dspy.teleprompt import MIPROv2
except ImportError:
    MIPROv2 = None

# Inferred strict mode from environment or existing config
STRICT_MODE = True if antigravity.ENVIRONMENT == "test" else False


def compile_mipro(
    program,
    trainset,
    auto="light",  # light/medium/heavy
    valset=None,
    teacher=None,
    save_path="artifacts/dspy/optimized_program.json",
    truth_key_candidates=("ground_truth", "answer", "label", "y", "output"),
    pred_key_candidates=("answer", "output", "prediction", "text"),
    strict=STRICT_MODE,
):
    """
    AFO Kingdom MIPROv2 Optimization (Trinity Score Integrated).
    Robust against missing fields and environmental issues.

    Args:
        strict (bool): If True, raise exceptions on failure instead of fallback.
                       Defaults to True in 'test' environment.
    """
    if antigravity.DRY_RUN:
        print(
            f"[DRY_RUN] compile_mipro called with {len(trainset)} examples. Returning original program."
        )
        return program.deepcopy()

    if MIPROv2 is None:
        msg = "DSPy not installed or MIPROv2 not available."
        if strict:
            raise ImportError(msg)
        print(f"[MIPRO][FALLBACK] reason={msg}")
        return program.deepcopy()

    # Robust field extractor
    def _pick_field(obj, keys):
        for k in keys:
            if hasattr(obj, k):
                v = getattr(obj, k)
                if v is not None:
                    return v
            try:
                if isinstance(obj, dict) and k in obj and obj[k] is not None:
                    return obj[k]
            except Exception:
                pass
        return None

    # Trinity Metric Wrapper (Fail-Closed)
    def trinity_metric_fn(example, prediction, trace=None):
        gt = _pick_field(example, truth_key_candidates)
        pred = _pick_field(prediction, pred_key_candidates) if prediction is not None else None

        # Fail-closed: Return 0.0 if critical fields are missing
        if not gt or not pred:
            # You might want to log this in debug mode
            return 0.0

        # Cast to string safely ensuring no 'None' gets passed if picked value was not None
        # (Though checks above ensure truthiness, strict existence is safer)
        gt_str = str(gt)
        pred_str = str(pred)

        score_result = calculate_trinity_score(pred_str, gt_str)
        return score_result.overall

    optimizer = MIPROv2(
        metric=trinity_metric_fn,
        auto=auto,
    )

    # Auto-split valset if not provided
    if valset is None:
        valset = trainset[-20:] if len(trainset) >= 20 else None

    print(f"[AFO] Starting MIPROv2 Optimization (auto={auto})...")
    try:
        optimized = optimizer.compile(
            program.deepcopy(),
            trainset=trainset,
            valset=valset,
            teacher=teacher,
        )

        if save_path:
            p = Path(save_path)
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
                optimized.save(str(p))
                print(f"[AFO] Optimization complete. Program saved to {save_path}")
            except Exception as e:
                print(f"[WARNING] Failed to save optimized program: {e}")
                if strict:
                    raise e

        return optimized

    except Exception as e:
        if strict:
            raise e
        print(f"[MIPRO][FALLBACK] reason={e}")
        return program.deepcopy()


# Simple Test Block
if __name__ == "__main__":
    if antigravity.DRY_RUN:
        print("Dry Run Check: OK")
    else:
        print("Live Run Check: Ready (Requires DSPy + Data)")
