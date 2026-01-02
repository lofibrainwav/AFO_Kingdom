# Trinity Score: 90.0 (Established by Chancellor)
import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from AFO.services.hybrid_rag import (
    generate_answer_async,
    generate_answer_stream_async,
    generate_hyde_query_async,
    get_embedding_async,
    query_graph_context,
    query_qdrant_async,
)


class HybridRAG:
    """
    Strangler Fig Compatibility Layer for Hybrid RAG Service.
    MyPy 87 Error Fix: Explicitly define async methods.
    """

    available = True

    @staticmethod
    async def generate_hyde_query_async(query: str, client: Any = None) -> str:
        return await generate_hyde_query_async(query, client)

    @staticmethod
    async def get_embedding_async(text: str, client: Any = None) -> list[float]:
        return await get_embedding_async(text, client)

    @staticmethod
    async def query_qdrant_async(
        embedding: list[float], top_k: int, client: Any = None
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


@router.post("/query/stream")
async def query_knowledge_base_stream(request: RAGRequest):
    """
    Real-time Streaming RAG Query Endpoint
    """
    if not HybridRAG.available:
        raise HTTPException(status_code=503, detail="RAG Service Unavailable")

    # 1. Hybrid Retrieval (Minimal logs for stream)
    # Reuse embedding and retrieval logic if possible,
    # but for simplicity in this router, we'll run a streamlined version.

    # Heuristic entities
    entities = [w for w in request.query.split() if len(w) > 4]

    # Retrieval (Sync for now inside the generator or pre-fetch)
    # We'll pre-fetch context to keep the stream focused on generation
    try:
        embedding = await HybridRAG.get_embedding_async(request.query)
        from qdrant_client import QdrantClient

        # Use container name for internal Docker communication
        q_client = QdrantClient("afo-qdrant", port=6333)
        results = await HybridRAG.query_qdrant_async(embedding, request.top_k, q_client)
        contexts = [r["content"] for r in results[:5]]
    except Exception as e:
        contexts = []
        print(f"Streaming Retrieval failed: {e}")

    async def token_generator():
        async for token in generate_answer_stream_async(
            query=request.query,
            contexts=contexts,
            temperature=0.7,
            response_format="markdown",
            additional_instructions="Streamed response for AFO Dashboard.",
        ):
            yield token

    return StreamingResponse(token_generator(), media_type="text/plain")


@router.post("/query", response_model=RAGResponse)
async def query_knowledge_base(request: RAGRequest):
    """
    Advanced GraphRAG Query Endpoint
    Orchestrates HyDE -> Hybrid Retrieval -> Graph Expansion -> Rerank -> Generation
    """
    if not HybridRAG.available:
        raise HTTPException(
            status_code=503, detail="RAG Service Unavailable (Missing dependencies)"
        )

    logs = []
    logs.append("🧠 Advanced RAG Pipeline Started")

    # 1. HyDE (Hypothetical Document Embeddings)
    search_query = request.query
    client = None

    if request.use_hyde and getattr(HybridRAG, "generate_hyde_query_async", None):
        try:
            import os

            from openai import OpenAI

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception:
            client = None

        search_query = await HybridRAG.generate_hyde_query_async(request.query, client)
        logs.append(f"✨ HyDE Generated: {search_query[:50]}...")
    else:
        logs.append("ℹ️ HyDE Skipped")

    # 2. Embedding
    try:
        embedding = await HybridRAG.get_embedding_async(search_query, client)
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
    if request.use_qdrant and getattr(HybridRAG, "query_qdrant_async", None):
        # Need client.
        try:
            from qdrant_client import QdrantClient

            q_client = QdrantClient("localhost", port=6333)
            tasks.append(HybridRAG.query_qdrant_async(embedding, request.top_k, q_client))
        except Exception:
            pass

    results: list[dict[str, Any]] = []
    if tasks:
        retrieval_results = await asyncio.gather(*tasks, return_exceptions=True)
        for r_chunk in retrieval_results:
            if isinstance(r_chunk, list) and all(isinstance(item, dict) for item in r_chunk):
                results.extend(r_chunk)
            elif isinstance(r_chunk, Exception):
                # Log exception but continue processing
                pass

    logs.append(f"🔍 Retrieved {len(results)} chunks from Vector Store")

    # 4. Graph Context (GraphRAG)
    graph_context = []
    if request.use_graph and getattr(HybridRAG, "query_graph_context", None):
        # Extract entities from results or query
        # Simple extraction: split query by space for keywords (MVP)
        entities = [w for w in request.query.split() if len(w) > 4]
        # Or use extracted entities from chunks payload if available
        for res in results:
            if isinstance(res, dict) and "metadata" in res and "content" in res["metadata"]:
                # Extract capitalized words as heuristic
                words = [w for w in res["metadata"]["content"].split() if w[0].isupper()]
                entities.extend(words[:3])

        entities = list(set(entities))[:5]  # Limit
        if entities:
            graph_context = HybridRAG.query_graph_context(entities)
            logs.append(f"🕸️ Graph Context: Found {len(graph_context)} connections for {entities}")

    # 5. Rerank / Selection
    # Simple selection for now
    contexts = [r["content"] for r in results[:5]]

    # 6. Generation
    answer = await HybridRAG.generate_answer_async(
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
