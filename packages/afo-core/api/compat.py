"""
AFO Kingdom Compatibility Layer (아름다운 코드 적용)
Strangler Fig Facade - HTML Legacy Data Compatibility Layer

Phase 15: The Grok Singularity - 아름다운 코드로 구현된 호환성 레이어
Trinity Score 기반 품질 관리 및 모듈화된 구조로 확장성 보장.

Author: AFO Kingdom Development Team
Date: 2025-12-24
Version: 2.0.0 (Beautiful Code Edition)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from api.routes.pillars import router as pillars_router
except ImportError:
    pillars_router = None

# Configure logging
logger = logging.getLogger(__name__)

# HTML Data Sources with validation
HTML_DASHBOARD_PATH = (
    Path(__file__).parent.parent.parent.parent
    / "packages/dashboard/public/legacy/kingdom_dashboard.html"
)


@dataclass
class HTMLSectionData:
    """
    HTML 섹션 데이터 구조체

    아름다운 코드 원칙 준수: 불변 데이터 구조 + 타입 안전성
    """

    id: str
    title: str
    content: dict[str, Any]
    last_updated: datetime


class PhilosophyDataProvider:
    """
    철학 데이터 제공자 (眞善美孝永 5기둥)

    Trinity Score: 眞 (Truth) - 정확한 철학 데이터 제공
    아름다운 코드: 단일 책임 + 불변 데이터 + 타입 안전성
    """

    @staticmethod
    def get_philosophy_data() -> dict[str, Any]:
        """5기둥 철학 데이터 반환"""
        return {
            "pillars": [
                {
                    "id": "truth",
                    "name": "眞",
                    "weight": 35,
                    "role": "제갈량 - 기술적 확실성",
                    "color": "#3b82f6",
                },
                {
                    "id": "goodness",
                    "name": "善",
                    "weight": 35,
                    "role": "사마의 - 윤리·안정성",
                    "color": "#10b981",
                },
                {
                    "id": "beauty",
                    "name": "美",
                    "weight": 20,
                    "role": "주유 - 단순함·우아함",
                    "color": "#8b5cf6",
                },
                {
                    "id": "serenity",
                    "name": "孝",
                    "weight": 8,
                    "role": "승상 - 평온 수호",
                    "color": "#f59e0b",
                },
                {
                    "id": "eternity",
                    "name": "永",
                    "weight": 2,
                    "role": "승상 - 영속성",
                    "color": "#ef4444",
                },
            ],
            "trinity_formula": "Trinity Score = 0.35×眞 + 0.35×善 + 0.20×美 + 0.08×孝 + 0.02×永",
            "auto_run_condition": "AUTO_RUN: Trinity Score ≥ 90 AND Risk Score ≤ 10",
        }


class PortDataProvider:
    """
    포트 데이터 제공자

    Trinity Score: 美 (Beauty) - 체계적이고 읽기 쉬운 데이터 구조
    """

    @staticmethod
    def get_port_data() -> list[dict[str, str]]:
        """서비스 포트 매핑 데이터 반환"""
        return [
            {"service": "Soul Engine", "port": "8010", "description": "FastAPI 백엔드"},
            {
                "service": "Dashboard",
                "port": "3000",
                "description": "Next.js 프론트엔드",
            },
            {"service": "Ollama", "port": "11435", "description": "LLM (영덕)"},
            {"service": "Redis", "port": "6379", "description": "캐시/세션"},
            {"service": "PostgreSQL", "port": "15432", "description": "데이터베이스"},
            {"service": "Grafana", "port": "3100", "description": "모니터링"},
            {"service": "Prometheus", "port": "9090", "description": "메트릭"},
        ]


class PersonaDataProvider:
    """
    페르소나 데이터 제공자

    Trinity Score: 永 (Eternity) - 확장 가능한 데이터 구조
    """

    @staticmethod
    def get_personas_data() -> list[dict[str, str]]:
        """AFO 왕국 페르소나 데이터 반환"""
        return [
            {
                "name": "승상",
                "code": "Chancellor",
                "role": "3책사 병렬 조율, 웹 오케스트레이터",
            },
            {
                "name": "제갈량",
                "code": "Zhuge Liang",
                "role": "眞 35% - 아키텍처·전략·개발",
            },
            {"name": "사마의", "code": "Sima Yi", "role": "善 35% - 윤리·안정·게이트"},
            {"name": "주유", "code": "Zhou Yu", "role": "美 20% - 서사·UX·취향정렬"},
            {
                "name": "방통",
                "code": "Bangtong",
                "role": "Codex - 구현·실행·프로토타이핑",
            },
            {"name": "자룡", "code": "Jaryong", "role": "Claude - 논리 검증·리팩터링"},
            {"name": "육손", "code": "Yukson", "role": "Gemini - 전략·철학·큰 그림"},
            {
                "name": "영덕",
                "code": "Yeongdeok",
                "role": "Ollama - 설명·보안·아카이빙",
            },
        ]


class RoyalRulesDataProvider:
    """
    왕실 규약 데이터 제공자

    Trinity Score: 善 (Goodness) - 윤리적이고 체계적인 규약 제공
    """

    @staticmethod
    def get_royal_rules_data() -> list[dict[str, Any]]:
        """왕실 헌법 규약 데이터 반환"""
        return [
            {
                "book": "손자병법",
                "weight": "眞 70% / 孝 30%",
                "rules": [
                    {
                        "id": 1,
                        "name": "지피지기 (Rule #0)",
                        "principle": "Context7과 DB 조회 필수",
                    },
                    {
                        "id": 2,
                        "name": "상병벌모",
                        "principle": "기존 라이브러리 활용 우선",
                    },
                    {"id": 3, "name": "병자궤도야", "principle": "DRY_RUN 기본값 True"},
                    {
                        "id": 4,
                        "name": "병귀신속",
                        "principle": "비동기 처리 (asyncio, Celery)",
                    },
                    {
                        "id": 5,
                        "name": "도천지장법",
                        "principle": "Trinity Score 5기둥 정렬 체크",
                    },
                ],
            },
            {
                "book": "삼국지",
                "weight": "永 60% / 善 40%",
                "rules": [
                    {
                        "id": 13,
                        "name": "도원결의",
                        "principle": "Interface 통일, Shared Context",
                    },
                    {
                        "id": 14,
                        "name": "삼고초려",
                        "principle": "Retry(max_attempts=3, backoff=exponential)",
                    },
                    {
                        "id": 15,
                        "name": "공성계",
                        "principle": "Graceful Degradation, Skeleton UI",
                    },
                    {
                        "id": 16,
                        "name": "제갈량의 초선차전",
                        "principle": "pip install, External API",
                    },
                    {
                        "id": 17,
                        "name": "연환계",
                        "principle": "Pipeline Pattern, LangGraph Node Linking",
                    },
                ],
            },
            {
                "book": "군주론",
                "weight": "善 50% / 眞 50%",
                "rules": [
                    {
                        "id": 25,
                        "name": "사랑보다 두려움",
                        "principle": "Strict Typing, Validation",
                    },
                    {
                        "id": 26,
                        "name": "비르투와 포르투나",
                        "principle": "Exception Handling",
                    },
                    {
                        "id": 27,
                        "name": "여우와 사자",
                        "principle": "Algorithm Selection",
                    },
                    {"id": 28, "name": "증오 피하기", "principle": "UX Optimization"},
                    {
                        "id": 29,
                        "name": "무장한 예언자",
                        "principle": "Executable Code Only",
                    },
                ],
            },
            {
                "book": "전쟁론",
                "weight": "眞 60% / 孝 40%",
                "rules": [
                    {
                        "id": 34,
                        "name": "전장의 안개",
                        "principle": "Null Check, Data Validation",
                    },
                    {"id": 35, "name": "마찰", "principle": "Complexity Estimation"},
                    {"id": 36, "name": "중심", "principle": "Root Cause Analysis"},
                    {
                        "id": 37,
                        "name": "공세 종말점",
                        "principle": "Resource Monitoring",
                    },
                    {
                        "id": 38,
                        "name": "지휘 통일",
                        "principle": "Singleton Pattern, Locking",
                    },
                ],
            },
        ]


class ArchitectureDataProvider:
    """
    아키텍처 데이터 제공자

    Trinity Score: 眞 (Truth) - 정확한 시스템 아키텍처 정보 제공
    """

    @staticmethod
    def get_architecture_data() -> dict[str, Any]:
        """시스템 아키텍처 데이터 반환"""
        return {
            "layers": [
                {
                    "name": "Presentation",
                    "description": "FastAPI 엔드포인트, 라우터, Pydantic 모델",
                },
                {
                    "name": "Application",
                    "description": "Chancellor Graph, RAG Graph, LLM 라우터",
                },
                {
                    "name": "Domain",
                    "description": "Trinity Score, Skill Cards, Rules 정의",
                },
                {
                    "name": "Infrastructure",
                    "description": "PostgreSQL, Redis, Qdrant, 외부 API",
                },
            ],
            "components": {
                "brain": {"name": "PostgreSQL", "description": "장기 기억 장치"},
                "heart": {"name": "Redis", "description": "실시간 캐시, 세션"},
                "lungs": {"name": "Qdrant", "description": "벡터 검색"},
                "digestive": {"name": "Ollama", "description": "로컬 LLM"},
                "testing": {"name": "Pytest", "description": "검증 시스템"},
            },
        }


class StatsDataProvider:
    """
    통계 데이터 제공자

    Trinity Score: 孝 (Serenity) - 안정적인 프로젝트 통계 제공
    """

    @staticmethod
    def get_stats_data() -> dict[str, int]:
        """프로젝트 통계 데이터 반환"""
        return {
            "python_files": 1506,
            "typescript_files": 5439,
            "markdown_docs": 1005,
            "total_commits": 120,
            "development_days": 5,
            "tracked_files": 1291,
        }


class HTMLDataFacade:
    """
    HTML 데이터 파사드 (아름다운 코드 적용)

    Strangler Fig 패턴을 아름다운 코드로 구현.
    각 데이터 제공자를 조율하여 체계적인 데이터 접근 제공.

    Trinity Score: 美 (Beauty) - 모듈화된 파사드 패턴 적용
    """

    def __init__(self) -> None:
        """Initialize HTML Data Facade with beautiful code principles."""
        self._philosophy_provider = PhilosophyDataProvider()
        self._port_provider = PortDataProvider()
        self._persona_provider = PersonaDataProvider()
        self._rules_provider = RoyalRulesDataProvider()
        self._architecture_provider = ArchitectureDataProvider()
        self._stats_provider = StatsDataProvider()

        logger.info("HTML Data Facade initialized with beautiful code principles")

    def get_philosophy_data(self) -> dict[str, Any]:
        """철학 데이터 조회"""
        return self._philosophy_provider.get_philosophy_data()

    def get_port_data(self) -> list[dict[str, str]]:
        """포트 데이터 조회"""
        return self._port_provider.get_port_data()

    def get_personas_data(self) -> list[dict[str, str]]:
        """페르소나 데이터 조회"""
        return self._persona_provider.get_personas_data()

    def get_royal_rules_data(self) -> list[dict[str, Any]]:
        """왕실 규약 데이터 조회"""
        return self._rules_provider.get_royal_rules_data()

    def get_architecture_data(self) -> dict[str, Any]:
        """아키텍처 데이터 조회"""
        return self._architecture_provider.get_architecture_data()

    def get_stats_data(self) -> dict[str, int]:
        """통계 데이터 조회"""
        return self._stats_provider.get_stats_data()


class SettingsManager:
    """
    설정 관리자 (아름다운 코드 적용)

    Trinity Score: 善 (Goodness) - 안전하고 검증된 설정 관리
    """

    @staticmethod
    def get_settings_safe() -> dict[str, Any]:
        """
        안전하게 설정값을 가져오는 함수

        Returns:
            검증된 설정값 딕셔너리
        """
        try:
            # 환경 변수에서 직접 로드 (순환 import 방지)
            config = {
                "app_name": os.getenv("AFO_APP_NAME", "AFO Kingdom"),
                "version": os.getenv("AFO_VERSION", "1.0.0"),
                "debug": os.getenv("AFO_DEBUG", "true").lower() == "true",
                "host": os.getenv("AFO_HOST", "0.0.0.0"),
                "port": int(os.getenv("AFO_PORT", "8010")),
                "cors_origins": os.getenv(
                    "AFO_CORS_ORIGINS", "http://localhost:3000"
                ).split(","),
                "database_url": os.getenv("DATABASE_URL", "sqlite:///./test.db"),
                "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379"),
                "ollama_url": os.getenv("OLLAMA_URL", "http://localhost:11435"),
            }

            logger.debug("Settings loaded successfully")
            return config

        except Exception as e:
            logger.error(f"Settings load failed: {e}")
            # Fallback to minimal config
            return SettingsManager._get_minimal_config()

    @staticmethod
    def _get_minimal_config() -> dict[str, Any]:
        """최소한의 기본 설정 반환"""
        return {
            "app_name": "AFO Kingdom",
            "version": "1.0.0",
            "debug": True,
            "host": "0.0.0.0",
            "port": 8010,
            "cors_origins": ["http://localhost:3000"],
        }


# Global instances with singleton pattern (beautiful code)
html_facade = HTMLDataFacade()
settings_manager = SettingsManager()


# Convenience functions for React components (beautiful code)
def get_philosophy_pillars() -> dict[str, Any]:
    """React component data provider for philosophy section.

    Trinity Score: 眞 (Truth) - 정확한 철학 데이터 제공 보장
    """
    return html_facade.get_philosophy_data()


def get_service_ports() -> list[dict[str, str]]:
    """React component data provider for ports table.

    Trinity Score: 美 (Beauty) - 체계적이고 읽기 쉬운 데이터 구조
    """
    return html_facade.get_port_data()


def get_personas_list() -> list[dict[str, str]]:
    """React component data provider for personas.

    Trinity Score: 永 (Eternity) - 확장 가능한 페르소나 데이터
    """
    return html_facade.get_personas_data()


def get_royal_constitution() -> list[dict[str, Any]]:
    """React component data provider for Royal Constitution.

    Trinity Score: 善 (Goodness) - 윤리적이고 체계적인 규약 제공
    """
    return html_facade.get_royal_rules_data()


def get_system_architecture() -> dict[str, Any]:
    """React component data provider for architecture diagram.

    Trinity Score: 眞 (Truth) - 정확한 시스템 아키텍처 정보
    """
    return html_facade.get_architecture_data()


def get_project_stats() -> dict[str, int]:
    """React component data provider for project statistics.

    Trinity Score: 孝 (Serenity) - 안정적인 프로젝트 통계 제공
    """
    return html_facade.get_stats_data()


def get_settings_safe() -> dict[str, Any]:
    """안전하게 설정값을 가져오는 함수.

    Trinity Score: 善 (Goodness) - 검증된 설정 관리
    """
    return settings_manager.get_settings_safe()


# Compatibility exports (Legacy support)
# LLM availability flags (디버깅용 기본값)
ANTHROPIC_AVAILABLE = False
OPENAI_AVAILABLE = False
GEMINI_AVAILABLE = False
CODEX_AVAILABLE = False
OLLAMA_AVAILABLE = False
LMSTUDIO_AVAILABLE = False

# Dummy routers for compatibility (실제 라우터가 없을 때 사용)
aicpa_router = None
auth_router = None
budget_router = None
chancellor_router = None
chat_router = None
council_router = None
education_system_router = None
finance_router = None
got_router = None
grok_stream_router = None
health_router = None
learning_log_router = None
learning_pipeline = None
matrix_router = None
modal_data_router = None
multi_agent_router = None
n8n_router = None
personas_router = None
# pillars_router is imported above
rag_query_router = None
root_router = None
serenity_router = None
skills_router = None
ssot_router = None
strangler_router = None
streams_router = None
system_health_router = None
trinity_policy_router = None
trinity_sbt_router = None
users_router = None
voice_router = None
wallet_router = None


# Trinity metrics class (더미)
class TrinityMetrics:
    """Trinity Score 메트릭 클래스"""

    def __init__(self) -> None:
        self.scores = {
            "truth": 0,
            "goodness": 0,
            "beauty": 0,
            "serenity": 0,
            "eternity": 0,
        }

    def calculate_score(self) -> float:
        return 0.0


# Trinity score calculator function
def calculate_trinity(scores: dict[str, float]) -> float:
    """Trinity Score 계산 함수

    Args:
        scores: 각 기둥별 점수 (0-100)

    Returns:
        계산된 Trinity Score (0-100)
    """
    weights = {
        "truth": 0.35,
        "goodness": 0.35,
        "beauty": 0.20,
        "serenity": 0.08,
        "eternity": 0.02,
    }

    normalized = {k: v / 100.0 for k, v in scores.items()}
    return sum(normalized[k] * weights[k] for k in weights) * 100


# AntiGravity control function (더미)
def get_antigravity_control() -> dict[str, Any]:
    """AntiGravity 제어 함수"""
    return {"status": "mock", "message": "AntiGravity not available"}


# Settings class (더미)
class Settings:
    """설정 클래스"""

    def __init__(self) -> None:
        pass
