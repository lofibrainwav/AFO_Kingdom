# Trinity Score: 90.0 (Established by Chancellor)
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

# 眞 (Truth): Neo4j Integration (GraphRAG)
try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None  # type: ignore[assignment, misc]

# Qdrant Integration
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qmodels
except ImportError:
    QdrantClient = None  # type: ignore[assignment, misc]
    qmodels = None  # type: ignore[assignment]

# Optional imports handling
try:
    from pgvector.psycopg2 import register_vector
    from psycopg2.extras import RealDictCursor
except ImportError:
    RealDictCursor = None  # type: ignore[assignment, misc]
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
    """
    眞 (Truth): 난수 기반 임베딩 생성 (폴백용)

    Args:
        dim: 임베딩 차원 (기본 1536)

    Returns:
        list[float]: 생성된 난수 리스트
    """
    return [random.gauss(0, 0.1) for _ in range(dim)]


def get_embedding(text: str, openai_client: Any) -> list[float]:
    """
    眞 (Truth): OpenAI API를 이용한 텍스트 임베딩 추출
    善 (Goodness): 예외 발생 시 난수 임베딩으로 안전하게 폴백

    Args:
        text: 임베딩할 텍스트
        openai_client: OpenAI 클라이언트 인스턴스

    Returns:
        list[float]: 추출된 임베딩 리스트
    """
    if openai_client is None:
        return random_embedding()

    try:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return cast("list[float]", response.data[0].embedding)
    except Exception as exc:
        print(f"[Hybrid RAG] Embedding 생성 실패, 난수로 대체합니다: {exc}")
        return random_embedding()


def query_pgvector(embedding: list[float], top_k: int, pg_pool: Any) -> list[dict[str, Any]]:
    """
    眞 (Truth): PostgreSQL pgvector를 이용한 벡터 검색
    善 (Goodness): 연결 풀 관리 및 예외 처리

    Args:
        embedding: 검색할 벡터
        top_k: 반환할 상위 항목 수
        pg_pool: PostgreSQL 연결 풀

    Returns:
        list[dict]: 검색 결과 리스트
    """
    if pg_pool is None or not embedding:
        return []

    conn = pg_pool.getconn()
    try:
        if register_vector:
            register_vector(conn)

        cursor_factory = RealDictCursor if RealDictCursor is not None else None
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
        print(f"[Hybrid RAG] PGVector query failed: {e}")
        return []
    finally:
        pg_pool.putconn(conn)

    if not rows:
        return []

    norm_query = math.sqrt(sum(v * v for v in embedding)) or 1.0
    scored: list[dict[str, Any]] = []
    for row in rows:
        content = row.get("content") or ""
        if not content:
            continue
        vector = row.get("embedding")
        if vector is None:
            continue
        if not isinstance(vector, (list, tuple)):
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


def query_redis(embedding: list[float], top_k: int, redis_client: Any) -> list[dict[str, Any]]:
    """
    眞 (Truth): Redis RediSearch를 이용한 KNN 벡터 검색
    善 (Goodness): 인덱스 확인 및 예외 차단

    Args:
        embedding: 검색할 벡터
        top_k: 반환할 상위 항목 수
        redis_client: Redis 클라이언트

    Returns:
        list[dict]: 검색 결과 리스트
    """
    if redis_client is None or not embedding:
        return []

    try:
        from AFO.config.settings import get_settings

        settings = get_settings()
        index_name = settings.REDIS_RAG_INDEX
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
        print(f"[Hybrid RAG] Redis 검색 실패: {exc}")
        return []

    docs = getattr(search_result, "docs", getattr(search_result, "documents", []))
    rows: list[dict[str, Any]] = []
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


