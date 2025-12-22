# 🏰 **Phase 2: Ruff 정화 작전 계획**

**작성일시**: 2025년 12월 21일  
**작성자**: 승상 (丞相) - AFO Kingdom  
**검증 방식**: Sequential Thinking + Context7 + 학자들

---

## 📊 **Phase 2.1: 현재 상태 분석**

### **Ruff 오류 현황**

- **통계 기준**: 120개 이슈
- **실제 오류**: 약 40개
- **자동 수정 가능**: 6개
- **목표**: 800개 이하 (이전 기준 대비)

### **주요 오류 유형**

1. **SIM117** (27개) - multiple-with-statements
2. **B904** (17개) - raise-without-from-inside-except
3. **E402** (9개) - module-import-not-at-top-of-file
4. **ARG004** (7개) - unused-static-method-argument
5. **F821** (6개) - undefined-name
6. **RUF012** (5개) - mutable-class-default
7. **기타** (49개)

---

## 🎯 **Phase 2.2: 수정 전략**

### **우선순위 1: 자동 수정 가능 이슈**
- `--fix` 옵션으로 자동 수정

### **우선순위 2: 주요 오류 유형 수정**
- SIM117: multiple-with-statements 통합
- B904: raise-without-from-inside-except 수정
- E402: import 순서 정리
- F821: undefined-name 해결

### **우선순위 3: 코드 품질 향상**
- RUF012: mutable-class-default 수정
- ARG004: unused-static-method-argument 정리

---

## 🚀 **다음 단계**

Sequential Thinking으로 단계별 수정 진행

---

**보고자**: 승상 (丞相) - AFO Kingdom  
**상태**: 🔄 **PHASE 2 IN PROGRESS**

