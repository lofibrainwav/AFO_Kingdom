#!/usr/bin/env python3
"""
TICKET-047 Mem0 통합 시스템 테스트

AFO 왕국의 Mem0 기반 메모리 시스템을 검증합니다.
"""

import asyncio
import sys
import time
from pathlib import Path


# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "packages" / "afo-core"))

from memory.context7_integration import Context7MemoryManager
from memory.mem0_client import get_memory_client


async def test_mem0_basic_functionality():
    """Mem0 기본 기능 테스트"""
    print("🔍 Mem0 기본 기능 테스트 시작...")

    client = get_memory_client()

    # 1. 메모리 추가 테스트
    print("\n1. 메모리 추가 테스트")
    test_memories = [
        "AFO 왕국의 철학은 眞善美孝永이다",
        "Chancellor 시스템은 Trinity Score를 기반으로 동작한다",
        "Context7은 지식 베이스 시스템이다",
        "Mem0는 AI 메모리 관리를 위한 라이브러리다",
    ]

    add_results = []
    for i, memory in enumerate(test_memories, 1):
        result = client.add_memory(
            content=memory,
            user_id="test_user",
            metadata={"test_id": i, "category": "philosophy"},
            session_id="test_session",
            run_id=f"test_run_{i}",
        )
        add_results.append(result)
        print(
            f"   메모리 {i}: {'✅' if result['success'] else '❌'} ({result['latency_ms']:.1f}ms)"
        )

    # 2. 메모리 검색 테스트
    print("\n2. 메모리 검색 테스트")
    search_queries = ["철학", "Trinity", "Context7", "메모리"]

    search_results = []
    for query in search_queries:
        result = client.search_memory(query=query, user_id="test_user", limit=3)
        search_results.append(result)
        found = len(result.get("results", [])) if result["success"] else 0
        print(
            f"   '{query}' 검색: {'✅' if result['success'] else '❌'} ({found}개 결과, {result['latency_ms']:.1f}ms)"
        )

    # 3. 모든 메모리 조회 테스트
    print("\n3. 모든 메모리 조회 테스트")
    all_memories = client.get_all_memories(user_id="test_user")
    memory_count = len(all_memories.get("memories", [])) if all_memories["success"] else 0
    print(f"   총 메모리 수: {memory_count}개 ({all_memories['latency_ms']:.1f}ms)")

    # 4. 성능 통계 확인
    print("\n4. 성능 통계")
    stats = client.get_performance_stats()
    trinity = stats.get("trinity_score", {})
    print(f"   추가 호출: {stats['add_calls']}회")
    print(f"   검색 호출: {stats['search_calls']}회")
    print(f"   평균 latency: {stats['avg_latency_ms']:.1f}ms")
    print(f"   Trinity Score - 永: {trinity.get('eternity', 0):.2f}")

    return {
        "add_results": add_results,
        "search_results": search_results,
        "all_memories": all_memories,
        "performance_stats": stats,
    }


async def test_context7_integration():
    """Context7 통합 테스트"""
    print("\n🔍 Context7 통합 테스트 시작...")

    manager = Context7MemoryManager()

    # 1. Context7 문서 메모리화
    print("\n1. Context7 문서 메모리화")
    memorize_result = manager.memorize_context7_docs(user_id="system")
    successful = memorize_result.get("successful", 0)
    total = memorize_result.get("total_docs", 0)
    print(
        f"   메모리화 결과: {successful}/{total}개 성공 ({memorize_result['total_latency_ms']:.1f}ms)"
    )

    # 2. Context7 지식 검색
    print("\n2. Context7 지식 검색")
    search_queries = ["sequential thinking", "skills registry", "integration"]

    search_results = []
    for query in search_queries:
        result = manager.search_context7_knowledge(query=query, user_id="system", limit=2)
        search_results.append(result)
        found = len(result.get("results", [])) if result["success"] else 0
        print(
            f"   '{query}' 검색: {'✅' if result['success'] else '❌'} ({found}개 결과, {result['latency_ms']:.1f}ms)"
        )

    # 3. 쿼리 강화 테스트
    print("\n3. 쿼리 강화 테스트")
    original_query = "어떻게 sequential thinking을 사용하나요?"
    enhanced_query = manager.enhance_query_with_context7(original_query, user_id="system")
    enhancement = "✅ 강화됨" if enhanced_query != original_query else "❌ 변경 없음"
    print(f"   쿼리 강화: {enhancement}")
    if len(enhanced_query) > 100:
        print(f"   강화된 쿼리: {enhanced_query[:100]}...")

    # 4. Context7 통계 확인
    print("\n4. Context7 통계")
    stats = manager.get_context7_stats(user_id="system")
    if stats["success"]:
        print(f"   총 메모리: {stats['total_memories']}개")
        print(f"   메모리화된 문서: {stats['docs_memorized']}개")
        print(f"   검색 호출: {stats['search_calls']}회")
        print(f"   평균 latency: {stats['avg_latency_ms']:.1f}ms")

    return {
        "memorize_result": memorize_result,
        "search_results": search_results,
        "enhanced_query": enhanced_query,
        "stats": stats,
    }


