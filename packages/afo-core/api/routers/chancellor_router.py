# Trinity Score: 90.0 (Established by Chancellor)
"""
Chancellor Router
Phase 3: Chancellor Graph API 엔드포인트
LangGraph 기반 3책사 (Zhuge Liang/Sima Yi/Zhou Yu) 시스템
"""

from __future__ import annotations

import logging
from typing import Any, Literal, cast

import anyio
from fastapi import APIRouter, HTTPException, Request

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

# Learning Profile Loader import (Boot-Swap)
try:
    from afo.learning_loader import get_learning_profile

    _learning_loader_available = True
    logger.info("✅ Learning profile loader imported successfully")
except ImportError as e:
    _learning_loader_available = False
    logger.warning(f"⚠️ Learning profile loader import failed: {e}")

# RAG Shadow Mode import (TICKET-008 Phase 1)
try:
    from afo.rag_shadow import (
        execute_rag_shadow,
        get_shadow_metrics,
        is_rag_shadow_enabled,
    )

    _rag_shadow_available = True
    logger.info("✅ RAG shadow mode imported successfully")
except ImportError:
    try:
        # 상대 경로로 재시도 (packages/afo-core/afo/)
        import os
        import sys

        sys.path.append(os.path.join(os.path.dirname(__file__), "../../../afo"))

        from rag_shadow import (
            execute_rag_shadow,
            get_shadow_metrics,
            is_rag_shadow_enabled,
        )

        _rag_shadow_available = True
        logger.info("✅ RAG shadow mode imported successfully (relative path)")
    except ImportError as e:
        _rag_shadow_available = False
        logger.warning(f"⚠️ RAG shadow mode import failed: {e}")

# RAG Flag + Gradual Mode import (TICKET-008 Phase 2 + 3)
try:
    from afo.rag_flag import execute_rag_with_mode, get_rag_config, init_rag_semaphore

    _rag_flag_available = True
    # 세마포어 초기화
    init_rag_semaphore()
    logger.info("✅ RAG flag + gradual mode imported successfully")
except ImportError:
    try:
        # 상대 경로로 재시도 (packages/afo-core/afo/)
        import os
        import sys

        sys.path.append(os.path.join(os.path.dirname(__file__), "../../../afo"))

        from rag_flag import execute_rag_with_mode, get_rag_config, init_rag_semaphore

        _rag_flag_available = True
        # 세마포어 초기화
        init_rag_semaphore()
        logger.info("✅ RAG flag + gradual mode imported successfully (relative path)")
    except ImportError as e:
        _rag_flag_available = False
        logger.warning(f"⚠️ RAG flag + gradual mode import failed: {e}")

# Chancellor Graph V2 import - [정복 완료] V1에서 V2로 전환
# PH23: V1 Strangler Collection - Phase A
_v2_runner_available = False
_chancellor_import_error: str | None = None

try:
    from AFO.api.chancellor_v2.graph.nodes.execute_node import execute_node
    from AFO.api.chancellor_v2.graph.nodes.verify_node import verify_node
    from AFO.api.chancellor_v2.graph.runner import run_v2
    from AFO.api.chancellor_v2.graph.state import GraphState

    _v2_runner_available = True
    logger.info("✅ Chancellor V2 runner loaded successfully")
except ImportError as e:
    _chancellor_import_error = str(e)
    logger.warning(f"⚠️ Chancellor V2 runner import failed: {e}")

# Legacy V1 import (deprecated, for fallback only)
build_chancellor_graph: Any = None
chancellor_graph: Any = None


def _import_chancellor_graph() -> None:
    """Legacy V1 import - DEPRECATED, kept for fallback only."""
    global build_chancellor_graph, chancellor_graph
    if _v2_runner_available:
        # V2 is available, skip V1 import
        return

    try:
        from AFO.chancellor_graph import build_chancellor_graph as _bcg
        from AFO.chancellor_graph import chancellor_graph as _cg

        build_chancellor_graph = _bcg
        chancellor_graph = _cg
        logger.warning("⚠️ Using DEPRECATED V1 chancellor_graph (V2 unavailable)")
    except ImportError as e:
        logger.error(f"⚠️ Both V2 and V1 chancellor_graph unavailable: {e}")


_import_chancellor_graph()

router = APIRouter(prefix="/chancellor", tags=["Chancellor"])

# Include chancellor engines endpoint from afo_agent_fabric
try:
    from AFO.afo_agent_fabric import _get_cached_engine_status

    @router.get("/engines")
    async def chancellor_engines():
        """
        Chancellor AI 엔진 설치 상태 확인 (캐시 최적화)

        Trinity Score: 眞 (Truth) - 정확한 라이브러리 상태
        성능 최적화: 5분 캐시 + 빠른 import 순서
        """
        return {"installed": _get_cached_engine_status()}

