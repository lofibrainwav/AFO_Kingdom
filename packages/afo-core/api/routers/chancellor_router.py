"""
Chancellor Router
Phase 3: Chancellor Graph API 엔드포인트
LangGraph 기반 3책사 (Zhuge Liang/Sima Yi/Zhou Yu) 시스템
"""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Antigravity import (통합)
try:
    from AFO.config.antigravity import antigravity
except ImportError:
    try:
        from config.antigravity import antigravity
    except ImportError:
        # Fallback: 기본값 사용
        class MockAntigravity:
            AUTO_DEPLOY = True
            DRY_RUN_DEFAULT = True

        antigravity = MockAntigravity()

# Chancellor Graph import
try:
    import sys
    from pathlib import Path

    # Add parent directory to path for chancellor_graph import
    _CORE_ROOT = Path(__file__).resolve().parent.parent.parent
    if str(_CORE_ROOT) not in sys.path:
        sys.path.insert(0, str(_CORE_ROOT))

    from chancellor_graph import (
        ChancellorState,
        build_chancellor_graph,
        chancellor_graph,  # Singleton instance
    )
except ImportError as e:
    # Fallback: Create a mock router if import fails
    print(f"⚠️  Chancellor Graph import 실패: {e}")
    build_chancellor_graph = None
    chancellor_graph = None

router = APIRouter(prefix="/chancellor", tags=["Chancellor"])


class ChancellorInvokeRequest(BaseModel):
    """Chancellor Graph 호출 요청 모델"""

    query: str = Field(..., description="사용자 쿼리")
    thread_id: str = Field(default="default", description="대화 스레드 ID")
    auto_run: bool = Field(
        default_factory=lambda: antigravity.AUTO_DEPLOY,
        description="자동 실행 여부 (孝: Serenity) - Antigravity.AUTO_DEPLOY 기본값 사용",
    )
    timeout_seconds: int = Field(default=30, ge=1, le=300, description="최대 실행 시간(초)")
    mode: Literal["auto", "offline", "fast", "lite", "full"] = Field(
        default="auto",
        description="실행 모드(auto=자동, offline=LLM 없이 상태 보고, fast=1회 LLM, lite=짧은 1회 LLM, full=LangGraph 3책사)",
    )
    max_strategists: int | None = Field(
        default=None,
        ge=0,
        le=3,
        description="사용할 책사 수(0~3). full 모드에서 적용 가능. None이면 mode/timeout 기반 자동 결정",
    )
    provider: Literal["auto", "ollama", "anthropic", "gemini", "openai"] = Field(
        default="auto",
        description="LLM 제공자 강제 선택(라우터 우회). auto이면 라우팅 사용",
    )
    ollama_model: str | None = Field(
        default=None, description="Ollama 모델 override (예: llama3.2:3b, qwen2.5:3b 등)"
    )
    ollama_timeout_seconds: float | None = Field(
        default=None, ge=0.5, le=300, description="Ollama HTTP 타임아웃(초)"
    )
    ollama_num_ctx: int | None = Field(
        default=None, ge=256, le=32768, description="Ollama num_ctx override (컨텍스트 윈도우)"
    )
    ollama_num_thread: int | None = Field(
        default=None, ge=1, le=64, description="Ollama num_thread override"
    )
    max_tokens: int | None = Field(default=None, ge=32, le=4096, description="최대 출력 토큰")
    temperature: float | None = Field(default=None, ge=0.0, le=2.0, description="온도")
    fallback_on_timeout: bool = Field(
        default=True, description="시간 초과 시 504 대신 상태 기반 답변으로 폴백"
    )


class ChancellorInvokeResponse(BaseModel):
    """Chancellor Graph 호출 응답 모델"""

    response: str = Field(..., description="Chancellor 응답")
    thread_id: str = Field(..., description="대화 스레드 ID")
    trinity_score: float = Field(default=0.0, description="Trinity Score")
    strategists_consulted: list[str] = Field(default_factory=list, description="상담한 책사 목록")


