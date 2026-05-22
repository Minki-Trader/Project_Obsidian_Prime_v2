# Stage267 Run267DU Runtime Gap Aware Fifth Follow-Up/Prune Materialization(267단계 267DU 런타임 공백 반영 5차 후속/가지치기 물질화)

- status(상태): `run267DU_runtime_gap_aware_fifth_followup_or_prune_materialized_execution_pending`
- parent_run(부모 실행): `run267DT_stage267_runtime_gap_aware_fifth_followup_or_prune_design_v1`
- variants(변형): `9`
- attempts(시도): `9`
- aggressive_variants(공격형 변형): `5`
- held_queue_rows(보류 대기열 행): `2`
- diagnostics(진단): `4`
- next_action(다음 행동): `run267DV_execute_runtime_gap_aware_fifth_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DU(267DU 실행)는 run267DT(267DT 실행)의 설계 queue(대기열)를 MT5(MetaTrader 5, 메타트레이더5) 실행 가능한 입력으로 바꿨다.
효과: s258_stc(258 STC)는 table handoff repair(테이블 인계 수리)와 aggressive noncalendar impulse(공격형 비달력 충격)를 분리했고, s264_aih(264 AIH)는 validation anchor(검증 앵커)와 2026.04 final month(2026년 4월 마지막 표본외 월)를 직접 압박하게 했다.
s264_lc(264 LC)는 same-month control(같은 월 대조)로만 남겼고, s264_aia/s262_lih(264 AIA/262 LIH)는 blind retry(무작정 재시도) 없이 supply diagnostic(공급 진단)으로 보류했다.

## Queue Decisions(대기열 판단)

| queue_id(대기열 ID) | decision(판단) | variants(변형) | attempts(시도) |
|---|---|---:|---:|
| `q01_s258_supply_continuity_table_handoff_repair` | materialized_for_mt5_execution | 3 | 3 |
| `q02_s258_noncalendar_impulse_reentry_cross_period` | materialized_for_mt5_execution | 3 | 3 |
| `q03_s264_aih_explosive_shock_state_oos_final_month` | materialized_for_mt5_execution | 2 | 2 |
| `q04_s264_lc_defensive_dd_cluster_control` | materialized_for_mt5_execution | 1 | 1 |
| `q05_s264_aia_s262_lih_supply_manifest_diagnostic` | diagnostic_only_no_mt5_scheduled | 0 | 0 |
| `q06_s264_aih_s258_similar_feature_replacement` | held_until_q02_q03_shape_available | 0 | 0 |

## Boundary(경계)

이 실행은 materialization(물질화)이다. 아직 MT5 KPI(MT5 핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), Adapter finalization(어댑터 최종화), ONNX parity(ONNX 동등성)는 없다.
따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 주장하지 않는다.

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DU/runtime_gap_aware_fifth_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DU/runtime_gap_aware_fifth_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DU/runtime_gap_aware_fifth_followup_or_prune_materialization/attempt_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DU/runtime_gap_aware_fifth_followup_or_prune_materialization/runtime_contract.csv`
- preflight_handoff_receipt(사전 인계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DU/runtime_gap_aware_fifth_followup_or_prune_materialization/preflight_handoff_receipt.csv`
- supply_diagnostic(공급 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DU/runtime_gap_aware_fifth_followup_or_prune_materialization/pre_runtime_supply_diagnostic.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DU/runtime_gap_aware_fifth_followup_or_prune_materialization/gate_audit.csv`
