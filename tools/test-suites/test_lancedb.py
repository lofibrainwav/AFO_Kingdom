#!/usr/bin/env python3
"""
LanceDB 테스트 스크립트 - AFO Kingdom용
眞善美孝永 - 최소 변경으로 최대 호환성 검증
"""

import os
import sys

# LanceDB import (optional)
try:
    import lancedb

    LANCEDB_AVAILABLE = True
    print("✅ LanceDB 라이브러리 사용 가능")
except ImportError:
    LANCEDB_AVAILABLE = False
    print("❌ LanceDB 라이브러리 미설치")


def test_lancedb_basic():
    """LanceDB 기본 기능 테스트"""
    if not LANCEDB_AVAILABLE:
        print("❌ LanceDB 미설치로 테스트 생략")
        return False

    try:
        # 데이터베이스 생성
        db_path = "./data/lancedb"
        os.makedirs(db_path, exist_ok=True)

        db = lancedb.connect(db_path)
        print(f"✅ LanceDB 데이터베이스 연결: {db_path}")

        # 테이블 생성 및 데이터 삽입
        table_name = "test_afokingdom"

        # 기존 테이블이 있으면 삭제
        if table_name in db.table_names():
            db.drop_table(table_name)
            print(f"  기존 테이블 삭제: {table_name}")

        # PyArrow 스키마 사용 (LanceDB 요구사항)
        import pyarrow as pa

        schema = pa.schema(
            [
                ("id", pa.string()),
                ("content", pa.string()),
                ("source", pa.string()),
                ("vector", pa.list_(pa.float32(), 1536)),  # 고정 크기 벡터
            ]
        )

        table = db.create_table(table_name, schema=schema)
        print(f"✅ 테이블 생성: {table_name}")

        # 테스트 데이터 삽입
        test_data = [
            {
                "id": "doc1",
                "content": "AFO Kingdom is an AI operating system.",
                "vector": [0.1] * 1536,  # 더미 벡터
            },
            {
                "id": "doc2",
                "content": "LanceDB provides fast vector search.",
                "vector": [0.2] * 1536,  # 더미 벡터
            },
        ]

        table.add(test_data)
        print(f"✅ 테스트 데이터 삽입: {len(test_data)}개 문서")

        # 검색 테스트
        query_vector = [0.15] * 1536
        results = table.search(query_vector).limit(2).to_list()
        print(f"✅ 벡터 검색 성공: {len(results)}개 결과")

        # 결과 출력
        for i, result in enumerate(results):
            print(f"  결과 {i+1}: ID={result['id']}, 내용={result['content'][:50]}...")

        return True

    except Exception as e:
        print(f"❌ LanceDB 테스트 실패: {e}")
        return False


def test_vector_store_adapter():
    """벡터 스토어 어댑터 테스트"""
    try:
        sys.path.append("packages/afo-core")
        from utils.vector_store import get_vector_store

        store = get_vector_store()
        print(f"✅ 벡터 스토어 어댑터 생성: {type(store).__name__}")

        # 기본 검색 테스트
        test_embedding = [0.1] * 1536
        results = store.search(test_embedding, 2)
        print(f"✅ 어댑터 검색 테스트: {len(results)}개 결과")

        return True

    except Exception as e:
        print(f"❌ 벡터 스토어 어댑터 테스트 실패: {e}")
        return False


if __name__ == "__main__":
    print("🏰 AFO Kingdom LanceDB 테스트 시작\n")

    # 환경변수 확인
    vector_db = os.getenv("VECTOR_DB", "qdrant")
    print(f"환경변수 VECTOR_DB: {vector_db}")

    # LanceDB 기본 테스트
    print("\n1. LanceDB 기본 기능 테스트")
    lancedb_ok = test_lancedb_basic()

    # 어댑터 테스트
    print("\n2. 벡터 스토어 어댑터 테스트")
    adapter_ok = test_vector_store_adapter()

    # 결과 요약
    print("\n📊 테스트 결과 요약")
    print(f"  LanceDB 라이브러리: {'✅' if LANCEDB_AVAILABLE else '❌'}")
    print(f"  LanceDB 기능: {'✅' if lancedb_ok else '❌'}")
    print(f"  어댑터 통합: {'✅' if adapter_ok else '❌'}")

    if lancedb_ok and adapter_ok:
        print("\n🎉 LanceDB 도입 준비 완료!")
        print("   이제 환경변수 VECTOR_DB=lancedb로 전환 가능")
    else:
        print("\n⚠️  추가 설정 필요")
