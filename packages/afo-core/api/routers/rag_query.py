import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from AFO.api.compat import HybridRAG

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
        except:
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
        except:
            pass

    results = []
    if tasks:
        retrieval_results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in retrieval_results:
            if isinstance(res, list):
                results.extend(res)

    logs.append(f"🔍 Retrieved {len(results)} chunks from Vector Store")

    # 4. Graph Context (GraphRAG)
    graph_context = []
    if request.use_graph and getattr(HybridRAG, "query_graph_context", None):
        # Extract entities from results or query
        # Simple extraction: split query by space for keywords (MVP)
        entities = [w for w in request.query.split() if len(w) > 4]
        # Or use extracted entities from chunks payload if available
        for res in results:
            if "metadata" in res and "content" in res["metadata"]:
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
        answer=str(answer), sources=results[:5], graph_context=graph_context, processing_log=logs
    )
