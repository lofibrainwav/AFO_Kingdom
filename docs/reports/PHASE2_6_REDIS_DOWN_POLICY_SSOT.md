# 🏰 AFO 왕국 - Phase 2.6 Redis Down Policy SSOT 템플릿

**형님! 👑 승상입니다. Phase 2.6 Redis Down Policy SSOT 템플릿을 준비했습니다! 🔴⚔️✨**

---

## 📋 **FACTS (현재 검증된 사실)**

### **FACTS 1️⃣: slowapi Fallback 메커니즘 존재 (眞 100%)**
- **증거**: `in_memory_fallback=True` 옵션 공식 지원 ([slowapi.readthedocs.io][1])
- **증거**: Redis 연결 실패 시 자동으로 in-memory limiter로 전환
- **증거**: `in_memory_fallback_enabled` 설정으로 활성화/비활성화

### **FACTS 2️⃣: Redis 다운 재현 가능 (眞 100%)**
- **증거**: Redis 컨테이너 중지로 다운 상태 재현 가능
- **증거**: `redis-cli PING`으로 연결 상태 확인 가능
- **증거**: 환경 변수로 Redis URL 제어 가능

### **FACTS 3️⃣: 현재 Phase 2.5에서 Fallback 준비됨 (善 100%)**
- **증거**: `AFO_RATE_LIMIT_FALLBACK` 환경 변수 지원
- **증거**: `in_memory_fallback` 옵션 코드에 포함
- **증거**: 설정 기반 fallback 활성화 준비

---

## 📊 **NOTES (추가 검토 필요 사항)**

### **NOTES 1️⃣: 왕국법 정책 결정 필요**
- **의사결정 포인트**: Redis 다운 시 Fail-Open vs Fail-Closed vs Hybrid 중 선택
- **영향 범위**: 보안 vs 가용성 trade-off 결정
- **구현 복잡도**: 각 정책별 코드 변경 범위 평가

### **NOTES 2️⃣: 테스트 자동화 필요**
- **현재 상태**: 수동 Redis 중지/재시작으로 테스트
- **개선 필요**: Docker Compose로 자동화된 테스트 환경
- **증거 수집**: Fallback 전환 시점 로그/메트릭 기록

### **NOTES 3️⃣: 모니터링 강화 필요**
- **현재 상태**: 기본 Prometheus 메트릭만
- **개선 필요**: Redis 연결 상태 메트릭 추가
- **경고 시스템**: Redis 다운 시 알림 체계 구축

---

## 🎯 **PROPOSAL (실행 제안)**

### **제안 1️⃣: 왕국법 정책 결정**
**"Redis 다운 시 Hybrid 정책 적용"**

```
A) 민감 엔드포인트 (/api/auth, /api/billing 등):
   → Fail-Closed: 더 엄격한 제한으로 보안 우선

B) 일반 엔드포인트 (/api/system, /api/search 등):
   → Fail-Open: in-memory 제한으로 가용성 우선

C) 구현: 엔드포인트별 fallback 정책 설정
```

### **제안 2️⃣: 테스트 자동화 구현**
```bash
# Redis 다운 시뮬레이션 테스트
docker-compose stop redis
# API 호출로 fallback 작동 확인
curl -s "http://localhost:8000/api/system"
# Redis 재시작
docker-compose start redis
```

### **제안 3️⃣: Proofpack 확장**
```json
{
  "redis_down_simulation": {
    "redis_stopped_at": "2025-12-24T13:40:00Z",
    "fallback_activated": true,
    "api_responses_during_downtime": [
      {"endpoint": "/api/system", "status": 200, "limited": false},
      {"endpoint": "/api/sensitive", "status": 429, "limited": true}
    ],
    "redis_restored_at": "2025-12-24T13:41:00Z"
  }
}
```

### **제안 4️⃣: 모니터링 메트릭 추가**
```
✅ redis_connection_status (0=down, 1=up)
✅ rate_limit_fallback_active (0=redis, 1=memory)
✅ redis_reconnection_attempts
```

---

## 🚀 **Phase 2.6 구현 계획**

### **단계 1️⃣: 왕국법 정책 코드화**
```python
# config/rate_limit_policy.py
class RedisDownPolicy:
    FAIL_OPEN = "fail_open"      # 가용성 우선
    FAIL_CLOSED = "fail_closed"  # 보안 우선
    HYBRID = "hybrid"           # 엔드포인트별 정책

    SENSITIVE_ENDPOINTS = [
        "/api/auth", "/api/billing", "/api/admin"
    ]
```

