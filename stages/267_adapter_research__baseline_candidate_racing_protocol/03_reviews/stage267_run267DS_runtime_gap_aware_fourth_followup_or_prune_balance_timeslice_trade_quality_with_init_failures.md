# Stage267 Run267DS Runtime Gap Aware Fourth Follow-Up/Prune Review(267단계 267DS 런타임 공백 반영 4차 후속/가지치기 검토)

- status(상태): `run267DS_runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures_completed`
- source_run(원천 실행): `run267DR_stage267_runtime_gap_aware_fourth_followup_or_prune_mt5_execution_v1`
- attempts_reviewed(검토 시도): `8`
- runtime_completed_attempts(런타임 완료 시도): `5`
- init_failure_attempts(초기화 실패 시도): `3`
- trade_records(거래 기록): `1827`
- candidate_profile_rows(후보-프로필 행): `5`
- negative_slices(음수 구간): `39`
- next_action(다음 행동): `run267DT_design_runtime_gap_aware_fifth_followup_or_prune_from_run267DS_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DS(267DS 실행)는 run267DR(267DR 실행)의 MT5(MetaTrader 5, 메타트레이더5) 결과를 숫자만 보지 않고 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), init failure(초기화 실패)로 다시 읽었다.
효과: s258_stc(258 STC 후보)는 Monday/late DD taper(월요일/후반 손실폭 완화) 3개 구간만 거래 근거가 있고, supply continuity(공급 연속성) 3개는 EBM table open failure(EBM 테이블 열기 실패)로 막혔다는 점을 분리했다.
효과: s264_lc(264 LC 후보)는 2024 historical(2024 과거 기간)에서 수익과 거래 수는 좋지만 DD(drawdown, 손실폭)가 24%대로 불편하고, Tier A+B(티어 A+B)는 true fallback(실제 대체)이 아니라 duplicate-boundary(중복 경계)라서 선택 근거로 쓰지 않는다.

## Candidate Summary(후보 요약)

| candidate(후보) | attempts(시도) | completed(완료) | init_fail(초기화 실패) | avg_net(평균 순수익) | max_DD%(최대 손실폭 %) | read(판독) |
|---|---:|---:|---:|---:|---:|---|
| `s258_stc` | 6 | 3 | 3 | 73.67 | 17.93 | `mixed_taper_survives_supply_continuity_init_failure_no_selection(완화형은 일부 살아남지만 공급 연속성은 초기화 실패, 선택 아님)` |
| `s264_lc` | 2 | 2 | 0 | 1522.61 | 24.39 | `defensive_control_profitable_but_dd_uncomfortable_no_selection(방어 대조는 수익이나 손실폭 불편, 선택 아님)` |

## Completed Profiles(완료 프로필)

| candidate(후보) | profile(프로필) | split(구간) | tier(티어) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | read(판독) |
|---|---|---|---|---:|---:|---:|---:|---|---|
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `historical_2024` | `tier_a_only` | 1522.61 | 1.4182 | 473 | 24.39 | `2024-06` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `historical_2024` | `duplicate_boundary_total_not_true_fallback` | 1522.61 | 1.4182 | 473 | 24.39 | `2024-06` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `adjacent_2023_h2_train_pre_2024` | `tier_a_only` | 190.76 | 1.2871 | 266 | 12.18 | `2023-09` | `constructive_but_trade_supply_thin_no_selection(건설적이나 거래 수 얇음, 선택 아님)` |
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `adjacent_2025_h2_oos_followthrough` | `tier_a_only` | 33.93 | 1.0426 | 259 | 16.39 | `2025-12` | `constructive_but_trade_supply_thin_no_selection(건설적이나 거래 수 얇음, 선택 아님)` |
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `adjacent_2025_h1_validation_post_2024` | `tier_a_only` | -3.69 | 0.9954 | 356 | 17.93 | `2025-02` | `validation_or_quality_break_no_selection(검증 또는 품질 붕괴, 선택 아님)` |

## Weak Slice Watch(약한 구간 관찰)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순수익) | trades(거래 수) |
|---|---|---|---|---:|---:|
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `weekday` | `Monday` | -235.05 | 70 |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `weekday` | `Monday` | -235.05 | 70 |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `month` | `2024-06` | -163.98 | 17 |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `month` | `2024-06` | -163.98 | 17 |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `session_report` | `session_07_12_report_time` | -133.21 | 3 |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `session_report` | `session_07_12_report_time` | -133.21 | 3 |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `month` | `2024-12` | -129.63 | 41 |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `month` | `2024-12` | -129.63 | 41 |
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `weekday` | `Tuesday` | -72.58 | 53 |
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `close_hour_report` | `19` | -68.09 | 25 |
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `weekday` | `Monday` | -61.52 | 32 |
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `close_hour_report` | `20` | -59.54 | 46 |

## Init Failure Boundary(초기화 실패 경계)

- run267dq_01/02/03(267DQ 01/02/03 시도)은 Strategy Tester report(전략 테스터 보고서)는 생성됐지만 runtime telemetry(런타임 텔레메트리)가 `init_failed`와 `ebm_table_open_failed:5003`을 남겼다.
- 이 3개는 zero-trade success(무거래 성공)가 아니라 candidate evidence blocked(후보 근거 차단)로 해석한다.
- run267dq_07 Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계)라 실제 fallback(대체) 복원 근거로 쓰지 않는다.

## Boundary(경계)

Run267DS(267DS 실행)는 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DS/runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/trade_records.csv`
- time_slice_kpi(시간구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DS/runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DS/runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DS/runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/candidate_profile_review.csv`
- candidate_init_failure_summary(후보 초기화 실패 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DS/runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/candidate_init_failure_summary.csv`
- attempt_outcome_review(시도 결과 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DS/runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/attempt_outcome_review.csv`
- performance_attribution_summary(성과 귀속 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DS/runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/performance_attribution_summary.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DS/runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/review_result.json`
