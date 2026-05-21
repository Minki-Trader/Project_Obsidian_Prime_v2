# Stage267 Run267BW Aggressive Impulse DD-shape Cross-period Materialization(267단계 267BW 공격형 임펄스 손실폭 형태 확장 기간 물질화)

## Summary(요약)

- run_id(실행 ID): `run267BW_stage267_aggressive_impulse_dd_shape_cross_period_materialization_v1`
- parent_run(상위 실행): `run267BV_stage267_directional_impulse_followup_or_prune_design_v1`
- source_materialization(원천 물질화): `run267BS_stage267_pool_wide_directional_impulse_followup_materialization_v1`
- status(상태): `run267BW_aggressive_impulse_dd_shape_cross_period_materialized_execution_pending`
- queue_rows(대기열 행): `11`
- materialized_attempts(물질화 시도): `9`
- feature_frames(피처 프레임): `9`
- blocked_or_audit_rows(차단/감사 행): `2`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BV(267BV 실행)의 materialization queue(물질화 대기열)를 받아 상위 3개 aggressive impulse(공격형 임펄스) 관찰 후보를 2023H2, 2025H1, 2025H2 기간별 MT5(MetaTrader 5, 메타트레이더5) 입력으로 만들었다.
Effect(효과): 다음 run267BX(267BX 실행)에서 후보를 바로 고르지 않고, 기간을 바꿔도 PF/DD(수익 팩터/손실폭)와 거래 품질이 덜 깨지는지 확인할 수 있다.

이번 실행은 baseline(기준 후보) 선택이 아니다. 숫자가 좋아 보여도 아직 MT5 실행 결과, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)가 없다.

## Queue Decision(대기열 판단)

| queue(대기열) | candidate(후보) | period(기간) | decision(판단) |
| --- | --- | --- | --- |
| `run267bw_q00_directional_asymmetry_prune_receipt` | `pool_wide` | `not_applicable` | `prune_receipt_consumed_no_mt5` |
| `run267bw_q01_s258_stc_2023h2_aggressive_impulse_period_pressure` | `s258_stc` | `2023H2` | `materialized_execution_pending` |
| `run267bw_q01_s258_stc_2025h1_aggressive_impulse_period_pressure` | `s258_stc` | `2025H1` | `materialized_execution_pending` |
| `run267bw_q01_s258_stc_2025h2_aggressive_impulse_period_pressure` | `s258_stc` | `2025H2` | `materialized_execution_pending` |
| `run267bw_q01_s264_aih_2023h2_aggressive_impulse_period_pressure` | `s264_aih` | `2023H2` | `materialized_execution_pending` |
| `run267bw_q01_s264_aih_2025h1_aggressive_impulse_period_pressure` | `s264_aih` | `2025H1` | `materialized_execution_pending` |
| `run267bw_q01_s264_aih_2025h2_aggressive_impulse_period_pressure` | `s264_aih` | `2025H2` | `materialized_execution_pending` |
| `run267bw_q01_s264_aia_2023h2_aggressive_impulse_period_pressure` | `s264_aia` | `2023H2` | `materialized_execution_pending` |
| `run267bw_q01_s264_aia_2025h1_aggressive_impulse_period_pressure` | `s264_aia` | `2025H1` | `materialized_execution_pending` |
| `run267bw_q01_s264_aia_2025h2_aggressive_impulse_period_pressure` | `s264_aia` | `2025H2` | `materialized_execution_pending` |
| `run267bw_q02_impulse_similar_replacement_design_probe` | `s258_stc,s264_aih,s264_aia` | `2024_then_extension` | `blocked_feature_availability_audit_before_mt5` |

## Attempt Inputs(시도 입력)

