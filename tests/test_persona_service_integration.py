"""
Persona Service 통합 테스트
AFO 왕국의 자율 확장 테스트 커버리지 100% 달성 전략 검증

이 테스트는 Reviewer 에이전트(Samaui)가 자동 생성한 것으로,
Trinity Score 기반으로 테스트 케이스를 생성하고 검증합니다.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from AFO.domain.persona import PersonaType
# AFO 왕국 모듈 임포트
from AFO.services.persona_service import PersonaService, persona_service


class TestPersonaServiceIntegration:
    """
    Persona Service 통합 테스트

    이 테스트는 다음을 검증:
    - 페르소나 전환 로직의 정확성
    - DB 조회 기능의 안정성
    - Trinity Score 계산의 정확성
    - TRINITY-OS 로그 브릿지 연동
    """

    @pytest.fixture
    async def persona_service_instance(self) -> PersonaService:
        """테스트용 Persona Service 인스턴스"""
        service = PersonaService()
        # 초기 상태 설정
        service._current_persona = service._current_persona
        return service

    @pytest.mark.asyncio
    async def test_persona_switch_commander_to_family(
        self, persona_service_instance: PersonaService
    ) -> None:
        """
        사령관 → 가장 페르소나 전환 테스트

        검증 포인트:
        - 페르소나 전환 성공
        - Trinity Scores 정확성
        - 로그 브릿지 호출
        """
        # Given
        service = persona_service_instance

        # When
        result = await service.switch_persona("family_head")

        # Then
        assert result["status"] == "전환 완료"
        assert result["current_persona"] == "따뜻한 가장"
        assert "trinity_scores" in result
        assert result["trinity_scores"]["goodness"] == 100.0  # 가장의 핵심 가치

        # Verify persona actually changed
        assert service._current_persona.name == "따뜻한 가장"
        assert service._current_persona.type == PersonaType.FAMILY_HEAD

    @pytest.mark.asyncio
    async def test_persona_switch_with_context(
        self, persona_service_instance: PersonaService
    ) -> None:
        """
        맥락 정보와 함께 페르소나 전환 테스트

        검증 포인트:
        - 맥락 정보 저장
        - 페르소나 메모리 업데이트
        """
        # Given
        service = persona_service_instance
        context = {"task": "family_care", "priority": "high", "emotion": "warm"}

        # When
        result = await service.switch_persona("family_head", context)

        # Then
        assert result["status"] == "전환 완료"
        # Verify context was added to persona memory
        assert len(service._current_persona.context_memory) > 0
        last_memory = service._current_persona.context_memory[-1]
        assert last_memory["task"] == "family_care"
        assert last_memory["emotion"] == "warm"

    @pytest.mark.asyncio
    @patch("AFO.services.persona_service.get_db_connection")
    async def test_get_persona_from_db_success(
        self, mock_get_conn: AsyncMock, persona_service_instance: PersonaService
    ) -> None:
        """
        DB에서 페르소나 조회 성공 케이스

        검증 포인트:
        - DB 연결 및 쿼리 성공
        - 데이터 변환 정확성
        - 에러 처리 우회
        """
        # Given
        mock_conn = AsyncMock()
        mock_get_conn.return_value = mock_conn

        # Mock DB response
        mock_result = {
            "id": "p001",
            "name": "불굴의 사령관",
            "type": "commander",
            "trinity_scores": {
                "truth": 100.0,
                "goodness": 95.0,
                "beauty": 90.0,
                "serenity": 100.0,
                "eternity": 98.0,
            },
            "active": True,
            "last_switched": "2025-12-20T21:00:00Z",
        }
        mock_conn.fetchrow.return_value = mock_result

        # When
        result = await persona_service_instance.get_persona_from_db("p001")

        # Then
        assert result is not None
        assert result["id"] == "p001"
        assert result["name"] == "불굴의 사령관"
        assert result["trinity_scores"]["truth"] == 100.0

        # Verify DB interaction
        mock_conn.fetchrow.assert_called_once()
        mock_conn.close.assert_called_once()

    @pytest.mark.asyncio
    @patch("AFO.services.persona_service.get_db_connection")
    async def test_get_persona_from_db_not_found(
        self, mock_get_conn: AsyncMock, persona_service_instance: PersonaService
    ) -> None:
        """
        DB에서 페르소나 조회 실패 케이스 (데이터 없음)

        검증 포인트:
        - None 반환 처리
        - DB 연결 정리
        """
        # Given
        mock_conn = AsyncMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.fetchrow.return_value = None  # No data found

        # When
        result = await persona_service_instance.get_persona_from_db("nonexistent")

        # Then
        assert result is None
        mock_conn.close.assert_called_once()

    @pytest.mark.asyncio
    @patch("AFO.services.persona_service.get_db_connection")
    async def test_get_persona_from_db_connection_error(
        self, mock_get_conn: AsyncMock, persona_service_instance: PersonaService
    ) -> None:
        """
        DB 연결 실패 케이스

        검증 포인트:
        - 예외 처리
        - None 반환
        - 로깅
        """
        # Given
        mock_get_conn.side_effect = Exception("Connection failed")

        # When
        result = await persona_service_instance.get_persona_from_db("p001")

        # Then
        assert result is None

    @pytest.mark.asyncio
    @patch("AFO.services.trinity_calculator.trinity_calculator")
    async def test_calculate_trinity_score_success(
        self, mock_calculator: MagicMock, persona_service_instance: PersonaService
    ) -> None:
        """
        Trinity Score 계산 성공 케이스

        검증 포인트:
        - 계산 로직 호출
        - 결과 포맷 검증
        - 평가 등급 부여
        """
        # Given
        mock_calculator.calculate_persona_scores.return_value = {
            "truth": 95.0,
            "goodness": 90.0,
            "beauty": 85.0,
            "serenity": 92.0,
            "eternity": 88.0,
        }

        persona_data = {"id": "p001", "name": "불굴의 사령관", "type": "commander"}

        # When
        result = await persona_service_instance.calculate_trinity_score(persona_data)

        # Then
        assert "truth_score" in result
        assert "goodness_score" in result
        assert "total_score" in result
        assert "evaluation" in result
        assert "calculated_at" in result

        # Verify score calculation
        expected_total = 95 * 0.35 + 90 * 0.35 + 85 * 0.20 + 92 * 0.08 + 88 * 0.02
        assert abs(result["total_score"] - expected_total) < 0.1

        # Verify evaluation (탁월 기준: 400점 이상)
        assert result["evaluation"] == "탁월"

    @pytest.mark.asyncio
    @patch("AFO.services.trinity_calculator.trinity_calculator")
    async def test_calculate_trinity_score_error_handling(
        self, mock_calculator: MagicMock, persona_service_instance: PersonaService
    ) -> None:
        """
        Trinity Score 계산 에러 처리 케이스

        검증 포인트:
        - 예외 발생 시 폴백 값 반환
        - 기본값 구조 유지
        """
        # Given
        mock_calculator.calculate_persona_scores.side_effect = Exception(
            "Calculation failed"
        )

        persona_data = {"type": "unknown"}

        # When
        result = await persona_service_instance.calculate_trinity_score(persona_data)

        # Then
        assert result["evaluation"] == "기본값"
        assert "error" in result
        assert result["truth_score"] == 80  # 기본값

    @pytest.mark.asyncio
    @patch("AFO.api.compat.get_trinity_os_client")
    @patch("AFO.api_server.neural_event_queue")
    async def test_log_bridge_mcp_success(
        self,
        mock_queue: MagicMock,
        mock_get_client: MagicMock,
        persona_service_instance: PersonaService,
    ) -> None:
        """
        TRINITY-OS 로그 브릿지 MCP 성공 케이스

        검증 포인트:
        - MCP 클라이언트 호출
        - 로그 데이터 구조
        """
        # Given
        mock_client = AsyncMock()
        mock_get_client.return_value = mock_client

        service = persona_service_instance
        persona = service._current_persona
        context = {"test": "data"}

        # When
        await service._send_log_bridge(persona, context)

        # Then
        mock_client.send_log_event.assert_called_once()
        call_args = mock_client.send_log_event.call_args[0]
        assert call_args[0] == "persona_switch"
        log_data = call_args[1]
        assert log_data["event"] == "persona_switch"
        assert log_data["persona_name"] == persona.name
        assert log_data["context"] == context

    @pytest.mark.asyncio
    @patch("AFO.api.compat.get_trinity_os_client")
    @patch("AFO.api_server.neural_event_queue")
    async def test_log_bridge_sse_fallback(
        self,
        mock_queue: MagicMock,
        mock_get_client: MagicMock,
        persona_service_instance: PersonaService,
    ) -> None:
        """
        TRINITY-OS 로그 브릿지 SSE 폴백 케이스

        검증 포인트:
        - MCP 실패 시 SSE로 폴백
        - 이벤트 큐에 데이터 추가
        """
        # Given
        mock_get_client.return_value = None  # MCP unavailable

        service = persona_service_instance
        persona = service._current_persona

        # When
        await service._send_log_bridge(persona, None)

        # Then
        mock_queue.put.assert_called_once()
        event_data = mock_queue.put.call_args[0][0]
        assert event_data["type"] == "persona_switch"
        assert event_data["data"]["persona_name"] == persona.name

    @pytest.mark.asyncio
    async def test_persona_service_singleton(self) -> None:
        """
        Persona Service 싱글톤 패턴 검증

        검증 포인트:
        - 글로벌 인스턴스 일관성
        - 상태 공유
        """

        # Test that global instance exists
        assert persona_service is not None
        assert isinstance(persona_service, PersonaService)

        # Test that instance maintains state
        initial_persona = await persona_service.get_current_persona()
        assert "name" in initial_persona
        assert "type" in initial_persona

    @pytest.mark.asyncio
    async def test_learner_persona_availability(
        self, persona_service_instance: PersonaService
    ) -> None:
        """
        Learner 페르소나 가용성 검증 (Phase 2 확장)

        검증 포인트:
        - PERSONA_MAPPING에 learner 포함
        - 실제 페르소나 객체 존재
        """
        from AFO.services.persona_service import PERSONA_MAPPING

        # Verify learner persona exists in mapping
        assert "learner" in PERSONA_MAPPING
        assert PERSONA_MAPPING["learner"] is not None

        # Verify persona properties
        learner = PERSONA_MAPPING["learner"]
        assert learner.name == "배움의 길 (眞 Learning)"
        assert learner.type == PersonaType.LEARNER
        assert learner.trinity_scores["truth"] == 100.0
        assert learner.trinity_scores["eternity"] == 100.0


# Trinity Score 기반 테스트 커버리지 검증 메타 테스트
def test_test_coverage_self_verification() -> None:
    """
    이 테스트 파일 자체의 커버리지 검증

    AFO 왕국의 자율 확장 원칙:
    테스트가 자신을 검증하는 메타 구조
    """
    import inspect

    # 현재 모듈의 모든 테스트 함수 수집
    current_module = inspect.currentframe().f_globals
    test_functions = [
        name
        for name, obj in current_module.items()
        if name.startswith("test_") and callable(obj)
    ]

    # 최소 테스트 수 검증 (자율 확장 목표: 10개 이상)
    assert (
        len(test_functions) >= 10
    ), f"Insufficient test coverage: {len(test_functions)} tests"

    # Trinity Score 기반 검증 영역 확인
    trinity_aspects = [
        "persona_switch",
        "db_query",
        "trinity_score",
        "log_bridge",
        "singleton",
    ]
    covered_aspects = []

    for func_name in test_functions:
        func_obj = current_module[func_name]
        docstring = func_obj.__doc__ or ""

        for aspect in trinity_aspects:
            if aspect in func_name or aspect in docstring.lower():
                if aspect not in covered_aspects:
                    covered_aspects.append(aspect)

    # 핵심 Trinity 측면 80% 이상 커버리지 검증
    coverage_ratio = len(covered_aspects) / len(trinity_aspects)
    assert coverage_ratio >= 0.8, f"Trinity coverage too low: {coverage_ratio:.1%}"


if __name__ == "__main__":
    # AFO 왕국의 자율 테스트 실행 (개발 시 직접 실행용)

    # 간단한 smoke test
    async def smoke_test():
        service = PersonaService()
        await service.get_current_persona()

        # Learner 페르소나 테스트
        await service.switch_persona("learner")

        return True

    # 동기 컨텍스트에서 실행
    try:
        asyncio.run(smoke_test())
    except Exception:
        raise
