# Beautiful Code Covenant (AFO)

## 1. Single Truth
- 티켓마다 Report 1개 + Evidence folder 1개만
- "완료/정상"은 말이 아니라 Evidence 파일로만 선언

## 2. Evidence-first
- 모든 기능/보안 검증은 파일 증거로만 인정
- 보고서에 적힌 `artifacts/...` 경로는 실제 존재해야 함

## 3. No side effects by default
- 승인/결제 같은 엔드포인트 검증은 `OPTIONS/HEAD`만
- POST/PUT는 부작용 가능성이 있으면 금지

## 4. Refactor by pressure
- 파일이 커지면 자동으로 Refactor Queue에 기록
- 다음 티켓에서 분해하는 것을 원칙으로 함

## 5. Small PR
- main 편입은 작은 단위로(한 티켓=한 목적)
- 티켓이 크면 여러 개로 분리

## 6. Boundaries
- UI/Service/API/DB 레이어 섞지 않기
- 의존성 역전 원칙 준수

## 7. Make it easy to delete
- 실험 코드는 feature flag/isolated module로
- 제거 비용 최소화

## 8. Readable > clever
- 3개월 뒤 내가 봐도 이해 가능해야 함
- 복잡한 로직은 주석 필수

## 9. Override is a ceremony
- 급할 땐 통과 가능하지만 OVERRIDE 문서로 빚 기록
- 후속 조치 계획 포함

## 10. Truth over speed
- 정확한 증거 > 빠른 완료
- 의심스러우면 UNVERIFIED로 두고 재검증