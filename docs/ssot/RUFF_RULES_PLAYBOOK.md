# Ruff Rules Playbook (Sejong)

## 한 줄 정의
Ruff는 "빠른 코드 검사기"입니다. 실수(버그)와 정리(스타일)를 잡습니다.

## Gate에서 Ruff가 하는 일
- `ruff check .` 가 0이면 PASS
- 하나라도 걸리면 FAIL (증거 로그를 보고 고칩니다)

## 자주 보는 코드(예시)
- F401: import 했는데 안 씀
- F821: 정의되지 않은 이름 사용
- I001: import 정렬 문제

## 3단계로 고치기 (안전 우선)
1) 통계 보기
```bash
ruff check . --statistics
```

2. "고쳐도 안전한 것"부터(선택적으로) 자동 수정

```bash
ruff check . --fix --select F401,I001
```

3. 다시 Gate 실행

```bash
./scripts/ssot_lock_sync_gate.sh
```

## 주의

* 자동 수정은 파일이 바뀝니다. 변경량이 크면 커밋/브랜치로 분리해서 진행합니다.
  EOF