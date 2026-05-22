# Stage267 Run267DD Shared Weakness Second Follow-up/Prune Materialization(267단계 267DD 공유 약점 2차 후속/가지치기 물질화)

- status(상태): `run267DD_shared_weakness_breakout_second_followup_or_prune_materialized_execution_pending`
- variants(변형): `8`
- attempts(시도): `13`
- held_rows(보류 행): `2`
- next_action(다음 행동): `run267DE_execute_shared_weakness_breakout_second_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DD(267DD 실행)는 run267DC(267DC 실행)의 설계를 실제 MT5(MetaTrader 5, 메타트레이더5) 입력으로 바꿨다.
Effect(효과): s258_stc는 인접 기간 압박, s264_aia는 유사 대체와 피처 중립화, s264_aih는 2024년 12월 파괴 압박, s264_lc/s262_lih는 대조 쌍으로 다음 실행에서 바로 비교할 수 있다.

아직 후보 선택(selection, 선택)이 아니다. 숫자를 보려면 run267DE(267DE 실행) MT5 실행과 run267DF(267DF 실행) balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 검토가 필요하다.

## Queue Decisions(대기열 판단)

| queue(대기열) | decision(판단) | effect(효과) |
|---|---|---|
| `dc_q01_s258_session_cross_period_stress` | `materialized_execution_pending` | variants=3개를 MT5 입력으로 만들었다. |
| `dc_q02_s264_aia_adapter_replacement_watch` | `materialized_execution_pending` | variants=2개를 MT5 입력으로 만들었다. |
| `dc_q03_s264_aih_destructive_prune_probe` | `materialized_execution_pending` | variants=1개를 MT5 입력으로 만들었다. |
| `dc_q04_control_pair_weekday_dd_audit` | `materialized_execution_pending` | variants=2개를 MT5 입력으로 만들었다. |
| `dc_q05_survivor_ablation_replacement_gate` | `held_until_run267DE_run267DF_survivors_exist` | P0 생존 후보가 아직 없어서 feature ablation(피처 제거)과 similar replacement(유사 대체)를 보류했다. |
| `dc_q06_runtime_handoff_receipt_gap` | `receipt_attached_no_mt5_attempt` | 모든 물질화 variant(변형)에 handoff receipt(인계 영수증)를 붙였고, runtime authority(런타임 권위)는 주장하지 않는다. |

## Variants(변형)

| variant(변형) | candidate(후보) | profile(프로필) | queue(대기열) |
|---|---|---|---|
| `run267dd_01_s258_stc_2023h2_session_cross_stress` | `s258_stc` | `s258_session_cross_period_stress` | `dc_q01_s258_session_cross_period_stress` |
| `run267dd_02_s258_stc_2025h1_session_cross_stress` | `s258_stc` | `s258_session_cross_period_stress` | `dc_q01_s258_session_cross_period_stress` |
| `run267dd_03_s258_stc_2025h2_session_cross_stress` | `s258_stc` | `s258_session_cross_period_stress` | `dc_q01_s258_session_cross_period_stress` |
| `run267dd_04_s264_aia_similar_replacement_watch` | `s264_aia` | `s264_aia_similar_replacement_watch` | `dc_q02_s264_aia_adapter_replacement_watch` |
| `run267dd_05_s264_aia_ablation_neutralized_watch` | `s264_aia` | `s264_aia_ablation_neutralized_watch` | `dc_q02_s264_aia_adapter_replacement_watch` |
| `run267dd_06_s264_aih_december_destructive_prune` | `s264_aih` | `s264_aih_december_destructive_prune` | `dc_q03_s264_aih_destructive_prune_probe` |
| `run267dd_07_s264_lc_weekday_dd_control` | `s264_lc` | `s264_lc_weekday_dd_control` | `dc_q04_control_pair_weekday_dd_audit` |
| `run267dd_08_s262_lih_weekday_dd_control` | `s262_lih` | `s262_lih_weekday_dd_control` | `dc_q04_control_pair_weekday_dd_audit` |

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DD/shared_weakness_breakout_second_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DD/shared_weakness_breakout_second_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DD/shared_weakness_breakout_second_followup_or_prune_materialization/attempt_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DD/shared_weakness_breakout_second_followup_or_prune_materialization/runtime_contract.csv`
- handoff_receipt(인계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DD/shared_weakness_breakout_second_followup_or_prune_materialization/handoff_receipt.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DD/shared_weakness_breakout_second_followup_or_prune_materialization/review_result.json`

## Boundary(경계)

이 실행은 materialization(물질화)만 닫는다. deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`
