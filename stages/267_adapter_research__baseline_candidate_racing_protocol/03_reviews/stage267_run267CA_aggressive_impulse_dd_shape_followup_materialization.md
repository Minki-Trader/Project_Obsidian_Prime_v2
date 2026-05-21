# Stage267 Run267CA Aggressive Impulse DD-shape Follow-up Materialization(267단계 267CA 공격형 임펄스 손실폭 형태 후속 물질화)

## Summary(요약)

- run_id(실행 ID): `run267CA_stage267_aggressive_impulse_dd_shape_followup_materialization_v1`
- parent_run(상위 실행): `run267BZ_stage267_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design_v1`
- source_materialization(원천 물질화): `run267BW_stage267_aggressive_impulse_dd_shape_cross_period_materialization_v1`
- status(상태): `run267CA_aggressive_impulse_dd_shape_followup_materialized_execution_pending`
- queue_rows(대기열 행): `3`
- materialized_attempts(물질화 시도): `2`
- held_rows(보류 행): `1`
- feature_frames(피처 프레임): `2`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BZ(267BZ 실행)의 P0 대기열 두 개를 MT5(MetaTrader 5, 메타트레이더5) 입력으로 만들고, P1 곡선 확대 점검은 보류 계획으로 남겼다.
Effect(효과): `s264_aih`는 후반 세션 손실폭 형태 방어, `s258_stc`는 손실폭 상한 압박으로 다음 실행에서 직접 깨뜨려 볼 수 있다.

## Queue Decision(대기열 판단)

| queue(대기열) | candidate(후보) | period(기간) | decision(판단) |
| --- | --- | --- | --- |
| `run267bz_q01_s264_aih_2025h2_late_session_dd_shape_guard` | `s264_aih` | `2025H2` | `materialized_execution_pending` |
| `run267bz_q02_s258_stc_2025h2_stress_dd_cap` | `s258_stc` | `2025H2` | `materialized_execution_pending` |
| `run267bz_q03_s264_aih_2023h2_curve_zoom_sanity` | `s264_aih` | `2023H2` | `held_review_only_no_mt5` |

## Attempt Inputs(시도 입력)

| attempt(시도) | candidate(후보) | feature_count(피처 수) | guard_mean(방어 평균) | feature_hash(피처 해시) | status(상태) |
| --- | --- | ---: | ---: | --- | --- |
| `run267ca_01_s264_aih_2025h2_ddshape_guard` | `s264_aih` | 5 | 0.09140096618357486 | `be7f0d6a603d3c7176e76017eaa256a15dd32cd91c7e32c05baf7ea9ef29a113` | `materialized_execution_pending` |
| `run267ca_02_s258_stc_2025h2_stress_ddcap` | `s258_stc` | 5 | 0.0966615273923322 | `56f9eda9c8475790a4226e3edfcb0adc347ff90089ab566b17ce45a98c1655ab` | `materialized_execution_pending` |

## Boundary(경계)

- run267CA(267CA 실행)는 materialization-only(물질화 전용) 증거다.
- MT5 execution(MT5 실행), KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)는 아직 없다.
- selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
- P1 curve zoom sanity(P1 곡선 확대 정상성)는 P0 실행 근거가 나온 뒤 재개한다.
- next_action(다음 행동): `run267CB_execute_aggressive_impulse_dd_shape_followup_mt5_batch`

## Artifact Lineage(산출물 계보)

- source queue(원천 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BZ/aggressive_impulse_dd_shape_cross_period_followup_or_prune_design/materialization_queue.csv`
- source variant manifest(원천 변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BW/aggressive_impulse_dd_shape_cross_period_materialization/variant_manifest.csv`
- source attempt manifest(원천 시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BW/aggressive_impulse_dd_shape_cross_period_materialization/attempt_manifest.csv`
- feature manifest(피처 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CA/aggressive_impulse_dd_shape_followup_materialization/feature_frame_manifest.csv`
- model manifest(모델 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CA/aggressive_impulse_dd_shape_followup_materialization/model_manifest.csv`
- attempt manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CA/aggressive_impulse_dd_shape_followup_materialization/attempt_manifest.csv`
- runtime contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CA/aggressive_impulse_dd_shape_followup_materialization/runtime_contract.csv`
