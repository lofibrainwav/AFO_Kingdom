# Redis Operations Guide - AFO Kingdom

## RedisInsight Setup

### Docker 실행 (포트 5540)
```bash
docker run -d --name redisinsight \
  -p 5540:5540 \
  -v redisinsight:/data \
  redis/redisinsight:latest
```

### docker-compose로 실행 (프로필: monitoring)
```bash
docker compose --profile monitoring up redisinsight
```

## Redis Streams - 운영 템플릿

### 기본 이벤트 스트림 (kingdom:logs)
```bash
# 이벤트 추가
redis-cli XADD kingdom:logs * level INFO message "system boot"
redis-cli XADD kingdom:logs * level ERROR message "connection failed"

# 이벤트 조회
redis-cli XRANGE kingdom:logs - + COUNT 50
```

### Consumer Groups (log_processors)
```bash
# 그룹 생성
redis-cli XGROUP CREATE kingdom:logs log_processors 0 MKSTREAM

# 메시지 소비
redis-cli XREADGROUP GROUP log_processors processor1 COUNT 10 BLOCK 5000 STREAMS kingdom:logs >

# 처리 완료 ACK
redis-cli XACK kingdom:logs log_processors <ENTRY_ID>
```

### 고급 운영 - 재처리 및 정리

#### 장애 복구 (XAUTOCLAIM)
```bash
# 죽은 컨슈머의 메시지 회수 (60초 타임아웃)
redis-cli XAUTOCLAIM kingdom:logs log_processors rescuer 60000 0-0 COUNT 50
```

#### 스트림 트리밍 (무한 성장 방지)
```bash
# 최대 100,000개 항목 유지 (근사)
redis-cli XTRIM kingdom:logs MAXLEN ~ 100000
```

#### ACK + 삭제 동시 처리
```bash
redis-cli XACKDEL kingdom:logs log_processors <ENTRY_ID>
```

## 메모리 모니터링

### 큰 키 찾기
```bash
redis-cli --bigkeys
```

### 메모리 사용량 분석
```bash
redis-cli INFO memory
```

## Copilot/AI 프롬프트 템플릿

### 자연어 → Redis 쿼리 변환
- "최근 에러 로그 20개 보여줘" → `redis-cli XRANGE kingdom:logs - + COUNT 20`
- "가장 큰 키들 확인" → `redis-cli --bigkeys`
- "메모리 사용량 분석" → `redis-cli INFO memory`
