"""
Compatibility Layer (Strangler Fig Pattern)
-------------------------------------------
Centralizes conditional imports and legacy support logic.
Ensures 'api_server.py' remains clean and type-safe (Truth 100%).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


# 7. Chancellor Router Type Models (Strangler Fig Facade)
class ChancellorInvokeRequest(BaseModel):
    """Chancellor Graph 호출 요청 모델 - 眞 (Truth) 타입 안전성 확보"""

    query: str = Field(..., description="사용자 쿼리")
    thread_id: str = Field(default="default", description="대화 스레드 ID")
    auto_run: bool = Field(
        default_factory=lambda: (
            get_antigravity_control().AUTO_DEPLOY if get_antigravity_control() else True
        ),
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
        default=None,
        description="Ollama 모델 override (예: llama3.2:3b, qwen2.5:3b 등)",
    )
    ollama_timeout_seconds: float | None = Field(
        default=None, ge=0.5, le=300, description="Ollama HTTP 타임아웃(초)"
    )
    ollama_num_ctx: int | None = Field(
        default=None,
        ge=256,
        le=32768,
        description="Ollama num_ctx override (컨텍스트 윈도우)",
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
    """Chancellor Graph 호출 응답 모델 - 美 (Beauty) 구조적 일관성 확보"""

    response: str = Field(..., description="Chancellor 응답")
    speaker: str = Field(default="Chancellor", description="응답자")
    thread_id: str = Field(..., description="대화 스레드 ID")
    trinity_score: float = Field(default=0.0, description="Trinity Score")
    strategists_consulted: list[str] = Field(default_factory=list, description="상담한 책사 목록")
    analysis_results: dict[str, Any] = Field(default_factory=dict, description="분석 결과")
    mode_used: str = Field(..., description="사용된 실행 모드")
    fallback_used: bool = Field(default=False, description="폴백 사용 여부")
    timed_out: bool = Field(default=False, description="타임아웃 발생 여부")
    system_metrics: dict[str, Any] = Field(default_factory=dict, description="시스템 메트릭")
    routing: dict[str, Any] = Field(default_factory=dict, description="라우팅 정보")


# 1. Environment & Settings

try:
    from dotenv import load_dotenv as _real_load_dotenv

    _load_dotenv: Any = _real_load_dotenv
except ImportError:
    _load_dotenv = None


def load_dotenv_safe() -> bool:
    """Safe wrapper for dotenv.load_dotenv"""
    if _load_dotenv is not None:
        return bool(_load_dotenv(dotenv_path=str(Path.cwd() / ".env"), override=True))
    return False


_get_settings_func: Any = None

try:
    from AFO.config.settings import get_settings as _real_get_settings

    _get_settings_func = _real_get_settings
except ImportError:
    try:
        # [대학] 격물치지 - 사물을 궁구하여 지식을 얻음
        from config.settings import get_settings as _fallback_get_settings

        _get_settings_func = _fallback_get_settings
    except ImportError:
        pass


# [노자] 도가도비상도 - 완벽한 타입 정의는 변화를 담지 못함
def get_settings_safe() -> Any:
    """Safe wrapper for get_settings"""
    if _get_settings_func is not None:
        try:
            return _get_settings_func()
        except (AttributeError, TypeError, RuntimeError) as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.debug("get_settings 호출 실패 (속성/타입/런타임 에러): %s", str(e))
            return None
        except Exception as e:  # - Intentional fallback for unexpected errors
            import logging

            logger = logging.getLogger(__name__)
            logger.debug("get_settings 호출 중 예상치 못한 에러: %s", str(e))
            return None
    return None


get_settings = get_settings_safe


# 2. Lazy Imports (External Libs)
class LazyModules:
    """Facade for optionally installed modules"""

    anthropic: Any = None
    chromadb: Any = None
    crewai: Any = None
    langchain: Any = None
    qdrant_client: Any = None
    sentry_sdk: Any = None

    @classmethod
    def load(cls) -> type[LazyModules]:
        try:
            # [주역] 무극이태극 - 무에서 유가 나옴
            from afo_soul_engine.utils.lazy_imports import (
                anthropic,
                chromadb,
                crewai,
                langchain,
                qdrant_client,
            )

            cls.anthropic = anthropic
            cls.chromadb = chromadb
            cls.crewai = crewai
            cls.langchain = langchain
            cls.qdrant_client = qdrant_client
        except ImportError:
            pass

        try:
            import sentry_sdk

            cls.sentry_sdk = sentry_sdk
        except ImportError:
            pass

        return cls


LazyModules.load()


# 3. Hybrid RAG Services
class HybridRAG:
    """Facade for Hybrid RAG services"""

    available: bool = False
    blend_results_async: Any = None
    generate_answer_async: Any = None
    get_embedding_async: Any = None
    query_pgvector_async: Any = None
    query_redis_async: Any = None
    select_context: Any = None

    @classmethod
    def load(cls) -> type[HybridRAG]:
        try:
            from AFO.services.hybrid_rag import (
                generate_answer_async,
                get_embedding_async,
                query_pgvector_async,
                query_redis_async,
                select_context,
            )

            cls.available = True
            cls.generate_answer_async = generate_answer_async
            cls.get_embedding_async = get_embedding_async
            cls.query_pgvector_async = query_pgvector_async
            cls.query_redis_async = query_redis_async
            cls.select_context = select_context
        except ImportError:
            cls.available = False

        return cls


HybridRAG.load()


# 4. Router Exports (Strangler Fig Facade)
def _get_fallback_router() -> Any:
    try:
        from fastapi import APIRouter

        return APIRouter()
    except ImportError:
        return None


# Initial Fallbacks
auth_router = _get_fallback_router()
chancellor_router = _get_fallback_router()
family_router = _get_fallback_router()
health_router = _get_fallback_router()
julie_router = _get_fallback_router()
personas_router = _get_fallback_router()
root_router = _get_fallback_router()
streams_router = _get_fallback_router()
users_router = _get_fallback_router()
skills_router = _get_fallback_router()
trinity_router = _get_fallback_router()
rag_router = _get_fallback_router()
system_health_router = _get_fallback_router()
trinity_policy_router = _get_fallback_router()
trinity_sbt_router = _get_fallback_router()
multi_agent_router = _get_fallback_router()
education_system_router = _get_fallback_router()
learning_log_router = _get_fallback_router()
grok_stream_router = _get_fallback_router()
budget_router = _get_fallback_router()
aicpa_router = _get_fallback_router()
voice_router = _get_fallback_router()
council_router = _get_fallback_router()
learning_pipeline = _get_fallback_router()
serenity_router = _get_fallback_router()
matrix_router = _get_fallback_router()
rag_query_router = _get_fallback_router()
finance_router = _get_fallback_router()
ssot_router = _get_fallback_router()
modal_data_router = _get_fallback_router()
n8n_router = _get_fallback_router()
wallet_router = _get_fallback_router()
chat_router = _get_fallback_router()
# [손자병법] 지피지기 - thoughts_router는 왕국의 사고를 투명하게 드러내는 창
thoughts_router = _get_fallback_router()
got_router = _get_fallback_router()
pillars_router = _get_fallback_router()
strangler_router = _get_fallback_router()

# Flags
ANTHROPIC_AVAILABLE: bool = LazyModules.anthropic is not None
OPENAI_AVAILABLE: bool = False


# Functions
# Metrics
try:
    from AFO.domain.metrics.trinity import TrinityMetrics
except ImportError:

    class TrinityMetrics:  # type: ignore
        def __init__(self, **kwargs):
            self.trinity_score = 0.0
            self.truth = 0.0
            self.goodness = 0.0
            self.beauty = 0.0
            self.filial_serenity = 0.0
            self.eternity = 0.0
            self.balance_status = "Unknown"

        def to_dict(self) -> dict:
            return {}


# Functions
def calculate_trinity(*args: Any, **kwargs: Any) -> Any:
    try:
        # Try to use real function if available
        from AFO.domain.metrics.trinity import calculate_trinity as real_calculate

        return real_calculate(*args, **kwargs)
    except ImportError as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.debug("Trinity 계산 모듈 import 실패: %s", str(e))
        # Fallback to mock if import fails or execution fails
        # Try importing TrinityMetrics to return a mock instance
        try:
            from AFO.domain.metrics.trinity import TrinityMetrics

            # If we have the class but function failed, we can't easily instantiate it
            # because it needs derived fields.
            # So we fall back into the Mock class below if possible,
            # OR we manually construct it with dummy derived fields if needed.
            # But easier to just return the Mock object defined locally if we can.
            pass
        except ImportError:
            pass

        # Return fallback mock
        m = TrinityMetrics(
            truth=0.8,
            goodness=0.8,
            beauty=0.8,
            filial_serenity=0.8,
            eternity=0.8,
            serenity_core=0.8,
            trinity_score=0.8,
            balance_delta=0.0,
            balance_status="balanced",
        )
        m.trinity_score = 0.8
        m.truth = 0.8
        m.goodness = 0.8
        m.beauty = 0.8
        m.filial_serenity = 0.8
        m.eternity = 0.8
        m.balance_status = "balanced"
        return m


# Try to load known routers
# [논어] 학이시습지 - 반복적으로 시도하여 지식을 쌓음
def load_routers() -> None:
    global \
        auth_router, \
        family_router, \
        health_router, \
        personas_router, \
        root_router, \
        streams_router, \
        users_router, \
        chancellor_router, \
        julie_router, \
        skills_router, \
        trinity_router, \
        skills_router, \
        trinity_router, \
        thoughts_router, \
        pillars_router, \
        thoughts_router, \
        pillars_router, \
        chat_router, \
        wallet_router

    try:
        from AFO.api.routers.auth import router as auth

        auth_router = auth
    except ImportError:
        pass

    try:
        from AFO.api.routers.family import router as family

        family_router = family
    except ImportError:
        pass

    try:
        from AFO.api.routers.health import router as health

        health_router = health
    except ImportError:
        pass

    try:
        from AFO.api.routers.personas import router as personas

        personas_router = personas
    except ImportError:
        pass

    try:
        from AFO.api.routers.root import router as root

        root_router = root
    except ImportError:
        pass

    try:
        from AFO.api.routes.streams import router as streams

        streams_router = streams
    except ImportError:
        pass

    try:
        from AFO.api.routers.users import router as users

        users_router = users
    except ImportError:
        pass

    try:
        from AFO.api.routers.chancellor_router import router as chancellor

        chancellor_router = chancellor
    except ImportError:
        pass

    try:
        from AFO.api.routers.julie_royal import router as julie

        julie_router = julie
    except ImportError:
        pass

    try:
        from AFO.api.routers.learning_log_router import router as learning_log

        global learning_log_router
        learning_log_router = learning_log
    except ImportError:
        pass

    try:
        from AFO.api.routers.grok_stream import router as grok_stream

        global grok_stream_router
        grok_stream_router = grok_stream
    except ImportError:
        pass

    try:
        from AFO.api.routers.skills import router as skills

        global skills_router
        skills_router = skills
    except ImportError:
        pass

    try:
        from api.routes.chat import router as chat

        chat_router = chat
    except ImportError:
        try:
            from AFO.api.routes.chat import router as chat

            chat_router = chat
        except ImportError:
            pass

    # Try to load others if possible
    # (Assuming paths based on naming convention)
    # If not found, they remain fallback routers (Safe)

    try:
        from AFO.api.routers.thoughts import router as thoughts

        global thoughts_router
        thoughts_router = thoughts
    except ImportError:
        pass

    try:
        from AFO.api.routes.pillars import router as pillars

        global pillars_router
        pillars_router = pillars
    except ImportError:
        pass

    try:
        from AFO.api.routes.wallet import wallet_router as wallet

        global wallet_router
        wallet_router = wallet
    except ImportError:
        pass

    # System Health (Crucial for Neudash)
    try:
        from AFO.api.routes.system_health import router as sys_health
        
        global system_health_router
        system_health_router = sys_health
    except ImportError:
        try:
             from api.routes.system_health import router as sys_health
             system_health_router = sys_health
        except ImportError:
             pass

    # Phase-specific routers
    try:
        from AFO.api.routers.budget import router as budget

        global budget_router
        budget_router = budget
    except ImportError:
        pass

    try:
        from AFO.api.routers.aicpa import router as aicpa

        global aicpa_router
        aicpa_router = aicpa
    except ImportError:
        pass

    try:
        from AFO.api.routers.voice import router as voice

        global voice_router
        voice_router = voice
    except ImportError:
        pass

    try:
        from AFO.api.routers.council import router as council

        global council_router
        council_router = council
    except ImportError:
        pass

    try:
        from AFO.api.routers.learning_pipeline import router as learning_pipe

        global learning_pipeline
        learning_pipeline = learning_pipe
    except ImportError:
        pass

    try:
        from AFO.api.routers.serenity_router import router as serenity

        global serenity_router
        serenity_router = serenity
    except ImportError:
        pass

    try:
        from AFO.api.routers.matrix import router as matrix

        global matrix_router
        matrix_router = matrix
    except ImportError:
        pass

    try:
        from AFO.api.routers.rag_query import router as rag_query

        global rag_query_router
        rag_query_router = rag_query
    except ImportError:
        pass

    try:
        from AFO.api.routers.finance import router as finance

        global finance_router
        finance_router = finance
    except ImportError:
        pass

    try:
        from AFO.api.routers.ssot import router as ssot

        global ssot_router
        ssot_router = ssot
    except ImportError:
        pass


load_routers()


# 5. Antigravity Facade (Pure Control)
def get_antigravity_control() -> Any:
    """
    [Pure] Get Antigravity Governance Controller
    Returns the singleton instance via facade.
    """
    try:
        from AFO.config.antigravity import antigravity

        return antigravity
    except ImportError:
        return None


# 6. TRINITY-OS MCP Client Facade
class TrinityOSMCPClient:
    """
    TRINITY-OS MCP 클라이언트 래퍼
    Phase 5: 실제 JSON-RPC 2.0 통신 구현
    """

    def __init__(self) -> None:
        self._available = False
        self._server_path: Path | None = None
        self._process: Any = None
        self._request_id = 0
        self._load_client()

    def _load_client(self) -> None:
        """MCP 클라이언트 로드 시도"""
        try:
            # TRINITY-OS MCP 서버 경로 확인
            from pathlib import Path

            trinity_os_path = Path(__file__).parent.parent.parent.parent / "trinity-os"
            mcp_server_path = (
                trinity_os_path / "trinity_os" / "servers" / "afo_ultimate_mcp_server.py"
            )

            if mcp_server_path.exists():
                self._server_path = mcp_server_path
                self._available = True
        except (OSError, FileNotFoundError, PermissionError) as e:
            logger = logging.getLogger(__name__)
            logger.debug("MCP 서버 경로 확인 실패 (파일 시스템 에러): %s", str(e))
            self._available = False
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger = logging.getLogger(__name__)
            logger.debug("MCP 서버 경로 확인 중 예상치 못한 에러: %s", str(e))
            self._available = False

    def _get_next_request_id(self) -> int:
        """다음 요청 ID 생성"""
        self._request_id += 1
        return self._request_id

    async def _send_jsonrpc_request(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        timeout: float = 5.0,
        max_retries: int = 3,
        retry_delay: float = 0.5,
    ) -> dict[str, Any] | None:
        """
        JSON-RPC 2.0 요청 전송 (재시도 메커니즘 포함)

        Args:
            method: JSON-RPC 메서드
            params: 요청 파라미터
            timeout: 타임아웃 (초)
            max_retries: 최대 재시도 횟수
            retry_delay: 재시도 간 지연 시간 (초)

        Returns:
            응답 결과 또는 None (실패 시)
        """
        if not self._available or not self._server_path:
            return None

        import asyncio
        import json
        import logging
        import subprocess

        logger = logging.getLogger(__name__)

        last_exception: Exception | None = None

        for attempt in range(max_retries):
            try:
                # MCP 서버 프로세스 시작 (stdio 통신)
                process = await asyncio.create_subprocess_exec(
                    "python3",
                    str(self._server_path),
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                # JSON-RPC 2.0 요청 생성
                request_id = self._get_next_request_id()
                request = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "method": method,
                    "params": params or {},
                }

                # 요청 전송
                request_json = json.dumps(request) + "\n"
                if process.stdin:
                    process.stdin.write(request_json.encode())
                    await process.stdin.drain()

                # 응답 수신 (타임아웃 적용)
                try:
                    if process.stdout:
                        response_line = await asyncio.wait_for(
                            process.stdout.readline(), timeout=timeout
                        )
                        if response_line:
                            response = json.loads(response_line.decode())
                            # 프로세스 종료
                            if process.returncode is None:
                                process.terminate()
                                await process.wait()
                            result = response.get("result")
                            # 타입 명시: dict[str, Any] | None
                            if isinstance(result, dict):
                                return result
                            return None
                except asyncio.TimeoutError:
                    if process.returncode is None:
                        process.terminate()
                        await process.wait()
                    # 타임아웃은 재시도 대상
                    last_exception = asyncio.TimeoutError("MCP 서버 응답 타임아웃")
                    if attempt < max_retries - 1:
                        logger.debug(
                            "MCP 요청 타임아웃 (시도 %d/%d), 재시도 중...",
                            attempt + 1,
                            max_retries,
                        )
                        await asyncio.sleep(retry_delay * (attempt + 1))  # 지수 백오프
                        continue
                    return None

            except (subprocess.SubprocessError, OSError) as e:
                # 프로세스 관련 오류는 재시도 대상
                last_exception = e
                if attempt < max_retries - 1:
                    logger.debug(
                        "MCP 서버 프로세스 오류 (시도 %d/%d): %s, 재시도 중...",
                        attempt + 1,
                        max_retries,
                        str(e),
                    )
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                logger.warning("MCP 서버 프로세스 오류 (최종 실패): %s", str(e))
                return None

            except (json.JSONDecodeError, ValueError) as e:
                # JSON 파싱 오류는 재시도하지 않음 (요청 자체 문제)
                logger.error("MCP 응답 JSON 파싱 오류: %s", str(e))
                return None

            except Exception as e:
                # 기타 예외는 재시도 대상
                last_exception = e
                if attempt < max_retries - 1:
                    logger.debug(
                        "MCP 요청 오류 (시도 %d/%d): %s, 재시도 중...",
                        attempt + 1,
                        max_retries,
                        str(e),
                    )
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                logger.warning("MCP 요청 오류 (최종 실패): %s", str(e))
                return None

        # 모든 재시도 실패
        if last_exception:
            logger.error("MCP 요청 최종 실패 (%d회 시도): %s", max_retries, str(last_exception))
        return None

    async def _send_request_to_process(
        self,
        process: Any,
        method: str,
        params: dict[str, Any] | None = None,
        request_id: int | None = None,
        timeout: float = 5.0,
    ) -> dict[str, Any] | None:
        """
        실행 중인 프로세스에 JSON-RPC 요청 전송 (프로세스 재사용)

        Args:
            process: 실행 중인 subprocess
            method: JSON-RPC 메서드
            params: 요청 파라미터
            request_id: 요청 ID (None이면 자동 생성)
            timeout: 타임아웃 (초)

        Returns:
            응답 결과 또는 None (실패 시)
        """
        import asyncio
        import json
        import logging

        logger = logging.getLogger(__name__)

        if request_id is None:
            request_id = self._get_next_request_id()

        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params or {},
        }

        try:
            # 요청 전송
            request_json = json.dumps(request) + "\n"
            if process.stdin:
                process.stdin.write(request_json.encode())
                await process.stdin.drain()

            # 응답 수신
            if process.stdout:
                response_line = await asyncio.wait_for(process.stdout.readline(), timeout=timeout)
                if response_line:
                    response = json.loads(response_line.decode())
                    # 에러 체크
                    if "error" in response:
                        logger.debug(
                            "MCP 서버 오류: %s",
                            response.get("error", {}).get("message", "Unknown error"),
                        )
                        return None
                    return response.get("result")
            return None

        except asyncio.TimeoutError:
            logger.debug("MCP 요청 타임아웃: %s", method)
            return None
        except json.JSONDecodeError as e:
            logger.debug("MCP 응답 JSON 파싱 오류: %s", str(e))
            return None
        except (ConnectionError, OSError, ValueError) as e:
            logger.debug("MCP 요청 오류 (연결/시스템/값 에러): %s - %s", method, str(e))
            return None
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("MCP 요청 오류 (예상치 못한 에러): %s - %s", method, str(e))
            return None

    async def send_log_event(self, event_type: str, data: dict[str, Any]) -> None:
        """
        로그 이벤트를 TRINITY-OS MCP 서버로 전송 (프로세스 재사용 방식)

        Args:
            event_type: 이벤트 타입 (예: "persona_switch")
            data: 이벤트 데이터
        """
        if not self._available or not self._server_path:
            import logging

            logger = logging.getLogger(__name__)
            logger.debug("[MCP] 클라이언트 사용 불가, 로컬 로깅")
            return

        import asyncio
        import json
        import logging

        logger = logging.getLogger(__name__)

        process: Any = None

        try:
            # MCP 서버 프로세스 시작 (한 번만)
            process = await asyncio.create_subprocess_exec(
                "python3",
                str(self._server_path),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            # 1단계: Initialize 요청
            init_result = await self._send_request_to_process(
                process,
                "initialize",
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "AFO-PersonaService", "version": "1.0"},
                },
                request_id=1,
                timeout=2.0,
            )

            if not init_result:
                logger.debug("[MCP] Initialize 실패, 로컬 로깅으로 폴백")
                logger.info(
                    "[TRINITY-OS MCP] %s 이벤트 로컬 로깅: %s",
                    event_type,
                    data.get("persona_name", "unknown"),
                )
                return

            # 2단계: Notifications/initialized (선택적, 서버가 요구하지 않으면 생략)
            # 현재 구현에서는 생략 (서버가 자동 처리)

            # 3단계: Tools/call - write_file을 통한 로그 저장
            log_path = f"logs/persona_events/{event_type}_{data.get('persona_id', 'unknown')}.json"
            tool_result = await self._send_request_to_process(
                process,
                "tools/call",
                {
                    "name": "write_file",
                    "arguments": {
                        "path": log_path,
                        "content": json.dumps(data, indent=2, ensure_ascii=False),
                    },
                },
                request_id=2,
                timeout=3.0,
            )

            if tool_result:
                logger.info(
                    "[TRINITY-OS MCP] %s 이벤트 전송 성공: %s (경로: %s)",
                    event_type,
                    data.get("persona_name", "unknown"),
                    log_path,
                )
            else:
                logger.debug(
                    "[TRINITY-OS MCP] %s 이벤트 MCP 전송 실패, 로컬 로깅: %s",
                    event_type,
                    data.get("persona_name", "unknown"),
                )

        except (OSError, ProcessLookupError, ValueError) as e:
            logger.debug("MCP 로그 이벤트 전송 실패 (시스템/프로세스/값 에러): %s", str(e))
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("MCP 로그 이벤트 전송 실패 (예상치 못한 에러): %s", str(e))
        finally:
            # 프로세스 정리
            if process and process.returncode is None:
                try:
                    process.terminate()
                    await asyncio.wait_for(process.wait(), timeout=2.0)
                except (OSError, ProcessLookupError, asyncio.TimeoutError) as e:
                    logger.debug("프로세스 종료 실패, 강제 종료 시도: %s", str(e))
                    # 프로세스 종료 실패 시 강제 종료
                    try:
                        process.kill()
                        await process.wait()
                    except (OSError, ProcessLookupError) as e2:
                        logger.debug("프로세스 강제 종료 실패: %s", str(e2))
                    except Exception as e2:  # - Intentional fallback
                        logger.debug("프로세스 강제 종료 중 예상치 못한 에러: %s", str(e2))

    @property
    def available(self) -> bool:
        """MCP 클라이언트 사용 가능 여부"""
        return self._available


# 싱글톤 인스턴스
_trinity_os_client: TrinityOSMCPClient | None = None


def get_trinity_os_client() -> TrinityOSMCPClient | None:
    """
    TRINITY-OS MCP 클라이언트 인스턴스 반환

    Returns:
        TrinityOSMCPClient 인스턴스 또는 None (사용 불가 시)
    """
    global _trinity_os_client
    if _trinity_os_client is None:
        _trinity_os_client = TrinityOSMCPClient()
    return _trinity_os_client if _trinity_os_client.available else None
