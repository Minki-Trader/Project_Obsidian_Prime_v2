# Stage267 Run267DJ Shared Weakness Second Follow-up/Prune Review(267단계 267DJ 공유 약점 2차 후속/가지치기 검토)

- status(상태): `run267DJ_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review_completed`
- trade records(거래 기록): `4509`
- time-slice rows(시간구간 행): `404`
- candidate-profile rows(후보-프로필 행): `4`
- negative slices(음수 구간): `26`
- next_action(다음 행동): `run267DK_design_shared_weakness_breakout_second_followup_or_prune_from_run267DJ_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DJ(267DJ 실행)는 run267DI(267DI 실행)의 MT5 report(MetaTrader 5 보고서)를 거래 목록, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.
효과: headline KPI(대표 핵심 성과 지표)만 보고 지나가지 않고, 후보가 어느 월, 요일, 세션, 구간에서 깨지는지 다음 설계 재료로 분해한다.

## Candidate/Profile Read(후보/프로필 판독)

| candidate(후보) | profile(프로필) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | worst_month_net(최악 월 순수익) | read(판독) |
|---|---|---:|---:|---:|---:|---|---:|---|
| `s264_aia` | `s264_aia_ablation_survivor_gate` | 1646.0 | 1.4481 | 507 | 15.45 | `2024-12` | -94.76 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s264_lc` | `s264_lc_weekday_dd_deescalation` | 1522.61 | 1.4182 | 473 | 24.39 | `2024-06` | -163.98 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s262_lih` | `s262_lih_validation_control_crosscheck` | 1304.06 | 1.3977 | 462 | 13.95 | `2024-12` | -118.64 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |
| `s264_aia` | `s264_aia_similar_survivor_gate` | 1292.34 | 1.3765 | 527 | 14.12 | `2024-12` | -89.61 | `mixed_constructive_needs_followup(혼합 건설적, 후속 필요)` |

## Profile Axis Read(프로필 축 판독)

| profile(프로필) | rows(행) | avg_net(평균 순수익) | avg_PF(평균 수익 팩터) | avg_trades(평균 거래 수) | avg_DD%(평균 손실폭 %) | profile_read(프로필 판독) |
|---|---:|---:|---:|---:|---:|---|
| `s262_lih_validation_control_crosscheck` | 1 | 1304.06 | 1.3977 | 462.0 | 13.95 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |
| `s264_aia_ablation_survivor_gate` | 1 | 1646.0 | 1.4481 | 507.0 | 15.45 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |
| `s264_aia_similar_survivor_gate` | 1 | 1292.34 | 1.3765 | 527.0 | 14.12 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |
| `s264_lc_weekday_dd_deescalation` | 1 | 1522.61 | 1.4182 | 473.0 | 24.39 | `profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)` |

## Weak Slice Watch(약점 구간 관찰)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순수익) | trades(거래 수) |
|---|---|---|---|---:|---:|
| `s264_lc` | `s264_lc_weekday_dd_deescalation` | `weekday` | `Monday` | -235.05 | 70 |
| `s264_lc` | `s264_lc_weekday_dd_deescalation` | `month` | `2024-06` | -163.98 | 17 |
| `s262_lih` | `s262_lih_validation_control_crosscheck` | `weekday` | `Monday` | -135.08 | 69 |
| `s264_lc` | `s264_lc_weekday_dd_deescalation` | `session_report` | `session_07_12_report_time` | -133.21 | 3 |
| `s264_lc` | `s264_lc_weekday_dd_deescalation` | `month` | `2024-12` | -129.63 | 41 |
| `s264_aia` | `s264_aia_ablation_survivor_gate` | `session_report` | `session_07_12_report_time` | -128.9 | 3 |
| `s262_lih` | `s262_lih_validation_control_crosscheck` | `session_report` | `session_07_12_report_time` | -124.22 | 3 |
| `s262_lih` | `s262_lih_validation_control_crosscheck` | `month` | `2024-12` | -118.64 | 43 |

## Boundary(경계)

Run267DJ(267DJ 실행)는 candidate selection(후보 선택)이나 ONNX readiness(ONNX 준비)를 선언하지 않는다. 이 검토는 다음 run267DK(267DK 실행) second follow-up/prune design(2차 후속/가지치기 설계)을 만들기 위한 근거다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DJ/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DJ/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DJ/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DJ/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DJ/shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
