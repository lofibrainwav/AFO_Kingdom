from __future__ import annotations

import asyncio
import math
import os
import random
import struct
import warnings
from concurrent.futures import ThreadPoolExecutor
from typing import Any, cast

from pydantic import BaseModel
from redis.commands.search.query import Query as RedisQuery

# Optional imports handling
try:
    from pgvector.psycopg2 import register_vector
    from psycopg2.extras import RealDictCursor
except ImportError:
    RealDictCursor = None
    register_vector = None

# Suppress Pydantic warnings locally
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# Executor for CPU-bound tasks
_executor = ThreadPoolExecutor(max_workers=16)


# Models
class HybridQueryRequest(BaseModel):
    query: str
    topK: int = 5
    contextLimit: int = 3500
    temperature: float = 0.3
    responseFormat: str = "markdown"
    additionalInstructions: str = ""
    returnChunks: bool = True
    llm_provider: str = "openai"


class HybridChunk(BaseModel):
    id: str
    content: str
    score: float
    source: str | None = None


class HybridQueryResponse(BaseModel):
    answer: str | dict
    chunks: list[HybridChunk] = []
    metadata: dict = {}


# Logic Functions


def random_embedding(dim: int = 1536) -> list[float]:
    return [random.gauss(0, 0.1) for _ in range(dim)]


def get_embedding(text: str, openai_client: Any) -> list[float]:
    if openai_client is None:
        return random_embedding()

    try:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return cast("list[float]", response.data[0].embedding)
    except Exception as exc:
        print(f"【Hybrid RAG】 Embedding 생성 실패, 난수로 대체합니다: {exc}")
        return random_embedding()


def query_pgvector(embedding: list[float], top_k: int, pg_pool: Any) -> list[dict]:
    if pg_pool is None or not embedding:
        return []

    conn = pg_pool.getconn()
    try:
        if register_vector:
            register_vector(conn)

        cursor_factory = RealDictCursor if RealDictCursor else None
        with conn.cursor(cursor_factory=cursor_factory) as cur:
            cur.execute(
                """
                SELECT id, title, url, content, embedding
                FROM rag_documents
                LIMIT 200;
                """
            )
            rows = cur.fetchall() if cur else []
    except Exception as e:
        print(f"【Hybrid RAG】 PGVector query failed: {e}")
        return []
    finally:
        pg_pool.putconn(conn)

    if not rows:
        return []

    # Manual similarity calculation (fallback if pgvector extension logic is complex to port)
    # Note: In production, this should be done by the DB using <-> or <=> operators
    # But here we are preserving the logic from api_server.py which fetches 200 rows and re-ranks in Python?
    # Wait, api_server.py code performs cosine similarity in Python.
    # This is inefficient but preserves exact behavior for now (refactor later).

    norm_query = math.sqrt(sum(v * v for v in embedding)) or 1.0
    scored: list[dict] = []
    for row in rows:
        # RealDictCursor returns dict-like, but standard cursor returns tuple.
        # api_server.py assumes dict access row['content']
        # If RealDictCursor is missing, this will fail. Handled by try-import above.

        content = row.get("content") or ""
        if not content:
            continue
        vector = row.get("embedding")
        if vector is None:
            continue
        if not isinstance(vector, (list, tuple)):
            # pgvector library returns numpy array or list usually
            vector = vector.tolist() if hasattr(vector, "tolist") else list(vector)

        norm_doc = math.sqrt(sum(v * v for v in vector)) or 1.0
        dot = sum(a * b for a, b in zip(embedding, vector, strict=False))
        similarity = dot / (norm_query * norm_doc)
        scored.append(
            {
                "id": str(row["id"]),
                "content": content,
                "score": float(similarity),
                "source": row.get("url") or row.get("title") or "pgvector",
            }
        )

    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored[:top_k]


