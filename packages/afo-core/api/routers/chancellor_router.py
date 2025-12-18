from typing import Any

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

try:
    from chancellor_graph import chancellor_graph
except ImportError:
    chancellor_graph = None  # type: ignore[assignment]

router = APIRouter(
    prefix="/chancellor",
    tags=["Chancellor (승상)"],
    responses={404: {"description": "Not found"}},
)


class ChancellorRequest(BaseModel):
    """Chancellor 요청 모델"""

    query: str
    trinity_score: float = 0.5  # V2: Single float value
    risk_score: float = 0.0  # V2: New field


@router.post("/invoke")
async def invoke_chancellor(request: ChancellorRequest) -> dict[str, Any]:
    """
    [Chancellor Endpoint]
    Invokes the LangGraph Chancellor to orchestrate the 3 Strategists.

    Args:
        request: ChancellorRequest - 쿼리 및 점수 정보

    Returns:
        dict[str, Any]: 응답, 화자, 전체 히스토리

    Raises:
        HTTPException: Chancellor 그래프가 없거나 실행 실패 시
    """
    if chancellor_graph is None:
        raise HTTPException(
            status_code=503,
            detail="Chancellor graph not available. Please check chancellor_graph module.",
        )

    try:
        # Generate a unique session ID for persistence (V2 Requirement)
        import uuid

        thread_id: str = str(uuid.uuid4())
        config: dict[str, Any] = {"configurable": {"thread_id": thread_id}}

        # Initial State
        initial_state: dict[str, Any] = {
            "messages": [HumanMessage(content=request.query)],
            "trinity_score": request.trinity_score,
            "risk_score": request.risk_score,
            "auto_run_eligible": False,
            "kingdom_context": {},
            "persistent_memory": {},
            "current_speaker": "user",
            "next_step": "chancellor",
            "analysis_results": {},
        }

        # Run Graph with Config
        # invoke returns the final state
        final_state: dict[str, Any] = await chancellor_graph.ainvoke(initial_state, config=config)

        # Extract Final Response
        last_message = final_state["messages"][-1]

        return {
            "response": str(last_message.content),
            "speaker": str(final_state.get("current_speaker", "system")),
            "full_history": [str(m.content) for m in final_state["messages"]],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