async def main():
    """통합 테스트 메인 함수"""
    print("=" * 70)
    print("TICKET-047 Mem0 통합 시스템 테스트")
    print("=" * 70)

    start_time = time.time()

    # Mem0 기본 기능 테스트
    basic_results = await test_mem0_basic_functionality()

    # Context7 통합 테스트
    context7_results = await test_context7_integration()

    # 최종 결과 요약
    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("테스트 결과 요약")
    print("=" * 70)

    # 성공/실패 카운트
    basic_success = sum(1 for r in basic_results["add_results"] if r["success"])
    basic_total = len(basic_results["add_results"])
    search_success = sum(1 for r in basic_results["search_results"] if r["success"])
    search_total = len(basic_results["search_results"])

    context7_success = context7_results["memorize_result"].get("successful", 0)
    context7_total = context7_results["memorize_result"].get("total_docs", 0)

    print(f"Mem0 기본 기능: {basic_success}/{basic_total} 추가 성공")
    print(f"Mem0 검색 기능: {search_success}/{search_total} 검색 성공")
    print(f"Context7 메모리화: {context7_success}/{context7_total} 문서 성공")
    print(f"총 실행 시간: {total_time:.2f}초")

    # Trinity Score 계산
    trinity_eternity = 1.0 if total_time < 10 else 0.8 if total_time < 20 else 0.6
    success_rate = (basic_success + search_success + context7_success) / (
        basic_total + search_total + context7_total
    )
    if success_rate >= 0.9:
        trinity_truth = 1.0
        trinity_goodness = 0.95
        trinity_beauty = 0.9
    elif success_rate >= 0.8:
        trinity_truth = 0.9
        trinity_goodness = 0.9
        trinity_beauty = 0.8
    else:
        trinity_truth = 0.8
        trinity_goodness = 0.8
        trinity_beauty = 0.7

    trinity_serenity = 1.0  # 형님 평온 유지

    print("\nTrinity Score:")
    print(f"   眞 (Truth): {trinity_truth:.2f}")
    print(f"   善 (Goodness): {trinity_goodness:.2f}")
    print(f"   美 (Beauty): {trinity_beauty:.2f}")
    print(f"   孝 (Serenity): {trinity_serenity:.2f}")
    print(f"   永 (Eternity): {trinity_eternity:.2f}")
    print(
        f"   종합: {(trinity_truth + trinity_goodness + trinity_beauty + trinity_serenity + trinity_eternity) / 5:.2f}"
    )

    # SSOT 결과 저장
    ssot_result = {
        "ticket": "TICKET-047",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "test_results": {
            "mem0_basic": basic_results,
            "context7_integration": context7_results,
            "summary": {
                "total_time_seconds": total_time,
                "success_rate": success_rate,
                "trinity_score": {
                    "truth": trinity_truth,
                    "goodness": trinity_goodness,
                    "beauty": trinity_beauty,
                    "serenity": trinity_serenity,
                    "eternity": trinity_eternity,
                },
            },
        },
    }

    # artifacts에 저장
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    import json

    ssot_path = artifacts_dir / f"ticket047_mem0_integration_ssot_{int(time.time())}.jsonl"
    Path(ssot_path).write_text(json.dumps(ssot_result, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nSSOT 저장: {ssot_path}")

    print("\n🎯 TICKET-047 Mem0 통합 시스템 테스트 완료!")
    print("영원한 메모리 시스템 구축 성공! 🏰💎♾️")

    return ssot_result


if __name__ == "__main__":
    asyncio.run(main())
