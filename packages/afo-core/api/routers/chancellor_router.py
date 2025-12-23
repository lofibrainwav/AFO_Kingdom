"""
Chancellor Router
Phase 3: Chancellor Graph API 엔드포인트
LangGraph 기반 3책사 (Zhuge Liang/Sima Yi/Zhou Yu) 시스템
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Literal

from fastapi import APIRouter, HTTPException

# 로깅 설정
logger = logging.getLogger(__name__)

# Strangler Fig: compat.py에서 타입 모델 import (眞: Truth 타입 안전성)
from AFO.api.compat import ChancellorInvokeRequest, ChancellorInvokeResponse

# Antigravity import (통합)
try:
    from AFO.config.antigravity import antigravity
except ImportError:
    try:
        from config.antigravity import antigravity as ag

        antigravity = ag  # type: ignore[assignment]
    except ImportError:
        # Fallback: 기본값 사용
        class MockAntigravity:
            AUTO_DEPLOY = True
            DRY_RUN_DEFAULT = True
            ENVIRONMENT = "dev"

        antigravity = MockAntigravity()  # type: ignore[assignment]

# Chancellor Graph import - [장자] 무용지용 = 없음도 쓰임이 있음
build_chancellor_graph: Any = None
chancellor_graph: Any = None
_chancellor_import_error: str | None = None


def _import_chancellor_graph() -> None:
    global build_chancellor_graph, chancellor_graph, _chancellor_import_error
    try:
        import sys
        from pathlib import Path

        # Add parent directory to path for chancellor_graph import
        _CORE_ROOT = Path(__file__).resolve().parent.parent.parent
        if str(_CORE_ROOT) not in sys.path:
            sys.path.insert(0, str(_CORE_ROOT))

        from chancellor_graph import ChancellorState as _CS  # Import State Definition
        from chancellor_graph import build_chancellor_graph as _bcg
        from chancellor_graph import chancellor_graph as _cg

        build_chancellor_graph = _bcg
        chancellor_graph = _cg
        ChancellorState = _CS
    except ImportError as e:
        print(f"⚠️  Chancellor Graph import 실패: {e}")
        _chancellor_import_error = str(e)

        class MockState(dict):
            pass

        ChancellorState = MockState


_import_chancellor_graph()

router = APIRouter(prefix="/chancellor", tags=["Chancellor"])

# Strangler Fig: Chancellor 타입 모델들은 compat.py로 이동됨 (眞: Truth 타입 안전성)


def _determine_execution_mode(
    request: ChancellorInvokeRequest,
) -> Literal["offline", "fast", "lite", "full"]:
    """
    실행 모드 결정 (美: 순수 함수 - 동일 입력에 동일 출력)

    Args:
        request: Chancellor 요청

    Returns:
        결정된 실행 모드
    """

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

    if request.mode == "auto":
        if _looks_like_system_query(request.query):
            return "offline"
        elif request.timeout_seconds <= 12:
            return "fast"
        elif request.timeout_seconds <= 45:
            return "lite"
        else:
            return "full"
    else:
        # [논어]言必信行必果 - 사용자 명시적 모드를 존중함
        return request.mode


def _build_llm_context(request: ChancellorInvokeRequest) -> dict[str, Any]:
    """
    LLM 컨텍스트 구축 (美: 순수 함수)

    Args:
        request: Chancellor 요청

    Returns:
        LLM 컨텍스트 딕셔너리
    """
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

    return llm_context


def _build_fallback_text(query: str, metrics: dict[str, Any]) -> str:
    """Build fallback text for offline mode responses."""

    def _looks_like_system_query(q: str) -> bool:
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
        return any(k in q.lower() for k in keywords)

    is_system = _looks_like_system_query(query)
    mem = metrics.get("memory_percent")
    swap = metrics.get("swap_percent")
    disk = metrics.get("disk_percent")
    redis_ok = metrics.get("redis_connected")
    langgraph_ok = metrics.get("langgraph_active")
    containers = metrics.get("containers_running")

    lines = [
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
        q_lower = query.lower()
        if any(k in q_lower for k in ["자기소개", "who are you", "너는 누구", "당신은 누구"]):
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


async def _execute_with_fallback(
    mode_used: Literal["offline", "fast", "lite", "full"],
    request: ChancellorInvokeRequest,
    llm_context: dict[str, Any],
) -> dict[str, Any]:
    """
    실행 모드에 따른 처리 및 폴백 (美: 순수 함수)

    Args:
        mode_used: 실행 모드
        request: Chancellor 요청
        llm_context: LLM 컨텍스트

    Returns:
        처리 결과
    """
    import asyncio

    async def _get_system_metrics_safe() -> dict[str, Any]:
        try:
            from api.routes.system_health import get_system_metrics
        except ImportError:
            try:
                from AFO.api.routes.system_health import get_system_metrics
            except ImportError as e:
                logger.debug("시스템 메트릭 모듈 import 실패: %s", str(e))
                return {"error": "system metrics route not available"}
        try:
            return dict(await get_system_metrics())
        except (AttributeError, TypeError, ValueError) as e:
            logger.warning("시스템 메트릭 수집 실패 (속성/타입/값 에러): %s", str(e))
            return {"error": f"failed to collect system metrics: {type(e).__name__}: {e}"}
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.warning("시스템 메트릭 수집 실패 (예상치 못한 에러): %s", str(e))
            return {"error": f"failed to collect system metrics: {type(e).__name__}: {e}"}

    async def _single_shot_answer(
        query: str, budget_seconds: float, context: dict[str, Any]
    ) -> tuple[str, dict[str, Any] | None, bool]:
        try:
            from llm_router import llm_router as _router
        except ImportError:
            try:
                from AFO.llm_router import (
                    llm_router as _afol_router,  # type: ignore[assignment]
                )

                _router = _afol_router
            except ImportError as e:
                logger.error("llm_router import 실패: %s", str(e))
                raise RuntimeError(f"llm_router import failed: {e}") from e

        timed_out = False
        try:
            result = await asyncio.wait_for(
                _router.execute_with_routing(query, context=context),
                timeout=max(0.5, budget_seconds),
            )
            return result.get("response", ""), result.get("routing"), timed_out
        except TimeoutError:
            timed_out = True
            return "", None, timed_out

    def _is_real_answer(answer: str, routing: dict[str, Any] | None) -> bool:
        text = (answer or "").strip()
        if not text:
            return False
        if routing and routing.get("is_fallback") is True:
            return False
        lowered = text.lower()
        return not (
            text.lstrip().startswith("[")
            and (
                " error" in lowered
                or lowered.startswith("[fallback")
                or "unavailable" in lowered
                or "api wrapper unavailable" in lowered
            )
        )

    # OFFLINE 모드
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

    # FAST/LITE 모드
    if mode_used in {"fast", "lite"}:
        budget_total = float(request.timeout_seconds)
        budget_llm = max(0.5, budget_total - 1.0)

        # 모드별 기본값 설정
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

    # FULL 모드 (LangGraph 기반 3책사)
    return await _execute_full_mode(request, llm_context)


async def _execute_full_mode(
    request: ChancellorInvokeRequest, llm_context: dict[str, Any]
) -> dict[str, Any]:
    """
    FULL 모드 실행 (LangGraph 기반 3책사)
    """
    try:
        from chancellor_graph import chancellor_graph
    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail="Chancellor Graph가 초기화되지 않았습니다. chancellor_graph.py를 확인하세요.",
        ) from e

    graph = chancellor_graph
    from AFO.api.compat import get_antigravity_control

    antigravity = get_antigravity_control()
    effective_auto_run = request.auto_run and not (antigravity and antigravity.DRY_RUN_DEFAULT)

    initial_state_dict = {
        "query": request.query,
        "messages": [],
        "summary": "",
        "context": {
            "llm_context": llm_context,
            "max_strategists": request.max_strategists,
            "antigravity": {
                "AUTO_DEPLOY": antigravity.AUTO_DEPLOY if antigravity else True,
                "DRY_RUN_DEFAULT": (antigravity.DRY_RUN_DEFAULT if antigravity else False),
                "ENVIRONMENT": antigravity.ENVIRONMENT if antigravity else "dev",
            },
            "auto_run_eligible": effective_auto_run,
        },
        "search_results": [],
        "multimodal_slots": {},
        "status": "INIT",
        "risk_score": 0.0,
        "trinity_score": 0.0,
        "analysis_results": {},
        "results": {},
        "actions": [],
    }

    # Cast to ChancellorState (TypedDict) for MyPy compliance
    # Note: ChancellorState is defined in chancellor_graph.py, imported at runtime
    # We use dict[str, Any] type annotation here for simplicity
    initial_state: dict[str, Any] = initial_state_dict

    from langchain_core.messages import HumanMessage

    # We can modify the dict because TypedDict is a dict at runtime
    initial_state["messages"].append(HumanMessage(content=request.query))

    config = {"configurable": {"thread_id": request.thread_id}}

    try:
        result = await asyncio.wait_for(
            graph.ainvoke(initial_state, config),
            timeout=float(request.timeout_seconds),
        )
    except TimeoutError as e:
        if not request.fallback_on_timeout:
            raise HTTPException(
                status_code=504,
                detail=f"Chancellor Graph timeout after {request.timeout_seconds}s",
            ) from e

        async def _get_system_metrics_safe() -> dict[str, Any]:
            try:
                from api.routes.system_health import get_system_metrics
            except ImportError:
                try:
                    from AFO.api.routes.system_health import get_system_metrics
                except ImportError as e:
                    logger.debug("시스템 메트릭 모듈 import 실패: %s", str(e))
                    return {"error": "system metrics route not available"}
            try:
                return dict(await get_system_metrics())
            except (AttributeError, TypeError, ValueError) as e:
                logger.warning("시스템 메트릭 수집 실패 (속성/타입/값 에러): %s", str(e))
                return {"error": f"failed to collect system metrics: {type(e).__name__}: {e}"}
            except Exception as e:  # - Intentional fallback for unexpected errors
                logger.warning("시스템 메트릭 수집 실패 (예상치 못한 에러): %s", str(e))
                return {"error": f"failed to collect system metrics: {type(e).__name__}: {e}"}

        metrics = await _get_system_metrics_safe()
        return {
            "response": _build_fallback_text(request.query, metrics),
            "thread_id": request.thread_id,
            "trinity_score": 0.0,
            "strategists_consulted": [],
            "mode_used": "full",
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

    strategists_consulted = []
    analysis_results = result.get("analysis_results", {})
    if analysis_results:
        strategists_consulted = list(analysis_results.keys())

    return {
        "response": response_text,
        "speaker": result.get("speaker", "Chancellor"),
        "thread_id": request.thread_id,
        "trinity_score": result.get("trinity_score", 0.0),
        "strategists_consulted": strategists_consulted,
        "analysis_results": analysis_results,
        "mode_used": "full",
        "fallback_used": False,
        "timed_out": False,
    }


@router.post("/invoke")
async def invoke_chancellor(
    request: ChancellorInvokeRequest,
) -> ChancellorInvokeResponse:
    """
    Chancellor Graph 호출 엔드포인트 (Strangler Fig 적용)

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
        # Strangler Fig Phase 2: 함수 분해 적용 (美: 우아한 구조)
        mode_used = _determine_execution_mode(request)
        llm_context = _build_llm_context(request)
        result = await _execute_with_fallback(mode_used, request, llm_context)

        # 결과 포맷팅 및 타입 검증
        return ChancellorInvokeResponse(**result)

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
        return {
            "status": "healthy",
            "message": "Chancellor Graph 정상 작동 중",
            "strategists": ["Zhuge Liang", "Sima Yi", "Zhou Yu"],
        }
    except (ImportError, AttributeError, RuntimeError) as e:
        logger.error("Chancellor Graph 초기화 실패 (import/속성/런타임 에러): %s", str(e))
        return {
            "status": "error",
            "message": f"Chancellor Graph 초기화 실패: {e!s}",
        }
    except Exception as e:  # - Intentional fallback for unexpected errors
        logger.error("Chancellor Graph 초기화 실패 (예상치 못한 에러): %s", str(e))
        return {
            "status": "error",
            "message": f"Chancellor Graph 초기화 실패: {e!s}",
        }
