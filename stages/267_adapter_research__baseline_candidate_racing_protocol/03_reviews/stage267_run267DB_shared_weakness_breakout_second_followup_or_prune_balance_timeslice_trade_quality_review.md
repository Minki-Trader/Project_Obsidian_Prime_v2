# Stage267 Run267DB Shared Weakness Second Follow-up/Prune Review(267단계 267DB 공유 약점 후속/가지치기 검토)

- status(상태): `run267DB_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review_completed`
- trade records(거래 기록): `6726`
- time-slice rows(시간구간 행): `532`
- candidate-profile rows(후보-프로필 행): `7`
- negative slices(음수 구간): `43`
- next_action(다음 행동): `run267DC_design_shared_weakness_breakout_second_followup_or_prune_from_run267DB_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Candidate/Profile Read(후보/프로필 판독)

| candidate(후보) | profile(프로필) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | worst_month_net(최악 월 순익) | read(판독) |
|---|---|---:|---:|---:|---:|---|---:|---|
| `s258_stc` | `explosive_second_survival` | 2311.59 | 1.4773 | 533 | 16.4 | `2024-07` | -124.56 | `constructive_stability_clue_no_selection(건설적 안정 단서, 선택 아님)` |
| `s264_lc` | `control_rejoin_guardrail_identity` | 1522.61 | 1.4182 | 473 | 24.39 | `2024-06` | -163.98 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s264_aia` | `aia_validation_damage_probe` | 1489.15 | 1.4019 | 529 | 14.2 | `2024-07` | -67.24 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s264_aia` | `explosive_second_survival` | 1445.48 | 1.3816 | 543 | 14.69 | `2024-07` | -95.66 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s264_aih` | `aih_final_supply_or_prune` | 1364.23 | 1.6705 | 307 | 16.71 | `2024-12` | -261.4 | `profit_but_dd_or_month_hole_uncomfortable(수익은 있으나 손실폭 또는 월별 구멍 불편)` |
| `s262_lih` | `control_rejoin_guardrail_identity` | 1304.06 | 1.3977 | 462 | 13.95 | `2024-12` | -118.64 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s264_aih` | `explosive_second_survival` | 1280.09 | 1.3264 | 516 | 24.03 | `2024-12` | -176.85 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |

## Profile Axis Read(프로필 축 판독)

| profile(프로필) | rows(행) | avg_net(평균 순익) | avg_PF(평균 수익 팩터) | avg_trades(평균 거래 수) | avg_DD%(평균 손실폭 %) | profile_read(프로필 판독) |
|---|---:|---:|---:|---:|---:|---|
| `aia_validation_damage_probe` | 1 | 1489.15 | 1.4019 | 529.0 | 14.2 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |
| `aih_final_supply_or_prune` | 1 | 1364.23 | 1.6705 | 307.0 | 16.71 | `profile_profitable_but_risk_rows_present(프로필 수익성은 있으나 위험 행 있음)` |
| `control_rejoin_guardrail_identity` | 2 | 1413.34 | 1.408 | 467.5 | 19.17 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |
| `explosive_second_survival` | 3 | 1679.05 | 1.3951 | 530.7 | 18.37 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |

## Weak Slice Watch(약점 구간 관찰)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순익) | trades(거래 수) |
|---|---|---|---|---:|---:|
| `s264_aih` | `aih_final_supply_or_prune` | `month` | `2024-12` | -261.4 | 27 |
| `s264_aih` | `aih_final_supply_or_prune` | `weekday` | `Monday` | -246.7 | 44 |
| `s264_lc` | `control_rejoin_guardrail_identity` | `weekday` | `Monday` | -235.05 | 70 |
| `s264_aih` | `explosive_second_survival` | `chron_segment` | `chron_mid` | -207.27 | 172 |
| `s264_aih` | `explosive_second_survival` | `month` | `2024-12` | -176.85 | 46 |
| `s264_lc` | `control_rejoin_guardrail_identity` | `month` | `2024-06` | -163.98 | 17 |
| `s258_stc` | `explosive_second_survival` | `session_report` | `session_07_12_report_time` | -162.28 | 3 |
| `s264_aih` | `explosive_second_survival` | `session_report` | `session_07_12_report_time` | -137.07 | 3 |

## Boundary(경계)

Run267DB(267DB 실행)는 후보 선택이나 ONNX readiness(ONNX 준비) 선언이 아니다. 이 검토는 다음 run267DC(267DC 실행)의 second follow-up/prune design(2차 후속/가지치기 설계)을 만들기 위한 근거다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DB/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DB/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DB/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DB/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DB/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
