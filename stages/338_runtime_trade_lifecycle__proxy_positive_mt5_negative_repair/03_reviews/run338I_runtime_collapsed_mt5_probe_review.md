# run338I Runtime-Collapsed MT5 Probe Review(런타임 축약 MT5 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `run338I_review_runtime_collapsed_onnx_mt5_probe_or_repair_without_db_v1`
- status(상태): `completed_stage338I_runtime_positive_clue_reviewed_trade_count_recovery_repair_required_no_selection`
- judgment(판정): `mt5_runtime_positive_exact_parity_but_trade_count_low_recovery_under_floor_no_selection`
- gates(게이트): `10/10`
- MT5 net profit(MT5 순수익): `42.01`
- profit factor(수익 팩터): `2.12`
- expectancy(기대값): `3.82`
- drawdown(낙폭): `53.87`
- recovery factor(회복 계수): `0.78`
- trade count(거래수): `11`
- long/short(롱/숏): `3/8`
- weakness(약점): `recovery_factor_below_1_00;trade_count_below_30;signal_side_short_heavy`
- next_run_id(다음 실행 ID): `run338J_materialize_trade_count_recovery_expansion_mt5_probe_package_without_db_v1`

## Action(행동)

run338H(338H 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 proxy(프록시), parity(동등성), KPI(핵심 성과 지표)로 나눠 검토했다.

Effect(효과): net profit(순수익) 42.01, profit factor(수익 팩터) 2.12, expectancy(기대값) 3.82라는 positive clue(긍정 단서)는 살리고, trade count(거래수) 11과 recovery factor(회복 계수) 0.78 때문에 operating promotion(운영 승격)은 막는다.

## Judgment(판정)

positive clue(긍정 단서)는 유효하다. 다만 selected model(선정 모델), runtime authority(런타임 권위), live readiness(실거래 준비), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.

## Evidence(근거)

- runtime review(런타임 검토): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338I/run338I_runtime_review_scorecard.csv`
- KPI judgment(KPI 판정): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338I/run338I_mt5_kpi_judgment.csv`
- proxy-MT5 attribution(프록시-MT5 귀속): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338I/run338I_proxy_mt5_diff_attribution.csv`
- repair queue(수리 대기열): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338I/run338J_repair_or_expansion_queue.csv`
- final decision(최종 결정): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338I/final_decision.json`
