# Stage359B High-Density Label Pivot MT5 Probe(359B 고밀도 라벨 전환 MT5 탐침)

## Result(결과)

- status(상태): `completed_stage359B_high_density_label_pivot_mt5_probe_executed_review_required_no_selection`
- judgment(판정): `runtime_probe_positive_but_review_required_no_selection`
- next_run_id(다음 실행 ID): `run359C_review_high_density_label_pivot_mt5_probe_without_db_v1`
- attempt_rows(시도 수): `4`
- runtime_completed_rows(런타임 완료 수): `4`
- report_available_rows(보고서 사용 가능 수): `4`
- matched_rows(일치 수): `27869`
- diff_mismatch_rows(차이 불일치 수): `0`

Action(행동): Stage358B(358B 실행)의 pside/all(방향확률/전체 세션) attempt(시도)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry(원격측정), report(보고서), proxy-MT5 diff(프록시-MT5 차이)를 수집했다.

Effect(효과): proxy expected value(프록시 예상값)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않도록 실제 runtime evidence(런타임 근거)와 분리해 비교할 수 있다.

## Best Runtime Read(최선 런타임 판독)

- best_attempt_name(최선 시도 이름): `q05_pside_all_oos`
- best_model_id(최선 모델 ID): `run357B_d04_h12_q45_55_high_density_band__extratrees_cls_depth10_leaf80_seed13`
- best_probe_split(최선 탐침 분할): `oos`
- best_net_profit(최선 순수익): `262.85`
- best_profit_factor(최선 수익 팩터): `1.09`
- best_expectancy(최선 기대값): `0.28`
- best_recovery_factor(최선 회복 계수): `0.92`
- best_trade_count(최선 거래 수): `936`
- best_trade_density_per_feature_day(최선 피처일별 거래 수): `7.145038167938932`

## Artifacts(산출물)

- execution_summary(실행 요약): `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359B/high_density_label_pivot_mt5_probe_summary.csv`
- proxy_mt5_diff(프록시-MT5 차이): `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359B/proxy_mt5_runtime_difference.csv`
- strategy_tester_reports(전략 테스터 보고서): `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359B/strategy_tester_report_records.json`
- runtime_identity(런타임 정체성): `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359B/runtime_identity.csv`
- gate_audit(게이트 감사): `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359B/required_gate_coverage_audit.csv`
- final_decision(최종 결정): `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359B/final_decision.json`

## Claim Boundary(주장 경계)

This run(이번 실행)은 runtime probe(런타임 탐침)이다. operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), goal achieve(목표 달성)는 주장하지 않는다.
