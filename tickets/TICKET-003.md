# 🎫 TICKET-003: LlamaIndex RAG 파이프라인 구축

**우선순위**: MEDIUM
**상태**: PENDING
**담당**: 인프라팀
**의존성**: TICKET-001
**예상 소요시간**: 3시간

## 🎯 목표 (Goal)

LlamaIndex를 통합하여 왕국 Context7 문서의 효율적인 검색 및 RAG 파이프라인을 구축한다.

## 📋 작업 내용

### 1. LlamaIndex 의존성 추가
```bash
poetry add llama-index
```

### 2. Context7 문서 인덱스 생성
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding

# docs/ 디렉토리에서 Context7 문서 로드
docs = SimpleDirectoryReader("docs/").load_data()
index = VectorStoreIndex.from_documents(docs, embed_model=OpenAIEmbedding())
```

### 3. 검색 인터페이스 구현
```python
retriever = index.as_retriever(similarity_top_k=6)
results = retriever.retrieve("AFO 왕국 철학")
```

### 4. DSPy + LlamaIndex 통합
```python
# MIPROv2 최적화된 RAG에서 검색 결과 활용
context = "\n".join([doc.text for doc in retrieved_docs])
```

## ✅ Acceptance Criteria

- [ ] LlamaIndex 설치 및 설정 완료
- [ ] Context7 문서 인덱싱 성공
- [ ] 검색 기능 동작 확인
- [ ] DSPy 통합 인터페이스 구현
- [ ] 검색 정확도 90% 이상

## 🔒 제약사항

- **LOCKED**: antigravity-seal-2025-12-30 관련 파일 절대 수정 금지
- **성능 우선**: 검색 속도 1초 이내 유지

## 🚨 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|-----------|
| 인덱싱 실패 | 낮음 | 높음 | 문서 포맷 검증 후 재시도 |
| 검색 성능 저하 | 중간 | 중간 | 벡터 DB 최적화 적용 |
| API 비용 증가 | 높음 | 중간 | 로컬 임베딩 모델 고려 |

## 📊 Trinity Score 영향

- **眞 (Truth)**: +3 (정확한 문서 검색)
- **善 (Goodness)**: +2 (효율적 리소스 사용)
- **美 (Beauty)**: +2 (우아한 검색 인터페이스)
- **孝 (Serenity)**: +1 (형님 검색 편의성 향상)
- **永 (Eternity)**: +2 (지속적 지식 관리)

**예상 총점**: 78.3 → 83.3
