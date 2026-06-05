# 2026-06-01 Stage342A Branch Decision(342A 단계 분기 결정)

- decision(결정): `stage342A_open_run342B_materialize_f01_session_long_firewall_mt5_probe_package`
- from(출발): `341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue` / `run341D_review_f01_stability_cost_regime_validation_without_db_v1`
- to(도착): `342_session_long_firewall__early_long_filter_mt5_probe` / `run342B_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1`
- superseded_run(대체된 실행): `run341E_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1`
- reason(이유): Stage 341(341단계)이 validation review(검증 검토) 뒤 MT5 package(MT5 패키지)까지 품으면 너무 무거워져 session-long firewall(세션 롱 방화벽)을 새 단계로 분리했다.

Action(행동): Stage 342(342단계)를 열고 run342B(342B 실행)를 package materialization(패키지 물질화) 다음 행동으로 둔다.
Effect(효과): run341D(341D 실행)의 positive clue(긍정 단서)를 보존하면서 다음 MT5 probe(MT5 탐침)를 가볍게 시작한다.

claim_boundary(주장 경계): `state_sync_stage_branch_session_long_firewall_handoff_only_no_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
