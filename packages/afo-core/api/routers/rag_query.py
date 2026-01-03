# Trinity Score: 90.0 (Established by Chancellor)
from __future__ import annotations

import asyncio
from typing import Any, Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from services.hybrid_rag import (
    generate_answer_async,
    generate_answer_stream_async,
    generate_hyde_query_async,
    get_embedding_async,
    query_graph_context,
    query_qdrant_async,
)


class HybridRAG:
    """Strangler Fig Compatibility Layer for Hybrid RAG Service.
    MyPy 87 Error Fix: Explicitly define async methods.
    """

    available = True

    @staticmethod
    async def generate_hyde_query_async(query: str, client: Any) -> str:
        return await generate_hyde_query_async(query, client)

    @staticmethod
    async def get_embedding_async(text: str, client: Any) -> list[float]:
        return await get_embedding_async(text, client)

    @staticmethod
    async def query_qdrant_async(
        embedding: list[float], top_k: int, client: Any
    ) -> list[dict[str, Any]]:
        return await query_qdrant_async(embedding, top_k, client)

    @staticmethod
    def query_graph_context(entities: list[str]) -> list[dict[str, Any]]:
        return query_graph_context(entities)

    @staticmethod
    async def generate_answer_async(
        query: str,
        contexts: list[str],
        temperature: float,
        response_format: str,
        additional_instructions: str,
        openai_client: Any = None,
        graph_context: list[dict[str, Any]] | None = None,
    ) -> str | dict[str, Any]:
        return await generate_answer_async(
            query,
            contexts,
            temperature,
            response_format,
            additional_instructions,
            openai_client=openai_client,
            graph_context=graph_context,
        )


router = APIRouter()


class RAGRequest(BaseModel):
    query: str
    top_k: int = 5
    # Optional flags
    use_hyde: bool = True
    use_graph: bool = True
    use_qdrant: bool = True
    llm_provider: str = "openai"
    temperature: float = 0.7
    response_format: str = "markdown"
    additional_instructions: str = ""


class RAGResponse(BaseModel):
    answer: str | dict[str, Any]
    sources: list[Any]
    graph_context: list[Any]
    processing_log: list[str]


@router.post("/query", response_model=RAGResponse)
async def query_knowledge_base(request: RAGRequest):
    """Advanced GraphRAG Query Endpoint
    Orchestrates HyDE -> Hybrid Retrieval -> Graph Expansion -> Rerank -> Generation
    """
    logs = ["🧠 Advanced RAG Pipeline Started"]

    # 1. HyDE & Client Initialization
    search_query = request.query
    client = None
    try:
        import os

        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
    except Exception:
        pass

    if request.use_hyde and client:
        try:
            search_query = await generate_hyde_query_async(request.query, client)
            logs.append(f"✨ HyDE Generated: {search_query[:50]}...")
        except Exception as e:
            logs.append(f"⚠️ HyDE Failed: {e}")

    # 2. Embedding
    try:
        embedding = await get_embedding_async(search_query, client)
    except Exception as e:
        logs.append(f"❌ Embedding Failed: {e}")
        embedding = [0.0] * 1536

    # 3. Retrieval
    tasks = []
    if request.use_qdrant:
        try:
            from qdrant_client import QdrantClient

            q_client = QdrantClient("localhost", port=6333)
            tasks.append(query_qdrant_async(embedding, request.top_k, q_client))
        except Exception:
            pass

    results = []
    if tasks:
        retrieval_results = await asyncio.gather(*tasks, return_exceptions=True)
        for r_chunk in retrieval_results:
            if isinstance(r_chunk, list):
                results.extend(r_chunk)

    logs.append(f"🔍 Retrieved {len(results)} chunks")

    # 4. Graph Context
    graph_context = []
    if request.use_graph:
        entities = [w for w in request.query.split() if len(w) > 4]
        if entities:
            graph_context = query_graph_context(entities[:5])
            logs.append(f"🕸️ Graph Context: Found {len(graph_context)} connections")

    # 5. Generation
    contexts = [r["content"] for r in results[:5]]
    answer = await generate_answer_async(
        query=request.query,
        contexts=contexts,
        temperature=request.temperature,
        response_format=request.response_format,
        additional_instructions=request.additional_instructions,
        openai_client=client,
        graph_context=graph_context,
    )

    # Convert answer to string if it's a dict for response_model compatibility
    final_answer = answer if isinstance(answer, (str, dict)) else str(answer)

    return RAGResponse(
        answer=final_answer,
        sources=results[:5],
        graph_context=graph_context,
        processing_log=logs,
    )


@router.post("/query/stream")
async def query_knowledge_base_stream(request: RAGRequest):
    """
    Advanced GraphRAG Streaming Query Endpoint
    Mirror of /query but streams generation tokens via SSE.
    """
    # 1. HyDE & Client Initialization
    search_query = request.query
    client = None
    try:
        import os

        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
    except Exception:
        pass

    if request.use_hyde and client:
        try:
            search_query = await generate_hyde_query_async(request.query, client)
        except Exception:
            pass

    # 2. Embedding
    try:
        embedding = await get_embedding_async(search_query, client)
    except Exception:
        embedding = [0.0] * 1536

    # 3. Retrieval
    tasks = []
    if request.use_qdrant:
        try:
            from qdrant_client import QdrantClient

            q_client = QdrantClient("localhost", port=6333)
            tasks.append(query_qdrant_async(embedding, request.top_k, q_client))
        except Exception:
            pass

    results = []
    if tasks:
        retrieval_results = await asyncio.gather(*tasks, return_exceptions=True)
        for r_chunk in retrieval_results:
            if isinstance(r_chunk, list):
                results.extend(r_chunk)

    # 4. Graph Context
    graph_context = []
    if request.use_graph:
        entities = [w for w in request.query.split() if len(w) > 4]
        if entities:
            graph_context = query_graph_context(entities[:5])

    # 5. Extraction
    contexts = [r["content"] for r in results[:5]]

    # 6. Streaming Generation
    headers = {"X-Accel-Buffering": "no", "Cache-Control": "no-cache"}

    return StreamingResponse(
        generate_answer_stream_async(
            query=request.query,
            contexts=contexts,
            temperature=request.temperature,
            response_format=request.response_format,
            additional_instructions=request.additional_instructions,
            openai_client=client,
        ),
        media_type="text/event-stream",
        headers=headers,
    )
