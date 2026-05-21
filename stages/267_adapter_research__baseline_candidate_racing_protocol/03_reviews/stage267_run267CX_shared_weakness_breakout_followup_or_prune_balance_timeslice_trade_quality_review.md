# Stage267 Run267CX Shared Weakness Follow-up/Prune Review(267단계 267CX 공유 약점 후속/가지치기 검토)

- status(상태): `run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review_completed`
- trade records(거래 기록): `4470`
- time-slice rows(시간구간 행): `380`
- candidate-profile rows(후보-프로필 행): `5`
- negative slices(음수 구간): `27`
- next_action(다음 행동): `run267CY_design_shared_weakness_breakout_followup_or_prune_from_run267CX_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Candidate/Profile Read(후보/프로필 판독)

| candidate(후보) | profile(프로필) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | worst_month_net(최악 월 순익) | read(판독) |
|---|---|---:|---:|---:|---:|---|---:|---|
| `s258_stc` | `redzone_monday_dd_pressure` | 2115.89 | 1.454 | 518 | 16.42 | `2024-07` | -113.17 | `constructive_stability_clue_no_selection(건설적 안정 단서, 선택 아님)` |
| `s258_stc` | `explosive_shock_state_combo` | 1846.96 | 1.4287 | 486 | 13.91 | `2024-06` | -129.48 | `high_profit_needs_curve_zoom_no_selection(고수익, 곡선 확대 검토 필요, 선택 아님)` |
| `s264_aih` | `explosive_shock_state_combo` | 1550.62 | 1.4321 | 464 | 26.18 | `2024-07` | -126.21 | `profit_but_dd_or_month_hole_uncomfortable(수익은 있으나 손실폭 또는 월별 구멍 불편)` |
| `s264_aia` | `explosive_shock_state_combo` | 1452.57 | 1.4374 | 484 | 14.63 | `2024-06` | -118.33 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s264_aih` | `aih_aggressive_supply_repair` | 1047.25 | 1.7443 | 283 | 12.18 | `2024-12` | -155.42 | `insufficient_curve_evidence_no_selection(곡선 근거 부족, 선택 아님)` |

## Profile Axis Read(프로필 축 판독)

| profile(프로필) | rows(행) | avg_net(평균 순익) | avg_PF(평균 수익 팩터) | avg_trades(평균 거래 수) | avg_DD%(평균 손실폭 %) | profile_read(프로필 판독) |
|---|---:|---:|---:|---:|---:|---|
| `aih_aggressive_supply_repair` | 1 | 1047.25 | 1.7443 | 283.0 | 12.18 | `profile_constructive_but_supply_thin(프로필 건설적이나 거래 공급 얇음)` |
| `explosive_shock_state_combo` | 3 | 1616.72 | 1.4328 | 478.0 | 18.24 | `profile_profitable_but_risk_rows_present(프로필 수익성은 있으나 위험 행 있음)` |
| `redzone_monday_dd_pressure` | 1 | 2115.89 | 1.454 | 518.0 | 16.42 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |

## Weak Slice Watch(약점 구간 관찰)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순익) | trades(거래 수) |
|---|---|---|---|---:|---:|
| `s264_aih` | `aih_aggressive_supply_repair` | `weekday` | `Monday` | -198.19 | 43 |
| `s258_stc` | `redzone_monday_dd_pressure` | `session_report` | `session_07_12_report_time` | -155.85 | 3 |
| `s264_aih` | `aih_aggressive_supply_repair` | `month` | `2024-12` | -155.42 | 24 |
| `s258_stc` | `explosive_shock_state_combo` | `session_report` | `session_07_12_report_time` | -152.67 | 3 |
| `s258_stc` | `explosive_shock_state_combo` | `weekday` | `Monday` | -149.94 | 72 |
| `s264_aih` | `explosive_shock_state_combo` | `session_report` | `session_07_12_report_time` | -136.22 | 3 |
| `s258_stc` | `explosive_shock_state_combo` | `month` | `2024-06` | -129.48 | 21 |
| `s264_aih` | `explosive_shock_state_combo` | `month` | `2024-07` | -126.21 | 58 |

## Boundary(경계)

Run267CX(267CX 실행)는 후보 선택이나 ONNX(오닉스) 준비 선언이 아니다. 이 검토는 다음 run267CY(267CY 실행)의 follow-up/prune design(후속/가지치기 설계)을 만들기 위한 근거다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CX/shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CX/shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CX/shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CX/shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CX/shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
