# Stage267 Run267CT Shared Weakness Follow-up Review(267단계 267CT 공유 약점 후속 검토)

- status(상태): `run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review_completed`
- trade records(거래 기록): `6054`
- time-slice rows(시간구간 행): `530`
- candidate-profile rows(후보-프로필 행): `7`
- negative slices(음수 구간): `40`
- next_action(다음 행동): `run267CU_design_shared_weakness_breakout_followup_or_prune_from_run267CT_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Candidate/Profile Read(후보/프로필 판독)

| candidate(후보) | profile(프로필) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | worst_month_net(최악 월 순익) | read(판독) |
|---|---|---:|---:|---:|---:|---|---:|---|
| `s258_stc` | `redzone_stress_blast` | 1900.77 | 1.4414 | 472 | 13.93 | `2024-06` | -130.26 | `high_profit_needs_curve_zoom_no_selection(고수익, 곡선 확대 검토 필요, 선택 아님)` |
| `s264_aih` | `state_phase_monday_replacement` | 1796.2 | 1.5013 | 437 | 12.77 | `2024-12` | -132.14 | `constructive_stability_clue_no_selection(건설적 안정 단서, 선택 아님)` |
| `s264_aia` | `state_phase_monday_replacement` | 1686.26 | 1.5103 | 461 | 14.6 | `2024-06` | -124.98 | `constructive_stability_clue_no_selection(건설적 안정 단서, 선택 아님)` |
| `s258_stc` | `state_phase_monday_replacement` | 1612.24 | 1.4094 | 471 | 22.25 | `2024-06` | -135.79 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s264_lc` | `state_phase_monday_replacement` | 1522.61 | 1.4182 | 473 | 24.39 | `2024-06` | -163.98 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s262_lih` | `state_phase_monday_replacement` | 1304.06 | 1.3977 | 462 | 13.95 | `2024-12` | -118.64 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s264_aih` | `aggressive_shock_supply_expansion` | 831.95 | 1.7811 | 251 | 10.58 | `2024-12` | -113.91 | `insufficient_curve_evidence_no_selection(곡선 근거 부족, 선택 아님)` |

## Profile Axis Read(프로필 축 판독)

| profile(프로필) | rows(행) | avg_net(평균 순익) | avg_PF(평균 수익 팩터) | avg_trades(평균 거래 수) | avg_DD%(평균 손실폭 %) | profile_read(프로필 판독) |
|---|---:|---:|---:|---:|---:|---|
| `aggressive_shock_supply_expansion` | 1 | 831.95 | 1.7811 | 251.0 | 10.58 | `profile_constructive_but_supply_thin(프로필 건설적이나 거래 공급 얇음)` |
| `redzone_stress_blast` | 1 | 1900.77 | 1.4414 | 472.0 | 13.93 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |
| `state_phase_monday_replacement` | 5 | 1584.27 | 1.4474 | 460.8 | 17.59 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |

## Weak Slice Watch(약점 구간 관찰)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순익) | trades(거래 수) |
|---|---|---|---|---:|---:|
| `s258_stc` | `state_phase_monday_replacement` | `weekday` | `Monday` | -273.01 | 70 |
| `s258_stc` | `redzone_stress_blast` | `weekday` | `Monday` | -266.64 | 70 |
| `s264_lc` | `state_phase_monday_replacement` | `weekday` | `Monday` | -235.05 | 70 |
| `s264_aih` | `aggressive_shock_supply_expansion` | `weekday` | `Monday` | -183.13 | 35 |
| `s264_lc` | `state_phase_monday_replacement` | `month` | `2024-06` | -163.98 | 17 |
| `s258_stc` | `redzone_stress_blast` | `session_report` | `session_07_12_report_time` | -153.98 | 3 |
| `s264_aih` | `state_phase_monday_replacement` | `session_report` | `session_07_12_report_time` | -143.63 | 3 |
| `s258_stc` | `state_phase_monday_replacement` | `session_report` | `session_07_12_report_time` | -138.68 | 3 |

## Boundary(경계)

Run267CT(267CT 실행)는 후보 선택이나 ONNX(오닉스) 준비 선언이 아니다. 이 검토는 다음 run267CU(267CU 실행)의 follow-up/prune design(후속/가지치기 설계)을 만들기 위한 근거다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CT/shared_weakness_breakout_followup_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CT/shared_weakness_breakout_followup_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CT/shared_weakness_breakout_followup_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CT/shared_weakness_breakout_followup_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CT/shared_weakness_breakout_followup_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
