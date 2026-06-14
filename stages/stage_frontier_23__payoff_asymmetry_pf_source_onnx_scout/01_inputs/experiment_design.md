# Frontier23 Experiment Design(전선23 실험 설계)

- hypothesis(가설): 평균 이익/손실 비, 우측 꼬리 대 최악 손실 억제, 불리 손실 필터가 좋은 진입 상태는 validation/OOS(검증/표본외)에서도 PF(수익 팩터) 원천에 가까운 단서를 줄 수 있다.
- decision_use(결정 사용처): F23B proxy scout(F23B 프록시 탐색)의 선택 지표와 중단 조건을 고정한다.
- comparison_baseline(비교 기준): unconditional same-side train baseline(무조건 동일 방향 학습 기준선)과 F22 negative memory(F22 부정 기억).
- control_variables(통제 변수): feature_set_v2 58 features(58개 피처 고정), future_log_return_12 fwd12 proxy(fwd12 프록시 고정), train-only selection(학습 전용 선택), validation/OOS read-only(검증/표본외 읽기 전용)
- changed_variables(변경 변수): selection metric becomes payoff asymmetry(선택 지표를 보상 비대칭으로 변경), no shock-required entry lock(충격 필수 진입 잠금 제거), pre-scout sanity gate(탐색 전 건전성 게이트) 추가
- sample_scope(표본 범위): Tier A separate(티어 A 분리); Tier B missing_required(티어 B 필수 누락); Tier A+B out_of_scope_by_claim(티어 A+B 주장 범위 밖).
- success_criteria(성공 기준): {"pre_scout_sanity": "at least one train-only asymmetry condition beats unconditional train baseline(학습 전용 비대칭 조건 하나 이상이 무조건 학습 기준선을 초과)", "scout_clue": "validation/OOS net positive, PF>=1.05, density 3-12/day, DD<=35(검증/표본외 순수익 양수, 수익 팩터 1.05 이상, 빈도 3-12/일, 손실폭 35 이하)", "seed_surface": "validation/OOS PF>=1.20 both, density 5-10/day, DD controlled(검증/표본외 둘 다 수익 팩터 1.20 이상, 빈도 5-10/일, 손실폭 억제)", "handoff_candidate": "PF>=1.50 both, density 5-10/day, DD<=12, smoothness pass, then Grok before WFO/MT5/ONNX(둘 다 수익 팩터 1.50 이상이면 비싼 검증 전 그록 검토)"}
- failure_criteria(실패 기준): pre-scout sanity gate fails(탐색 전 건전성 게이트 실패), no validation/OOS positive PF clue(검증/표본외 양수 수익 팩터 단서 없음), best rows are shock+trend or F20 atlas restatement(최상위 행이 충격+추세 또는 F20 규칙 지도 재진술)
- invalid_conditions(무효 조건): validation/OOS used for selection stats(검증/표본외를 선택 통계에 사용), lifecycle repair before proxy seed(프록시 씨앗 전 생명주기 수리), ONNX/model training before handoff candidate(인계 후보 전 ONNX/모델 학습)
- stop_conditions(중단 조건): pre-scout sanity gate fails(탐색 전 건전성 게이트 실패), handoff-like row appears and pre-expensive Grok is required(인계성 행 발생 시 비싼 검증 전 그록 필요), capped proxy and repair cannot create seed/handoff(상한 프록시/수리가 씨앗/인계를 못 만듦)
