# Stage267 Run267CN Shared Weakness Breakout Materialization(267단계 267CN 공유 약점 돌파 물질화)

## Summary(요약)

- run_id(실행 ID): `run267CN_stage267_pool_wide_shared_weakness_breakout_materialization_v1`
- parent_run(상위 실행): `run267CM_stage267_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_v1`
- source_materialization(원천 물질화): `run267CF_stage267_pool_wide_orthogonal_loss_shape_state_materialization_v1`
- status(상태): `run267CN_pool_wide_shared_weakness_breakout_materialized_execution_pending`
- queue_rows(대기열 행): `4`
- materialized_variants(물질화 변형): `6`
- materialized_attempts(물질화 시도): `12`
- control_receipts(대조 영수증): `2`
- guardrail_receipts(가드레일 영수증): `2`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267CM(267CM 실행)의 shared weakness/state breakout(공유 약점/상태 돌파) 큐를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다.
Effect(효과): 다음 run267CO(267CO 실행)에서 headline KPI(대표 핵심 성과 지표)가 아니라 weak slice(약점 구간), curve(곡선), trade quality(거래 품질)로 다시 깨뜨려 볼 수 있다.

## Queue Decision(대기열 판단)

| queue(대기열) | candidates(후보) | decision(판단) | effect(효과) |
| --- | --- | --- | --- |
| `run267cn_q01_shared_monday_december_state_interaction` | `s264_aih;s264_lc;s262_lih;s264_aia;s258_stc` | `materialized_execution_pending` | `5`개 variant rows(변형 행)을 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다 |
| `run267cn_q02_s264_aih_aggressive_shock_release_reentry` | `s264_aih` | `materialized_execution_pending` | `1`개 variant rows(변형 행)을 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다 |
| `run267cn_q03_anchor_control_holdout_trace` | `s264_lc;s264_aia` | `control_holdout_receipt_no_new_attempt` | run267CJ/run267CL(267CJ/267CL 실행)의 수익 행을 변경 없는 control(대조)로 남겼다 |
| `run267cn_q04_validation_and_stress_guardrails` | `s262_lih;s258_stc` | `guardrail_receipt_no_new_attempt` | validation-heavy/stress(검증 중심/압박) 역할을 실패 조건 guardrail(가드레일)로 연결했다 |

## Attempt Inputs(시도 입력)

| attempt(시도) | candidate(후보) | profile(프로필) | tier(티어) | status(상태) |
| --- | --- | --- | --- | --- |
| `run267cn_01_s264_aih_shared_state_breakout_ta_2024` | `s264_aih` | `shared_weakness_state_interaction` | `Tier A` | `execution_pending` |
| `run267cn_01_s264_aih_shared_state_breakout_rt_2024` | `s264_aih` | `shared_weakness_state_interaction` | `Tier A+B` | `execution_pending` |
| `run267cn_02_s264_lc_shared_state_breakout_ta_2024` | `s264_lc` | `shared_weakness_state_interaction` | `Tier A` | `execution_pending` |
| `run267cn_02_s264_lc_shared_state_breakout_rt_2024` | `s264_lc` | `shared_weakness_state_interaction` | `Tier A+B` | `execution_pending` |
| `run267cn_03_s262_lih_shared_state_breakout_ta_2024` | `s262_lih` | `shared_weakness_state_interaction` | `Tier A` | `execution_pending` |
| `run267cn_03_s262_lih_shared_state_breakout_rt_2024` | `s262_lih` | `shared_weakness_state_interaction` | `Tier A+B` | `execution_pending` |
| `run267cn_04_s264_aia_shared_state_breakout_ta_2024` | `s264_aia` | `shared_weakness_state_interaction` | `Tier A` | `execution_pending` |
| `run267cn_04_s264_aia_shared_state_breakout_rt_2024` | `s264_aia` | `shared_weakness_state_interaction` | `Tier A+B` | `execution_pending` |
| `run267cn_05_s258_stc_shared_state_breakout_ta_2024` | `s258_stc` | `shared_weakness_state_interaction` | `Tier A` | `execution_pending` |
| `run267cn_05_s258_stc_shared_state_breakout_rt_2024` | `s258_stc` | `shared_weakness_state_interaction` | `Tier A+B` | `execution_pending` |
| `run267cn_06_s264_aih_aggressive_shock_release_reentry_ta_2024` | `s264_aih` | `aggressive_shock_release_reentry` | `Tier A` | `execution_pending` |
| `run267cn_06_s264_aih_aggressive_shock_release_reentry_rt_2024` | `s264_aih` | `aggressive_shock_release_reentry` | `Tier A+B` | `execution_pending` |

## Boundary(경계)

- 이 run(실행)은 materialization only(물질화 전용)이고 아직 MT5 KPI(MT5 핵심 성과 지표)는 없다.
- The unchanged s264_lc/s264_aia controls(변경 없는 s264_lc/s264_aia 대조군)는 control_holdout_receipt(대조 보류 영수증)로 남겼다.
- s262_lih/s258_stc guardrails(가드레일)는 q01 active batch(q01 활성 묶음)에 포함되지만 선택 후보 주장에는 쓰지 않는다.
- next_action(다음 행동): `run267CO_execute_pool_wide_shared_weakness_breakout_mt5_batch`

## Artifact Lineage(산출물 계보)

- source_queue(원천 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/materialization_queue.csv`
- source_variant_manifest(원천 변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CF/pool_wide_orthogonal_loss_shape_state_materialization/orthogonal_variant_manifest.csv`
- source_attempt_manifest(원천 시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CF/pool_wide_orthogonal_loss_shape_state_materialization/attempt_manifest.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CN/pool_wide_shared_weakness_breakout_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CN/pool_wide_shared_weakness_breakout_materialization/attempt_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CN/pool_wide_shared_weakness_breakout_materialization/runtime_contract.csv`
