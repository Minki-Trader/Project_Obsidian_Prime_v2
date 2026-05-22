# Stage267 Run267DQ Runtime Gap Aware Fourth Follow-Up/Prune Materialization(267단계 267DQ 런타임 공백 반영 4차 후속/가지치기 물질화)

## Summary(요약)

- run_id(실행 ID): `run267DQ_stage267_runtime_gap_aware_fourth_followup_or_prune_materialization_v1`
- parent_run(상위 실행): `run267DP_stage267_runtime_gap_aware_fourth_followup_or_prune_design_v1`
- source_materializer(원천 물질화): `run267DL_stage267_shared_weakness_breakout_third_followup_or_prune_materialization_v1`
- status(상태): `run267DQ_runtime_gap_aware_fourth_followup_or_prune_materialized_execution_pending`
- variants(변형): `7`
- attempts(시도): `8`
- materialized_queue_rows(물질화 대기열 행): `3`
- held_rows(보류 행): `1`
- supply_diagnostics(공급 진단): `3`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run267DR_execute_runtime_gap_aware_fourth_followup_or_prune_mt5_batch`

## Easy Read(쉬운 설명)

`run267DQ`는 후보를 고른 것이 아니라, `run267DP`가 남긴 다음 실험 대기열을 실제 입력으로 바꾼 실행이다. `s258_stc`는 거래가 생긴 `sidefilter_open(사이드필터 개방)` 축만 2023H2/2025H1/2025H2로 이어가고, `threshold_release(임계값 해제)`는 다시 돌리지 않는다. 별도의 `s258_stc` 위험 완화 축은 필터를 더 붙이는 방식이 아니라 보유 시간과 위험 크기만 줄인 형태다.

`s264_lc`는 방어 대조(control, 대조)로만 2024 DD(drawdown, 손실폭)를 확대검토한다. `s264_aia`와 `s262_lih`는 현재 경로가 무거래/런타임 공백이므로 MT5(MetaTrader 5, 메타트레이더5)에 넣지 않고 pre-runtime supply diagnostic(런타임 전 공급 진단)으로만 남겼다.

## Queue Decisions(대기열 판단)

| queue(대기열) | decision(판단) | variants(변형) | effect(효과) |
| --- | --- | ---: | --- |
| `q01_s258_supply_shape_continuity_cross_period` | `materialized_for_mt5_execution` | `3` | 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 곡선/시간구간/거래품질을 볼 수 있다. |
| `q02_s258_monday_late_session_dd_taper_cross_period` | `materialized_for_mt5_execution` | `3` | 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 곡선/시간구간/거래품질을 볼 수 있다. |
| `q03_s264_lc_defensive_dd_zoom_control` | `materialized_for_mt5_execution` | `1` | 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 곡선/시간구간/거래품질을 볼 수 있다. |
| `q04_s264_aia_s262_lih_supply_rebuild_diagnostic_no_mt5` | `held_as_pre_runtime_supply_diagnostic_no_mt5` | `0` | 무거래/런타임 공백 후보를 다시 실행하지 않고 신호 공급 증명으로 분리한다. |

## Attempt Inputs(시도 입력)

| attempt(시도) | candidate(후보) | split(구간) | risk shape(위험 형태) | status(상태) |
| --- | --- | --- | --- | --- |
| `run267dq_01_s258_stc_2023h2_supply_continuity_sidefilter_open_ta_2023h2` | `s258_stc` | `adjacent_2023_h2_train_pre_2024` | `supply_continuity` | `materialized_execution_pending` |
| `run267dq_02_s258_stc_2025h1_supply_continuity_sidefilter_open_ta_2025h1` | `s258_stc` | `adjacent_2025_h1_validation_post_2024` | `supply_continuity` | `materialized_execution_pending` |
| `run267dq_03_s258_stc_2025h2_supply_continuity_sidefilter_open_ta_2025h2` | `s258_stc` | `adjacent_2025_h2_oos_followthrough` | `supply_continuity` | `materialized_execution_pending` |
| `run267dq_04_s258_stc_2023h2_monday_late_dd_taper_ta_2023h2` | `s258_stc` | `adjacent_2023_h2_train_pre_2024` | `monday_late_dd_taper` | `materialized_execution_pending` |
| `run267dq_05_s258_stc_2025h1_monday_late_dd_taper_ta_2025h1` | `s258_stc` | `adjacent_2025_h1_validation_post_2024` | `monday_late_dd_taper` | `materialized_execution_pending` |
| `run267dq_06_s258_stc_2025h2_monday_late_dd_taper_ta_2025h2` | `s258_stc` | `adjacent_2025_h2_oos_followthrough` | `monday_late_dd_taper` | `materialized_execution_pending` |
| `run267dq_07_s264_lc_defensive_dd_zoom_control_ta_2024` | `s264_lc` | `historical_2024` | `dd_zoom_control` | `materialized_execution_pending` |
| `run267dq_07_s264_lc_defensive_dd_zoom_control_rt_2024` | `s264_lc` | `historical_2024` | `dd_zoom_control` | `materialized_execution_pending` |

## Held Diagnostic(보류 진단)

| diagnostic(진단) | candidate(후보) | rows(행) | nonzero rows(비영 행) | status(상태) |
| --- | --- | ---: | ---: | --- |
| `aia_similar_survivor_supply_rebuild` | `s264_aia` | `11651` | `11651` | `held_no_mt5_until_nonzero_signal_supply_proof` |
| `aia_ablation_survivor_supply_rebuild` | `s264_aia` | `11651` | `11651` | `held_no_mt5_until_nonzero_signal_supply_proof` |
| `s262_guardrail_supply_rebuild` | `s262_lih` | `11651` | `11651` | `held_no_mt5_until_nonzero_signal_supply_proof` |

## Boundary(경계)

- 이 run(실행)은 materialization only(물질화 전용)이며 아직 fresh KPI(새 핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), trade list(거래 목록)는 없다.
- `q04`는 no-MT5 diagnostic(무 MT5 진단)이다. 실행은 공급 증명과 handoff/tooling repair(인계/도구 수리)가 생긴 뒤에만 재개한다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Artifact Lineage(산출물 계보)

- source_queue(원천 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DP/runtime_gap_aware_fourth_followup_or_prune_design/materialization_queue.csv`
- source_variant_manifest(원천 변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DL/shared_weakness_breakout_third_followup_or_prune_materialization/variant_manifest.csv`
- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DQ/runtime_gap_aware_fourth_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DQ/runtime_gap_aware_fourth_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DQ/runtime_gap_aware_fourth_followup_or_prune_materialization/attempt_manifest.csv`
- pre_runtime_supply_diagnostic(런타임 전 공급 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DQ/runtime_gap_aware_fourth_followup_or_prune_materialization/pre_runtime_supply_diagnostic.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DQ/runtime_gap_aware_fourth_followup_or_prune_materialization/runtime_contract.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DQ/runtime_gap_aware_fourth_followup_or_prune_materialization/review_result.json`
