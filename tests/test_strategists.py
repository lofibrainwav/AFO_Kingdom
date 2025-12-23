import pytest
from strategists.sima_yi import review as sima_review
from strategists.zhou_yu import optimize as zhou_optimize
from strategists.zhuge_liang import evaluate as zhuge_evaluate

# Since the actual implementations might rely on external services or specific logic,
# we will test the structure and error handling primarily, or assume the mocks if we were using dependency injection.
# However, for this integration, we are importing the functions directly.
# We assume the functions are pure or can handle the basic dictionary inputs.


@pytest.mark.asyncio
async def test_zhuge_liang_truth_pass():
    """Test Zhuge Liang (Truth) with valid data."""
    query_data = {"query": "Valid Query", "context": {"valid_structure": True}}
    # Assuming zhuge_evaluate returns a score (float)
    # If the actual implementation is complex, we might need to mock internal calls.
    # For now, we simulate the expected behavior based on phase 5 refactoring.
    score = zhuge_evaluate(query_data)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


@pytest.mark.asyncio
async def test_sima_yi_goodness_pass():
    """Test Sima Yi (Goodness) with low risk."""
    query_data = {"query": "Safe Query", "risk_level": 0.05, "ethics_pass": True}
    score = sima_review(query_data)
    assert score == 1.0 or score >= 0.9


@pytest.mark.asyncio
async def test_zhou_yu_beauty_pass():
    """Test Zhou Yu (Beauty) with narrative."""
    query_data = {"query": "UI Update", "narrative": "Glassmorphism"}
    score = zhou_optimize(query_data)
    assert score >= 0.0


@pytest.mark.asyncio
async def test_strategist_error_handling():
    """Test robust execution with invalid input (should not crash)."""
    # Zhuge
    try:
        zhuge_evaluate(None)
    except Exception:
        pytest.fail("Zhuge Liang raised exception on None input")

    # Sima
    try:
        sima_review(None)
    except Exception:
        pytest.fail("Sima Yi raised exception on None input")