def query_graph_context(entities: list[str], limit: int = 5) -> list[dict[str, Any]]:
    """
    美 (Beauty): GraphRAG Context Retrieval
    Neo4j 지식 그래프에서 엔티티 간의 관계를 탐색.
    """
    if GraphDatabase is None or not entities:
        return []

    uri = "bolt://localhost:7687"
    auth = ("neo4j", "password")  # MVP credential

    try:
        results = []
        with (
            GraphDatabase.driver(uri, auth=auth) as driver,
            driver.session() as session,
        ):
            # Find related nodes (1-hop)
            query = """
                MATCH (n)-[r]-(m)
                WHERE n.name IN $entities OR n.id IN $entities
                RETURN n.name AS source, type(r) AS rel, m.name AS target, m.description AS desc
                LIMIT $limit
                """
            records = session.run(query, entities=entities, limit=limit)
            for record in records:
                results.append(
                    {
                        "source": record["source"],
                        "relationship": record["rel"],
                        "target": record["target"],
                        "description": record["desc"] or "",
                    }
                )
        return results
    except Exception as e:
        print(f"[GraphRAG] Neo4j query failed: {e}")
        return []


def query_qdrant(embedding: list[float], top_k: int, qdrant_client: Any) -> list[dict[str, Any]]:
    """
    眞 (Truth): Qdrant 벡터 검색 (Brain Organ)

    Args:
        embedding: 검색할 벡터
        top_k: 반환할 상위 항목 수
        qdrant_client: Qdrant 클라이언트

    Returns:
        list[dict]: 검색 결과 리스트
    """
    if qdrant_client is None or not embedding:
        return []

    try:
        from AFO.config.settings import get_settings

        settings = get_settings()
        collection_name = "afokingdom_knowledge"  # Default collection
    except Exception:
        collection_name = "afokingdom_knowledge"

    try:
        # 1. Search in Qdrant
        search_result = qdrant_client.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=top_k,
            with_payload=True,
        )

        # 2. Format results
        rows: list[dict[str, Any]] = []
        for hit in search_result:
            payload = hit.payload or {}
            content = payload.get("content") or ""
            if not content:
                continue

            rows.append(
                {
                    "id": str(hit.id),
                    "content": content,
                    "score": float(hit.score),
                    "source": payload.get("source") or "qdrant",
                    "metadata": payload,
                }
            )

        return rows
    except Exception as exc:
        print(f"[Hybrid RAG] Qdrant 검색 실패 (컬렉션이 없거나 연결 실패): {exc}")
        return []


def generate_hyde_query(query: str, openai_client: Any) -> str:
    """
    眞 (Truth) & 美 (Beauty): HyDE (Hypothetical Document Embeddings)
    질문에 대한 '가상의 이상적인 답변'을 생성하여 검색 정확도를 높임.

    Args:
        query: 사용자 질문
        openai_client: OpenAI 클라이언트

    Returns:
        str: HyDE로 강화된 쿼리 (또는 가상 답변)
    """
    if not openai_client:
        return query

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Fast model for HyDE
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful expert. Write a theoretical, concise passage that answers the user's question perfectly. Do not explain, just write the answer content.",
                },
                {"role": "user", "content": f"Question: {query}"},
            ],
            temperature=0.7,
        )
        hypothetical_answer = completion.choices[0].message.content
        return f"{query}\n{hypothetical_answer}"  # Combine for richer context
    except Exception as e:
        print(f"[Advanced RAG] HyDE generation failed: {e}")
        return query


