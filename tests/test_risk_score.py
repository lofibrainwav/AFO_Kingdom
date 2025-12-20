import pytest

# Simulating Risk Calculator logic
async def calculate_risk_score(query_data):
    if "risk_level" in query_data:
        r = query_data["risk_level"]
        if not (0.0 <= r <= 1.0):
            raise ValueError("Risk range error")
        return r
    
    if query_data.get("query") == "delete all":
        return 1.0
        
    return 0.0

@pytest.mark.asyncio
async def test_risk_score_safe():
    query_data = {"query": "safe", "risk_level": 0.05}
    risk = await calculate_risk_score(query_data)
    
    assert isinstance(risk, float)
    assert 0.0 <= risk <= 0.1, "Risk should be safe (<= 0.1)"

@pytest.mark.asyncio
async def test_risk_score_danger():
    query_data = {"query": "delete all"}
    risk = await calculate_risk_score(query_data)
    
    assert risk == 1.0
    assert risk > 0.1, "Should exceed safety threshold"

def test_risk_score_invalid():
    with pytest.raises(ValueError):
        # We need to run the coroutine, but for exception testing on sync part (if any)
        # or just test the logic validation if extracted.
        # Here we simulated it in the function.
        import asyncio
        asyncio.run(calculate_risk_score({"risk_level": -0.5}))