def query_redis(embedding: list[float], top_k: int, redis_client: Any) -> list[dict]:
    if redis_client is None or not embedding:
        return []

    # Phase 2-4: settings 사용
    try:
        try:
            from config.settings import get_settings

            settings = get_settings()
            index_name = settings.REDIS_RAG_INDEX
        except ImportError:
            try:
                from AFO.config.settings import get_settings

                settings = get_settings()
                index_name = settings.REDIS_RAG_INDEX
            except ImportError:
                index_name = os.getenv("REDIS_RAG_INDEX", "rag_docs")
    except Exception:
        index_name = os.getenv("REDIS_RAG_INDEX", "rag_docs")

    try:
        vector_blob = struct.pack(f"<{len(embedding)}f", *embedding)
        query = RedisQuery(f"*=>[KNN {top_k} @embedding $vector AS score]")
        query = query.return_fields("content", "source", "score").dialect(2)
        search_result = redis_client.ft(index_name).search(
            query, query_params={"vector": vector_blob}
        )
    except Exception as exc:
        print(f"【Hybrid RAG】 Redis 검색 실패: {exc}")
        return []

    docs = getattr(search_result, "docs", getattr(search_result, "documents", []))
    rows: list[dict] = []
    for doc in docs:
        payload = getattr(doc, "__dict__", doc)
        content = payload.get("content") or ""
        if not content:
            continue
        score_value = payload.get("score")
        try:
            score = float(score_value)
        except (TypeError, ValueError):
            score = 0.0

        rows.append(
            {
                "id": getattr(doc, "id", payload.get("id", "redis")),
                "content": content,
                "score": score,
                "source": payload.get("source") or "redis",
            }
        )

    return rows


def blend_results(pg_rows: list[dict], redis_rows: list[dict], top_k: int) -> list[dict]:
    merged: dict[str, dict] = {}

    def boost(row: dict, origin: str) -> None:
        row_id = str(row["id"])
        existing = merged.get(row_id)
        adjusted = row["score"] * (1.1 if origin == "pg" else 1.0)
        if existing is None or adjusted > existing["score"]:
            merged[row_id] = {**row, "score": adjusted}

    for row in pg_rows:
        boost(row, "pg")
    for row in redis_rows:
        boost(row, "redis")

    return sorted(merged.values(), key=lambda r: r["score"], reverse=True)[:top_k]


def select_context(rows: list[dict], limit: int) -> list[dict]:
    selected: list[dict] = []
    used = 0

    for row in rows:
        content = row.get("content") or ""
        if not content:
            continue
        if used + len(content) > limit:
            break
        selected.append(row)
        used += len(content)

    return selected


def generate_answer(
    query: str,
    contexts: list[str],
    temperature: float,
    response_format: str,
    additional_instructions: str,
    llm_provider: str = "openai",
    openai_client: Any = None,
    # In future, other clients can be passed here
) -> str | dict:
    context_block = "\n\n".join([f"Chunk {idx + 1}:\n{ctx}" for idx, ctx in enumerate(contexts)])

    # Simple prompt construction
    system_prompt = " ".join(
        part
        for part in [
            "You are the Brnestrm Hybrid RAG assistant.",
            "Answer using ONLY the provided chunks. If unsure, say you do not know.",
            "Reference the source when possible.",
            additional_instructions,
        ]
        if part
    )

    # Only supporting OpenAI for now as per original code logic in this function
    # The original _generate_answer relied on global OPENAI_CLIENT or _call_claude_api (which uses local import)
    # We will stick to OpenAI here and handle Claude separately or pass it in.

    if openai_client:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context_block}\n\nQuestion: {query}"},
            ]

            # Simple simulation of response for now if we want to be pure
            # but let's copy the logic.
            completion = openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=temperature,
            )
            return str(completion.choices[0].message.content)
        except Exception as e:
            return f"Error generating answer: {e}"

    return "No LLM client available."


# Async Wrappers


async def get_embedding_async(text: str, client: Any) -> list[float]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, get_embedding, text, client)


async def query_pgvector_async(embedding: list[float], top_k: int, pool: Any) -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, query_pgvector, embedding, top_k, pool)


async def query_redis_async(embedding: list[float], top_k: int, client: Any) -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, query_redis, embedding, top_k, client)


async def blend_results_async(
    pg_rows: list[dict], redis_rows: list[dict], top_k: int
) -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, blend_results, pg_rows, redis_rows, top_k)


async def generate_answer_async(
    query: str,
    contexts: list[str],
    temperature: float,
    response_format: str,
    additional_instructions: str,
    llm_provider: str = "openai",
    openai_client: Any = None,
) -> str | dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        _executor,
        generate_answer,
        query,
        contexts,
        temperature,
        response_format,
        additional_instructions,
        llm_provider,
        openai_client,
    )
