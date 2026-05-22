# Stage267 Run267EO Runtime Gap Aware Tenth Follow-Up/Prune Materialization(267단계 267EO 런타임 공백 반영 10차 후속/가지치기 물질화)

- status(상태): `run267EO_runtime_gap_aware_tenth_followup_or_prune_materialized_execution_pending`
- source_run(원천 실행): `run267EN_stage267_runtime_gap_aware_tenth_followup_or_prune_design_v1`
- variants(변형): `12`
- attempts(시도): `12`
- held_rows(보류 행): `1`
- handoff_precheck_attempts(인계 사전검사 시도): `4`
- shared_state_attempts(공유 상태 시도): `4`
- identity_attempts(정체성 감사 시도): `2`
- aggressive_attempts(공격 시도): `2`
- next_action(다음 행동): `run267EP_execute_runtime_gap_aware_tenth_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267EO(267EO 실행)는 run267EN(267EN 실행)의 설계를 MT5(MetaTrader 5, 메타트레이더5)가 실행할 수 있는 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.
효과: blocked row(차단 행)는 handoff precheck(인계 사전검사)로 먼저 분리하고, 2026.04 weakness(약점)는 same-month filter(같은 월 필터)가 아니라 shared-state feature pivot(공유 상태 피처 전환)으로 물질화했다.
효과: s262_lih와 s264_aia는 identity audit(정체성 감사)로 다시 묶었고, q04 validation watch(검증 관찰)는 단독 실행하지 않고 held(보류)로 남겼다.
효과: aggressive non-filter(공격형 비필터) 시도 2개를 포함해 방어 필터만 쌓는 흐름을 피했다.

## Queue Decision(대기열 판단)

| queue_id(대기열 ID) | decision(판단) | variants(변형) | attempts(시도) | held(보류) |
|---|---|---:|---:|---:|
| `q01_runtime_handoff_gap_bounded_precheck` | materialized_for_mt5_execution | 4 | 4 | 0 |
| `q02_202604_shared_state_feature_pivot` | materialized_for_mt5_execution | 4 | 4 | 0 |
| `q03_s262_s264_aia_signature_identity_audit` | materialized_for_mt5_execution | 2 | 2 | 0 |
| `q04_validation_low_pf_wide_period_watch` | held_watch_anchor_only_no_standalone_mt5 | 0 | 0 | 1 |
| `q05_aggressive_non_filter_reentry_after_precheck` | materialized_conditional_aggressive_after_precheck | 2 | 2 | 0 |

## Attempts(시도)

| attempt(시도) | candidate(후보) | queue(대기열) | role(역할) | dependency(의존성) |
|---|---|---|---|---|
| `run267eo_01_s258_stc_2025h1_survival_handoff_precheck_2025h1` | `s258_stc` | `q01_runtime_handoff_gap_bounded_precheck` | `survival_handoff_precheck_2025h1` | `none` |
| `run267eo_02_s258_stc_2025h2_explosive_handoff_precheck_2025h2` | `s258_stc` | `q01_runtime_handoff_gap_bounded_precheck` | `explosive_handoff_precheck_2025h2` | `none` |
| `run267eo_03_s264_aih_validation_explosive_handoff_precheck_validation` | `s264_aih` | `q01_runtime_handoff_gap_bounded_precheck` | `validation_explosive_handoff_precheck` | `none` |
| `run267eo_04_s264_aih_202604_explosive_handoff_precheck_202604` | `s264_aih` | `q01_runtime_handoff_gap_bounded_precheck` | `final_month_explosive_handoff_precheck` | `none` |
| `run267eo_05_s264_aih_202604_shared_state_pivot_202604` | `s264_aih` | `q02_202604_shared_state_feature_pivot` | `shared_state_pivot_core_202604` | `none` |
| `run267eo_06_s264_lc_202604_shared_state_control_202604` | `s264_lc` | `q02_202604_shared_state_feature_pivot` | `shared_state_control_202604` | `none` |
| `run267eo_07_s262_lih_202604_shared_state_pivot_202604` | `s262_lih` | `q02_202604_shared_state_feature_pivot` | `shared_state_validation_heavy_202604` | `none` |
| `run267eo_08_s264_aia_202604_shared_state_pivot_202604` | `s264_aia` | `q02_202604_shared_state_feature_pivot` | `shared_state_oos_anchor_202604` | `none` |
| `run267eo_09_s262_lih_validation_identity_receipt_validation` | `s262_lih` | `q03_s262_s264_aia_signature_identity_audit` | `identity_surface_receipt_s262` | `none` |
| `run267eo_10_s264_aia_validation_identity_receipt_validation` | `s264_aia` | `q03_s262_s264_aia_signature_identity_audit` | `identity_surface_receipt_s264_aia` | `none` |
| `run267eo_11_s258_stc_aggressive_nonfilter_reentry_2025h1` | `s258_stc` | `q05_aggressive_non_filter_reentry_after_precheck` | `aggressive_nonfilter_reentry_s258` | `requires_q01_precheck_receipt_before_interpretation` |
| `run267eo_12_s264_aih_aggressive_nonfilter_reentry_202604` | `s264_aih` | `q05_aggressive_non_filter_reentry_after_precheck` | `aggressive_nonfilter_reentry_s264_aih` | `requires_q01_precheck_receipt_before_interpretation` |

## Boundary(경계)

run267EO(267EO 실행)는 materialization(물질화)이다. 아직 MT5(MetaTrader 5, 메타트레이더5) 성능 결과, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)는 없다.
따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EO/runtime_gap_aware_tenth_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EO/runtime_gap_aware_tenth_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EO/runtime_gap_aware_tenth_followup_or_prune_materialization/attempt_manifest.csv`
- preflight_handoff_receipt(사전 인계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EO/runtime_gap_aware_tenth_followup_or_prune_materialization/preflight_handoff_receipt.csv`
- pool_coverage_receipt(후보군 커버리지 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EO/runtime_gap_aware_tenth_followup_or_prune_materialization/pool_coverage_receipt.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EO/runtime_gap_aware_tenth_followup_or_prune_materialization/runtime_parity_receipt.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EO/runtime_gap_aware_tenth_followup_or_prune_materialization/review_result.json`
