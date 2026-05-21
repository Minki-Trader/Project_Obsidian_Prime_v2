# Stage267 Run267CV Shared Weakness Follow-up/Prune Materialization(267단계 267CV 공유 약점 후속/가지치기 물질화)

- status(상태): `run267CV_shared_weakness_breakout_followup_or_prune_materialized_execution_pending`
- variants(변형): `5`
- attempts(시도): `10`
- held_queue_rows(보류 대기열 행): `3`
- score_table_validation_passed(점수표 검증 통과): `5`
- aggressive_variants(공격형 변형): `5`
- next_action(다음 행동): `run267CW_execute_shared_weakness_breakout_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267CV(267CV 실행)는 run267CU(267CU 실행)의 materialization queue(물질화 대기열) 중 지금 바로 MT5(MetaTrader 5, 메타트레이더5) 입력으로 만들 수 있는 축만 물질화했다.
효과: redzone Monday/DD pressure(위험 구역 월요일/손실폭 압박), explosive shock-state combo(폭발형 충격-상태 조합), s264_aih supply repair(s264_aih 공급 수리)를 `.set/.ini`, feature CSV(피처 CSV), model CSV(모델 CSV)로 만들었다.

cross-period state_phase(확장 기간 상태 구간)와 feature ablation/replacement(피처 제거/대체)는 아직 가짜로 만들지 않았다.
효과: 기간별 feature frame(피처 프레임)이나 P0/P1 실행 결과가 필요한 작업은 held(보류)로 기록되어, 다음 연구가 허술한 근거로 이어지지 않는다.

## Materialized Variants(물질화된 변형)

| variant(변형) | candidate(후보) | profile(프로필) | source_profile(원천 프로필) | feature_count(피처 수) |
|---|---|---|---|---:|
| `run267cv_01_s258_stc_redzone_monday_dd` | `s258_stc` | `redzone_monday_dd_pressure` | `redzone_stress_blast` | 38 |
| `run267cv_02_s264_aih_aih_supply_repair` | `s264_aih` | `aih_aggressive_supply_repair` | `aggressive_shock_supply_expansion` | 38 |
| `run267cv_03_s264_aih_explosive_combo` | `s264_aih` | `explosive_shock_state_combo` | `state_phase_monday_replacement` | 38 |
| `run267cv_04_s264_aia_explosive_combo` | `s264_aia` | `explosive_shock_state_combo` | `state_phase_monday_replacement` | 38 |
| `run267cv_05_s258_stc_explosive_combo` | `s258_stc` | `explosive_shock_state_combo` | `redzone_stress_blast` | 38 |

## Queue Decisions(대기열 판단)

| queue(대기열) | decision(판단) | effect(효과) |
|---|---|---|
| `cu_q01_balanced_pair_cross_period_pressure` | held_for_true_adjacent_period_state_phase_feature_frames | 2023H2/2025H1/2025H2 state_phase feature frames are required; run267CV does not fake cross-period pressure from 2024 files. |
| `cu_q02_s258_redzone_monday_dd_pressure` | materialized_execution_pending | 1 variant rows were converted into feature/model/set/ini inputs. |
| `cu_q03_control_guardrail_retest` | held_until_p0_outputs_to_avoid_duplicate_retest | Control and guardrail retest should consume finalized P0 outputs, not duplicate the already-executed run267CS controls. |
| `cu_q04_aih_aggressive_supply_repair_or_prune` | materialized_execution_pending | 1 variant rows were converted into feature/model/set/ini inputs. |
| `cu_q05_explosive_shock_state_combo` | materialized_execution_pending | 3 variant rows were converted into feature/model/set/ini inputs. |
| `cu_q06_feature_reliance_ablation_replacement_audit` | held_until_p0_p1_survivors_define_ablation_scope | Feature ablation/replacement audit is meaningful only after run267CV P0/P1 candidates survive execution and curve review. |

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CV/shared_weakness_breakout_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CV/shared_weakness_breakout_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CV/shared_weakness_breakout_followup_or_prune_materialization/attempt_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CV/shared_weakness_breakout_followup_or_prune_materialization/runtime_contract.csv`
- held_queue(보류 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CV/shared_weakness_breakout_followup_or_prune_materialization/held_queue.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CV/shared_weakness_breakout_followup_or_prune_materialization/review_result.json`

## Boundary(경계)

run267CV(267CV 실행)는 execution pending(실행 대기) 물질화다. 아직 MT5 실행, balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질) 판정은 없다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`