except ImportError:
    logger.warning("afo_agent_fabric functions not available")

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

    # Backward compatibility: query가 없으면 input 사용
    query_text = request.query or request.input

    if request.mode == "auto":
        if _looks_like_system_query(query_text):
            return "offline"
        elif request.timeout_seconds <= 12:
            return "fast"
        elif request.timeout_seconds <= 45:
            return "lite"
        else:
            return "full"
    else:
        # [논어]言必信行必果 - 사용자 명시적 모드를 존중함
        mode = request.mode
        if mode in ["offline", "fast", "lite", "full"]:
            return cast("Literal['offline', 'fast', 'lite', 'full']", mode)
        return "full"  # fallback


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
        if any(
            k in q_lower
            for k in ["자기소개", "who are you", "너는 누구", "당신은 누구"]
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


async def _execute_with_fallback(
    mode_used: Literal["offline", "fast", "lite", "full"],
    request: ChancellorInvokeRequest,
    llm_context: dict[str, Any],
    headers: dict[str, str] | None = None,
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

    # TICKET-008 Phase 3: RAG 통합 실행 (Shadow + Flag + Gradual)
    rag_result = None
    if _rag_flag_available:
        query = request.query or request.input
        # 통합 모드 실행 (timeout + fallback 보장)
        rag_result = await execute_rag_with_mode(
            query,
            request.headers if hasattr(request, "headers") else None,
            headers,
            {
                "llm_context": llm_context,
                "thread_id": request.thread_id,
                "mode_used": mode_used,
            },
        )

    # TICKET-008 Phase 1: RAG Shadow 실행 (위험 0, 메트릭만 기록)
    # Flag 모드와 별개로 항상 Shadow 실행 (메트릭 수집)
    if _rag_shadow_available and is_rag_shadow_enabled():
        query = request.query or request.input
        # Shadow 실행은 응답에 영향 없음 (비동기 실행)
        asyncio.create_task(
            execute_rag_shadow(
                query, {"llm_context": llm_context, "thread_id": request.thread_id}
            )
        )

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
            return {
                "error": f"failed to collect system metrics: {type(e).__name__}: {e}"
            }
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.warning("시스템 메트릭 수집 실패 (예상치 못한 에러): %s", str(e))
            return {
                "error": f"failed to collect system metrics: {type(e).__name__}: {e}"
            }

    async def _single_shot_answer(
        query: str, budget_seconds: float, context: dict[str, Any]
    ) -> tuple[str, dict[str, Any] | None, bool]:
        try:
            from llm_router import llm_router as _router
        except ImportError:
            try:
                from AFO.llm_router import llm_router as _afol_router

                _router = _afol_router  # type: ignore[assignment]
            except ImportError as e:
                logger.error("llm_router import 실패: %s", str(e))
                raise RuntimeError(f"llm_router import failed: {e}") from e

        timed_out = False
        try:
            with anyio.fail_after(max(0.5, budget_seconds)):
                result = await _router.execute_with_routing(query, context=context)
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
            "response": _build_fallback_text(request.query or request.input, metrics),
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
            request.query or request.input, budget_llm, llm_context
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
            "response": _build_fallback_text(request.query or request.input, metrics),
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
    return await _execute_full_mode(request, llm_context, headers)


async def _execute_full_mode(
    request: ChancellorInvokeRequest,
    llm_context: dict[str, Any],
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    FULL 모드 실행 - Phase 24: Unified ChancellorGraph 사용
    """
    from AFO.chancellor_graph import ChancellorGraph

    query = request.query or request.input

    # Unified Invoke (Handles Canary, Shadow, and Routine)
    result = await ChancellorGraph.invoke(
        query,
        headers=headers,
        llm_context=llm_context,
        thread_id=request.thread_id,
        max_strategists=getattr(request, "max_strategists", 3),
    )

    # Extract response text from potentially complex graph outputs
    outputs = result.get("outputs", {})
    execute_result = outputs.get("EXECUTE", {})
    report_result = outputs.get("REPORT", {})

    response_text = ""
    if isinstance(report_result, dict):
        response_text = report_result.get("result", "")
    if not response_text and isinstance(execute_result, dict):
        response_text = execute_result.get("result", "")

    if not response_text:
        # Fallback to direct output if V1 or no standard node output
        response_text = outputs.get("V1", "Execution completed")

    return {
        "response": response_text,
        "speaker": result.get("engine", "Chancellor"),
        "thread_id": request.thread_id,
        "trinity_score": 0.9,
        "strategists_consulted": ["TRUTH", "GOODNESS", "BEAUTY"],
        "analysis_results": outputs,
        "mode_used": "full_scaling",
        "fallback_used": result.get("engine") == "V1 (Legacy)",
        "timed_out": False,
        "v2_trace_id": result.get("trace_id"),
    }


async def _execute_full_mode_v2(
    request: ChancellorInvokeRequest, llm_context: dict[str, Any]
) -> dict[str, Any]:
    """V2 Runner execution with MCP Contract enforcement."""
    from AFO.api.chancellor_v2.graph.nodes.execute_node import execute_node
    from AFO.api.chancellor_v2.graph.nodes.verify_node import verify_node
    from AFO.api.chancellor_v2.graph.runner import run_v2

    # Build V2 input payload
    input_payload = {
        "query": request.query or request.input,
        "llm_context": llm_context,
        "thread_id": request.thread_id,
        "skill_id": "chancellor_invoke",
        "max_strategists": request.max_strategists,
    }

    # Build V2 nodes (minimal for now, expand as needed)
    def ok_node(step: str):
        def _fn(state):
            state.outputs[step] = "ok"
            return state

        return _fn

    from AFO.chancellor_graph import mipro_node

    nodes = {
        "CMD": ok_node("CMD"),
        "PARSE": ok_node("PARSE"),
        "TRUTH": ok_node("TRUTH"),
        "GOODNESS": ok_node("GOODNESS"),
        "BEAUTY": ok_node("BEAUTY"),
        "MIPRO": mipro_node,  # PH30 Expansion: MIPRO 최적화 노드 추가
        "MERGE": ok_node("MERGE"),
        "EXECUTE": execute_node,
        "VERIFY": verify_node,
        "REPORT": ok_node("REPORT"),
    }

    try:
        state = run_v2(input_payload, nodes)

        # Extract response from state
        execute_result = state.outputs.get("EXECUTE", {})
        verify_result = state.outputs.get("VERIFY", {})

        response_text = (
            execute_result.get("result", "")
            if isinstance(execute_result, dict)
            else str(execute_result)
        )

        return {
            "response": response_text or "V2 execution completed",
            "speaker": "Chancellor V2",
            "thread_id": request.thread_id,
            "trinity_score": 0.9,  # Default high score for V2
            "strategists_consulted": ["TRUTH", "GOODNESS", "BEAUTY"],
            "analysis_results": state.outputs,
            "mode_used": "full_v2",
            "fallback_used": False,
            "timed_out": False,
            "v2_trace_id": state.trace_id,
        }
    except Exception as e:
        logger.error(f"V2 Runner failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Chancellor V2 execution failed: {type(e).__name__}: {e}",
        ) from e


async def _execute_full_mode_v1_legacy(
    request: ChancellorInvokeRequest, llm_context: dict[str, Any]
) -> dict[str, Any]:
    """DEPRECATED: V1 LangGraph execution - kept for fallback only."""
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
    effective_auto_run = request.auto_run and not (
        antigravity and antigravity.DRY_RUN_DEFAULT
    )

    initial_state_dict: dict[str, Any] = {
        "query": request.query or request.input,
        "messages": [],
        "summary": "",
        "context": {
            "llm_context": llm_context,
            "max_strategists": request.max_strategists,
            "antigravity": {
                "AUTO_DEPLOY": antigravity.AUTO_DEPLOY if antigravity else True,
                "DRY_RUN_DEFAULT": (
                    antigravity.DRY_RUN_DEFAULT if antigravity else False
                ),
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

    initial_state: dict[str, Any] = initial_state_dict

    from langchain_core.messages import HumanMessage

    initial_state["messages"].append(
        HumanMessage(content=request.query or request.input)
    )

    config = {"configurable": {"thread_id": request.thread_id}}

    try:
        with anyio.fail_after(float(request.timeout_seconds)):
            result = await graph.ainvoke(initial_state, config)
    except TimeoutError as e:
        if not request.fallback_on_timeout:
            raise HTTPException(
                status_code=504,
                detail=f"Chancellor Graph timeout after {request.timeout_seconds}s",
            ) from e

        return {
            "response": "V1 Timeout - Please use V2 mode",
            "thread_id": request.thread_id,
            "trinity_score": 0.0,
            "strategists_consulted": [],
            "mode_used": "full_v1_deprecated",
            "fallback_used": True,
            "timed_out": True,
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
        "speaker": result.get("speaker", "Chancellor V1"),
        "thread_id": request.thread_id,
        "trinity_score": result.get("trinity_score", 0.0),
        "strategists_consulted": strategists_consulted,
        "analysis_results": analysis_results,
        "mode_used": "full_v1_deprecated",
        "fallback_used": False,
        "timed_out": False,
    }


@router.post("/invoke")
async def invoke_chancellor(
    request: ChancellorInvokeRequest,
    http_request: Request,
) -> ChancellorInvokeResponse:
    """
    Chancellor Graph 호출 엔드포인트 (Strangler Fig 적용)

    Phase 24 Scaling:
    - X-AFO-Engine: v2 헤더 지원
    - Shadow 모드 자동 적용 (백그라운드 Diff)
    """
    try:
        # FastAPI Headers extract
        headers = dict(http_request.headers)

        # Strangler Fig Phase 2: 함수 분해 적용 (美: 우아한 구조)
        mode_used = _determine_execution_mode(request)
        llm_context = _build_llm_context(request)
        result = await _execute_with_fallback(mode_used, request, llm_context, headers)

        # Pydantic Response Mapping (Fixing response -> result if needed)
        if "response" in result and "result" not in result:
            result["result"] = result["response"]
        if "speaker" in result and "engine_used" not in result:
            result["engine_used"] = result["speaker"]
        if "execution_time" not in result:
            result["execution_time"] = 1.0  # Static or calculated
        if "mode" not in result:
            result["mode"] = mode_used

        # 결과 포맷팅 및 타입 검증
        return ChancellorInvokeResponse(**result)

    except HTTPException as e:
        raise e
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
        logger.error(
            "Chancellor Graph 초기화 실패 (import/속성/런타임 에러): %s", str(e)
        )
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


@router.get("/learning/health")
async def learning_profile_health() -> dict[str, Any]:
    """
    Learning Profile Boot-Swap 상태 체크 (TICKET-007)

    Returns:
        Learning profile 로드 상태 및 메타데이터 + effective_config
    """
    if not _learning_loader_available:
        return {
            "status": "unavailable",
            "message": "Learning profile loader가 초기화되지 않았습니다.",
            "available": False,
        }

    try:
        from afo.trinity_config import BASE_CONFIG, apply_learning_profile

        profile = get_learning_profile()
        response = profile.to_dict()

        # Boot-Swap: effective_config + applied_overrides 추가
        effective_config = apply_learning_profile(
            BASE_CONFIG, profile.data.get("overrides", {})
        )
        response["effective_config"] = effective_config

        return response
    except Exception as e:
        logger.error("Learning profile health check failed: %s", str(e))
        return {
            "status": "error",
            "message": f"Learning profile health check failed: {e!s}",
            "available": False,
        }


@router.get("/rag/shadow/health")
async def rag_shadow_health() -> dict[str, Any]:
    """
    RAG Shadow + Flag 모드 상태 체크 (TICKET-008 Phase 1 + Phase 2)

    Returns:
        RAG Shadow + Flag 모드 상태 및 메트릭 통계
    """
    response = {
        "shadow": {"available": False, "enabled": False},
        "flag": {"available": False, "enabled": False, "config": None},
        "overall_status": "partial",
    }

    # Shadow 모드 상태
    if _rag_shadow_available:
        try:
            shadow_enabled = is_rag_shadow_enabled()
            response["shadow"] = {
                "available": True,
                "enabled": shadow_enabled,
            }

            if shadow_enabled:
                # Shadow 메트릭 조회
                metrics = await get_shadow_metrics(limit=50)
                response["shadow"]["metrics"] = metrics

        except Exception as e:
            logger.error("RAG Shadow health check failed: %s", str(e))
            response["shadow"]["error"] = str(e)

    # Flag 모드 상태
    if _rag_flag_available:
        try:
            config = get_rag_config()
            response["flag"] = {
                "available": True,
                "enabled": config["flag_enabled"] == "1",
                "config": config,
            }

        except Exception as e:
            logger.error("RAG Flag health check failed: %s", str(e))
            response["flag"]["error"] = str(e)

    # 전체 상태 결정
    shadow_ok = response["shadow"]["available"] and response["shadow"]["enabled"]
    flag_ok = response["flag"]["available"]

    if shadow_ok and flag_ok:
        response["overall_status"] = "enabled"
        response["message"] = "RAG Shadow + Flag 모드 정상 작동 중"
    elif shadow_ok or flag_ok:
        response["overall_status"] = "partial"
        response["message"] = "RAG 모드 부분 활성화됨"
    else:
        response["overall_status"] = "disabled"
        response["message"] = "RAG 모드 비활성화됨"

    return response
