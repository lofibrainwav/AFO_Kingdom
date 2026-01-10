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
    # DSPy가 설치되지 않은 경우 모의 클래스 제공
    class MockMIPROv2:
        def __init__(self, **kwargs):
            pass

        def compile(self, program, trainset=None, valset=None):
            return program

    MIPROv2 = MockMIPROv2

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
        pred = (
            _pick_field(prediction, pred_key_candidates)
            if prediction is not None
            else None
        )

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

                # Safe-Save: try multiple methods to serialize the optimized program
                saved = False

                # Method 1: DSPy native save() if available
                if hasattr(optimized, "save") and callable(optimized.save):
                    try:
                        optimized.save(str(p))
                        saved = p.exists() and p.stat().st_size > 0
                    except Exception as save_err:
                        print(f"[AFO] DSPy save() failed: {save_err}")

                # Method 2: JSON fallback using state_dict or __dict__
                if not saved:
                    import json

                    state = None
                    if hasattr(optimized, "state_dict"):
                        state = optimized.state_dict()
                    elif hasattr(optimized, "dump_state"):
                        state = optimized.dump_state()
                    elif hasattr(optimized, "__dict__"):
                        # Extract serializable parts
                        state = {
                            "type": type(optimized).__name__,
                            "module_keys": list(
                                getattr(optimized, "__dict__", {}).keys()
                            ),
                            "timestamp": __import__("datetime")
                            .datetime.now()
                            .isoformat(),
                        }

                    if state is not None:
                        with open(p, "w", encoding="utf-8") as f:
                            json.dump(state, f, indent=2, default=str)
                        saved = p.exists() and p.stat().st_size > 0

                # Validation: 0-byte is failure
                if not saved or not p.exists() or p.stat().st_size == 0:
                    raise RuntimeError(
                        f"[AFO][FATAL] Artifact save failed: {p} is empty or missing"
                    )

                print(
                    f"[AFO] Optimization complete. Program saved to {save_path} ({p.stat().st_size} bytes)"
                )

            except Exception as e:
                # Write meta file for debugging
                meta_path = p.with_suffix(".meta.json")
                import json
                import os

                meta = {
                    "error": str(e),
                    "model": os.getenv("AFO_DSPY_MODEL", "unknown"),
                    "dspy_version": getattr(
                        __import__("dspy"), "__version__", "unknown"
                    ),
                    "timestamp": __import__("datetime").datetime.now().isoformat(),
                    "save_path": str(p),
                }
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2)
                print(f"[AFO][ERROR] Save failed. Meta written to {meta_path}")

                if strict:
                    raise

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