@router.post("/invoke")
async def invoke_chancellor(request: ChancellorInvokeRequest) -> dict[str, Any]:
    """
    Chancellor Graph 호출 엔드포인트

    3책사 (Zhuge Liang/Sima Yi/Zhou Yu)를 LangGraph로 연결하여
    사용자 쿼리에 대한 최적의 답변을 생성합니다.

    Args:
        request: Chancellor 호출 요청

    Returns:
        Chancellor 응답 (3책사 분석 결과 포함)

    Raises:
        HTTPException: Chancellor Graph 초기화 실패 시
    """
    try:
        import asyncio

        def _looks_like_system_query(query: str) -> bool:
            q = query.lower()
            keywords = [
                "상태",
                "health",
                "헬스",
                "metrics",
                "메트릭",
                "redis",
                "postgres",
                "postgresql",
                "db",
                "데이터베이스",
                "포트",
                "서버",
                "메모리",
                "스왑",
                "디스크",
                "오장육부",
                "langgraph",
                "엔드포인트",
            ]
            return any(k in q for k in keywords)

        async def _get_system_metrics_safe() -> dict[str, Any]:
            try:
                from api.routes.system_health import get_system_metrics
            except Exception:
                try:
                    from AFO.api.routes.system_health import get_system_metrics  # type: ignore
                except Exception:
                    return {"error": "system metrics route not available"}
            try:
                return await get_system_metrics()
            except Exception as e:
                return {"error": f"failed to collect system metrics: {type(e).__name__}: {e}"}

        def _build_fallback_text(query: str, metrics: dict[str, Any]) -> str:
            is_system = _looks_like_system_query(query)
            mem = metrics.get("memory_percent")
            swap = metrics.get("swap_percent")
            disk = metrics.get("disk_percent")
            redis_ok = metrics.get("redis_connected")
            langgraph_ok = metrics.get("langgraph_active")
            containers = metrics.get("containers_running")

            lines: list[str] = [
                "승상 보고(폴백 모드): LLM 응답이 지연되어 현재는 제한된 방식으로 답변합니다.",
                "",
                f"- 요청: {query}",
            ]

            if is_system:
                lines.extend(
                    [
                        f"- 메모리: {mem}%",
                        f"- 스왑: {swap}%",
                        f"- 디스크: {disk}%",
                        f"- Redis: {'연결됨' if redis_ok else '미연결'}",
                        f"- LangGraph: {'활성' if langgraph_ok else '비활성'}",
                        f"- 감지된 서비스(추정): {containers}",
                    ]
                )
            else:
                # Give a minimally useful offline reply for common non-system queries.
                q_lower = query.lower()
                if any(
                    k in q_lower for k in ["자기소개", "who are you", "너는 누구", "당신은 누구"]
                ):
                    lines.append(
                        "- 오프라인 응답: 저는 AFO Kingdom의 승상(Chancellor)이며, 시스템 상태/전략/실행을 정리해 사령관의 결정을 돕습니다."
                    )
                else:
                    lines.append(
                        "- 오프라인 응답: 현재 LLM이 제시간에 응답하지 못해 질문에 대한 생성형 답변을 확정할 수 없습니다."
                    )

            lines.extend(
                [
                    "",
                    "504를 줄이고 실제 LLM 답변 확률을 올리려면:",
                    "- `mode=fast` 또는 `mode=lite`로 LLM 호출 수를 1회로 제한",
                    "- 더 작은(빠른) 모델 사용: `ollama_model` (예: `llama3.2:3b`, `qwen2.5:3b`)",
                    "- Ollama 성능 옵션: `ollama_num_ctx`(예: 2048~4096), `ollama_num_thread`",
                    "- 시간 예산 확대: `timeout_seconds` (예: 20~60초)",
                ]
            )
            return "\n".join(lines)

        async def _single_shot_answer(
            query: str, budget_seconds: float, llm_context: dict[str, Any]
        ) -> tuple[str, dict[str, Any] | None, bool]:
            try:
                from llm_router import llm_router as _router
            except Exception:
                try:
                    from AFO.llm_router import llm_router as _router  # type: ignore
                except Exception as e:
                    raise RuntimeError(f"llm_router import failed: {e}") from e

            timed_out = False
            try:
                result = await asyncio.wait_for(
                    _router.execute_with_routing(query, context=llm_context),
                    timeout=max(0.5, budget_seconds),
                )
                return result.get("response", ""), result.get("routing"), timed_out
            except asyncio.TimeoutError:
                timed_out = True
                return "", None, timed_out

        def _is_real_answer(answer: str, routing: dict[str, Any] | None) -> bool:
            text = (answer or "").strip()
            if not text:
                return False
            if routing and routing.get("is_fallback") is True:
                return False
            lowered = text.lower()
            if text.lstrip().startswith("[") and (
                " error" in lowered
                or lowered.startswith("[fallback")
                or "unavailable" in lowered
                or "api wrapper unavailable" in lowered
            ):
                return False
            return True

        # Decide mode based on timeout/query
        mode_used: Literal["offline", "fast", "lite", "full"]
        if request.mode == "auto":
            if _looks_like_system_query(request.query):
                mode_used = "offline"
            elif request.timeout_seconds <= 12:
                mode_used = "fast"
            elif request.timeout_seconds <= 45:
                mode_used = "lite"
            else:
                mode_used = "full"
        else:
            mode_used = request.mode  # type: ignore[assignment]

        # Build shared LLM context overrides
        llm_context: dict[str, Any] = {}
        if request.provider != "auto":
            llm_context["provider"] = request.provider
        if request.ollama_model:
            llm_context["ollama_model"] = request.ollama_model
        if request.ollama_timeout_seconds is not None:
            llm_context["ollama_timeout_seconds"] = request.ollama_timeout_seconds
        if request.ollama_num_ctx is not None:
            llm_context["ollama_num_ctx"] = request.ollama_num_ctx
        if request.ollama_num_thread is not None:
            llm_context["ollama_num_thread"] = request.ollama_num_thread
        if request.max_tokens is not None:
            llm_context["max_tokens"] = request.max_tokens
        if request.temperature is not None:
            llm_context["temperature"] = request.temperature

        # OFFLINE: always return a deterministic answer
        if mode_used == "offline":
            metrics = await _get_system_metrics_safe()
            return {
                "response": _build_fallback_text(request.query, metrics),
                "thread_id": request.thread_id,
                "trinity_score": 0.0,
                "strategists_consulted": [],
                "mode_used": mode_used,
                "fallback_used": True,
                "timed_out": False,
                "system_metrics": metrics,
            }

        # FAST/LITE: single LLM call with tight budget, fallback to system metrics
        if mode_used in {"fast", "lite"}:
            # Budgeting: keep a small buffer for JSON serialization + fallback work
            budget_total = float(request.timeout_seconds)
            budget_llm = max(0.5, budget_total - 1.0)

            # Mode defaults (can be overridden by request fields)
            if mode_used == "fast":
                llm_context.setdefault("max_tokens", 128)
                llm_context.setdefault("temperature", 0.2)
                llm_context.setdefault("ollama_timeout_seconds", budget_llm)
                llm_context.setdefault("ollama_num_ctx", 2048)
            else:
                llm_context.setdefault("max_tokens", 384)
                llm_context.setdefault("temperature", 0.4)
                llm_context.setdefault("ollama_timeout_seconds", budget_llm)
                llm_context.setdefault("ollama_num_ctx", 4096)

            answer, routing, timed_out = await _single_shot_answer(
                request.query, budget_llm, llm_context
            )

            if _is_real_answer(answer, routing):
                return {
                    "response": answer,
                    "thread_id": request.thread_id,
                    "trinity_score": 0.0,
                    "strategists_consulted": ["single_shot"],
                    "mode_used": mode_used,
                    "fallback_used": False,
                    "timed_out": timed_out,
                    "routing": routing,
                }

            if not request.fallback_on_timeout:
                raise HTTPException(
                    status_code=504,
                    detail=f"Chancellor LLM timeout after {request.timeout_seconds}s",
                )

            metrics = await _get_system_metrics_safe()
            return {
                "response": _build_fallback_text(request.query, metrics),
                "thread_id": request.thread_id,
                "trinity_score": 0.0,
                "strategists_consulted": [],
                "mode_used": mode_used,
                "fallback_used": True,
                "timed_out": True,
                "system_metrics": metrics,
                "routing": routing,
            }

        # FULL: LangGraph 기반 3책사 (필요 시 strategist 수 제한)
        if chancellor_graph is None:
            raise HTTPException(
                status_code=503,
                detail="Chancellor Graph가 초기화되지 않았습니다. chancellor_graph.py를 확인하세요.",
            )

        graph = chancellor_graph

        # 초기 상태 설정 (Antigravity 통합)
        # auto_run_eligible: request.auto_run과 antigravity.AUTO_DEPLOY를 모두 고려
        # DRY_RUN 모드일 때는 auto_run을 False로 강제 (善: 안전 우선)
        effective_auto_run = request.auto_run and not antigravity.DRY_RUN_DEFAULT

        initial_state: ChancellorState = {
            "messages": [],
            "trinity_score": 0.0,
            "risk_score": 0.0,
            "auto_run_eligible": effective_auto_run,
            "kingdom_context": {
                "llm_context": llm_context,
                "max_strategists": request.max_strategists,
                # Antigravity 설정을 컨텍스트에 포함 (眞: 명시적 전달)
                "antigravity": {
                    "AUTO_DEPLOY": antigravity.AUTO_DEPLOY,
                    "DRY_RUN_DEFAULT": antigravity.DRY_RUN_DEFAULT,
                    "ENVIRONMENT": antigravity.ENVIRONMENT,
                },
            },
            "persistent_memory": {},
            "current_speaker": "user",
            "next_step": "chancellor",
            "analysis_results": {},
        }

        # 사용자 메시지 추가
        from langchain_core.messages import HumanMessage

        initial_state["messages"].append(HumanMessage(content=request.query))

        # Graph 실행
        #
        # NOTE:
        # - LangGraph 내부가 sync I/O를 사용하면 event loop가 블로킹될 수 있어
        #   asyncio.wait_for 타임아웃이 동작하지 않을 수 있습니다.
        # - 안전하게 별도 스레드에서 sync `invoke()`를 실행하고, 타임아웃은 event loop에서 관리합니다.
        config = {"configurable": {"thread_id": request.thread_id}}
        try:
            result = await asyncio.wait_for(
                graph.ainvoke(initial_state, config),  # type: ignore[arg-type]
                timeout=float(request.timeout_seconds),
            )
        except asyncio.TimeoutError as e:
            if not request.fallback_on_timeout:
                raise HTTPException(
                    status_code=504,
                    detail=f"Chancellor Graph timeout after {request.timeout_seconds}s",
                ) from e

            metrics = await _get_system_metrics_safe()
            return {
                "response": _build_fallback_text(request.query, metrics),
                "thread_id": request.thread_id,
                "trinity_score": 0.0,
                "strategists_consulted": [],
                "mode_used": mode_used,
                "fallback_used": True,
                "timed_out": True,
                "system_metrics": metrics,
            }

        # 응답 추출
        messages = result.get("messages", [])
        last_message = messages[-1] if messages else None

        response_text = ""
        if last_message and hasattr(last_message, "content"):
            response_text = last_message.content
        elif isinstance(last_message, dict):
            response_text = last_message.get("content", "")

        # 책사 목록 추출
        strategists_consulted = []
        analysis_results = result.get("analysis_results", {})
        if analysis_results:
            strategists_consulted = list(analysis_results.keys())

        return {
            "response": response_text,
            "thread_id": request.thread_id,
            "trinity_score": result.get("trinity_score", 0.0),
            "strategists_consulted": strategists_consulted,
            "analysis_results": analysis_results,
            "mode_used": mode_used,
            "fallback_used": False,
            "timed_out": False,
        }

    except HTTPException:
        raise
    except BaseException as e:
        # Prevent process-level crashes (e.g., SystemExit) from killing the server connection.
        raise HTTPException(
            status_code=500,
            detail=f"Chancellor Graph crashed: {type(e).__name__}: {e}",
        ) from e


@router.get("/health")
async def chancellor_health() -> dict[str, Any]:
    """
    Chancellor Graph 건강 상태 체크

    Returns:
        Chancellor Graph 초기화 상태
    """
    if chancellor_graph is None:
        return {
            "status": "unavailable",
            "message": "Chancellor Graph가 초기화되지 않았습니다.",
        }

    try:
        graph = chancellor_graph
        return {
            "status": "healthy",
            "message": "Chancellor Graph 정상 작동 중",
            "strategists": ["Zhuge Liang", "Sima Yi", "Zhou Yu"],
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Chancellor Graph 초기화 실패: {e!s}",
        }
