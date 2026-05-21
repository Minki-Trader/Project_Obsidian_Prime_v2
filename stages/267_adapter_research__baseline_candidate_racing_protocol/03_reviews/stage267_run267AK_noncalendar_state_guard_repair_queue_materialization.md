# Stage267 Run267AK Noncalendar State Guard Repair Queue Materialization(267단계 267AK 비달력 상태 방어 수리 큐 물질화)

- action(행동): run267AJ(267AJ 실행)의 P0 수리 큐를 score table/model/set/ini(점수표/모델/설정/초기화) 실행 입력으로 만들었다.
- effect(효과): `s264_aia` 두 constructive row(건설적 행)를 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 같은 조건으로 시험할 수 있다.
- status(상태): `run267AK_noncalendar_state_guard_repair_queue_materialized_execution_pending`
- judgment(판정): `repair_queue_materialized_execution_pending_no_candidate_selection`
- variants(변형): `2`
- attempts(시도): `4`
- deferred_queue(보류 큐): `3`
- model_audit(모델 감사): `2/2` pass(통과)
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

`s264_aia`의 두 줄만 실제 실행 대기 입력으로 만들었다.
Effect(효과): 좋아 보였던 후보를 바로 고르지 않고, Monday(월요일)와 2024-12 구멍이 줄어드는지 다음 실행에서 본다.

`s264_aih`는 이번 물질화에서 제외하고 gate(게이트)만 남겼다.
Effect(효과): 약해진 core role(핵심 역할)을 계속 끌고 가는 repair loop(수리 반복)를 막는다.

Tier A+B(Tier A+B 합산)는 아직 fallback disabled(대체 비활성) 경계다.
Effect(효과): 다음 실행 결과가 나오더라도 real fallback routing(실제 대체 라우팅) 근거로 과장하지 않는다.

## Repair Queue(수리 큐)

| queue_id | candidate_alias | source_test_id | repair_profile | materialization_status | success_criteria |
| --- | --- | --- | --- | --- | --- |
| run267AK_q01a_s264_aia_rep_trend_strength_adx_repair | s264_aia | rep_trend_strength_adx | aia_dual_replacement_state_guard_repair_v3 | ready_for_score_table_materialization | trade_count_at_least_280;net_profit_at_least_900;PF_at_least_1.35;DD_at_most_18;Monday_loss_above_-180;December_loss_above_-120 |
| run267AK_q01b_s264_aia_rep_volatility_atr_repair | s264_aia | rep_volatility_atr | aia_dual_replacement_state_guard_repair_v3 | ready_for_score_table_materialization | trade_count_at_least_280;net_profit_at_least_900;PF_at_least_1.35;DD_at_most_18;Monday_loss_above_-180;December_loss_above_-120 |

## Deferred Queue(보류 큐)

| queue_id | candidate_scope | materialization_readiness | defer_reason | next_condition |
| --- | --- | --- | --- | --- |
| run267AK_q02_s264_aih_core_role_prune_confirmation | s264_aih | design_gate_before_any_materialization | design_gate_only_s264_aih_needs_state_reason_before_any_new_materialization | only_materialize_if_s264_aia_repair_fails_or_specific_noncalendar_state_reason_is_named |
| run267AK_q03_real_fallback_routing_probe_design | s264_aia;s264_aih | deferred_until_q01_survives | real_Tier_B_fallback_probe_deferred_until_q01_survives | q01_MT5_review_survives_without_duplicate_Tier_A_plus_B_claim |
| run267AK_q04_broader_period_pressure_after_repair | surviving_watch_rows | deferred_until_q01_or_q02_survives | broader_period_pressure_deferred_until_repair_survives_2024 | q01_or_q02_survivor_has_cleaner_2024_curve |

## Candidate Gate(후보 게이트)

| candidate_alias | run267AJ_decision_label | run267AK_gate_decision | materialized_variant_count |
| --- | --- | --- | --- |
| s264_aih | downgrade_core_role_to_prune_boundary | design_gate_only_core_role_prune_boundary | 0 |
| s264_lc | preserve_defensive_control_no_new_run267AI_evidence | preserved_role_no_new_run267AK_materialization | 0 |
| s262_lih | preserve_validation_heavy_control_no_new_run267AI_evidence | preserved_role_no_new_run267AK_materialization | 0 |
| s264_aia | continue_bounded_state_guard_materialization_watch | materialized_P0_bounded_repair_watch_not_selection | 2 |
| s258_stc | preserve_stress_boundary_no_new_run267AI_evidence | preserved_role_no_new_run267AK_materialization | 0 |

## Evidence(근거)

- repair_variant_manifest(수리 변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AK/noncalendar_state_guard_repair_queue_materialization/repair_variant_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AK/noncalendar_state_guard_repair_queue_materialization/runtime_contract.csv`
- model_repair_audit(모델 수리 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AK/noncalendar_state_guard_repair_queue_materialization/model_repair_audit.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AK/noncalendar_state_guard_repair_queue_materialization/attempt_manifest.csv`
- run_manifest(실행 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AK/noncalendar_state_guard_repair_queue_materialization/run_manifest.json`

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267AK_stage267_noncalendar_state_guard_repair_queue_materialization_v1`.
- evidence_available(사용 근거): variants(변형) `2`, attempts(시도) `4`, audit_pass(감사 통과) `2/2`.
- evidence_missing(부족 근거): MT5 execution(MT5 실행), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질), real Tier B fallback(실제 Tier B 대체).
- judgment_label(판정 라벨): `repair_queue_materialized_execution_pending_no_candidate_selection`.
- claim_boundary(주장 경계): 물질화 완료만 주장한다. 선택 후보, ONNX 준비, 목표 달성은 주장하지 않는다.
- next_condition(다음 조건): `run267AL_execute_noncalendar_state_guard_repair_mt5_batch`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AJ/noncalendar_state_guard_followup_design/next_experiment_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AG/noncalendar_state_guard_followup_queue_materialization/followup_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AI/noncalendar_state_guard_followup_balance_timeslice_trade_quality_review/candidate_test_review.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AK_noncalendar_state_guard_repair_queue_materialization.py`.
- outputs(출력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AK/noncalendar_state_guard_repair_queue_materialization/repair_materialization_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AK/noncalendar_state_guard_repair_queue_materialization/repair_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AK/noncalendar_state_guard_repair_queue_materialization/attempt_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AK/noncalendar_state_guard_repair_queue_materialization/review_result.json`.
- consumer(소비자): `run267AL_execute_noncalendar_state_guard_repair_mt5_batch`.
- lineage_judgment(계보 판정): `connected_with_boundary`.