| attempt(시도) | candidate(후보) | period(기간) | rows(행) | feature_hash(피처 해시) | status(상태) |
| --- | --- | --- | ---: | --- | --- |
| `run267bw_01_s258_stc_2023h2_impulse_repl` | `s258_stc` | `2023H2` | 6090 | `bf253081e72e5e3aba136ab4ac537e0cd0afaf7b9ae41873ac012aa5818869ed` | `materialized_execution_pending` |
| `run267bw_02_s258_stc_2025h1_impulse_repl` | `s258_stc` | `2025H1` | 6867 | `bf253081e72e5e3aba136ab4ac537e0cd0afaf7b9ae41873ac012aa5818869ed` | `materialized_execution_pending` |
| `run267bw_03_s258_stc_2025h2_impulse_repl` | `s258_stc` | `2025H2` | 6486 | `bf253081e72e5e3aba136ab4ac537e0cd0afaf7b9ae41873ac012aa5818869ed` | `materialized_execution_pending` |
| `run267bw_04_s264_aih_2023h2_impulse_repl` | `s264_aih` | `2023H2` | 6090 | `717ec4ea4c47a03dd6d21cf5fc057711e76efe3f2b875bebecfbc0ca762430df` | `materialized_execution_pending` |
| `run267bw_05_s264_aih_2025h1_impulse_repl` | `s264_aih` | `2025H1` | 6867 | `717ec4ea4c47a03dd6d21cf5fc057711e76efe3f2b875bebecfbc0ca762430df` | `materialized_execution_pending` |
| `run267bw_06_s264_aih_2025h2_impulse_repl` | `s264_aih` | `2025H2` | 6486 | `717ec4ea4c47a03dd6d21cf5fc057711e76efe3f2b875bebecfbc0ca762430df` | `materialized_execution_pending` |
| `run267bw_07_s264_aia_2023h2_impulse_repl` | `s264_aia` | `2023H2` | 6090 | `1b4d49d6868c370ad277cae0031ab10137724c014579d56ef8e51db54b55ae42` | `materialized_execution_pending` |
| `run267bw_08_s264_aia_2025h1_impulse_repl` | `s264_aia` | `2025H1` | 6867 | `1b4d49d6868c370ad277cae0031ab10137724c014579d56ef8e51db54b55ae42` | `materialized_execution_pending` |
| `run267bw_09_s264_aia_2025h2_impulse_repl` | `s264_aia` | `2025H2` | 6486 | `1b4d49d6868c370ad277cae0031ab10137724c014579d56ef8e51db54b55ae42` | `materialized_execution_pending` |

## Boundary(경계)

- MT5 execution(MT5 실행): `not_executed`, 다음 run267BX(267BX 실행)에서 확인한다.
- similar replacement(유사 피처 대체): `blocked_feature_availability_audit_before_mt5`, 원천 피처 계보 감사가 먼저 필요하다.
- Tier B fallback(Tier B 대체): `blocked`, true fallback manifest(실제 대체 목록)이 아직 없다.
- Adapter(어댑터): 보류. cross-period MT5 KPI(확장 기간 MT5 핵심 성과 지표), 거래 목록, 곡선, 시간 구간 검토 뒤 판단한다.
- ONNX parity(ONNX 동등성): 금지. Goal gate(목표 게이트) 전에는 검토하지 않는다.
- next_action(다음 행동): `run267BX_execute_aggressive_impulse_dd_shape_cross_period_mt5_batch`

## Artifact Lineage(산출물 계보)

- source queue(원천 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BV/directional_impulse_followup_or_prune_design/materialization_queue.csv`
- source variant manifest(원천 변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BS/pool_wide_directional_impulse_followup_materialization/directional_impulse_variant_manifest.csv`
- source attempt manifest(원천 시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BS/pool_wide_directional_impulse_followup_materialization/attempt_manifest.csv`
- feature manifest(피처 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BW/aggressive_impulse_dd_shape_cross_period_materialization/feature_frame_manifest.csv`
- attempt manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BW/aggressive_impulse_dd_shape_cross_period_materialization/attempt_manifest.csv`
- runtime contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BW/aggressive_impulse_dd_shape_cross_period_materialization/runtime_contract.csv`
