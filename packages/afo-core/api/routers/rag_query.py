# Trinity Score: 90.0 (Established by Chancellor)
import asyncio
from typing import Any

from AFO.services.hybrid_rag import (
    HybridRAG,
    generate_answer_async,
    generate_answer_stream_async,
    generate_hyde_query_async,
    get_embedding_async,
    query_graph_context,
    query_qdrant_async,
)
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


class HybridRAGService:
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


class RAGResponse(BaseModel):
    answer: str
    sources: list[Any]
    graph_context: list[Any]
    processing_log: list[str]


@router.post("/query", response_model=RAGResponse)
async def query_knowledge_base(request: RAGRequest):
    """Advanced GraphRAG Query Endpoint
    Orchestrates HyDE -> Hybrid Retrieval -> Graph Expansion -> Rerank -> Generation
    """
    if not HybridRAGService.available:
        raise HTTPException(
            status_code=503, detail="RAG Service Unavailable (Missing dependencies)"
        )

    logs = []
    logs.append("🧠 Advanced RAG Pipeline Started")

    # 1. HyDE (Hypothetical Document Embeddings)
    search_query = request.query
    client = None

    if request.use_hyde and getattr(
        HybridRAGService, "generate_hyde_query_async", None
    ):
        try:
            import os

            from openai import OpenAI

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception:
            client = None

        search_query = await HybridRAGService.generate_hyde_query_async(
            request.query, client
        )
        logs.append(f"✨ HyDE Generated: {search_query[:50]}...")
    else:
        logs.append("ℹ️ HyDE Skipped")

    # 2. Embedding
    try:
        embedding = await HybridRAGService.get_embedding_async(search_query, client)
    except Exception as e:
        logs.append(f"❌ Embedding Failed: {e}")
        embedding = [0.0] * 1536  # Fallback

    # 3. Retrieval (Parallel)
    tasks = []

    # PGVector
    # We need pg_pool. Assuming unavailable in straightforward way here without DI.
    # For MVP Router, we might skip PG or use a global pool if available.
    # We'll skip PG for now to focus on Qdrant which we set up.

    # Qdrant
    if request.use_qdrant and getattr(HybridRAGService, "query_qdrant_async", None):
        # Need client.
        try:
            from qdrant_client import QdrantClient

            q_client = QdrantClient("localhost", port=6333)
            tasks.append(
                HybridRAGService.query_qdrant_async(embedding, request.top_k, q_client)
            )
        except Exception:
            pass

    results: list[dict[str, Any]] = []
    if tasks:
        retrieval_results = await asyncio.gather(*tasks, return_exceptions=True)
        for r_chunk in retrieval_results:
            if isinstance(r_chunk, list) and all(
                isinstance(item, dict) for item in r_chunk
            ):
                results.extend(r_chunk)
            elif isinstance(r_chunk, Exception):
                # Log exception but continue processing
                pass

    logs.append(f"🔍 Retrieved {len(results)} chunks from Vector Store")

    # 4. Graph Context (GraphRAG)
    graph_context = []
    if request.use_graph and getattr(HybridRAGService, "query_graph_context", None):
        # Extract entities from results or query
        # Simple extraction: split query by space for keywords (MVP)
        entities = [w for w in request.query.split() if len(w) > 4]
        # Or use extracted entities from chunks payload if available
        for res in results:
            if (
                isinstance(res, dict)
                and "metadata" in res
                and "content" in res["metadata"]
            ):
                # Extract capitalized words as heuristic
                words = [
                    w for w in res["metadata"]["content"].split() if w[0].isupper()
                ]
                entities.extend(words[:3])

        entities = list(set(entities))[:5]  # Limit
        if entities:
            graph_context = HybridRAGService.query_graph_context(entities)
            logs.append(
                f"🕸️ Graph Context: Found {len(graph_context)} connections for {entities}"
            )

    # 5. Rerank / Selection
    # Simple selection for now
    contexts = [r["content"] for r in results[:5]]

    # 6. Generation
    answer = await HybridRAGService.generate_answer_async(
        query=request.query,
        contexts=contexts,
        temperature=0.7,
        response_format="markdown",
        additional_instructions="Use the provided Graph Context to enrich the answer.",
        openai_client=client,
        graph_context=graph_context,  # Passed to our updated function
    )

    return RAGResponse(
        answer=str(answer),
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
    if not HybridRAGService.available:
        raise HTTPException(
            status_code=503, detail="RAG Service Unavailable (Missing dependencies)"
        )

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

    # 3. Retrieval (Mirror of /query)
    tasks = []
    if request.use_qdrant:
        try:
            from qdrant_client import QdrantClient

            q_client = QdrantClient("localhost", port=6333)
            tasks.append(query_qdrant_async(embedding, request.top_k, q_client))
        except Exception:
            pass

    results: list[dict[str, Any]] = []
    if tasks:
        retrieval_results = await asyncio.gather(*tasks, return_exceptions=True)
        for r_chunk in retrieval_results:
            if isinstance(r_chunk, list):
                results.extend(r_chunk)

    # 4. Graph Context (Mirror of /query)
    graph_context = []
    if request.use_graph:
        entities = [w for w in request.query.split() if len(w) > 4]
        for res in results:
            if (
                isinstance(res, dict)
                and "metadata" in res
                and "content" in res["metadata"]
            ):
                words = [
                    w for w in res["metadata"]["content"].split() if w[0].isupper()
                ]
                entities.extend(words[:3])
        entities = list(set(entities))[:5]
        if entities:
            graph_context = query_graph_context(entities)

    # 5. Extraction
    contexts = [r["content"] for r in results[:5]]

    # 6. Streaming Generation
    # Headers to prevent buffering
    headers = {"X-Accel-Buffering": "no", "Cache-Control": "no-cache"}

    return StreamingResponse(
        generate_answer_stream_async(
            query=request.query,
            contexts=contexts,
            temperature=0.7,
            response_format="markdown",
            additional_instructions="Use the provided Graph Context to enrich the answer.",
            openai_client=client,
        ),
        media_type="text/event-stream",
        headers=headers,
    )
