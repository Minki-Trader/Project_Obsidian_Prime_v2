# Stage267 Run267EG Runtime Gap Aware Eighth Follow-Up/Prune Materialization(267단계 267EG 런타임 공백 반영 8차 후속/가지치기 물질화)

- status(상태): `run267EG_runtime_gap_aware_eighth_followup_or_prune_materialized_execution_pending`
- source_run(원천 실행): `run267EF_stage267_runtime_gap_aware_eighth_followup_or_prune_design_v1`
- source_materialization(원천 물질화): `run267EC_stage267_runtime_gap_aware_seventh_followup_or_prune_materialization_v1`
- variants(변형): `15`
- attempts(시도): `15`
- held_rows(보류 행): `1`
- covered_candidates(커버된 후보): `5/5`
- aggressive_attempts(공격형 시도): `4`
- next_action(다음 행동): `run267EH_execute_runtime_gap_aware_eighth_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267EG(267EG 실행)는 후보를 뽑은 것이 아니다. run267EF(267EF 실행)의 materialization queue(물질화 대기열)를 MT5(MetaTrader 5, 메타트레이더5)가 실행할 수 있는 입력으로 바꾼 단계다.
효과는 다음 run267EH(267EH 실행)에서 s258_stc 생존성, s264_aih 제한 수리, 2026.04 공유 매도 취약성, s262/s264_aia feature order(피처 순서), 공격형 handoff(인계)를 같은 묶음으로 검증할 수 있다는 것이다.

baseline candidate(기준 후보) 정리가 오래 걸리는 이유는 숫자 1등을 뽑는 일이 아니기 때문이다. 각 후보가 여러 기간, 약한 구간, feature/order(피처/순서), runtime handoff(런타임 인계)에서 덜 깨지는지 확인해야 한다.

## Queue Decision(대기열 판단)

| queue_id(대기열 ID) | decision(판단) | variants(변형) | attempts(시도) | held(보류) |
|---|---|---:|---:|---:|
| `q01_s258_period_survival_quality_split` | materialized_for_mt5_execution | 2 | 2 | 0 |
| `q02_s258_explosive_init_failure_triage` | materialized_for_mt5_execution | 2 | 2 | 0 |
| `q03_s264_aih_validation_final_month_bounded_repair` | materialized_for_mt5_execution | 3 | 3 | 0 |
| `q04_pool_202604_shared_sell_fragility_pressure` | materialized_for_mt5_execution | 4 | 4 | 0 |
| `q05_s262_s264_aia_identity_and_feature_order_audit` | materialized_for_mt5_execution | 2 | 2 | 0 |
| `q06_s264_aih_explosive_counter_impulse_handoff_triage` | materialized_for_mt5_execution | 2 | 2 | 0 |
| `q07_pool_prune_guard_and_next_pivot_receipt` | held_guardrail_only_no_standalone_mt5(가드레일 보류, 단독 MT5 없음) | 0 | 0 | 1 |

## Attempts(시도)

| attempt(시도) | candidate(후보) | split(구간) | role(역할) |
|---|---|---|---|
| `run267eg_01_s258_stc_2025h1_survival_quality_recheck_2025h1` | `s258_stc` | `adjacent_2025_h1_validation_post_2024` | `survival_quality_recheck_2025h1` |
| `run267eg_02_s258_stc_2025h2_survival_quality_recheck_2025h2` | `s258_stc` | `adjacent_2025_h2_oos_followthrough` | `survival_quality_recheck_2025h2` |
| `run267eg_03_s258_stc_2025h1_explosive_handoff_triage_2025h1` | `s258_stc` | `adjacent_2025_h1_validation_post_2024` | `explosive_handoff_triage_2025h1` |
| `run267eg_04_s258_stc_2025h2_explosive_handoff_triage_2025h2` | `s258_stc` | `adjacent_2025_h2_oos_followthrough` | `explosive_handoff_triage_2025h2` |
| `run267eg_05_s264_aih_validation_integrity_recheck_validation_is` | `s264_aih` | `validation_is` | `validation_integrity_recheck` |
| `run267eg_06_s264_aih_202604_bounded_repair_202604` | `s264_aih` | `oos_final_month_2026_04` | `final_month_bounded_repair` |
| `run267eg_07_s264_lc_202604_paired_control_202604` | `s264_lc` | `oos_final_month_2026_04` | `paired_final_month_control` |
| `run267eg_08_s264_aih_202604_shared_sell_pressure_202604` | `s264_aih` | `oos_final_month_2026_04` | `shared_sell_fragility_pressure` |
| `run267eg_09_s264_lc_202604_shared_sell_pressure_202604` | `s264_lc` | `oos_final_month_2026_04` | `shared_sell_fragility_pressure` |
| `run267eg_10_s262_lih_202604_shared_sell_pressure_202604` | `s262_lih` | `oos_final_month_2026_04` | `shared_sell_fragility_pressure` |
| `run267eg_11_s264_aia_202604_shared_sell_pressure_202604` | `s264_aia` | `oos_final_month_2026_04` | `shared_sell_fragility_pressure` |
| `run267eg_12_s262_lih_validation_identity_audit_validation_is` | `s262_lih` | `validation_is` | `identity_feature_order_audit_validation` |
| `run267eg_13_s264_aia_validation_identity_audit_validation_is` | `s264_aia` | `validation_is` | `identity_feature_order_audit_validation` |
| `run267eg_14_s264_aih_validation_explosive_handoff_triage_validation_is` | `s264_aih` | `validation_is` | `validation_explosive_handoff_triage` |
| `run267eg_15_s264_aih_202604_explosive_handoff_triage_202604` | `s264_aih` | `oos_final_month_2026_04` | `final_month_explosive_handoff_triage` |

## Boundary(경계)

run267EG(267EG 실행)는 materialization(물질화)이다. 아직 MT5(MetaTrader 5, 메타트레이더5) 성능 결과, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)는 없다.
따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EG/runtime_gap_aware_eighth_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EG/runtime_gap_aware_eighth_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EG/runtime_gap_aware_eighth_followup_or_prune_materialization/attempt_manifest.csv`
- preflight_handoff_receipt(사전 인계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EG/runtime_gap_aware_eighth_followup_or_prune_materialization/preflight_handoff_receipt.csv`
- pool_coverage_receipt(후보군 커버리지 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EG/runtime_gap_aware_eighth_followup_or_prune_materialization/pool_coverage_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EG/runtime_gap_aware_eighth_followup_or_prune_materialization/result_judgment.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EG/runtime_gap_aware_eighth_followup_or_prune_materialization/gate_audit.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EG/runtime_gap_aware_eighth_followup_or_prune_materialization/review_result.json`
