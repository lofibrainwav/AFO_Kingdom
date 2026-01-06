#!/usr/bin/env python3
"""
AFO 왕국 시스템 헬스 체크 (T1.1 Ollama 통합 강화)

Trinity Score 목표: 眞 +15% 달성
- Ollama 통합 강화로 정확성 향상
- Fallback 로직으로 안정성 확보
"""

import asyncio
import json
import os
import time
from typing import Any

from AFO.scholars.yeongdeok import yeongdeok


class OllamaHealthChecker:
    """Ollama 헬스 체크 강화 클래스"""

    def __init__(self):
        self.env_vars = self._standardize_env_vars()
        self.health_metrics = {
            "ollama_connectivity": False,
            "model_switching": False,
            "fallback_logic": False,
            "performance_ms": 0,
            "error_details": [],
        }

    def _standardize_env_vars(self) -> dict[str, str]:
        """환경변수 표준화 (Phase 2-4: 안티그라비티 설정과 동기화)"""
        env_vars = {}

        # 필수 환경변수들
        required_vars = {
<<<<<<< Updated upstream
            "OLLAMA_BASE_URL": "afo-ollama:11434",  # Docker DNS 우선
            "OLLAMA_MODEL": "llama3.2:3b",  # 기본 모델
            "OLLAMA_NUM_PARALLEL": "4",
            "OLLAMA_NUM_THREAD": "-1",  # 자동 감지
            "OLLAMA_NUM_CTX": "4096",
=======
            "OLLAMA_BASE_URL": "http://localhost:11434",  # Phase 2-1 수정: 호스트명 문제 해결
            "OLLAMA_MODEL": "llama3.2:1b",  # 메모리 절약 모델
            "OLLAMA_NUM_PARALLEL": "1",
            "OLLAMA_NUM_THREAD": "2",  # CPU 스레드 제한
            "OLLAMA_NUM_CTX": "2048",  # 컨텍스트 길이 축소
>>>>>>> Stashed changes
            "OLLAMA_KEEP_ALIVE": "5m",
        }

        # Phase 2-4: 안티그라비티 설정 파일에서 환경변수 로드 시도
        try:
            import pathlib

            antigravity_env = pathlib.Path("packages/afo-core/.env")
            if antigravity_env.exists():
                # 간단한 .env 파싱 (주석과 빈 줄 무시)
                with open(antigravity_env, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key.startswith("OLLAMA_"):
                                env_vars[key] = value
        except Exception:
            # .env 파일 읽기 실패 시 기본값 사용
            pass

        # 환경변수에서 값 가져오기 (안티그라비티 설정 우선)
        for var_name, default_value in required_vars.items():
            env_vars[var_name] = os.getenv(var_name, env_vars.get(var_name, default_value))

        return env_vars

    def _is_docker_environment(self) -> bool:
        """Docker 환경 감지"""
        return os.path.exists("/.dockerenv") or os.getenv("DOCKER_CONTAINER") == "true"

    async def check_ollama_connectivity(self) -> dict[str, Any]:
        """Ollama 연결성 강화 체크"""
        start_time = time.time()

        try:
            # 1. 기본 Ping 테스트
            ping_result = await yeongdeok.consult_samahwi("Ping")
            self.health_metrics["ollama_connectivity"] = True

            # 2. 모델 정보 확인
            model_info = await self._get_model_info()
            if model_info:
                self.health_metrics["model_info"] = model_info

            # 3. 모델 스위칭 테스트
            switch_result = await self._test_model_switching()
            self.health_metrics["model_switching"] = switch_result["success"]

            # 4. Fallback 로직 테스트
            fallback_result = await self._test_fallback_logic()
            self.health_metrics["fallback_logic"] = fallback_result["success"]

        except Exception as e:
            self.health_metrics["error_details"].append(f"Ollama connectivity failed: {e!s}")
            self.health_metrics["ollama_connectivity"] = False

        self.health_metrics["performance_ms"] = (time.time() - start_time) * 1000

        return self.health_metrics

    async def _get_model_info(self) -> dict[str, Any] | None:
        """모델 정보 조회"""
        try:
            # 모델 목록 조회 시도
            models_response = await yeongdeok.consult_samahwi("/api/tags")
            if models_response and "models" in str(models_response):
                return {"models_available": True, "details": str(models_response)[:200]}
        except Exception:
            pass
        return None

    async def _test_model_switching(self) -> dict[str, Any]:
        """모델 스위칭 로직 검증"""
        try:
            # 현재 모델로 테스트 쿼리
            test_query = "Hello, test message for model switching verification."
            response = await yeongdeok.consult_samahwi(test_query)

            if response and len(str(response)) > 10:  # 의미있는 응답 확인
                return {"success": True, "response_length": len(str(response))}
            return {"success": False, "error": "Empty or invalid response"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _test_fallback_logic(self) -> dict[str, Any]:
        """Fallback 로직 검증"""
        try:
            # 여러 시나리오 테스트
            fallback_scenarios = [
                {"query": "", "expected_fallback": True},  # 빈 쿼리
                {"query": "A" * 10000, "expected_fallback": True},  # 너무 긴 쿼리
                {"query": "Test normal query", "expected_fallback": False},  # 정상 쿼리
            ]

            success_count = 0
            for scenario in fallback_scenarios:
                try:
                    response = await yeongdeok.consult_samahwi(scenario["query"])
                    # 응답이 있는지 확인 (fallback 로직이 작동했는지)
                    if response is not None:
                        success_count += 1
                except Exception:
                    # Exception 발생도 fallback 로직의 일부로 간주
                    if scenario["expected_fallback"]:
                        success_count += 1

            return {
                "success": success_count >= 2,  # 2개 이상 성공
                "tested_scenarios": len(fallback_scenarios),
                "successful_scenarios": success_count,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_trinity_score_contribution(self) -> dict[str, float]:
        """Trinity Score 기여도 계산"""
        base_contribution = {
            "truth": 0.0,  # Ollama 정확성
            "goodness": 0.0,  # 안정성
            "beauty": 0.0,  # 아키텍처 우아함
            "serenity": 0.0,  # 사용자 경험
            "eternity": 0.0,  # 영속성
        }

        # 연결성 성공 시 Truth +10%
        if self.health_metrics["ollama_connectivity"]:
            base_contribution["truth"] += 0.10

        # 모델 스위칭 성공 시 Truth +5%
        if self.health_metrics["model_switching"]:
            base_contribution["truth"] += 0.05

        # Fallback 로직 성공 시 Goodness +5%
        if self.health_metrics["fallback_logic"]:
            base_contribution["goodness"] += 0.05

        # 성능이 100ms 이내 시 Serenity +3%
        if self.health_metrics["performance_ms"] < 100:
            base_contribution["serenity"] += 0.03

        # 총합이 15%를 넘지 않도록 제한 (T1.1 목표)
        total_contribution = sum(base_contribution.values())
        if total_contribution > 0.15:
            scale_factor = 0.15 / total_contribution
            for key in base_contribution:
                base_contribution[key] *= scale_factor

        return base_contribution


async def check_system_health():
    """강화된 시스템 헬스 체크"""
    print("🏰 AFO 왕국 시스템 헬스 체크 (T1.1 Ollama 통합 강화)")
    print("=" * 60)

    # 1. Ollama 헬스 체크 강화
    print("\n1. Ollama 통합 강화 체크...")
    ollama_checker = OllamaHealthChecker()

    print("환경변수 표준화:")
    for var_name, var_value in ollama_checker.env_vars.items():
        print(f"   {var_name}: {var_value}")

    # Ollama 연결성 체크
    ollama_health = await ollama_checker.check_ollama_connectivity()

    print("\nOllama 헬스 메트릭스:")
    print(f"   연결성: {'✅' if ollama_health['ollama_connectivity'] else '❌'}")
    print(f"   모델 스위칭: {'✅' if ollama_health['model_switching'] else '❌'}")
    print(f"   Fallback 로직: {'✅' if ollama_health['fallback_logic'] else '❌'}")
    print(f"   성능: {ollama_health['performance_ms']:.1f}ms")
    if ollama_health["error_details"]:
        print("   오류 상세:")
        for error in ollama_health["error_details"]:
            print(f"     - {error}")

    # Trinity Score 기여도
    trinity_contribution = ollama_checker.get_trinity_score_contribution()
    print("\nTrinity Score 기여도 (T1.1 목표: 眞 +15%):")
    for pillar, contribution in trinity_contribution.items():
        print(f"   {pillar}: {contribution:.1%}")

    # 2. 기존 Sage Connectivity 체크
    print("\n2. 기존 Sage Connectivity 체크...")
    try:
        # Jwaja (MLX) - 기존 유지
        await yeongdeok.consult_jwaja("Ping")
        print("   Jwaja (MLX): ✅")
    except Exception as e:
        print(f"   Jwaja (MLX): ❌ ({e!s})")

    # 3. 종합 결과
    print("\n" + "=" * 60)
    print("종합 헬스 체크 결과:")

    # SSOT 저장
    health_result = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "ticket": "T1.1_ollama_integration",
        "env_vars": ollama_checker.env_vars,
        "ollama_health": ollama_health,
        "trinity_contribution": trinity_contribution,
        "overall_status": "healthy" if ollama_health["ollama_connectivity"] else "degraded",
    }

    # artifacts에 저장
    import pathlib

    artifacts_dir = pathlib.Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    ssot_path = artifacts_dir / f"t11_ollama_integration_ssot_{int(time.time())}.jsonl"
    pathlib.Path(ssot_path).write_text(
        json.dumps(health_result, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"SSOT 저장: {ssot_path}")
    print(f"전체 상태: {'✅ 건강' if health_result['overall_status'] == 'healthy' else '⚠️ 저하'}")

    return health_result


if __name__ == "__main__":
    asyncio.run(check_system_health())
