# Stage267 Run267AR Pool-wide State Feature Engineering Follow-up/Adapter Branch Design(267단계 267AR 후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계)

- action(행동): run267AQ(267AQ 실행)의 profile review(프로필 검토)를 candidate role decision(후보 역할 결정), next experiment queue(다음 실험 큐), failure memory(실패 기억)로 바꿨다.
- effect(효과): 높은 headline KPI(대표 핵심 성과 지표)를 바로 고르지 않고, Monday(월요일), 2024-12(2024년 12월), Tier A+B duplicate boundary(Tier A+B 중복 경계)를 다음 압박 조건으로 쓴다.
- status(상태): `run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch_design_completed`
- judgment(판정): `followup_adapter_branch_design_completed_no_candidate_selection`
- profile_decisions(프로필 결정): `20`
- candidate_decisions(후보 결정): `5`
- next_queue_rows(다음 큐 행): `5`
- failure_memory(실패 기억): `8`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 해석)

run267AQ(267AQ 실행)는 숫자가 좋아진 후보를 많이 만들었다. 하지만 모든 후보에 깊은 구간 구멍이 남았다.
Effect(효과): run267AR(267AR 실행)는 후보를 고르는 단계가 아니라, 누가 다음 압박을 받을지와 무엇을 반복하지 않을지를 정한다.

가장 중요한 경계는 Tier A+B(Tier A+B 합산)다. 이번 Tier A+B는 duplicate boundary(중복 경계)라서 real fallback(실제 대체) 근거가 아니다.
Effect(효과): runtime reproduction(런타임 재현)이나 ONNX parity(ONNX 동등성) 쪽으로 가기 전에 실제 fallback manifest(대체 목록)가 따로 필요하다.

## Candidate Decisions(후보 결정)

