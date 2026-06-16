# F70B Label-Regime Asymmetric Value Proxy Scout(F70B 라벨-장세 비대칭 가치 프록시 탐색)

Updated(갱신): 2026-06-16T21:28:30Z

## Hypothesis(가설)

Density-aware asymmetric value labels(밀도 인식 비대칭 가치 라벨)이 F69 sparse/dense fracture(F69 희박/조밀 균열)를 줄일 수 있는지 시험했다.

## Action And Effect(행동 및 효과)

Action(행동): label/target and regime/session(라벨/목표 및 장세/세션)을 선도 축으로 두고 proxy scout(프록시 탐색)를 실행했다.

Effect(효과): threshold/cooldown/daily quota(임계값/쿨다운/일별 할당) 수리가 아니라 라벨 자체가 PF/density(수익 팩터/밀도)를 같이 움직이는지 기록했다.

## KPI Summary(KPI 요약)

- candidate rows(후보 행): `420`.
- meaningful joint-soft candidates(의미 있는 공동 완화 후보): `0`.
- final-like candidates(최종 조건 유사 후보): `0`.
- top candidate(상위 후보): `f70b_4e38e079ea0d`.
- top validation net/PF/DD/trades_day(검증 순수익/수익 팩터/손실폭/일거래): `-786.7759` / `0.79163` / `9.328551` / `1.072907`.
- top OOS net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래): `1058.848302` / `1.513466` / `1.498869` / `0.998838`.

## Required Records(필수 기록)

- test period(테스트 기간): validation 2025-01-01..2025-09-30, OOS 2025-10-01..2026-04-13.
- proxy expectation(프록시 예상): label-regime candidates(라벨-장세 후보)가 PF와 density(수익 팩터와 밀도)를 함께 움직이면 pre-MT5 Grok review(사전 MT5 그록 검토)로 간다.
- proxy KPI(프록시 KPI): `stages/stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation/02_runs/frontier70B_label_regime_asymmetric_value_proxy_scout_v1/f70b_proxy_candidate_summary.csv`.
- runtime probe KPI(런타임 탐침 KPI): pending(대기), proxy-only boundary(프록시 전용 경계).
- signal count parity(신호 수 동등성): not_applicable_before_runtime(런타임 전 해당 없음).
- feature readiness parity(피처 준비 동등성): not_applicable_before_runtime(런타임 전 해당 없음).
- proxy/runtime gap cause(프록시/런타임 간극 원인): pending_runtime_probe(런타임 탐침 대기).
- next action(다음 행동): `frontier70C_label_regime_repair_or_closeout_decision_v1`.

Claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