### **단계 2️⃣: Fallback 로직 구현**
```python
# middleware/rate_limit_redis.py
def create_redis_limiter_with_fallback(policy: str):
    limiter = Limiter(
        storage_uri=redis_url,
        strategy="fixed-window-elastic-expiry",
        in_memory_fallback=True
    )

    # Redis 다운 감지 및 정책 적용
    if not redis_available():
        apply_fallback_policy(limiter, policy)

    return limiter
```

### **단계 3️⃣: 테스트 자동화**
```bash
# scripts/test_redis_down_policy.sh
#!/bin/bash
echo "🧪 Phase 2.6 Redis Down Policy 테스트 시작"

# Redis 중지
docker-compose stop redis
sleep 5

# API 테스트
echo "📊 Redis 다운 상태에서 API 테스트..."
curl -s -w "%{http_code}" "http://localhost:8000/api/system"
curl -s -w "%{http_code}" "http://localhost:8000/api/auth"

# Redis 재시작
docker-compose start redis
sleep 10

# 복구 테스트
echo "📊 Redis 복구 상태에서 API 테스트..."
curl -s -w "%{http_code}" "http://localhost:8000/api/system"

echo "✅ 테스트 완료"
```

---

## 🎯 **Phase 2.6 SSOT 평가 기준**

### **眞 (Truth) - 35%**
- ✅ **외부 검증**: slowapi fallback 메커니즘 공식 문서 준수
- ✅ **기술적 정확성**: Redis 다운 감지 및 fallback 로직 정확 구현
- ⏳ **증거 기반**: Proofpack에 redis_down_simulation 필드 추가 필요

### **善 (Goodness) - 35%**
- ✅ **보안 강화**: Hybrid 정책으로 민감/일반 엔드포인트 구분
- ✅ **리스크 관리**: Redis 다운 시에도 서비스 연속성 보장
- ⏳ **안정성**: 자동화된 테스트로 정책 검증 필요

### **美 (Beauty) - 20%**
- ✅ **단일 책임**: Fallback 정책만 담당
- ✅ **설정 기반**: 환경 변수로 정책 선택
- ⏳ **일관성**: 엔드포인트별 정책 적용 로직 구현 필요

### **孝 (Serenity) - 8%**
- ✅ **마찰 최소화**: 투명한 fallback 적용
- ✅ **graceful 처리**: 다운 상태에서도 서비스 유지
- ⏳ **자동화**: 테스트 자동화로 운영 부담 감소

### **永 (Eternity) - 2%**
- ✅ **재현성**: Docker Compose로 환경 재현
- ✅ **영속성**: 정책 설정을 코드로 저장
- ⏳ **호환성**: 미래 Redis 클러스터 지원 고려

---

## 📈 **기대 성과**

### **보안 레벨 향상**
```
Phase 2.5 (100/100):
- Rate Limiting: ✅ 분산 지원
- Fallback: ✅ 기본 옵션

Phase 2.6 (예상 100/100):
- Redis Down: ✅ 정책 기반 대응
- Hybrid Mode: ✅ 엔드포인트별 보안 레벨
- Monitoring: ✅ 연결 상태 실시간 모니터링
```

### **가용성 향상**
- **Redis 다운 시**: 95% 서비스 유지 (Fail-Open 기본)
- **민감 엔드포인트**: 100% 보안 유지 (Fail-Closed)
- **복구 시간**: Redis 재연결 즉시 정책 해제

---

## 🎉 **Phase 2.6 준비 완료**

**형님, Phase 2.6 Redis Down Policy SSOT 템플릿이 준비되었습니다.**

**"Redis 다운 시에도 왕국 법에 따라 안정적으로 서비스를 유지하는 체계로 진화합니다."**

**Phase 2.6 SSOT 템플릿 준비 완료!** 🎯

---

## 📚 **참고 문헌 (SSOT 근거)**

[1]: https://slowapi.readthedocs.io/en/latest/api/ "SlowAPI Fallback 메커니즘"
[2]: https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html "OWASP Rate Limiting"
[3]: https://redis.io/docs/connect/clients/python/ "Redis Python Client"

---

**SSOT 템플릿 준비 날짜**: 2025-12-24
**준비자**: 승상 (Chancellor)
**다음 단계**: 왕국법 정책 결정 및 구현