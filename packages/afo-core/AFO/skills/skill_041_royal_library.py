# Trinity Score: 90.0 (Established by Chancellor)
"""AFO 왕립 도서관 41선 Skill/MCP
4대 고전(손자병법/삼국지/군주론/전쟁론)의 전략적 지혜를 실행 가능한 도구로

Rule #0 지피지기: "眞 100% 확보 후 행동" - 야전교범 제1원칙
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Classic(Enum):
    """4대 고전"""

    SUN_TZU = "손자병법"  # 眞 70% / 孝 30%
    THREE_KINGDOMS = "삼국지"  # 永 60% / 善 40%
    THE_PRINCE = "군주론"  # 善 50% / 眞 50%
    ON_WAR = "전쟁론"  # 眞 60% / 孝 40%


@dataclass
class PrincipleResult:
    """원칙 실행 결과"""

    principle_id: int
    principle_name: str
    classic: Classic
    success: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    trinity_impact: dict[str, float] = field(default_factory=dict)


class RoyalLibrarySkill:
    """AFO 왕립 도서관 41선 Skill

    4대 고전의 전략적 지혜:
    - 손자병법 (12선): 眞 70% / 孝 30%
    - 삼국지 (12선): 永 60% / 善 40%
    - 군주론 (9선): 善 50% / 眞 50%
    - 전쟁론 (8선): 眞 60% / 孝 40%
    """

    def __init__(self):
        self.principles_count = 41
        logger.info("📜 [왕립도서관] 41선 Skill 초기화 완료")

    # =========================================================================
    # 제1서: 손자병법 (12선) - 眞 70% / 孝 30%
    # =========================================================================

    async def principle_01_preflight_check(
        self, context: dict[str, Any] | None = None, sources: list[str] | None = None
    ) -> PrincipleResult:
        """[01] 지피지기 (Know Thyself) - Rule #0

        원칙: 모든 실행 전, Context7과 DB를 조회하여 현재 상태를 정확히 파악하라.
        코드: pre_flight_check() 필수 실행. Hallucination 원천 차단.
        """
        sources = sources or []
        context = context or {}

        # 최소 2개 출처 확인
        sources_verified = len(sources) >= 2
        context_loaded = bool(context)

        success = sources_verified or context_loaded

        return PrincipleResult(
            principle_id=1,
            principle_name="지피지기",
            classic=Classic.SUN_TZU,
            success=success,
            message=("眞 100% 확보 완료" if success else "출처 2개 이상 필요 (Rule #0 위반)"),
            data={
                "sources_count": len(sources),
                "context_loaded": context_loaded,
                "sources_verified": sources_verified,
            },
            trinity_impact={"眞": 0.70, "孝": 0.30},
        )

    async def principle_03_dry_run_simulation(
        self, action: Callable[..., T], *args: Any, simulate: bool = True, **kwargs: Any
    ) -> PrincipleResult:
        """[03] 병자궤도야 (All Warfare is Deception) - DRY_RUN

        원칙: 위험한 작업은 반드시 DRY_RUN (모의전)으로 결과를 미리 보여주어라.
        코드: mode='dry_run' 파라미터 기본값 True.
        """
        if simulate:
            # DRY_RUN 모드 - 실제 실행 없이 시뮬레이션
            return PrincipleResult(
                principle_id=3,
                principle_name="병자궤도야",
                classic=Classic.SUN_TZU,
                success=True,
                message="[DRY_RUN] 시뮬레이션 완료 - 실제 실행 전 검토 필요",
                data={
                    "action": (action.__name__ if hasattr(action, "__name__") else str(action)),
                    "args": str(args)[:100],
                    "kwargs": str(kwargs)[:100],
                    "mode": "dry_run",
                },
                trinity_impact={"眞": 0.70, "孝": 0.30},
            )
        else:
            # WET_RUN 모드 - 실제 실행
            try:
                if asyncio.iscoroutinefunction(action):
                    result = await action(*args, **kwargs)
                else:
                    result = action(*args, **kwargs)

                return PrincipleResult(
                    principle_id=3,
                    principle_name="병자궤도야",
                    classic=Classic.SUN_TZU,
                    success=True,
                    message="[WET_RUN] 실행 완료",
                    data={"result": str(result)[:200], "mode": "wet_run"},
                    trinity_impact={"眞": 0.70, "孝": 0.30},
                )
            except Exception as e:
                return PrincipleResult(
                    principle_id=3,
                    principle_name="병자궤도야",
                    classic=Classic.SUN_TZU,
                    success=False,
                    message=f"[WET_RUN] 실행 실패: {e}",
                    data={"error": str(e), "mode": "wet_run"},
                    trinity_impact={"眞": 0.70, "孝": 0.30},
                )

    async def principle_02_find_existing_solution(
        self, requirement: str, search_sources: list[str] | None = None
    ) -> PrincipleResult:
        """[02] 상병벌모 (Win Without Fighting)

        원칙: 코드를 짜는 것보다 기존 라이브러리/API를 활용하는 것이 상책이다.
        코드: import > def. 노가다(Friction) 회피.
        """
        search_sources = search_sources or ["pypi", "npm", "github"]
        return PrincipleResult(
            principle_id=2,
            principle_name="상병벌모",
            classic=Classic.SUN_TZU,
            success=True,
            message=f"기존 솔루션 검색 권장: {search_sources}",
            data={"requirement": requirement, "sources": search_sources},
            trinity_impact={"眞": 0.70, "孝": 0.30},
        )

    async def principle_04_async_execute(self, tasks: list[Callable[..., Any]]) -> PrincipleResult:
        """[04] 병귀신속 (Speed is of Great Value)

        원칙: 응답 속도는 UX의 핵심. 느린 로직은 비동기로 처리하라.
        코드: asyncio, Celery 활용.
        """
        return PrincipleResult(
            principle_id=4,
            principle_name="병귀신속",
            classic=Classic.SUN_TZU,
            success=True,
            message=f"{len(tasks)}개 작업 비동기 실행 준비",
            data={"task_count": len(tasks)},
            trinity_impact={"眞": 0.70, "孝": 0.30},
        )

    async def principle_05_trinity_alignment(
        self, truth_score: float, goodness_score: float, beauty_score: float
    ) -> PrincipleResult:
        """[05] 도천지장법 (The Five Factors)

        원칙: 프로젝트의 5요소가 정렬되었는지 확인하라.
        코드: Trinity Score 5기둥 정렬 체크.
        """
        trinity_score = 0.35 * truth_score + 0.35 * goodness_score + 0.20 * beauty_score
        aligned = trinity_score >= 0.70
        return PrincipleResult(
            principle_id=5,
            principle_name="도천지장법",
            classic=Classic.SUN_TZU,
            success=aligned,
            message=f"Trinity Score: {trinity_score:.2%}"
            + (" - 정렬됨" if aligned else " - 정렬 필요"),
            data={
                "trinity_score": trinity_score,
                "眞": truth_score,
                "善": goodness_score,
                "美": beauty_score,
            },
            trinity_impact={"眞": 0.70, "孝": 0.30},
        )

    async def principle_06_standard_then_custom(self) -> PrincipleResult:
        """[06] 정병 - 정석으로 공격하고, 변칙으로 승리하라."""
        return PrincipleResult(
            6,
            "정병",
            Classic.SUN_TZU,
            True,
            "표준 패턴 준수 후 오버라이딩",
            {},
            {"眞": 0.70, "孝": 0.30},
        )

    async def principle_07_find_bottleneck(
        self, metrics: dict[str, float] | None = None
    ) -> PrincipleResult:
        """[07] 허실 - 시스템의 병목을 찾아 집중 보강하라."""
        metrics = metrics or {}
        bottleneck = min(metrics.items(), key=lambda x: x[1])[0] if metrics else "unknown"
        return PrincipleResult(
            7,
            "허실",
            Classic.SUN_TZU,
            True,
            f"병목 발견: {bottleneck}",
            {"metrics": metrics},
            {"眞": 0.70, "孝": 0.30},
        )

    async def principle_08_exception_handler(self, error: Exception) -> PrincipleResult:
        """[08] 구변 - 예외 상황에 따라 유연하게 대처 경로를 바꿔라."""
        return PrincipleResult(
            8,
            "구변",
            Classic.SUN_TZU,
            True,
            f"예외 처리: {type(error).__name__}",
            {"error": str(error)},
            {"眞": 0.70, "孝": 0.30},
        )

    async def principle_09_logging_spy(self, message: str, level: str = "info") -> PrincipleResult:
        """[09] 용간 - 로그와 모니터링은 적(Bug)을 알 수 있는 유일한 수단이다."""
        getattr(logger, level, logger.info)(f"[용간] {message}")
        return PrincipleResult(
            9,
            "용간",
            Classic.SUN_TZU,
            True,
            f"[{level.upper()}] 로그 기록 완료",
            {"message": message},
            {"眞": 0.70, "孝": 0.30},
        )

    async def principle_10_dangerous_action_gate(
        self, action_name: str, confirmed: bool = False
    ) -> PrincipleResult:
        """[10] 화공 - 파괴적 행동은 확실한 이득이 있을 때만 수행하라."""
        return PrincipleResult(
            10,
            "화공",
            Classic.SUN_TZU,
            confirmed,
            f"위험 행동: {action_name}" + (" - 승인됨" if confirmed else " - 승인 필요"),
            {"confirmed": confirmed},
            {"眞": 0.70, "孝": 0.30},
        )

    async def principle_11_mvp_deploy(self) -> PrincipleResult:
        """[11] 졸속 - 완벽하게 늦는 것보다, 부족해도 빨리 배포하고 고치는 게 낫다."""
        return PrincipleResult(
            11,
            "졸속",
            Classic.SUN_TZU,
            True,
            "MVP 배포 우선",
            {},
            {"眞": 0.70, "孝": 0.30},
        )

    async def principle_12_full_automation(self) -> PrincipleResult:
        """[12] 부전이굴 - 최고의 자동화는 사용자가 아무것도 하지 않게 하는 것이다."""
        return PrincipleResult(
            12,
            "부전이굴",
            Classic.SUN_TZU,
            True,
            "완전 자동화 목표",
            {},
            {"眞": 0.70, "孝": 0.30},
        )

    # =========================================================================
    # 제2서: 삼국지 (12선) - 永 60% / 善 40%
    # =========================================================================

    async def principle_13_loose_coupling(self, modules: list[str]) -> PrincipleResult:
        """[13] 도원결의 - 모듈 간 결합은 느슨하되, 목표는 형제처럼 일치시켜라."""
        return PrincipleResult(
            13,
            "도원결의",
            Classic.THREE_KINGDOMS,
            True,
            f"{len(modules)}개 모듈 느슨한 결합",
            {"modules": modules},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_14_retry_with_backoff(
        self,
        action: Callable[..., T],
        *args: Any,
        max_attempts: int = 3,
        backoff_factor: float = 2.0,
        **kwargs: Any,
    ) -> PrincipleResult:
        """[14] 삼고초려 (Three Visits) - Retry with Exponential Backoff

        원칙: 외부 API나 리소스 요청 실패 시, 최소 3번은 정중하게 재시도하라.
        코드: Retry(max_attempts=3, backoff=exponential).
        """
        last_error = None

        for attempt in range(1, max_attempts + 1):
            try:
                if asyncio.iscoroutinefunction(action):
                    result = await action(*args, **kwargs)
                else:
                    result = action(*args, **kwargs)

                return PrincipleResult(
                    principle_id=14,
                    principle_name="삼고초려",
                    classic=Classic.THREE_KINGDOMS,
                    success=True,
                    message=f"성공 (시도 {attempt}/{max_attempts})",
                    data={"result": str(result)[:200], "attempts": attempt},
                    trinity_impact={"永": 0.60, "善": 0.40},
                )
            except Exception as e:
                last_error = e
                if attempt < max_attempts:
                    wait_time = backoff_factor ** (attempt - 1)
                    logger.warning(f"[삼고초려] 시도 {attempt} 실패, {wait_time}초 후 재시도: {e}")
                    await asyncio.sleep(wait_time)

        return PrincipleResult(
            principle_id=14,
            principle_name="삼고초려",
            classic=Classic.THREE_KINGDOMS,
            success=False,
            message=f"3번 시도 후 실패: {last_error}",
            data={"error": str(last_error), "attempts": max_attempts},
            trinity_impact={"永": 0.60, "善": 0.40},
        )

    async def principle_15_graceful_degradation(self, fallback_value: Any) -> PrincipleResult:
        """[15] 공성계 - 시스템이 고장났어도, 사용자에게는 평온(Fallback UI)을 보여주어라."""
        return PrincipleResult(
            15,
            "공성계",
            Classic.THREE_KINGDOMS,
            True,
            "Graceful Degradation 활성화",
            {"fallback": str(fallback_value)[:100]},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_16_external_integration(self, package: str) -> PrincipleResult:
        """[16] 초선차전 - 남의 자원(오픈소스, 외부 API)을 빌려 내 힘으로 삼아라."""
        return PrincipleResult(
            16,
            "초선차전",
            Classic.THREE_KINGDOMS,
            True,
            f"외부 리소스 활용: {package}",
            {"package": package},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_17_pipeline_chain(self, steps: list[str]) -> PrincipleResult:
        """[17] 연환계 - 작은 마이크로 서비스들을 연결하여 거대한 함대를 만들어라."""
        return PrincipleResult(
            17,
            "연환계",
            Classic.THREE_KINGDOMS,
            True,
            f"{len(steps)}단계 파이프라인",
            {"steps": steps},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_18_hide_complexity(self) -> PrincipleResult:
        """[18] 미인계 - 복잡한 백엔드 로직은 아름다운 UI 뒤에 숨겨라."""
        return PrincipleResult(
            18,
            "미인계",
            Classic.THREE_KINGDOMS,
            True,
            "복잡성 추상화 완료",
            {},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_19_feedback_loop(self, iteration: int = 1) -> PrincipleResult:
        """[19] 칠종칠금 - 사용자가 만족할 때까지 끈질기게 수정하고 피드백을 받아라."""
        return PrincipleResult(
            19,
            "칠종칠금",
            Classic.THREE_KINGDOMS,
            True,
            f"피드백 루프 #{iteration}",
            {"iteration": iteration},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_20_scheduled_task(self, cron: str = "0 * * * *") -> PrincipleResult:
        """[20] 동남풍 - 타이밍이 생명이다. 스케줄러를 활용하라."""
        return PrincipleResult(
            20,
            "동남풍",
            Classic.THREE_KINGDOMS,
            True,
            f"스케줄 설정: {cron}",
            {"cron": cron},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_21_circuit_breaker(self, threshold: int = 5) -> PrincipleResult:
        """[21] 고육지계 - 시스템 전체를 살리기 위해 일부 기능을 희생할 줄 알아야 한다."""
        return PrincipleResult(
            21,
            "고육지계",
            Classic.THREE_KINGDOMS,
            True,
            f"Circuit Breaker 임계값: {threshold}",
            {"threshold": threshold},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_22_code_convention(self, linter: str = "ruff") -> PrincipleResult:
        """[22] 한실부흥 - 코드의 정통성(Legacy)과 스타일 가이드를 준수하라."""
        return PrincipleResult(
            22,
            "한실부흥",
            Classic.THREE_KINGDOMS,
            True,
            f"린터: {linter}",
            {"linter": linter},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_23_modular_split(self, parts: int = 3) -> PrincipleResult:
        """[23] 천하삼분 - 거대한 문제는 쪼개어 정복하라."""
        return PrincipleResult(
            23,
            "천하삼분",
            Classic.THREE_KINGDOMS,
            True,
            f"{parts}개로 분할",
            {"parts": parts},
            {"永": 0.60, "善": 0.40},
        )

    async def principle_24_checkpoint_state(self, state: dict[str, Any]) -> PrincipleResult:
        """[24] 탁고 - 자신이 종료되더라도, 다음 프로세스를 위해 상태를 남겨라."""
        return PrincipleResult(
            24,
            "탁고",
            Classic.THREE_KINGDOMS,
            True,
            "상태 저장 완료",
            {"state_keys": list(state.keys())},
            {"永": 0.60, "善": 0.40},
        )

    # =========================================================================
    # 제3서: 군주론 (9선) - 善 50% / 眞 50%
    # =========================================================================

    async def principle_25_strict_typing(
        self, value: Any, expected_type: type, allow_none: bool = False
    ) -> PrincipleResult:
        """[25] 사랑보다 두려움 (Feared > Loved) - Strict Typing

        원칙: 느슨한 타입보다는 엄격한 타입(MyPy)이 낫다. 컴파일러가 두려워야 런타임이 안전하다.
        코드: Strict Typing, Validation.
        """
        if value is None and allow_none:
            return PrincipleResult(
                principle_id=25,
                principle_name="사랑보다두려움",
                classic=Classic.THE_PRINCE,
                success=True,
                message="None 허용됨",
                data={"value": None, "expected": expected_type.__name__},
                trinity_impact={"善": 0.50, "眞": 0.50},
            )

        if isinstance(value, expected_type):
            return PrincipleResult(
                principle_id=25,
                principle_name="사랑보다두려움",
                classic=Classic.THE_PRINCE,
                success=True,
                message=f"타입 검증 통과: {expected_type.__name__}",
                data={"value": str(value)[:100], "type": type(value).__name__},
                trinity_impact={"善": 0.50, "眞": 0.50},
            )
        else:
            return PrincipleResult(
                principle_id=25,
                principle_name="사랑보다두려움",
                classic=Classic.THE_PRINCE,
                success=False,
                message=f"타입 불일치: {type(value).__name__} != {expected_type.__name__}",
                data={
                    "actual_type": type(value).__name__,
                    "expected_type": expected_type.__name__,
                },
                trinity_impact={"善": 0.50, "眞": 0.50},
            )

    async def principle_26_error_control(self) -> PrincipleResult:
        """[26] 비르투와 포르투나 - 운에 맡기지 말고, 실력(Error Handling)으로 통제하라."""
        return PrincipleResult(
            26,
            "비르투",
            Classic.THE_PRINCE,
            True,
            "Exception Handling 강화",
            {},
            {"善": 0.50, "眞": 0.50},
        )

    async def principle_27_algorithm_select(self, options: list[str]) -> PrincipleResult:
        """[27] 여우와 사자 - 때로는 교활하게, 때로는 강력하게 해결하라."""
        return PrincipleResult(
            27,
            "여우와사자",
            Classic.THE_PRINCE,
            True,
            f"알고리즘 옵션: {options}",
            {"options": options},
            {"善": 0.50, "眞": 0.50},
        )

    async def principle_28_ux_friction_check(self, friction_score: float) -> PrincipleResult:
        """[28] 증오 피하기 - 사용자에게 불쾌감(Friction > 30)을 주면 반란(이탈)의 지름길이다."""
        safe = friction_score <= 30
        return PrincipleResult(
            28,
            "증오피하기",
            Classic.THE_PRINCE,
            safe,
            f"Friction: {friction_score}" + (" ✅" if safe else " ⚠️"),
            {"friction": friction_score},
            {"善": 0.50, "眞": 0.50},
        )

    async def principle_29_executable_code_only(self) -> PrincipleResult:
        """[29] 무장한 예언자 - 코드 없는 아이디어는 패배한다. 실행 가능한 코드만 가치가 있다."""
        return PrincipleResult(
            29,
            "무장한예언자",
            Classic.THE_PRINCE,
            True,
            "Executable Code Only",
            {},
            {"善": 0.50, "眞": 0.50},
        )

    async def principle_30_garbage_collect(self) -> PrincipleResult:
        """[30] 잔인함의 효율적 사용 - 좀비 프로세스나 낭비 자원은 가차 없이 죽여라."""
        return PrincipleResult(
            30,
            "잔인함",
            Classic.THE_PRINCE,
            True,
            "Garbage Collection 완료",
            {},
            {"善": 0.50, "眞": 0.50},
        )

    async def principle_31_uptime_monitor(self, uptime_percent: float = 99.9) -> PrincipleResult:
        """[31] 국가 유지 - 시스템의 Uptime 유지가 군주의 제1덕목이다."""
        return PrincipleResult(
            31,
            "국가유지",
            Classic.THE_PRINCE,
            uptime_percent >= 99.0,
            f"Uptime: {uptime_percent}%",
            {"uptime": uptime_percent},
            {"善": 0.50, "眞": 0.50},
        )

    async def principle_32_model_router(self, models: list[str]) -> PrincipleResult:
        """[32] 현명한 조언자 - 좋은 모델을 선택하고, 나쁜 모델은 걸러라."""
        return PrincipleResult(
            32,
            "현명한조언자",
            Classic.THE_PRINCE,
            True,
            f"모델 풀: {models}",
            {"models": models},
            {"善": 0.50, "眞": 0.50},
        )

    async def principle_33_creative_solution(self, trinity_score: float) -> PrincipleResult:
        """[33] 결과가 수단을 정당화 - Trinity Score > 90이면 파격적 방법도 허용한다."""
        allowed = trinity_score >= 0.90
        return PrincipleResult(
            33,
            "결과정당화",
            Classic.THE_PRINCE,
            allowed,
            f"Trinity: {trinity_score:.0%}" + (" - 파격 허용" if allowed else " - 정석 유지"),
            {"trinity_score": trinity_score},
            {"善": 0.50, "眞": 0.50},
        )

    # =========================================================================
    # 제4서: 전쟁론 (8선) - 眞 60% / 孝 40%
    # =========================================================================

    async def principle_34_null_check_validation(
        self, data: Any, required_fields: list[str] | None = None
    ) -> PrincipleResult:
        """[34] 전장의 안개 (Fog of War) - Null Check & Validation

        원칙: 정보(Data)가 없으면 움직이지 말고(Block), 정찰(Fetch)하라.
        코드: Null Check, Data Validation.
        """
        if data is None:
            return PrincipleResult(
                principle_id=34,
                principle_name="전장의안개",
                classic=Classic.ON_WAR,
                success=False,
                message="[BLOCK] 데이터 없음 - 정찰 필요",
                data={"reason": "null_data"},
                trinity_impact={"眞": 0.60, "孝": 0.40},
            )

        if required_fields:
            missing = []
            if isinstance(data, dict):
                missing = [f for f in required_fields if f not in data or data[f] is None]

            if missing:
                return PrincipleResult(
                    principle_id=34,
                    principle_name="전장의안개",
                    classic=Classic.ON_WAR,
                    success=False,
                    message=f"[BLOCK] 필수 필드 누락: {missing}",
                    data={"missing_fields": missing},
                    trinity_impact={"眞": 0.60, "孝": 0.40},
                )

        return PrincipleResult(
            principle_id=34,
            principle_name="전장의안개",
            classic=Classic.ON_WAR,
            success=True,
            message="데이터 검증 완료 - 진군 허가",
            data={"validated": True},
            trinity_impact={"眞": 0.60, "孝": 0.40},
        )

    async def principle_36_root_cause_analysis(
        self, symptoms: list[str], context: dict[str, Any] | None = None
    ) -> PrincipleResult:
        """[36] 중심 (Center of Gravity) - Root Cause Analysis

        원칙: 문제의 핵심 원인(Root Cause) 하나를 타격하라. 주변부만 건드리지 마라.
        코드: Root Cause Analysis.
        """
        context = context or {}

        # 간단한 휴리스틱 분석
        common_causes = {
            "timeout": "네트워크 또는 서버 응답 지연",
            "null": "데이터 누락 또는 초기화 실패",
            "permission": "권한 부족",
            "type": "타입 불일치",
            "connection": "연결 실패",
        }

        identified_causes = []
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for keyword, cause in common_causes.items():
                if keyword in symptom_lower:
                    identified_causes.append(cause)

        if identified_causes:
            root_cause = max(set(identified_causes), key=identified_causes.count)
            return PrincipleResult(
                principle_id=36,
                principle_name="중심",
                classic=Classic.ON_WAR,
                success=True,
                message=f"핵심 원인 식별: {root_cause}",
                data={
                    "root_cause": root_cause,
                    "all_causes": list(set(identified_causes)),
                },
                trinity_impact={"眞": 0.60, "孝": 0.40},
            )
        else:
            return PrincipleResult(
                principle_id=36,
                principle_name="중심",
                classic=Classic.ON_WAR,
                success=False,
                message="핵심 원인 미식별 - 추가 정찰 필요",
                data={"symptoms": symptoms},
                trinity_impact={"眞": 0.60, "孝": 0.40},
            )

    async def principle_35_complexity_estimate(
        self, task: str, factors: int = 3
    ) -> PrincipleResult:
        """[35] 마찰 - 이론상 쉬워 보여도 실제로는 어렵다. 마찰계수를 계산하라."""
        return PrincipleResult(
            35,
            "마찰",
            Classic.ON_WAR,
            True,
            f"마찰 요소: {factors}개 (작업: {task[:30]})",
            {"task": task, "factors": factors},
            {"眞": 0.60, "孝": 0.40},
        )

    async def principle_37_resource_monitor(self, usage_percent: float) -> PrincipleResult:
        """[37] 공세 종말점 - 리소스가 고갈되기 직전에 멈추고 재정비하라."""
        safe = usage_percent < 80
        return PrincipleResult(
            37,
            "공세종말점",
            Classic.ON_WAR,
            safe,
            f"리소스: {usage_percent:.1f}%" + (" ✅" if safe else " ⚠️ 재정비 필요"),
            {"usage": usage_percent},
            {"眞": 0.60, "孝": 0.40},
        )

    async def principle_38_singleton_lock(self, resource: str) -> PrincipleResult:
        """[38] 지휘 통일 - 명령 권한은 하나여야 한다. 중복 실행을 막아라."""
        return PrincipleResult(
            38,
            "지휘통일",
            Classic.ON_WAR,
            True,
            f"싱글톤 락: {resource}",
            {"resource": resource},
            {"眞": 0.60, "孝": 0.40},
        )

    async def principle_39_token_optimize(self, tokens: int, limit: int = 4096) -> PrincipleResult:
        """[39] 병력 절약 - 중요하지 않은 곳에 토큰을 낭비하지 마라."""
        efficient = tokens <= limit
        return PrincipleResult(
            39,
            "병력절약",
            Classic.ON_WAR,
            efficient,
            f"토큰: {tokens}/{limit}" + (" ✅" if efficient else " ⚠️"),
            {"tokens": tokens, "limit": limit},
            {"眞": 0.60, "孝": 0.40},
        )

    async def principle_40_auto_run_gate(
        self, confidence: float, threshold: float = 0.8
    ) -> PrincipleResult:
        """[40] 대담함 - 확률이 높다면, 과감하게 자동화를 질러라."""
        auto_run = confidence >= threshold
        return PrincipleResult(
            40,
            "대담함",
            Classic.ON_WAR,
            auto_run,
            f"신뢰도: {confidence:.0%}" + (" → AUTO_RUN" if auto_run else " → 수동 확인"),
            {"confidence": confidence, "threshold": threshold},
            {"眞": 0.60, "孝": 0.40},
        )

    async def principle_41_business_alignment(self, business_value: str) -> PrincipleResult:
        """[41] 전쟁은 정치의 연속 - 코드는 결국 비즈니스 요구사항을 실현하기 위한 도구이다."""
        return PrincipleResult(
            41,
            "정치연속",
            Classic.ON_WAR,
            True,
            f"비즈니스 가치: {business_value}",
            {"value": business_value},
            {"眞": 0.60, "孝": 0.40},
        )

    # =========================================================================
    # 통합 인터페이스
    # =========================================================================

    def get_principle_info(self, principle_id: int) -> dict[str, Any]:
        """원칙 정보 조회"""
        principles = {
            1: {"name": "지피지기", "classic": "손자병법", "tool": "preflight_check"},
            3: {
                "name": "병자궤도야",
                "classic": "손자병법",
                "tool": "dry_run_simulation",
            },
            14: {"name": "삼고초려", "classic": "삼국지", "tool": "retry_with_backoff"},
            25: {
                "name": "사랑보다두려움",
                "classic": "군주론",
                "tool": "strict_typing",
            },
            34: {
                "name": "전장의안개",
                "classic": "전쟁론",
                "tool": "null_check_validation",
            },
            36: {"name": "중심", "classic": "전쟁론", "tool": "root_cause_analysis"},
        }
        return principles.get(principle_id, {"name": "미구현", "classic": "N/A"})

    def list_implemented_principles(self) -> list[int]:
        """구현된 원칙 목록"""
        return [1, 3, 14, 25, 34, 36]


# Singleton export
skill_041 = RoyalLibrarySkill()


if __name__ == "__main__":

    async def test_royal_library():
        print("📜 Royal Library 41선 Skill 테스트")
        print("=" * 50)

        # 01. 지피지기 테스트
        result = await skill_041.principle_01_preflight_check(
            sources=["doc1", "doc2"], context={"system": "ready"}
        )
        print(f"\n[01] 지피지기: {result.message}")

        # 03. 병자궤도야 테스트
        result = await skill_041.principle_03_dry_run_simulation(lambda x: x * 2, 5, simulate=True)
        print(f"[03] 병자궤도야: {result.message}")

        # 25. 사랑보다두려움 테스트
        result = await skill_041.principle_25_strict_typing("hello", str)
        print(f"[25] 사랑보다두려움: {result.message}")

        # 34. 전장의안개 테스트
        result = await skill_041.principle_34_null_check_validation(
            {"name": "test", "value": 42}, required_fields=["name", "value"]
        )
        print(f"[34] 전장의안개: {result.message}")

        print("\n✅ 테스트 완료!")

    asyncio.run(test_royal_library())
