# Stage267 Run267DO Runtime-Gap-Aware Review(267단계 267DO 런타임 공백 포함 검토)

- status(상태): `run267DO_shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps_completed`
- source_run(원천 실행): `run267DM_stage267_shared_weakness_breakout_third_followup_or_prune_mt5_execution_v1`
- retry_run(재시도 실행): `run267DN_stage267_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry_v1`
- attempts_reviewed(검토 시도): `14`
- runtime_completed_attempts(런타임 완료 시도): `5`
- runtime_gap_attempts(런타임 공백 시도): `9`
- recovered_retry_kpi_records(재시도 회복 KPI 기록): `0`
- trade_records(거래 기록): `1827`
- candidate_profile_rows(후보-프로필 행): `5`
- negative_slices(음수 구간): `6`
- next_action(다음 행동): `run267DP_design_runtime_gap_aware_fourth_followup_or_prune_from_run267DO_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DO(267DO 실행)는 run267DM(267DM 실행)의 completed runtime(완료 런타임) 5개를 곡선/시간구간/거래품질로 읽고, run267DN(267DN 실행)의 retry(재시도) 9개가 모두 runtime gap(런타임 공백)과 zero-trade report(무거래 보고)로 끝난 점을 같이 기록했다.
효과: 같은 attempt(시도)를 계속 재시도하는 병목을 끊고, 어떤 후보가 거래 공급을 만들었는지와 어떤 후보가 런타임/무거래 공백으로 막혔는지를 다음 설계 입력으로 분리한다.

## Candidate Runtime Gap Summary(후보 런타임 공백 요약)

| candidate(후보) | attempts(시도) | completed(완료) | blocked(차단) | retry(재시도) | zero_trade(무거래) | avg_net(평균 순수익) | max_DD%(최대 손실폭 %) | read(판독) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `s258_stc` | 6 | 3 | 3 | 3 | 3 | 603.06 | 24.72 | `mixed_completed_companion_but_retry_gap_blocks_selection(완료 동반 행은 있으나 재시도 공백이 선택 차단)` |
| `s262_lih` | 2 | 0 | 2 | 2 | 2 |  |  | `runtime_gap_and_zero_trade_dominant_prune_or_rebuild(런타임 공백과 무거래 우세, 가지치기 또는 재구축)` |
| `s264_aia` | 4 | 0 | 4 | 4 | 4 |  |  | `runtime_gap_and_zero_trade_dominant_prune_or_rebuild(런타임 공백과 무거래 우세, 가지치기 또는 재구축)` |
| `s264_lc` | 2 | 2 | 0 | 0 | 0 | 1522.61 | 24.39 | `completed_runtime_but_curve_dd_uncomfortable(런타임 완료이나 곡선 손실폭 불편)` |

## Completed Runtime Profiles(완료 런타임 프로필)

| candidate(후보) | profile(프로필) | split(구간) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | read(판독) |
|---|---|---|---:|---:|---:|---:|---|---|
| `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `historical_2024` | 1522.61 | 1.4182 | 473 | 24.39 | `2024-06` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |
| `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `historical_2024` | 1522.61 | 1.4182 | 473 | 24.39 | `2024-06` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |
| `s258_stc` | `s258_stc_explosive_supply_sidefilter_open` | `adjacent_2023_h2_train_pre_2024` | 1225.63 | 1.7531 | 265 | 12.98 | `2023-07` | `constructive_but_trade_supply_thin_no_selection(건설적이나 거래 공급 얇음, 선택 아님)` |
| `s258_stc` | `s258_stc_explosive_supply_sidefilter_open` | `adjacent_2025_h1_validation_post_2024` | 343.7 | 1.1732 | 357 | 17.93 | `2025-05` | `positive_but_weak_quality_or_decay_no_selection(양수이나 품질 약화/감쇠, 선택 아님)` |
| `s258_stc` | `s258_stc_explosive_supply_sidefilter_open` | `adjacent_2025_h2_oos_followthrough` | 239.86 | 1.1507 | 259 | 24.72 | `2025-12` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |

## Weak Slice Watch(약점 구간 관찰)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순수익) | trades(거래 수) |
|---|---|---|---|---:|---:|
| `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `weekday` | `Monday` | -235.05 | 70 |
| `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `month` | `2024-06` | -163.98 | 17 |
| `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `session_report` | `session_07_12_report_time` | -133.21 | 3 |
| `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `month` | `2024-12` | -129.63 | 41 |
| `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `month` | `2024-07` | -46.9 | 57 |
| `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `close_hour_report` | `19` | -39.75 | 26 |

## Runtime Gap Boundary(런타임 공백 경계)

- run267DN(267DN 실행) retry(재시도)는 recovered KPI records(회복 KPI 기록) `0`개다.
- s264_aia(264 AIA 후보) similar/ablation(유사/제거), s262_lih(262 LIH 후보) guardrail(가드레일), s258_stc(258 STC 후보) threshold_release(임계값 해제)는 현 상태에서 zero-trade report(무거래 보고)와 runtime gap(런타임 공백)이 같이 남았다.
- s258_stc(258 STC 후보) sidefilter_open(사이드필터 개방)은 거래 공급을 만들었지만 2025 구간에서 PF(수익 팩터)와 DD(drawdown, 손실폭)가 약해졌다.
- s264_lc(264 LC 후보)는 수익과 거래 수가 있으나 DD(drawdown, 손실폭)가 방어 대조로도 불편하다.

## Boundary(경계)

Run267DO(267DO 실행)는 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 선언하지 않는다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DO/shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps/trade_records.csv`
- time_slice_kpi(시간구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DO/shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DO/shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DO/shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps/candidate_profile_review.csv`
- candidate_runtime_gap_summary(후보 런타임 공백 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DO/shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps/candidate_runtime_gap_summary.csv`
- attempt_outcome_review(시도 결과 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DO/shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps/attempt_outcome_review.csv`
- performance_attribution_summary(성과 귀속 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DO/shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps/performance_attribution_summary.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DO/shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps/review_result.json`
