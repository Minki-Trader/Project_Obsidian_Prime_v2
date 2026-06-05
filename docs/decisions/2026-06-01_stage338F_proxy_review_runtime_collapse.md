# 2026-06-01 Stage338F Decision(338F 결정)

- run_id(실행 ID): `run338F_review_group_safe_onnx_proxy_scores_for_mt5_probe_without_db_v1`
- decision(결정): `stage338F_open_run338G_runtime_collapsed_mt5_probe_package`
- judgment(판정): `proxy_positive_after_runtime_timestamp_collapse_mt5_probe_package_required_no_selection`
- next_run_id(다음 실행 ID): `run338G_materialize_runtime_collapsed_onnx_mt5_probe_package_without_db_v1`
- evidence(근거): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338F/run338F_runtime_collapsed_proxy_score.csv`, `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338F/run338G_mt5_probe_package_queue.csv`

Action(행동): proxy(프록시)를 MT5(메타트레이더5)가 소비 가능한 timestamp-unique(시각 고유) 형태로 축약했다.
Effect(효과): 다음 실행은 proxy-MT5 comparison(프록시-MT5 비교)을 위해 실제 패키지를 만들 수 있다.

claim_boundary(주장 경계): `research_development_proxy_review_and_runtime_shape_control_only_no_candidate_selection_no_mt5_execution_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
