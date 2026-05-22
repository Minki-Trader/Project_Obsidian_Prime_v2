# Stage267 Run267EI Balance/Time-Slice/Trade-Quality Review(267단계 267EI 잔액/시간구간/거래품질 검토)

- status(상태): `run267EI_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review_completed_with_init_failures`
- source_run(원천 실행): `run267EH_stage267_runtime_gap_aware_eighth_followup_or_prune_mt5_execution_v1`
- candidate_profile_rows(후보-프로필 행): `9`
- trade_records(거래 기록): `1485`
- init_failure_groups(초기화 실패 묶음): `6`
- negative_slices(음수 구간): `80`
- parser_errors(파서 오류): `0`
- next_action(다음 행동): `run267EJ_design_runtime_gap_aware_ninth_followup_or_prune_from_run267EI_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267EH(267EH 실행)는 15개 시도 중 9개만 KPI(핵심 성과 지표)까지 갔다. run267EI(267EI 실행)는 그 9개를 곡선/구간/거래품질로 읽고, 막힌 6개는 성능 실패가 아니라 init/runtime gap(초기화/런타임 공백)으로 분리했다.
효과는 후보를 성급히 뽑지 않고 다음 설계에서 무엇을 수리하고, 무엇을 압박하고, 무엇을 중복 후보로 의심해야 하는지 분리하는 것이다.

## Candidate Profile(후보 프로필)

| candidate(후보) | profile(프로필) | net(순손익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | weakest(최약) | read(판독) |
|---|---|---:|---:|---:|---:|---|---|
| `s264_aih` | `s264_aih_validation_integrity_recheck` | 442.89 | 1.210 | 467 | 15.74 | `2025-09=-19.36` | `positive_low_pf_watch_no_selection(양수지만 PF 낮음, 선택 아님)` |
| `s264_aih` | `s264_aih_202604_bounded_repair` | -27.89 | 0.433 | 17 | 7.85 | `2026-04=-27.89` | `breaks_on_measured_slice_no_selection(측정 구간에서 깨짐, 선택 아님)` |
| `s264_lc` | `s264_lc_202604_paired_control` | -39.29 | 0.404 | 17 | 10.36 | `2026-04=-39.29` | `breaks_on_measured_slice_no_selection(측정 구간에서 깨짐, 선택 아님)` |
| `s264_aih` | `s264_aih_202604_shared_sell_pressure` | -28.77 | 0.442 | 17 | 8.26 | `2026-04=-28.77` | `breaks_on_measured_slice_no_selection(측정 구간에서 깨짐, 선택 아님)` |
| `s264_lc` | `s264_lc_202604_shared_sell_pressure` | -30.22 | 0.431 | 17 | 8.51 | `2026-04=-30.22` | `breaks_on_measured_slice_no_selection(측정 구간에서 깨짐, 선택 아님)` |
| `s262_lih` | `s262_lih_202604_shared_sell_pressure` | -30.10 | 0.420 | 17 | 8.19 | `2026-04=-30.10` | `breaks_on_measured_slice_no_selection(측정 구간에서 깨짐, 선택 아님)` |
| `s264_aia` | `s264_aia_202604_shared_sell_pressure` | -28.77 | 0.442 | 17 | 8.26 | `2026-04=-28.77` | `breaks_on_measured_slice_no_selection(측정 구간에서 깨짐, 선택 아님)` |
| `s262_lih` | `s262_lih_validation_identity_audit` | 574.21 | 1.213 | 458 | 13.39 | `2025-09=-33.51` | `positive_low_pf_watch_no_selection(양수지만 PF 낮음, 선택 아님)` |
| `s264_aia` | `s264_aia_validation_identity_audit` | 574.21 | 1.213 | 458 | 13.39 | `2025-09=-33.51` | `positive_low_pf_watch_no_selection(양수지만 PF 낮음, 선택 아님)` |

## Init/Runtime Gaps(초기화/런타임 공백)

- `s258_stc` `q01_s258_period_survival_quality_split` `survival_quality_recheck_2025h1`: blocked_attempts(차단 시도) `1`. runtime_output_gap_or_init_failure_requires_bounded_handoff_triage(런타임 출력 공백 또는 초기화 실패라 제한된 인계 진단 필요)
- `s258_stc` `q01_s258_period_survival_quality_split` `survival_quality_recheck_2025h2`: blocked_attempts(차단 시도) `1`. runtime_output_gap_or_init_failure_requires_bounded_handoff_triage(런타임 출력 공백 또는 초기화 실패라 제한된 인계 진단 필요)
- `s258_stc` `q02_s258_explosive_init_failure_triage` `explosive_handoff_triage_2025h1`: blocked_attempts(차단 시도) `1`. runtime_output_gap_or_init_failure_requires_bounded_handoff_triage(런타임 출력 공백 또는 초기화 실패라 제한된 인계 진단 필요)
- `s258_stc` `q02_s258_explosive_init_failure_triage` `explosive_handoff_triage_2025h2`: blocked_attempts(차단 시도) `1`. runtime_output_gap_or_init_failure_requires_bounded_handoff_triage(런타임 출력 공백 또는 초기화 실패라 제한된 인계 진단 필요)
- `s264_aih` `q06_s264_aih_explosive_counter_impulse_handoff_triage` `final_month_explosive_handoff_triage`: blocked_attempts(차단 시도) `1`. runtime_output_gap_or_init_failure_requires_bounded_handoff_triage(런타임 출력 공백 또는 초기화 실패라 제한된 인계 진단 필요)
- `s264_aih` `q06_s264_aih_explosive_counter_impulse_handoff_triage` `validation_explosive_handoff_triage`: blocked_attempts(차단 시도) `1`. runtime_output_gap_or_init_failure_requires_bounded_handoff_triage(런타임 출력 공백 또는 초기화 실패라 제한된 인계 진단 필요)

## Attribution(성과 귀인)

- `s258_stc`: all_s258_runtime_outputs_blocked(모든 s258 런타임 출력 차단) Next(다음): bounded_handoff_triage_before_any_performance_judgment(성능 판단 전 제한된 인계 진단)
- `s264_aih`: validation_positive_but_202604_negative_and_aggressive_handoff_blocked(검증 양수지만 2026.04 음수이고 공격형 인계 차단) Next(다음): separate_final_month_structure_from_runtime_handoff_gap(마지막 월 구조와 런타임 인계 공백 분리)
- `s264_lc`: defensive_control_also_negative_on_202604(방어 대조도 2026.04에서 음수) Next(다음): use_as_market_control_not_selection_candidate(시장 대조로만 사용, 선택 후보 아님)
- `s262_lih`: validation_identity_positive_but_202604_pressure_negative(검증 정체성은 양수지만 2026.04 압박은 음수) Next(다음): keep_validation_heavy_watch_but_test_identity_collapse(검증 중심 관찰 유지, 정체성 붕괴 검사)
- `s264_aia`: oos_anchor_identity_duplicates_s262_and_202604_pressure_negative(표본외 앵커가 s262와 중복되고 2026.04 압박 음수) Next(다음): do_not_treat_oos_anchor_as_distinct_until_signature_separates(서명이 분리되기 전 독립 후보로 보지 않음)

## Follow-Up Queue(후속 대기열)

- `q01_runtime_handoff_gap_bounded_triage` `P0` `s258_stc;s264_aih`: repair_or_prune_runtime_handoff_gap_before_performance_claim(성능 주장 전 런타임 인계 공백 수리 또는 가지치기)
- `q02_202604_shared_sell_fragility_pivot` `P0` `s264_aih;s264_lc;s262_lih;s264_aia`: pivot_to_structure_or_feature_engineering_not_more_same_month_filtering(같은 월 필터 반복이 아니라 구조/피처 엔지니어링으로 전환)
- `q03_s262_s264_aia_signature_collapse_audit` `P1` `s262_lih;s264_aia`: audit_feature_order_model_identity_before_distinct_candidate_claim(독립 후보 주장 전 피처 순서/모델 정체성 감사)
- `q04_validation_positive_low_pf_watch` `P1` `s264_aih;s262_lih;s264_aia`: keep_as_watch_not_baseline_selection(관찰로 유지하되 기준 후보 선택 아님)
- `q05_aggressive_experiment_after_handoff_fix` `P2_aggressive` `s258_stc;s264_aih`: after_handoff_fix_run_one_aggressive_non_filter_experiment(인계 수리 뒤 필터가 아닌 공격형 실험 1회)

## Boundary(경계)

- 이 검토는 exploratory review(탐색 검토)이며 후보 선택, 연구 기준 후보 선택, ONNX(온엑스) 준비, Goal Achieve(목표 달성)를 주장하지 않는다.
- 다음 run267EJ(267EJ 실행)는 같은 필터를 더 붙이는 작업이 아니라 handoff gap(인계 공백), 2026.04 shared fragility(공유 취약성), duplicate signature(중복 서명), 공격형 실험 재개 조건을 설계해야 한다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EI/runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간구간 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EI/runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EI/runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EI/runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- init_failure_summary(초기화 실패 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EI/runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review/init_failure_summary.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EI/runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
- followup_decision_queue(후속 판단 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EI/runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review/followup_decision_queue.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EI/runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review/result_judgment.csv`