| candidate(후보) | role(역할) | mean net(평균 순수익) | min net(최소 순수익) | worst slice(최악 구간) | holes(구멍) | decision(결정) | next use(다음 용도) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s264_aih` | `challenger_core` | 1146.43 | 844.71 | -289.49 | 3 | `retain_core_challenger_but_require_slice_pressure(핵심 도전자는 유지하되 구간 압박 필요)` | `core_challenger_pressure_branch(핵심 도전자 압박 분기)` |
| `s264_lc` | `defensive_control` | 1101.04 | 1062.29 | -281.82 | 4 | `retain_defensive_control_no_candidate_selection(방어 통제 유지, 후보 선택 아님)` | `defensive_control_audit(방어 통제 감사)` |
| `s262_lih` | `validation_heavy` | 1103.33 | 962.36 | -283.73 | 4 | `retain_validation_heavy_control_no_candidate_selection(검증 중심 통제 유지, 후보 선택 아님)` | `validation_heavy_control_audit(검증 중심 통제 감사)` |
| `s264_aia` | `oos_anchor` | 1113.34 | 1015.10 | -330.16 | 4 | `retain_oos_anchor_adapter_watch_with_gate(게이트 포함 표본외 앵커 어댑터 관찰 유지)` | `adapter_watch_if_DD_edge_survives_slice_pressure(구간 압박 후 손실폭 장점 생존 시 어댑터 관찰)` |
| `s258_stc` | `stress_challenger` | 1157.32 | 885.68 | -394.14 | 4 | `retain_stress_challenger_only_under_deep_pressure(깊은 압박 조건에서만 압박 도전자 유지)` | `stress_challenger_prune_or_rescue_gate(압박 도전자 가지치기 또는 회수 게이트)` |

## Top Profile Pressure Rows(상위 프로필 압박 행)

| candidate(후보) | source(원천) | profile(프로필) | net(순수익) | PF(수익 팩터) | worst slice(최악 구간) | gate(게이트) | next use(다음 용도) |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| `s258_stc` | `abl_volatility_bandwidth` | `volatility_regime_expansion` | 1450.57 | 1.59 | `weekday`/`Monday` -394.14 | `fail_severe_slice_hole(심한 구간 구멍 실패)` | `stress_test_noncalendar_slice_pressure_before_adapter_watch(어댑터 관찰 전 비달력 구간 압박)` |
| `s258_stc` | `rep_trend_strength_adx` | `trend_strength_disagreement` | 1385.53 | 1.54 | `month`/`2024-12` -239.82 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `stress_test_noncalendar_slice_pressure_before_adapter_watch(어댑터 관찰 전 비달력 구간 압박)` |
| `s264_aih` | `rep_volatility_atr` | `range_expansion_pressure` | 1297.62 | 1.64 | `month`/`2024-12` -270.78 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `core_challenger_noncalendar_december_monday_pressure(핵심 도전자 비달력 12월/월요일 압박)` |
| `s264_aih` | `rep_volatility_atr` | `volatility_regime_expansion` | 1297.57 | 1.62 | `month`/`2024-12` -289.49 | `fail_severe_slice_hole(심한 구간 구멍 실패)` | `core_challenger_noncalendar_december_monday_pressure(핵심 도전자 비달력 12월/월요일 압박)` |
| `s262_lih` | `rep_volatility_atr` | `volatility_regime_expansion` | 1196.86 | 1.59 | `weekday`/`Monday` -283.73 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `control_audit_against_challenger_pressure(도전자 압박 대비 통제 감사)` |
| `s264_aia` | `rep_volatility_atr` | `volatility_regime_expansion` | 1167.06 | 1.59 | `weekday`/`Monday` -279.00 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `watch_only_or_prune_if_next_pressure_fails(관찰 전용 또는 다음 압박 실패 시 가지치기)` |
| `s264_aia` | `rep_volatility_atr` | `range_expansion_pressure` | 1151.94 | 1.61 | `weekday`/`Monday` -278.42 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `adapter_watch_only_after_slice_gate_improves(구간 게이트 개선 뒤 어댑터 관찰 전용)` |
| `s264_aih` | `rep_volatility_atr` | `return_shock_absorption` | 1145.81 | 1.59 | `weekday`/`Monday` -248.98 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `watch_only_or_prune_if_next_pressure_fails(관찰 전용 또는 다음 압박 실패 시 가지치기)` |
| `s264_lc` | `rep_volatility_atr` | `volatility_regime_expansion` | 1145.20 | 1.57 | `weekday`/`Monday` -280.51 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `control_audit_against_challenger_pressure(도전자 압박 대비 통제 감사)` |
| `s262_lih` | `rep_volatility_atr` | `range_expansion_pressure` | 1136.40 | 1.58 | `weekday`/`Monday` -275.19 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `control_audit_against_challenger_pressure(도전자 압박 대비 통제 감사)` |
| `s264_aia` | `rep_volatility_atr` | `return_shock_absorption` | 1119.25 | 1.60 | `weekday`/`Monday` -273.11 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `adapter_watch_only_after_slice_gate_improves(구간 게이트 개선 뒤 어댑터 관찰 전용)` |
| `s262_lih` | `rep_volatility_atr` | `return_shock_absorption` | 1117.68 | 1.57 | `weekday`/`Monday` -274.62 | `fail_deep_slice_hole(깊은 구간 구멍 실패)` | `control_audit_against_challenger_pressure(도전자 압박 대비 통제 감사)` |

## Next Experiment Queue(다음 실험 큐)

| priority(우선순위) | queue(큐) | workstream(작업 흐름) | candidate scope(후보 범위) | decision use(결정 용도) | stop(중단) |
| --- | --- | --- | --- | --- | --- |
| `P0` | `run267AS_q01_noncalendar_slice_pressure_matrix` | `noncalendar_slice_resilience_pressure(비달력 구간 견고성 압박)` | `s264_aih;s264_aia;s258_stc` | `decide_whether_any_P0_candidate_deserves_adapter_watch_after_pressure(압박 뒤 P0 후보가 어댑터 관찰 가치가 있는지 판단)` | `one_materialized_pressure_pass_then_prune_or_redirect_if_holes_persist(물질화 압박 1회 후 구멍 지속 시 가지치기 또는 방향 전환)` |
| `P0` | `run267AS_q02_candidate_role_pressure_and_prune_gate` | `candidate_role_pressure_gate(후보 역할 압박 게이트)` | `s264_aih;s264_aia;s258_stc` | `split_keep_watch_or_prune_for_core_challenger_oos_anchor_stress_challenger(핵심 도전자/표본외 앵커/압박 도전자의 유지/관찰/가지치기 분리)` | `if_P0_pressure_fails_do_not_extend_same_repair_more_than_one_more_stage(P0 압박 실패 시 같은 수리를 한 단계 이상 늘리지 않음)` |
| `P1` | `run267AS_q03_defensive_validation_control_audit` | `control_audit(통제 감사)` | `s264_lc;s262_lih` | `keep_or_prune_controls_after_P0_pressure(우선 압박 뒤 통제 유지/가지치기 결정)` | `keep_as_control_only_or_archive_if_no_longer_informative(정보 가치 없으면 통제 전용 유지 또는 보관)` |
| `P1_deferred` | `run267AS_q04_real_tier_b_fallback_probe_design` | `real_fallback_boundary_design(실제 대체 경계 설계)` | `survivors_only_after_run267AS_run267AT(267AS/267AT 이후 생존 후보만)` | `prevent_duplicate_combined_result_from_becoming_robustness_claim(중복 합산 결과가 견고성 주장으로 바뀌는 것을 방지)` | `do_not_start_runtime_reproduction_until_real_fallback_boundary_exists(실제 대체 경계 전 런타임 재현 시작 금지)` |
| `P2_guardrail` | `run267AS_q05_no_single_calendar_repair_guard` | `anti_bottleneck_guard(병목 방지 가드)` | `all_candidates(전체 후보)` | `block_single_month_or_single_weekday_micro_tuning(단일 월/요일 미세조정 차단)` | `stop_repair_loop_if_same_slice_target_repeats_after_one_more_pass(한 번 더 수행 후 같은 구간 목표가 반복되면 수리 루프 중단)` |

## Experiment Design Receipt(실험 설계 기록)

- hypothesis/decision_use/comparison/control/changed/sample/success/failure/invalid/stop/evidence fields(가설/결정/비교/고정/변경/표본/성공/실패/무효/중단/근거 필드)는 `next_experiment_queue.csv`에 기록했다.
- failure memory(실패 기억)는 single Monday/December repair(단일 월요일/12월 수리), Tier A+B duplicate boundary(Tier A+B 중복 경계), headline-only selection(대표 숫자만 보고 선택)을 반복 금지로 남긴다.
- claim boundary(주장 경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AQ/pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review/review_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AQ/pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review/candidate_state_profile_review.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AQ/pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review/negative_slice_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AQ/pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review/tier_duplicate_review.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch.py`.
- consumer(소비자): `run267AS_materialize_pool_wide_state_feature_engineering_followup_queue`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AR/pool_wide_state_feature_engineering_followup_or_adapter_branch/profile_decision_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AR/pool_wide_state_feature_engineering_followup_or_adapter_branch/candidate_branch_decision_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AR/pool_wide_state_feature_engineering_followup_or_adapter_branch/next_experiment_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AR/pool_wide_state_feature_engineering_followup_or_adapter_branch/review_result.json`.
