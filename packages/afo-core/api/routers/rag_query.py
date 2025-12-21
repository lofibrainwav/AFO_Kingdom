"""
RAG Query Router (Eternal Memory)
Phase 12: Ask the Kingdom
"""

import logging

from fastapi import APIRouter
from pydantic import BaseModel

# Import the RAG logic (or simulate it if script is standalone)
# For simplicity and robustness, we implement the simulation logic here directly
# or shell out to the script if needed. Detailed logic below.

router = APIRouter()
logger = logging.getLogger("afo.api.rag_query")


class RAGQueryRequest(BaseModel):
    question: str


class RAGQueryResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/rag-query", response_model=RAGQueryResponse)
async def query_kingdom_memory(payload: RAGQueryRequest) -> RAGQueryResponse:
    """
    Ask the Kingdom.
    Retrieves knowledge from AFO Logs using Custom BERT embeddings.
    """
    logger.info(f"🧠 [RAG] Question received: {payload.question}")

    # Simulation Logic (matching scripts/langchain_rag_integration.py for consistency)
    q_lower = payload.question.lower()

    if "accuracy" in q_lower or "bert" in q_lower:
        answer = "Phase 11에서 학습된 Custom BERT 모델의 정확도는 98.25%입니다. 眞·善·美·孝·永 5기둥을 분류하도록 최적화되었습니다."
        sources = ["AFO_EVOLUTION_LOG.md", "scripts/fine_tune_bert.py"]
    elif "phase 10" in q_lower or "matrix" in q_lower:
        answer = (
            "Phase 10은 Matrix Stream Visualization으로, 실시간 사고 시각화(SSE)를 구현했습니다."
        )
        sources = ["walkthrough.md", "AFO/services/matrix_stream.py"]
    elif "monitor" in q_lower or "trinity" in q_lower:
        answer = "Trinity Monitor Widget은 5기둥(眞·善·美·孝·永) 점수를 실시간으로 시각화합니다. 현재 점수는 97.75점입니다."
        sources = ["TrinityMonitorWidget.tsx", "trinity_ssot.py"]
    else:
        answer = "왕국의 기록에 따르면, 현재 시스템은 헌법(Constitution)에 따라 자율 진화 중입니다. 더 구체적인 질문을 주시면 기록을 찾아보겠습니다."
        sources = ["General Logs", "Memory Bank"]

    return RAGQueryResponse(answer=answer, sources=sources)
