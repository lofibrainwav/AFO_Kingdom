import pytest
import asyncio
from AFO.chancellor_graph import samaui_node, juyu_node, ChancellorState
from langchain_core.messages import HumanMessage

@pytest.mark.asyncio
async def test_samaui_node_sage_integration():
    print("\n🛡️ Testing Samaui Node (Sage Integration)...")
    
    # Mock State
    state: ChancellorState = {
        "messages": [HumanMessage(content="Initialize a secure payment gateway.")],
        "analysis_results": {"jegalryang": "Use Stripe API with webhook verification."},
        "kingdom_context": {},
        "steps_taken": 1
    }

    # Execute Node
    result = await samaui_node(state)
    
    # Verify
    assert "samaui" in result["analysis_results"]
    content = result["analysis_results"]["samaui"]
    print(f"✅ Samaui Response Length: {len(content)}")
    print(f"📝 Content Preview: {content[:100]}...")
    assert len(content) > 10

@pytest.mark.asyncio
async def test_juyu_node_sage_integration():
    print("\n桥 Testing Juyu Node (Sage Integration)...")
    
    state: ChancellorState = {
        "messages": [HumanMessage(content="Design a dashboard for Family Happiness.")],
        "analysis_results": {
            "jegalryang": "React/Next.js with Recharts.",
            "samaui": "Ensure data privacy for family members."
        },
        "kingdom_context": {},
        "steps_taken": 2
    }

    result = await juyu_node(state)
    
    assert "juyu" in result["analysis_results"]
    content = result["analysis_results"]["juyu"]
    print(f"✅ Juyu Response Length: {len(content)}")
    print(f"📝 Content Preview: {content[:100]}...")
    assert "**UI Strategy (Jwaja)**" in content
    assert "**UX Narrative (Hwata)**" in content

if __name__ == "__main__":
    asyncio.run(test_samaui_node_sage_integration())
    asyncio.run(test_juyu_node_sage_integration())
