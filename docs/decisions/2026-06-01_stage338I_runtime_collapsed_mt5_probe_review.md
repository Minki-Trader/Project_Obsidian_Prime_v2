# 2026-06-01 Stage338I Decision(338I 결정)

- run_id(실행 ID): `run338I_review_runtime_collapsed_onnx_mt5_probe_or_repair_without_db_v1`
- decision(결정): `stage338I_open_run338J_trade_count_recovery_expansion_or_confirmation_probe`
- judgment(판정): `mt5_runtime_positive_exact_parity_but_trade_count_low_recovery_under_floor_no_selection`
- next_run_id(다음 실행 ID): `run338J_materialize_trade_count_recovery_expansion_mt5_probe_package_without_db_v1`
- evidence(근거): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338I/run338I_runtime_review_scorecard.csv`, `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338I/run338I_mt5_kpi_judgment.csv`, `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338I/run338J_repair_or_expansion_queue.csv`

Action(행동): MT5 positive clue(MT5 양수 단서)를 operating promotion(운영 승격)이 아니라 trade count/recovery expansion(거래수/회복 확장) 문제로 넘겼다.

Effect(효과): 좋은 단서를 버리지 않고, 약한 KPI(핵심 성과 지표)를 다음 run338J(338J 실행)의 제약으로 고정한다.

claim_boundary(주장 경계): `research_development_mt5_runtime_probe_review_only_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
