# Stage267 Run267CJ Follow-up Materialization(267단계 267CJ 후속 물질화)

## Summary(요약)

- run_id(실행 ID): `run267CJ_stage267_pool_wide_orthogonal_loss_shape_state_followup_materialization_v1`
- parent_run(상위 실행): `run267CI_stage267_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_v1`
- source_materialization(원천 물질화): `run267CF_stage267_pool_wide_orthogonal_loss_shape_state_materialization_v1`
- status(상태): `run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialized_execution_pending`
- queue_rows(대기열 행): `5`
- materialized_variants(물질화 변형): `2`
- materialized_attempts(물질화 시도): `4`
- held_rows(보류 행): `3`
- state_attribution_seed_rows(상태 귀속 씨앗 행): `10`
- stress_receipts(압박 영수증): `1`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267CI(267CI 실행)의 P0 두 줄을 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다.
Effect(효과): `s264_lc`와 `s264_aia`를 다음 MT5(MetaTrader 5, 메타트레이더5) batch(묶음)에서 곧바로 깨뜨려 볼 수 있다.

## Queue Decision(대기열 판단)

| queue(대기열) | candidates(후보) | decision(판단) | effect(효과) |
| --- | --- | --- | --- |
| `run267cj_q01_s264_lc_impulse_dd_constrained_state` | `s264_lc` | `materialized_execution_pending` | P0 feature/model/set/ini(피처/모델/설정/초기화) inputs(입력)이 next MT5 batch(다음 MT5 묶음) 준비 상태다 |
| `run267cj_q02_s264_aia_oos_anchor_impulse_pressure` | `s264_aia` | `materialized_execution_pending` | P0 feature/model/set/ini(피처/모델/설정/초기화) inputs(입력)이 next MT5 batch(다음 MT5 묶음) 준비 상태다 |
| `run267cj_q03_loss_shape_proxy_trade_supply_lift_pool` | `s264_lc;s264_aih;s262_lih` | `held_until_p0_execution_review` | P1 supply-lift pool(거래 공급 확장 묶음)은 P0 curve/trade-quality evidence(P0 곡선/거래 품질 근거) 뒤로 보류했다 |
| `run267cj_q04_monday_noncalendar_state_attribution` | `s264_lc;s264_aih;s264_aia;s262_lih;s258_stc` | `analysis_seed_created_no_mt5_attempt` | weak Monday rows(약한 월요일 행)를 calendar rule(달력 규칙) 전에 state attribution seed(상태 귀속 씨앗)로 바꿨다 |
| `run267cj_q05_s258_stc_stress_comparator_receipt` | `s258_stc` | `stress_comparator_prune_receipt_no_mt5_attempt` | s258_stc를 repair loop(수리 반복) 없이 stress comparator(압박 비교군)로 기록했다 |

## Attempt Inputs(시도 입력)

| attempt(시도) | candidate(후보) | tier(티어) | feature_count(피처 수) | feature_hash(피처 해시) | status(상태) |
| --- | --- | --- | ---: | --- | --- |
| `run267cj_01_s264_lc_impulse_dd_state_throttle_ta_2024` | `s264_lc` | `Tier A` | 36 | `09b1adae335c8021b5bc910d87e4bbb311ff6aa0f14a3f68f2c01e7745c8b0df` | `execution_pending` |
| `run267cj_01_s264_lc_impulse_dd_state_throttle_rt_2024` | `s264_lc` | `Tier A+B` | 36 | `09b1adae335c8021b5bc910d87e4bbb311ff6aa0f14a3f68f2c01e7745c8b0df` | `execution_pending` |
| `run267cj_02_s264_aia_oos_anchor_impulse_pressure_ta_2024` | `s264_aia` | `Tier A` | 36 | `c39c3817b3973911d2798458d86353de3d83fb85abb11006e6f8b73f9e38a3d6` | `execution_pending` |
| `run267cj_02_s264_aia_oos_anchor_impulse_pressure_rt_2024` | `s264_aia` | `Tier A+B` | 36 | `c39c3817b3973911d2798458d86353de3d83fb85abb11006e6f8b73f9e38a3d6` | `execution_pending` |

## Boundary(경계)

- run267CJ(267CJ 실행)는 materialization-only(물질화 전용) 근거다.
- MT5 execution(MT5 실행), KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)는 아직 없다.
- selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
- q04는 MT5 시도 대신 state attribution seed(상태 귀속 씨앗)로 남겼다. 효과는 weekday(요일)를 permission rule(허용 규칙)로 착각하지 않는 것이다.
- q05는 stress comparator receipt(압박 비교 영수증)로 남겼다. 효과는 s258_stc(258 짧은 타이트 대조)를 깊은 repair loop(수리 반복)로 끌고 가지 않는 것이다.
- next_action(다음 행동): `run267CK_execute_pool_wide_orthogonal_loss_shape_state_followup_mt5_batch`

## Artifact Lineage(산출물 계보)

- source queue(원천 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CI/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/materialization_queue.csv`
- source variant manifest(원천 변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CF/pool_wide_orthogonal_loss_shape_state_materialization/orthogonal_variant_manifest.csv`
- source attempt manifest(원천 시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CF/pool_wide_orthogonal_loss_shape_state_materialization/attempt_manifest.csv`
- feature manifest(피처 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CJ/pool_wide_orthogonal_loss_shape_state_followup_materialization/feature_frame_manifest.csv`
- model manifest(모델 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CJ/pool_wide_orthogonal_loss_shape_state_followup_materialization/model_manifest.csv`
- attempt manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CJ/pool_wide_orthogonal_loss_shape_state_followup_materialization/attempt_manifest.csv`
- runtime contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CJ/pool_wide_orthogonal_loss_shape_state_followup_materialization/runtime_contract.csv`
