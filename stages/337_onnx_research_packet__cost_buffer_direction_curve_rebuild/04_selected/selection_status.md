# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `run337AO_asof_regime_and_db_source_materialization_v1`
- latest_decision(최신 결정): `stage337AO_open_run337AP_broker_tester_history_repair_no_selection`
- current_run(현재 실행): `run337AP_broker_tester_history_repair_or_next_rollover_v1`
- broker_forward_boundary(브로커 전진 경계): `failed`
- asof_regime_sources_materialized(시점 기준 국면 원천 물질화): `3/3`
- asof_join_trade_rows(시점 기준 거래 조인 행): `344`
- no_future_source_violations(미래 원천 위반): `0`
- db_source_status(D/B 원천 상태): `missing_required_columns_7`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_feature_last_not_reached_and_db_source_missing`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run337AP_broker_tester_history_repair_or_next_rollover_v1`
- effect(효과): run337AO(337AO 실행)은 macro as-of join(거시 시점 기준 결합)을 만들고 D/B source(D/B 원천) 누락을 고정했다.