def rerank_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    善 (Goodness): Reranking & Deduplication
    여러 소스(PG, Redis, Qdrant)의 결과를 재정렬 및 중복 제거.
    (추후 Cross-Encoder 모델 도입 가능)
    """
    unique_map = {}
    for r in results:
        # Content hash or ID based deduplication
        key = r.get("id")
        if not key or key in unique_map:
            continue
        unique_map[key] = r

    # Simple score sort for now (Placeholder for Cohere/CrossEncoder)
    deduplicated = list(unique_map.values())
    deduplicated.sort(key=lambda x: x["score"], reverse=True)
    return deduplicated


def blend_results(
    pg_rows: list[dict[str, Any]], redis_rows: list[dict[str, Any]], top_k: int
) -> list[dict[str, Any]]:
    """
    美 (Beauty): PGVector와 Redis 결과를 통합 및 가중치 정렬 (RRF 유사 방식)

    Args:
        pg_rows: DB 검색 결과
        redis_rows: Cache 검색 결과
        top_k: 최종 반환 수

    Returns:
        list[dict]: 혼합 및 정렬된 결과
    """
    merged: dict[str, dict[str, Any]] = {}

    def boost(row: dict[str, Any], origin: str) -> None:
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


def blend_results_advanced(
    pg_rows: list[dict[str, Any]],
    redis_rows: list[dict[str, Any]],
    qdrant_rows: list[dict[str, Any]],
    top_k: int,
) -> list[dict[str, Any]]:
    """
    美 (Beauty): Advanced RRF (Reciprocal Rank Fusion)
    PGVector(구조적), Redis(빈도/캐시), Qdrant(의미적) 결과 통합
    """
    merged: dict[str, dict[str, Any]] = {}

    # RRF constant
    k = 60

    def apply_rrf(rows: list[dict[str, Any]], source_weight: float):
        for rank, row in enumerate(rows):
            row_id = str(row["id"])
            if row_id not in merged:
                merged[row_id] = {
                    **row,
                    "rrf_score": 0.0,
                    "score": row["score"],
                }  # Keep original score mostly

            # RRF formula: 1 / (k + rank)
            # We multiply by source_weight to prioritize trusted sources
            rrf_score = (1 / (k + rank)) * source_weight
            merged[row_id]["rrf_score"] += rrf_score

            # Update source list
            if "sources" not in merged[row_id]:
                merged[row_id]["sources"] = []
            merged[row_id]["sources"].append(row.get("source", "unknown"))

    # Apply Fusion
    apply_rrf(pg_rows, 1.0)  # PostgreSQL (Baseline)
    apply_rrf(redis_rows, 0.8)  # Redis (Cache/Recent)
    apply_rrf(qdrant_rows, 1.2)  # Qdrant (Semantic/Brain - High Trust)

    # Sort by RRF score
    final_results = list(merged.values())
    final_results.sort(key=lambda r: r["rrf_score"], reverse=True)

    return final_results[:top_k]


def select_context(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """
    眞 (Truth): 토큰 제한에 맞춰 컨텍스트 선별

    Args:
        rows: 검색된 청크들
        limit: 글자수 제한

    Returns:
        list[dict]: 선별된 청크들
    """
    selected: list[dict[str, Any]] = []
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
    graph_context: list[dict[str, Any]] | None = None,  # New: Graph Context
) -> str | dict[str, Any]:
    """
    眞 (Truth): 컨텍스트 기반 LLM 답변 생성 (GraphRAG Enhanced)
    善 (Goodness): API 호출 실패 시 에러 메시지 반환

    Args:
        query: 사용자 질문
        contexts: 선별된 컨텍스트 리스트
        temperature: LLM 온도
        response_format: 응답 형식 (markdown 등)
        additional_instructions: 추가 지침
        llm_provider: LLM 제공자
        openai_client: OpenAI 클라이언트
        graph_context: 그래프 RAG에서 추출된 컨텍스트 (선택 사항)

    Returns:
        Union[str, dict]: 생성된 답변 또는 에러 정보
    """
    context_block = "\n\n".join([f"Chunk {idx + 1}:\n{ctx}" for idx, ctx in enumerate(contexts)])

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

    if openai_client:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Context:\n{context_block}\n\nQuestion: {query}",
                },
            ]

            completion = openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=temperature,
            )
            return str(completion.choices[0].message.content)
        except Exception as e:
            return f"Error generating answer: {e}"

    return "No LLM client available."


async def get_embedding_async(text: str, client: Any) -> list[float]:
    """비동기 임베딩 생성 래퍼"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, get_embedding, text, client)


