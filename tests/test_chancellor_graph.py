import pytest
import asyncio
# Assuming chancellor_graph has an entry point, potentially 'o5_tigers_parallel_execution' or similar
# If 'chancellor_integrated_execution' exists as per prompt description.
# Looking at file list, 'chancellor_graph.py' exists.
from chancellor_graph import o5_tigers_parallel_execution

@pytest.mark.asyncio
async def test_integration_o5_tigers():
    """Test the parallel execution of 5 Tigers."""
    query_data = {"query": "Integration Test", "risk": 0.05, "code": "pass"}
    results = await o5_tigers_parallel_execution(query_data)
    
    assert isinstance(results, list)
    assert len(results) == 5
    # Depending on implementation, results might be floats or strings
    # Just asserting we got 5 results back
