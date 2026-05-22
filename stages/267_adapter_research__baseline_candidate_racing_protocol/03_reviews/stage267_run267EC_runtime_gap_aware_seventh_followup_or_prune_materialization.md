# Stage267 Run267EC Runtime Gap Aware Seventh Follow-Up/Prune Materialization(267단계 267EC 런타임 공백 반영 7차 후속/가지치기 물질화)

- status(상태): `run267EC_runtime_gap_aware_seventh_followup_or_prune_materialized_execution_pending`
- source_run(원천 실행): `run267EB_stage267_runtime_gap_aware_seventh_followup_or_prune_design_v1`
- source_materialization(원천 물질화): `run267DY_stage267_runtime_gap_aware_sixth_followup_or_prune_materialization_v1`
- variants(변형): `14`
- attempts(시도): `14`
- held_rows(보류 행): `1`
- aggressive_attempts(공격형 시도): `5`
- coverage_variants(커버리지 변형): `4`
- next_action(다음 행동): `run267ED_execute_runtime_gap_aware_seventh_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267EC(267EC 실행)는 run267EB(267EB 실행)의 8개 queue(대기열)를 실제 MT5(MetaTrader 5, 메타트레이더5) 입력으로 바꾼 단계다.
q01-q02는 s258_stc의 2025H1/H2 생존 압박을 따로 본다. q03은 s258_stc의 aggressive/explosive(공격/폭발) 공급 실험을 2023H2, 2025H1, 2025H2로 나눴다.
q04-q06은 s264_aih 검증 앵커, 2026.04 제한 수리, 공격형 역임펄스를 분리했다. s264_lc는 같은 달 시장 대조(control, 대조)로만 둔다.
q07은 빠졌던 s262_lih와 s264_aia를 validation(검증)과 2026.04 final month(마지막 달)에 다시 붙였다. q08은 필터 누적 방지 held(보류)로 남겼다.

## Queue Decision(대기열 판단)

| queue_id(대기열 ID) | decision(판단) | variants(변형) | attempts(시도) | held(보류) |
|---|---|---:|---:|---:|
| `q01_s258_2025h1_period_survival_gate` | materialized_for_mt5_execution | 1 | 1 | 0 |
| `q02_s258_2025h2_period_survival_gate` | materialized_for_mt5_execution | 1 | 1 | 0 |
| `q03_s258_explosive_impulse_supply_probe` | materialized_for_mt5_execution | 3 | 3 | 0 |
| `q04_s264_aih_validation_anchor_integrity_check` | materialized_for_mt5_execution | 1 | 1 | 0 |
| `q05_s264_aih_202604_counter_shock_rebuild` | materialized_for_mt5_execution | 2 | 2 | 0 |
| `q06_s264_aih_explosive_counter_impulse_probe` | materialized_for_mt5_execution | 2 | 2 | 0 |
| `q07_s262_s264_aia_pool_coverage_rejoin` | materialized_for_mt5_execution | 4 | 4 | 0 |
| `q08_filter_stack_prune_guard_hold` | held_guardrail_only_no_standalone_mt5(가드레일 전용 보류, 단독 MT5 없음) | 0 | 0 | 1 |

## Attempts(시도)

| attempt(시도) | candidate(후보) | split(구간) | role(역할) |
|---|---|---|---|
| `run267ec_01_s258_stc_2025h1_period_survival_gate_2025h1` | `s258_stc` | `adjacent_2025_h1_validation_post_2024` | `period_survival_gate_2025h1` |
| `run267ec_02_s258_stc_2025h2_period_survival_gate_2025h2` | `s258_stc` | `adjacent_2025_h2_oos_followthrough` | `period_survival_gate_2025h2` |
| `run267ec_03_s258_stc_2023h2_explosive_impulse_supply_2023h2` | `s258_stc` | `adjacent_2023_h2_train_pre_2024` | `explosive_impulse_supply_2023h2` |
| `run267ec_04_s258_stc_2025h1_explosive_impulse_supply_2025h1` | `s258_stc` | `adjacent_2025_h1_validation_post_2024` | `explosive_impulse_supply_2025h1` |
| `run267ec_05_s258_stc_2025h2_explosive_impulse_supply_2025h2` | `s258_stc` | `adjacent_2025_h2_oos_followthrough` | `explosive_impulse_supply_2025h2` |
| `run267ec_06_s264_aih_validation_anchor_integrity_validation_is` | `s264_aih` | `validation_is` | `validation_anchor_integrity` |
| `run267ec_07_s264_aih_202604_counter_shock_rebuild_202604` | `s264_aih` | `oos_final_month_2026_04` | `final_month_counter_shock_rebuild` |
| `run267ec_08_s264_lc_202604_counter_shock_control_202604` | `s264_lc` | `oos_final_month_2026_04` | `paired_final_month_control` |
| `run267ec_09_s264_aih_validation_explosive_counter_impulse_validation_is` | `s264_aih` | `validation_is` | `validation_explosive_counter_impulse` |
| `run267ec_10_s264_aih_202604_explosive_counter_impulse_202604` | `s264_aih` | `oos_final_month_2026_04` | `final_month_explosive_counter_impulse` |
| `run267ec_11_s262_lih_validation_coverage_rejoin_validation_is` | `s262_lih` | `validation_is` | `coverage_rejoin_validation` |
| `run267ec_12_s262_lih_202604_coverage_rejoin_202604` | `s262_lih` | `oos_final_month_2026_04` | `coverage_rejoin_final_month` |
| `run267ec_13_s264_aia_validation_coverage_rejoin_validation_is` | `s264_aia` | `validation_is` | `coverage_rejoin_validation` |
| `run267ec_14_s264_aia_202604_coverage_rejoin_202604` | `s264_aia` | `oos_final_month_2026_04` | `coverage_rejoin_final_month` |

## Boundary(경계)

run267EC(267EC 실행)는 materialization(물질화)이다. 아직 MT5(MetaTrader 5, 메타트레이더5) 성능 결과, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)는 없다.
따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EC/runtime_gap_aware_seventh_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EC/runtime_gap_aware_seventh_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EC/runtime_gap_aware_seventh_followup_or_prune_materialization/attempt_manifest.csv`
- preflight_handoff_receipt(사전 인계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EC/runtime_gap_aware_seventh_followup_or_prune_materialization/preflight_handoff_receipt.csv`
- anti_filter_stack_receipt(필터 누적 방지 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EC/runtime_gap_aware_seventh_followup_or_prune_materialization/anti_filter_stack_receipt.csv`
- pool_coverage_receipt(후보군 커버리지 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EC/runtime_gap_aware_seventh_followup_or_prune_materialization/pool_coverage_receipt.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EC/runtime_gap_aware_seventh_followup_or_prune_materialization/review_result.json`
