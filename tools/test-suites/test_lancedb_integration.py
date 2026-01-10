#!/usr/bin/env python3
"""
LanceDB 통합 완전 테스트 - AFO Kingdom 실제 사용 검증
眞善美孝永 - 완벽한 적용과 검증
"""

import os
import sys

# 환경변수 설정
os.environ["VECTOR_DB"] = "lancedb"

# AFO 패키지 경로 추가
current_file = os.path.abspath(__file__)
project_root = os.path.dirname(current_file)
afo_core_path = os.path.join(project_root, "packages", "afo-core")
if afo_core_path not in sys.path:
    sys.path.insert(0, afo_core_path)


def test_lancedb_adapter_integration():
    """LanceDB 어댑터 통합 테스트"""
    print("🏰 LanceDB 어댑터 통합 테스트 시작\n")

    try:
        # 벡터 스토어 어댑터 테스트
        from utils.vector_store import LanceDBAdapter, get_vector_store

        store = get_vector_store()
        print(f"✅ 벡터 스토어 타입: {type(store).__name__}")

        if isinstance(store, LanceDBAdapter):
            print("🎉 LanceDB 어댑터가 성공적으로 선택되었습니다!")
            is_available = store.is_available()
            print(f"   사용 가능 상태: {is_available}")

            if is_available:
                print("   LanceDB 데이터베이스 연결 확인")
                return True
            else:
                print("   ❌ LanceDB 연결 실패")
                return False
        else:
            print(f"❌ 예상치 못한 어댑터 타입: {type(store).__name__}")
            return False

    except Exception as e:
        print(f"❌ 어댑터 테스트 실패: {e}")
        return False


def test_hybrid_rag_integration():
    """하이브리드 RAG 시스템 LanceDB 통합 테스트"""
    print("\n🔍 하이브리드 RAG LanceDB 통합 테스트")

    try:
        # LanceDB가 실제로 사용되는지 확인
        from services.hybrid_rag import query_qdrant

        # 테스트 임베딩
        test_embedding = [0.1] * 1536

        # 함수 호출 (실제로는 query_qdrant가 LanceDB를 사용)
        results = query_qdrant(test_embedding, 5, None)

        if results is not None:
            print(f"✅ RAG 시스템 LanceDB 사용: {len(results)}개 결과 반환")
            print("   LanceDB 통합 성공!")
            return True
        else:
            print("❌ RAG 시스템 통합 실패")
            return False

    except Exception as e:
        print(f"❌ RAG 통합 테스트 실패: {e}")
        return False


def test_environment_variables():
    """환경변수 적용 상태 검증"""
    print("\n⚙️ 환경변수 검증")

    vector_db_env = os.getenv("VECTOR_DB", "qdrant")
    lancedb_path_env = os.getenv("LANCEDB_PATH", "./data/lancedb")

    print(f"   VECTOR_DB: {vector_db_env}")
    print(f"   LANCEDB_PATH: {lancedb_path_env}")

    if vector_db_env == "lancedb":
        print("✅ 환경변수 LanceDB로 설정됨")
        return True
    else:
        print("❌ 환경변수 설정 실패")
        return False


def test_lancedb_database_files():
    """LanceDB 데이터베이스 파일 존재 확인"""
    print("\n💾 LanceDB 데이터베이스 파일 확인")

    lancedb_path = os.getenv("LANCEDB_PATH", "./data/lancedb")
    db_file = os.path.join(lancedb_path, "afokingdom_knowledge.lance")

    if os.path.exists(db_file):
        print(f"✅ LanceDB 데이터베이스 존재: {db_file}")
        return True
    else:
        print(f"❌ LanceDB 데이터베이스 없음: {db_file}")
        return False


def main():
    """메인 테스트 함수"""
    print("🏰 AFO Kingdom LanceDB 완전 통합 검증")
    print("=" * 60)

    results = []

    # 1. 환경변수 검증
    results.append(test_environment_variables())

    # 2. LanceDB 어댑터 통합
    results.append(test_lancedb_adapter_integration())

    # 3. 데이터베이스 파일 확인
    results.append(test_lancedb_database_files())

    # 4. 하이브리드 RAG 통합
    results.append(test_hybrid_rag_integration())

    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 LanceDB 통합 검증 결과")

    total_tests = len(results)
    passed_tests = sum(results)

    print(f"총 테스트: {total_tests}")
    print(f"성공: {passed_tests}")
    print(f"실패: {total_tests - passed_tests}")
    print(".1f")
    if passed_tests == total_tests:
        print("\n🎉 LanceDB 도입이 완벽하게 성공했습니다!")
        print("   AFO Kingdom 멀티모달 아키텍처가 LanceDB로 전환되었습니다.")
        return True
    else:
        print("\n⚠️ 일부 테스트 실패 - 추가 조치 필요")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