async def query_pgvector_async(
    embedding: list[float], top_k: int, pool: Any
) -> list[dict[str, Any]]:
    """비동기 PGVector 검색 래퍼"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, query_pgvector, embedding, top_k, pool)


async def query_redis_async(
    embedding: list[float], top_k: int, client: Any
) -> list[dict[str, Any]]:
    """비동기 Redis 검색 래퍼"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, query_redis, embedding, top_k, client)


async def blend_results_async(
    pg_rows: list[dict[str, Any]], redis_rows: list[dict[str, Any]], top_k: int
) -> list[dict[str, Any]]:
    """비동기 결과 혼합 래퍼"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, blend_results, pg_rows, redis_rows, top_k)


async def query_qdrant_async(
    embedding: list[float], top_k: int, client: Any
) -> list[dict[str, Any]]:
    """비동기 Qdrant 검색 래퍼"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, query_qdrant, embedding, top_k, client)


async def generate_hyde_query_async(query: str, client: Any) -> str:
    """비동기 HyDE 쿼리 생성"""
    if not client:
        return query
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, generate_hyde_query, query, client)


async def generate_answer_async(
    query: str,
    contexts: list[str],
    temperature: float,
    response_format: str,
    additional_instructions: str,
    llm_provider: str = "openai",
    openai_client: Any = None,
    graph_context: list[dict[str, Any]] | None = None,
) -> str | dict[str, Any]:
    """비동기 답변 생성 래퍼"""
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
        graph_context,
    )


def _sse_fmt(event: str, data: Any) -> bytes:
    import json

    return (f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n").encode()


async def generate_answer_stream_async(
    query: str,
    contexts: list[str],
    temperature: float,
    response_format: str,
    additional_instructions: str,
    openai_client: Any = None,
) -> Any:  # AsyncIterator[bytes]
    """
    眞 (Truth): SSE 패턴을 따르는 비동기 스트리밍 답변 생성
    善 (Goodness): OpenAI 실패 시 Ollama로 자동 라우팅 (로컬 지능 주권)
    """
    context_block = "\n\n".join([f"Chunk {idx + 1}:\n{ctx}" for idx, ctx in enumerate(contexts)])
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

    # 1. Start event
    yield _sse_fmt("start", {"engine": "hybrid_rag_stream"})

    # 2. Try OpenAI if client available
    if openai_client:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Context:\n{context_block}\n\nQuestion: {query}",
                },
            ]

            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            for i, chunk in enumerate(response):
                if chunk.choices and chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    yield _sse_fmt("token", {"i": i, "t": token})

            yield _sse_fmt("done", {"ok": True, "provider": "openai"})
            return
        except Exception as e:
            print(f"[Hybrid RAG] OpenAI Streaming failed, falling back to Ollama: {e}")

    # 3. Fallback to Ollama (Local Sovereignty)
    try:
        import json

        import httpx

        # Default Ollama config from AFO environment
        ollama_url = os.getenv("AFO_OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("AFO_DSPY_MODEL", "deepseek-r1:14b")

        payload = {
            "model": ollama_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Context:\n{context_block}\n\nQuestion: {query}",
                },
            ],
            "stream": True,
            "options": {"temperature": temperature},
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", f"{ollama_url}/api/chat", json=payload) as resp:
                if resp.status_code != 200:
                    yield _sse_fmt(
                        "error", {"error": f"Ollama failed with status {resp.status_code}"}
                    )
                    return

                i = 0
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                        if "message" in chunk and "content" in chunk["message"]:
                            token = chunk["message"]["content"]
                            yield _sse_fmt("token", {"i": i, "t": token})
                            i += 1
                        if chunk.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue

        yield _sse_fmt("done", {"ok": True, "provider": "ollama"})

    except Exception as e:
        yield _sse_fmt("error", {"error": f"All LLM providers failed: {e!s}"})
