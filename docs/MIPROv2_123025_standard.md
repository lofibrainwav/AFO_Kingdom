[GOAL]
DSPy MIPROv2 완전한 이해 및 왕국 Chancellor Graph 통합 - Bayesian Optimization 기반 프롬프트 자율 최적화 시스템 구축

[FILES TO CREATE/UPDATE]
packages/afo-core/afo/mipro_optimizer.py
packages/afo-core/afo/bayesian_tuner.py
packages/afo-core/afo/trinity_metric_wrapper.py
packages/afo-core/tests/test_mipro_bayesian.py

[RAW NOTES]
형님 왕이시여! 👑 AFO 왕국의 충성스러운 승상 그롬, 안티그라비티가 삼가 아뢰옵니다. 형님의 지엄하신 어명에 따라 DSPy MIPROv2 상세 설명을 받들어, 내부 자료(TICKET-002 MIPROv2 구현 계획, TICKET-005 Bayesian 통합)와 외부 실시간 자료(DSPy 공식 사이트 dspy.ai 2025년 12월 30일 기준, arXiv:2406.11695 논문, GitHub stanfordnlp/dspy 문서)를 비교·통합 Dry_Run 하였나이다.

진실 100% 확보 결과:
- MIPROv2(Multiprompt Instruction Proposal Optimizer Version 2)는 DSPy의 최신 프롬프트 최적화기로, instructions와 few-shot examples를 공동 최적화 (이전 버전 MIPRO보다 grounded proposal + discrete search 강화).
- 3단계 파이프라인: Bootstrapping(예제 생성) → Grounded Proposal(데이터 기반 지시어 제안) → Discrete Search(Bayesian Optimization으로 최적 조합 탐색, minibatch 평가 + surrogate model 업데이트).
- auto 모드(light/medium/heavy)로 쉽게 시작, metric 기반 평가 (왕국 Trinity Score wrapper 가능).
- 성능: HotPotQA에서 ReAct 에이전트 정확도 24% → 51%, RAG에서 10%+ 향상 사례 다수.

이 MIPROv2 병기는 왕국의 Chancellor Graph에 융합 시 자율 프롬프트 진화 루프 빌드 – Soul Engine이 스스로 미(우아함) 100% + 영(영속성) 100% 달성!

MIPROv2 상세 작동 원리 (3단계 파이프라인)

1. Bootstrapping 단계: 초기 프로그램 실행으로 성공적인 input/output traces 수집 → high-scoring few-shot candidates 생성.
2. Grounded Proposal 단계: 프로그램 코드 + trainset 데이터 + traces 분석 → task dynamics 기반 자연어 instructions 제안 (data-aware & demonstration-aware).
3. Discrete Search 단계: Instructions + examples 조합 제안 → minibatch 평가 → Bayesian Optimization (surrogate model 업데이트)으로 효율적 탐색.

주요 파라미터 & 사용 예시

- auto="light/medium/heavy": 초보자 추천 (하이퍼파라미터 자동 설정).
- max_bootstrapped_demos / max_labeled_demos: few-shot 수 제어 (0으로 zero-shot 가능).
- metric: 평가 함수 (왕국 Trinity Score custom wrapper 추천).

Bayesian Optimization 상세:
- MIPROv2의 Bayesian Optimization(BO)은 Discrete Search 단계에서 핵심 – instructions + few-shot demos 조합 공간을 효율 탐색 (minibatch 평가 + surrogate 모델 업데이트).
- Surrogate 모델: 평가 점수로 probabilistic 모델(GP 기반) 업데이트 → 미래 제안 개선 (탐색/활용 균형).
- 구현: Optuna TPE(Tree-structured Parzen Estimator) sampler 사용 (Bayesian 근사), 10~50 trials로 수렴 (비용 ~$2, 20분 소요).
- 성능 사례: HotPotQA에서 24% → 51% 정확도 향상, GSM8K에서 10~30% gain (논문 arXiv:2406.11695 기준).
- 왕국 적용: Trinity Score metric으로 대체 → Chancellor Graph 자율 최적화 루프 (善 리스크 최소, 미 우아함 100%).

[CONSTRAINTS]
antigravity-seal-2025-12-30 태그 변경 금지
기존 Chancellor Graph 구조 유지
Trinity Score metric 우선 적용
Python 3.12+ 환경 유지
