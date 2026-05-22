# Stage267 Run267DY Runtime Gap Aware Sixth Follow-Up/Prune Materialization(267단계 267DY 런타임 공백 반영 6차 후속/가지치기 물질화)

- status(상태): `run267DY_runtime_gap_aware_sixth_followup_or_prune_materialized_execution_pending`
- source_run(원천 실행): `run267DX_stage267_runtime_gap_aware_sixth_followup_or_prune_design_v1`
- variants(변형): `9`
- attempts(시도): `9`
- held_rows(보류 행): `1`
- aggressive_or_explosive_attempts(공격/폭발 시도): `4`
- next_action(다음 행동): `run267DZ_execute_runtime_gap_aware_sixth_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DY(267DY 실행)는 run267DX(267DX 실행)의 설계를 MT5(MetaTrader 5, 메타트레이더5)가 실행할 수 있는 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.
효과: s258_stc(258 STC 후보)는 DD(drawdown, 손실폭) 구조 분리 3개와 불리 구간 반증 3개로 나뉘었다.
효과: s264_aih(264 AIH 후보)는 validation anchor(검증 앵커) 1회 수리와 2026.04 counter shock(반대 충격) 탐침으로 제한했다.
효과: s264_lc(264 LC 후보)는 q03/q04 해석용 같은 달 control(대조)로만 물질화했다.
효과: q06 filter-stack(필터 누적) 분기는 단독 실행하지 않고 held(보류)로 기록했다.

## Queue Decision(대기열 판단)

| queue_id(대기열 ID) | decision(판단) | variants(변형) | attempts(시도) |
|---|---|---:|---:|
| `q01_s258_stc_structural_dd_shape_split` | materialized_for_mt5_execution | 3 | 3 |
| `q02_s258_stc_adverse_slice_falsification` | materialized_for_mt5_execution | 3 | 3 |
| `q03_s264_aih_validation_anchor_one_repair` | materialized_for_mt5_execution | 1 | 1 |
| `q04_s264_aih_counter_shock_final_month_probe` | materialized_for_mt5_execution | 1 | 1 |
| `q05_s264_lc_same_month_control_hold` | materialized_as_paired_control(쌍 대조로 물질화) | 1 | 1 |
| `q06_prune_micro_filter_stack` | guardrail_only_no_standalone_mt5(가드레일 전용, 단독 MT5 없음) | 0 | 0 |

## Attempts(시도)

| attempt(시도) | candidate(후보) | split(구간) | role(역할) |
|---|---|---|---|
| `run267dy_01_s258_stc_2023h2_dd_shape_split_2023h2` | `s258_stc` | `adjacent_2023_h2_train_pre_2024` | `structural_dd_shape_split` |
| `run267dy_02_s258_stc_2025h1_dd_shape_split_2025h1` | `s258_stc` | `adjacent_2025_h1_validation_post_2024` | `structural_dd_shape_split` |
| `run267dy_03_s258_stc_2025h2_dd_shape_split_2025h2` | `s258_stc` | `adjacent_2025_h2_oos_followthrough` | `structural_dd_shape_split` |
| `run267dy_04_s258_stc_2023h2_state_falsification_2023h2` | `s258_stc` | `adjacent_2023_h2_train_pre_2024` | `adverse_slice_state_falsification` |
| `run267dy_05_s258_stc_2025h1_state_falsification_2025h1` | `s258_stc` | `adjacent_2025_h1_validation_post_2024` | `adverse_slice_state_falsification` |
| `run267dy_06_s258_stc_2025h2_state_falsification_2025h2` | `s258_stc` | `adjacent_2025_h2_oos_followthrough` | `adverse_slice_state_falsification` |
| `run267dy_07_s264_aih_validation_anchor_repair_validation_is` | `s264_aih` | `validation_is` | `validation_anchor_one_repair` |
| `run267dy_08_s264_aih_202604_counter_shock_probe_202604` | `s264_aih` | `oos_final_month_2026_04` | `counter_shock_final_month_falsification` |
| `run267dy_09_s264_lc_202604_same_month_control_202604` | `s264_lc` | `oos_final_month_2026_04` | `paired_same_month_control` |

## Boundary(경계)

run267DY(267DY 실행)는 materialization(물질화)이다. MT5(MetaTrader 5, 메타트레이더5) 성능 결과와 balance/equity curve(잔액/평가금 곡선) 검토는 아직 없다.
따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DY/runtime_gap_aware_sixth_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DY/runtime_gap_aware_sixth_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DY/runtime_gap_aware_sixth_followup_or_prune_materialization/attempt_manifest.csv`
- preflight_handoff_receipt(사전 인계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DY/runtime_gap_aware_sixth_followup_or_prune_materialization/preflight_handoff_receipt.csv`
- anti_filter_stack_receipt(필터 누적 방지 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DY/runtime_gap_aware_sixth_followup_or_prune_materialization/anti_filter_stack_receipt.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DY/runtime_gap_aware_sixth_followup_or_prune_materialization/review_result.json`
