# Stage267 Run267CZ Second Follow-up/Prune Materialization(267단계 267CZ 2차 후속/가지치기 물질화)

- status(상태): `run267CZ_shared_weakness_breakout_second_followup_or_prune_materialized_execution_pending`
- variants(변형): `7`
- attempts(시도): `14`
- materialized_queue_rows(물질화 대기열 행): `4`
- held_rows(보류 행): `2`
- next_action(다음 행동): `run267DA_execute_shared_weakness_breakout_second_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 판독)

run267CZ(267CZ 실행)는 run267CY(267CY 실행)의 queue(대기열)를 실제 MT5(MetaTrader 5, 메타트레이더5) 입력으로 바꿨다.
Effect(효과): explosive second-survival(폭발형 2차 생존), s264_aia validation damage(검증 손상), s264_aih final supply(최종 공급), control rejoin(대조 재합류)을 다음 실행에서 바로 볼 수 있다.

q01 redzone cross-period(위험 구역 확장 기간)와 q05 ablation/replacement(제거/대체)는 held(보류)다.
Effect(효과): 2024-only(2024년 전용) 파일로 확장 기간 근거를 꾸미지 않고, 생존 후보가 나온 뒤 제거/대체를 붙이게 했다.

## Queue Decisions(대기열 판단)

| queue(대기열) | decision(판단) | effect(효과) |
|---|---|---|
| `cy_q01_s258_redzone_cross_period_survival` | `held_for_dedicated_adjacent_period_redzone_pack(전용 인접 기간 위험 구역 묶음까지 보류)` | 이 queue(대기열)는 2023H2/2025H1/2025H2 redzone feature frames(위험 구역 피처 프레임)가 필요하다. run267CZ(267CZ 실행)는 2024-only files(2024년 전용 파일)로 cross-period evidence(확장 기간 근거)를 꾸미지 않는다. |
| `cy_q02_explosive_combo_cross_period_prune_gate` | `materialized_execution_pending(물질화 완료, 실행 대기)` | 3개 variant rows(변형 행)를 MT5 input attempts(MT5 입력 시도)로 바꿨다. |
| `cy_q03_s264_aia_validation_damage_probe` | `materialized_execution_pending(물질화 완료, 실행 대기)` | 1개 variant rows(변형 행)를 MT5 input attempts(MT5 입력 시도)로 바꿨다. |
| `cy_q04_aih_final_supply_or_prune` | `materialized_execution_pending(물질화 완료, 실행 대기)` | 1개 variant rows(변형 행)를 MT5 input attempts(MT5 입력 시도)로 바꿨다. |
| `cy_q05_feature_reliance_ablation_replacement` | `held_until_p0_survivors_exist(P0 생존 후보가 나온 뒤까지 보류)` | Feature ablation/replacement(피처 제거/대체)는 q02/q03/q04에서 survivors(생존 후보)가 나온 뒤에만 의미가 있음; 그렇지 않으면 이미 죽은 branch(분기)만 제거하게 됨. |
| `cy_q06_control_rejoin_guardrail` | `materialized_execution_pending(물질화 완료, 실행 대기)` | 2개 variant rows(변형 행)를 MT5 input attempts(MT5 입력 시도)로 바꿨다. |

## Variants(변형)

| variant(변형) | candidate(후보) | profile(프로필) | queue(대기열) |
|---|---|---|---|
| `run267cz_01_s258_stc_explosive_second` | `s258_stc` | `explosive_second_survival` | `cy_q02_explosive_combo_cross_period_prune_gate` |
| `run267cz_02_s264_aia_explosive_second` | `s264_aia` | `explosive_second_survival` | `cy_q02_explosive_combo_cross_period_prune_gate` |
| `run267cz_03_s264_aih_explosive_second` | `s264_aih` | `explosive_second_survival` | `cy_q02_explosive_combo_cross_period_prune_gate` |
| `run267cz_04_s264_aia_aia_val_damage` | `s264_aia` | `aia_validation_damage_probe` | `cy_q03_s264_aia_validation_damage_probe` |
| `run267cz_05_s264_aih_aih_final_supply` | `s264_aih` | `aih_final_supply_or_prune` | `cy_q04_aih_final_supply_or_prune` |
| `run267cz_06_s264_lc_control_rejoin` | `s264_lc` | `control_rejoin_guardrail_identity` | `cy_q06_control_rejoin_guardrail` |
| `run267cz_07_s262_lih_control_rejoin` | `s262_lih` | `control_rejoin_guardrail_identity` | `cy_q06_control_rejoin_guardrail` |

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CZ/shared_weakness_breakout_second_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CZ/shared_weakness_breakout_second_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CZ/shared_weakness_breakout_second_followup_or_prune_materialization/attempt_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CZ/shared_weakness_breakout_second_followup_or_prune_materialization/runtime_contract.csv`
- held_queue(보류 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CZ/shared_weakness_breakout_second_followup_or_prune_materialization/held_queue.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CZ/shared_weakness_breakout_second_followup_or_prune_materialization/review_result.json`

## Boundary(경계)

run267CZ(267CZ 실행)는 materialization(물질화)이다. MT5(MetaTrader 5, 메타트레이더5) 실행 결과, balance/equity curve(잔액/평가금 곡선), selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비)는 주장하지 않는다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`
