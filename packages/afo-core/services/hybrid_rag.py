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


def blend_results(pg_rows: list[dict[str, Any]], redis_rows: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
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
) -> str | dict[str, Any]:
    """
    眞 (Truth): 컨텍스트 기반 LLM 답변 생성
    善 (Goodness): API 호출 실패 시 에러 메시지 반환
    
    Args:
        query: 사용자 질문
        contexts: 선별된 컨텍스트 리스트
        temperature: LLM 온도
        response_format: 응답 형식 (markdown 등)
        additional_instructions: 추가 지침
        llm_provider: LLM 제공자
        openai_client: OpenAI 클라이언트
        
    Returns:
        str | dict: 생성된 답변 또는 에러 정보
    """
    context_block = "\n\n".join([ f"Chunk {idx + 1}:\n{ctx}" for idx, ctx in enumerate(contexts) ])

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
                {"role": "user", "content": f"Context:\n{context_block}\n\nQuestion: {query}"},
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


async def query_pgvector_async(embedding: list[float], top_k: int, pool: Any) -> list[dict[str, Any]]:
    """비동기 PGVector 검색 래퍼"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, query_pgvector, embedding, top_k, pool)


async def query_redis_async(embedding: list[float], top_k: int, client: Any) -> list[dict[str, Any]]:
    """비동기 Redis 검색 래퍼"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, query_redis, embedding, top_k, client)


async def blend_results_async(
    pg_rows: list[dict[str, Any]], redis_rows: list[dict[str, Any]], top_k: int
) -> list[dict[str, Any]]:
    """비동기 결과 혼합 래퍼"""
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
    )
