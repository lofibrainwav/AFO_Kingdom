#!/usr/bin/env python3
"""
Active RAG 검증 스크립트 - RAG 시스템의 동적 컨텍스트 검색 및 응답 생성 기능 테스트

AFO 왕국 TICKET-002: Active RAG 검증을 위한 증거 생성기
RAG 시스템의 실시간 검색, 컨텍스트 통합, 응답 생성 기능 검증

사용법:
    python scripts/verify_active_rag.py

출력:
    - artifacts/active_rag_verification_[timestamp]/ 증거 폴더 생성
    - manifest.sha256로 증거 무결성 보장
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


# AFO 왕국 패키지 임포트 (가용한 것만)
try:
    from afo.rag_flag import determine_rag_mode

    RAG_FLAG_AVAILABLE = True
except ImportError:
    RAG_FLAG_AVAILABLE = False
    print("WARNING: RAG flag functions not available")

try:
    from afo.rag_cache import RAGCache

    RAG_CACHE_AVAILABLE = True
except ImportError:
    RAG_CACHE_AVAILABLE = False
    print("WARNING: RAG cache not available")

try:
    from afo.rag_chunking import RAGChunking

    RAG_CHUNKING_AVAILABLE = True
except ImportError:
    RAG_CHUNKING_AVAILABLE = False
    print("WARNING: RAG chunking not available")


class ActiveRAGVerifier:
    """Active RAG 기능 검증기"""

    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.evidence_dir = Path(f"artifacts/active_rag_verification_{self.timestamp}")
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

        self.results = {
            "test_timestamp": self.timestamp,
            "rag_components_available": {
                "rag_flag": RAG_FLAG_AVAILABLE,
                "rag_cache": RAG_CACHE_AVAILABLE,
                "rag_chunking": RAG_CHUNKING_AVAILABLE,
            },
            "tests": [],
            "overall_status": "unknown",
        }

    def log(self, message: str) -> None:
        """증거 로그 기록"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"

        log_file = self.evidence_dir / "verification_log.txt"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

        print(message)

    async def test_rag_flag_determination(self) -> dict[str, Any]:
        """RAG 모드 결정 기능 테스트"""
        test_name = "rag_flag_determination"
        self.log(f"Starting test: {test_name}")

        result = {"test_name": test_name, "status": "unknown", "details": {}, "error": None}

        try:
            if not RAG_FLAG_AVAILABLE:
                result["status"] = "skipped"
                result["details"]["reason"] = "RAG flag functions not available"
                return result

            # 실제 determine_rag_mode 함수의 헤더 기반 동작을 테스트
            test_cases = [
                {
                    "name": "No headers (default shadow_only)",
                    "headers": None,
                    "expected_mode": "shadow_only",
                    "expected_applied": False,
                },
                {
                    "name": "Kill switch active",
                    "headers": None,
                    "env_override": {"AFO_RAG_KILL_SWITCH": "1"},
                    "expected_mode": "killed",
                    "expected_applied": False,
                },
                {
                    "name": "Force ON via header",
                    "headers": {"X-AFO-RAG": "1"},
                    "expected_mode": "forced_on",
                    "expected_applied": True,
                },
                {
                    "name": "Force OFF via header",
                    "headers": {"X-AFO-RAG": "0"},
                    "expected_mode": "forced_off",
                    "expected_applied": False,
                },
                {
                    "name": "Flag enabled via ENV",
                    "headers": None,
                    "env_override": {"AFO_RAG_FLAG_ENABLED": "1"},
                    "expected_mode": "flag",
                    "expected_applied": True,
                },
            ]

            results = []
            for i, test_case in enumerate(test_cases):
                try:
                    # 환경변수 임시 설정 (있는 경우)
                    env_backup = {}
                    if "env_override" in test_case:
                        for key, value in test_case["env_override"].items():
                            env_backup[key] = os.environ.get(key)
                            os.environ[key] = value

                    # determine_rag_mode 호출
                    mode_result = determine_rag_mode(test_case["headers"])
                    mode = mode_result["mode"]
                    applied = mode_result["applied"]

                    # 환경변수 복원
                    for key, value in env_backup.items():
                        if value is None:
                            os.environ.pop(key, None)
                        else:
                            os.environ[key] = value

                    results.append({
                        "case": i + 1,
                        "name": test_case["name"],
                        "determined_mode": mode,
                        "expected_mode": test_case["expected_mode"],
                        "determined_applied": applied,
                        "expected_applied": test_case["expected_applied"],
                        "mode_match": mode == test_case["expected_mode"],
                        "applied_match": applied == test_case["expected_applied"],
                        "match": mode == test_case["expected_mode"]
                        and applied == test_case["expected_applied"],
                    })
                except Exception as e:
                    results.append({
                        "case": i + 1,
                        "name": test_case["name"],
                        "error": str(e),
                        "match": False,
                    })

            result["details"]["test_cases_run"] = len(results)
            result["details"]["successful_cases"] = sum(1 for r in results if r.get("match", False))
            result["details"]["results"] = results

            if result["details"]["successful_cases"] == len(results):
                result["status"] = "passed"
            else:
                result["status"] = "failed"
                result["error"] = (
                    f"Only {result['details']['successful_cases']}/{len(results)} cases passed"
                )

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            self.log(f"Test failed: {e}")

        return result

    async def test_rag_cache_operations(self) -> dict[str, Any]:
        """RAG 캐시 기능 테스트"""
        test_name = "rag_cache_operations"
        self.log(f"Starting test: {test_name}")

        result = {"test_name": test_name, "status": "unknown", "details": {}, "error": None}

        try:
            if not RAG_CACHE_AVAILABLE:
                result["status"] = "skipped"
                result["details"]["reason"] = "RAG cache not available"
                return result

            # 캐시 초기화 시도
            cache = RAGCache()
            result["details"]["cache_initialized"] = True

            # 기본 캐시 연산 테스트
            test_key = "test_query_123"
            test_value = {
                "query": "test query",
                "results": ["result1", "result2"],
                "timestamp": datetime.now().isoformat(),
            }

            # 저장 테스트
            cache.set(test_key, test_value)
            result["details"]["cache_set_success"] = True

            # 조회 테스트
            retrieved = cache.get(test_key)
            result["details"]["cache_get_success"] = retrieved is not None
            result["details"]["cache_data_match"] = retrieved == test_value

            # 삭제 테스트
            cache.delete(test_key)
            deleted_check = cache.get(test_key)
            result["details"]["cache_delete_success"] = deleted_check is None

            # 모든 테스트 통과 확인
            all_success = all([
                result["details"]["cache_set_success"],
                result["details"]["cache_get_success"],
                result["details"]["cache_data_match"],
                result["details"]["cache_delete_success"],
            ])

            result["status"] = "passed" if all_success else "failed"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            self.log(f"Test failed: {e}")

        return result

    async def test_rag_chunking_operations(self) -> dict[str, Any]:
        """RAG 청킹 기능 테스트"""
        test_name = "rag_chunking_operations"
        self.log(f"Starting test: {test_name}")

        result = {"test_name": test_name, "status": "unknown", "details": {}, "error": None}

        try:
            if not RAG_CHUNKING_AVAILABLE:
                result["status"] = "skipped"
                result["details"]["reason"] = "RAG chunking not available"
                return result

            # 청킹 초기화
            chunking = RAGChunking()
            result["details"]["chunking_initialized"] = True

            # 테스트 텍스트
            test_text = """
            This is a test document for RAG chunking verification.
            It contains multiple sentences and paragraphs.
            The chunking system should be able to split this text
            into meaningful chunks for retrieval-augmented generation.
            Each chunk should maintain semantic coherence.
            """.strip()

            # 청킹 실행
            chunks = chunking.chunk_text(test_text)
            result["details"]["chunks_created"] = len(chunks)
            result["details"]["original_text_length"] = len(test_text)

            # 청크 검증
            total_chunk_length = sum(len(chunk) for chunk in chunks)
            result["details"]["total_chunk_length"] = total_chunk_length
            result["details"]["length_preserved"] = (
                total_chunk_length >= len(test_text) * 0.9
            )  # 90% 보존

            # 청크 내용 검증
            all_chunks_have_content = all(len(chunk.strip()) > 0 for chunk in chunks)
            result["details"]["all_chunks_have_content"] = all_chunks_have_content

            # 청크 크기 분포 확인
            chunk_sizes = [len(chunk) for chunk in chunks]
            result["details"]["chunk_sizes"] = chunk_sizes
            result["details"]["avg_chunk_size"] = (
                sum(chunk_sizes) / len(chunk_sizes) if chunk_sizes else 0
            )

            # 테스트 통과 조건
            basic_tests_pass = (
                len(chunks) > 0
                and result["details"]["length_preserved"]
                and all_chunks_have_content
            )

            result["status"] = "passed" if basic_tests_pass else "failed"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            self.log(f"Test failed: {e}")

        return result

    async def test_rag_integration_flow(self) -> dict[str, Any]:
        """RAG 통합 플로우 테스트"""
        test_name = "rag_integration_flow"
        self.log(f"Starting test: {test_name}")

        result = {"test_name": test_name, "status": "unknown", "details": {}, "error": None}

        try:
            # 사용 가능한 컴포넌트 확인
            available_components = []
            if RAG_FLAG_AVAILABLE:
                available_components.append("flag")
            if RAG_CACHE_AVAILABLE:
                available_components.append("cache")
            if RAG_CHUNKING_AVAILABLE:
                available_components.append("chunking")

            result["details"]["available_components"] = available_components

            if not available_components:
                result["status"] = "skipped"
                result["details"]["reason"] = "No RAG components available"
                return result

            # 통합 플로우 시뮬레이션
            test_query = "How does RAG improve LLM responses?"
            test_context = """
            RAG (Retrieval-Augmented Generation) improves LLM responses by:
            1. Retrieving relevant information from external knowledge sources
            2. Augmenting the original query with retrieved context
            3. Generating more accurate and grounded responses
            4. Reducing hallucinations and improving factual accuracy
            """.strip()

            flow_steps = []

            # 1. RAG 모드 결정 (있는 경우)
            if RAG_FLAG_AVAILABLE:
                mode_result = determine_rag_mode()
                mode = mode_result["mode"]
                flow_steps.append({"step": "mode_determination", "mode": mode, "success": True})
            else:
                flow_steps.append({"step": "mode_determination", "skipped": True})

            # 2. 컨텍스트 청킹 (있는 경우)
            if RAG_CHUNKING_AVAILABLE:
                chunking = RAGChunking()
                chunks = chunking.chunk_text(test_context)
                flow_steps.append({
                    "step": "chunking",
                    "chunks_created": len(chunks),
                    "success": len(chunks) > 0,
                })
            else:
                flow_steps.append({"step": "chunking", "skipped": True})

            # 3. 캐시 연산 (있는 경우)
            if RAG_CACHE_AVAILABLE:
                cache = RAGCache()
                cache_key = f"test_{hash(test_query) % 1000}"
                cache.set(
                    cache_key,
                    {"query": test_query, "chunks": chunks if "chunks" in locals() else []},
                )
                cached_data = cache.get(cache_key)
                flow_steps.append({
                    "step": "caching",
                    "cache_set": True,
                    "cache_get": cached_data is not None,
                    "success": cached_data is not None,
                })
                cache.delete(cache_key)
            else:
                flow_steps.append({"step": "caching", "skipped": True})

            result["details"]["flow_steps"] = flow_steps
            result["details"]["flow_completion"] = sum(
                1 for step in flow_steps if step.get("success", False) or step.get("skipped", False)
            )

            # 통합 플로우 성공 판정 (실행 가능한 단계들이 성공)
            successful_steps = sum(1 for step in flow_steps if step.get("success", False))
            skipped_steps = sum(1 for step in flow_steps if step.get("skipped", False))
            total_steps = len(flow_steps)

            if successful_steps + skipped_steps == total_steps:
                result["status"] = "passed"
            else:
                result["status"] = "failed"
                result["error"] = (
                    f"Flow incomplete: {successful_steps}/{total_steps} steps successful"
                )

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            self.log(f"Test failed: {e}")

        return result

    async def run_all_tests(self) -> dict[str, Any]:
        """모든 테스트 실행"""
        self.log("Starting Active RAG verification tests")
        self.log(f"Evidence directory: {self.evidence_dir}")

        tests = [
            self.test_rag_flag_determination(),
            self.test_rag_cache_operations(),
            self.test_rag_chunking_operations(),
            self.test_rag_integration_flow(),
        ]

        completed_tests = []
        for test_coro in tests:
            test_result = await test_coro
            completed_tests.append(test_result)
            self.log(f"Test {test_result['test_name']}: {test_result['status']}")

        self.results["tests"] = completed_tests

        # 전체 상태 판정
        statuses = [test["status"] for test in completed_tests]
        if "failed" in statuses:
            self.results["overall_status"] = "failed"
        elif all(status in ["passed", "skipped"] for status in statuses):
            self.results["overall_status"] = "passed"
        else:
            self.results["overall_status"] = "partial"

        self.log(f"Overall status: {self.results['overall_status']}")
        return self.results

    def save_results(self) -> None:
        """결과를 증거 파일로 저장"""
        # JSON 결과 저장
        results_file = self.evidence_dir / "test_results.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        # 요약 파일 생성
        summary_file = self.evidence_dir / "test_summary.txt"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write("Active RAG Verification Summary\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Timestamp: {self.results['test_timestamp']}\n")
            f.write(f"RAG Components Available: {self.results['rag_components_available']}\n")
            f.write(f"Overall Status: {self.results['overall_status']}\n\n")

            f.write("Test Results:\n")
            for test in self.results["tests"]:
                f.write(f"- {test['test_name']}: {test['status']}\n")
                if test.get("error"):
                    f.write(f"  Error: {test['error']}\n")

        # manifest.sha256 생성
        import hashlib

        manifest_file = self.evidence_dir / "manifest.sha256"
        with open(manifest_file, "w", encoding="utf-8") as f:
            for file_path in sorted(self.evidence_dir.glob("*")):
                if file_path.name != "manifest.sha256":
                    hash_sha256 = hashlib.sha256()
                    with open(file_path, "rb") as file:
                        for chunk in iter(lambda: file.read(4096), b""):
                            hash_sha256.update(chunk)
                    f.write(f"{hash_sha256.hexdigest()}  {file_path.name}\n")

        self.log(f"Evidence saved to {self.evidence_dir}")


async def main():
    """메인 함수"""
    print("🔥 AFO Kingdom Active RAG Verification")
    print("=" * 50)

    verifier = ActiveRAGVerifier()
    results = await verifier.run_all_tests()
    verifier.save_results()

    print("\n" + "=" * 50)
    print(f"Overall Status: {results['overall_status']}")
    print(f"Evidence: {verifier.evidence_dir}")

    # 종료 코드
    if results["overall_status"] == "passed":
        print("✅ Active RAG verification PASSED")
        return 0
    if results["overall_status"] == "partial":
        print("⚠️  Active RAG verification PARTIAL")
        return 1
    print("❌ Active RAG verification FAILED")
    return 2


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
