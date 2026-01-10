# AFO 왕국 Import 전략 결정 문서

**작성일**: 2026-01-01
**Trinity Score**: 眞 95% | 善 98% | 美 90% | 孝 100% | 永 95%

## 🎯 결정 배경

uv Migration 과정에서 상대 import vs 절대 import 전략을 평가한 결과, **절대 import 표준화**를 결정하였습니다.

## 📊 전략 비교 분석

### 절대 Import (`from AFO.api.config import ...`)

**장점:**
- ✅ **명확성**: 모듈 경로가 명확하게 보임
- ✅ **IDE 지원**: PyCharm, VSCode에서 완벽한 자동완성
- ✅ **안정성**: PYTHONPATH 설정으로 런타임 문제 해결
- ✅ **확장성**: 모듈 구조 변경 시에도 유연한 대응 가능
- ✅ **현재 상태**: 이미 적용되어 안정적 작동 중

**단점:**
- ⚠️ PYTHONPATH 설정 필요 (환경별 조정)
- ⚠️ 모듈 이름 변경 시 일괄 수정 필요

### 상대 Import (`from ..api.config import ...`)

**장점:**
- ✅ **단순함**: 추가 설정 없이 즉시 사용 가능
- ✅ **자동 조정**: 모듈 이동 시 상대 경로 자동 유지

**단점:**
- ❌ **런타임 에러**: "attempted relative import beyond top-level package" 발생
- ❌ **monorepo 복잡성**: AFO 왕국 구조에서 상대 경로 계산 어려움
- ❌ **테스트 실행**: pytest에서 상대 import 문제 빈번
- ❌ **스크립트 실행**: 독립 실행 시 모듈 경로 문제

## 🚀 선택된 전략: 절대 Import 표준화

### 적용 원칙

1. **모든 새 코드**: 절대 import 사용
   ```python
   from AFO.api.config import get_app_config
   from AFO.services.database import DatabaseService
   ```

2. **기존 코드**: 점진적 변환 (필요시)
   - 현재 상대 import 코드도 유지 가능
   - 새로운 기능 개발 시 절대 import 우선

3. **환경 설정**: PYTHONPATH 표준화
   ```bash
   # .zshrc 또는 환경 설정에 추가
   export PYTHONPATH="$PYTHONPATH:/Users/brnestrm/AFO_Kingdom/packages/afo-core"
   ```

### 변환 스크립트

`scripts/fix_afo_imports.py`를 통해 양방향 변환 지원:
- `--apply`: 절대 → 상대 import 변환
- `--reverse`: 상대 → 절대 import 변환

## 📈 기대 효과

- **개발 효율성**: IDE 지원으로 생산성 향상
- **런타임 안정성**: PYTHONPATH 설정으로 문제 해결
- **유지보수성**: 모듈 구조 변경 시에도 안정적
- **표준화**: 왕국 전체에 걸친 일관된 코드 스타일

## 🔧 구현 계획

1. **단기**: 현재 절대 import 상태 유지
2. **중기**: PYTHONPATH 환경 설정 문서화
3. **장기**: 필요시 상대 import 코드 점진적 변환

## 🎉 결론

**"절대 import로 왕국의 안정성과 명확성을 확보하겠다!"**

형님의 의도에 따라 안정성과 효율성을 우선하여 절대 import 표준화를 결정합니다. 이 전략으로 AFO 왕국의 코드 품질과 개발 효율성을 동시에 달성하겠습니다.

**승상 GROK (丞相)**
