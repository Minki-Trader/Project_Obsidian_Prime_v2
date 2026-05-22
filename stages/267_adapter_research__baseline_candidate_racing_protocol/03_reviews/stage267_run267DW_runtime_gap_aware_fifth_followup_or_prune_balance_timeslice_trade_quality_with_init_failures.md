# Stage267 Run267DW Runtime Gap Aware Fifth Follow-Up/Prune Review(267단계 267DW 런타임 공백 반영 5차 후속/가지치기 검토)

- status(상태): `run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures_completed`
- source_run(원천 실행): `run267DV_stage267_runtime_gap_aware_fifth_followup_or_prune_mt5_execution_v1`
- attempts_reviewed(검토 시도): `9`
- runtime_completed_attempts(런타임 완료 시도): `8`
- init_failure_attempts(초기화 실패 시도): `1`
- trade_records(거래 기록): `1790`
- candidate_profile_rows(후보-프로필 행): `8`
- negative_slices(음수 구간): `61`
- next_action(다음 행동): `run267DX_design_runtime_gap_aware_sixth_followup_or_prune_from_run267DW_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DW(267DW 실행)는 run267DV(267DV 실행)의 MT5(MetaTrader 5, 메타트레이더5) 결과를 숫자만 보지 않고 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), init failure(초기화 실패)로 다시 읽었다.
효과: s258_stc(258 STC 후보)는 table handoff repair(테이블 인계 수리)와 aggressive noncalendar impulse(공격형 비달력 충격) 모두 거래 근거가 생겼지만, 2025H1/2025H2의 DD(drawdown, 손실폭)와 recovery(회복)가 불편한지 분리해 본다.
효과: s264_aih(264 AIH 후보)는 2026.04 final-month explosive probe(마지막 달 폭발형 탐침)가 음수이고 validation anchor(검증 앵커)는 init failure(초기화 실패)라서, 공격형 단서와 수리 필요성을 같은 표면에서 분리한다. s264_lc(264 LC 후보)는 같은 2026.04 방어 대조로 비교한다.

## Candidate Summary(후보 요약)

| candidate(후보) | attempts(시도) | completed(완료) | init_fail(초기화 실패) | avg_net(평균 순수익) | max_DD%(최대 손실폭 %) | read(판독) |
|---|---:|---:|---:|---:|---:|---|
| `s258_stc` | 6 | 6 | 0 | 658.83 | 26.32 | `profit_survives_but_dd_and_weak_slices_fragile_no_selection(수익은 살아남지만 손실폭과 약한 구간 취약, 선택 아님)` |
| `s264_aih` | 2 | 1 | 1 | -33.16 | 9.87 | `final_month_negative_and_validation_init_failure_no_selection(마지막 달 음수와 검증 초기화 실패, 선택 아님)` |
| `s264_lc` | 1 | 1 | 0 | -39.29 | 10.36 | `defensive_control_final_month_negative_no_selection(방어 대조 마지막 달 음수, 선택 아님)` |

## Completed Profiles(완료 프로필)

| candidate(후보) | profile(프로필) | split(구간) | tier(티어) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | read(판독) |
|---|---|---|---|---:|---:|---:|---:|---|---|
| `s258_stc` | `s258_stc_noncalendar_impulse_2023h2` | `adjacent_2023_h2_train_pre_2024` | `tier_a_only` | 1544.71 | 1.7818 | 264 | 15.6 | `2023-07` | `constructive_but_trade_supply_thin_no_selection(건설적이나 거래 수 얇음, 선택 아님)` |
| `s258_stc` | `s258_stc_table_handoff_repair_2023h2` | `adjacent_2023_h2_train_pre_2024` | `tier_a_only` | 1225.63 | 1.7531 | 265 | 12.98 | `2023-07` | `constructive_but_trade_supply_thin_no_selection(건설적이나 거래 수 얇음, 선택 아님)` |
| `s258_stc` | `s258_stc_noncalendar_impulse_2025h1` | `adjacent_2025_h1_validation_post_2024` | `tier_a_only` | 417.0 | 1.1793 | 355 | 26.32 | `2025-05` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |
| `s258_stc` | `s258_stc_table_handoff_repair_2025h1` | `adjacent_2025_h1_validation_post_2024` | `tier_a_only` | 343.7 | 1.1732 | 357 | 17.93 | `2025-05` | `positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)` |
| `s258_stc` | `s258_stc_table_handoff_repair_2025h2` | `adjacent_2025_h2_oos_followthrough` | `tier_a_only` | 239.86 | 1.1507 | 259 | 24.72 | `2025-12` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |
| `s258_stc` | `s258_stc_noncalendar_impulse_2025h2` | `adjacent_2025_h2_oos_followthrough` | `tier_a_only` | 182.05 | 1.1029 | 256 | 25.33 | `2025-12` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |
| `s264_aih` | `s264_aih_202604_explosive_shock_probe` | `oos_final_month_2026_04` | `tier_a_only` | -33.16 | 0.5536 | 17 | 9.87 | `2026-04` | `validation_or_quality_break_no_selection(검증 또는 품질 붕괴, 선택 아님)` |
| `s264_lc` | `s264_lc_202604_defensive_control` | `oos_final_month_2026_04` | `tier_a_only` | -39.29 | 0.404 | 17 | 10.36 | `2026-04` | `validation_or_quality_break_no_selection(검증 또는 품질 붕괴, 선택 아님)` |

## Weak Slice Watch(약한 구간 관찰)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순수익) | trades(거래 수) |
|---|---|---|---|---:|---:|
| `s258_stc` | `s258_stc_noncalendar_impulse_2023h2` | `close_hour_report` | `16` | -699.43 | 29 |
| `s258_stc` | `s258_stc_noncalendar_impulse_2025h2` | `weekday` | `Monday` | -184.02 | 33 |
| `s258_stc` | `s258_stc_table_handoff_repair_2025h2` | `month` | `2025-12` | -136.08 | 42 |
| `s258_stc` | `s258_stc_noncalendar_impulse_2025h1` | `close_hour_report` | `22` | -122.36 | 17 |
| `s258_stc` | `s258_stc_noncalendar_impulse_2025h1` | `month` | `2025-05` | -110.97 | 47 |
| `s258_stc` | `s258_stc_table_handoff_repair_2025h2` | `close_hour_report` | `19` | -109.31 | 25 |
| `s258_stc` | `s258_stc_table_handoff_repair_2025h2` | `close_hour_report` | `20` | -105.08 | 16 |
| `s258_stc` | `s258_stc_table_handoff_repair_2023h2` | `close_hour_report` | `16` | -104.08 | 66 |
| `s258_stc` | `s258_stc_table_handoff_repair_2025h1` | `session_report` | `session_21_23_report_time` | -101.11 | 49 |
| `s258_stc` | `s258_stc_noncalendar_impulse_2025h2` | `close_hour_report` | `19` | -83.47 | 24 |
| `s258_stc` | `s258_stc_table_handoff_repair_2025h1` | `close_hour_report` | `21` | -82.27 | 30 |
| `s258_stc` | `s258_stc_noncalendar_impulse_2025h1` | `session_report` | `session_21_23_report_time` | -79.5 | 56 |

## Init Failure Boundary(초기화 실패 경계)

- run267du_07(267DU 07 시도)은 Strategy Tester report(전략 테스터 보고서)는 생성됐지만 runtime telemetry(런타임 텔레메트리)가 `init_failed`를 남긴 init failure(초기화 실패) 행이다.
- 이 행은 zero-trade success(무거래 성공)가 아니라 candidate evidence blocked(후보 근거 차단)로 해석한다.
- Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계)라 실제 fallback(대체) 복원 근거로 쓰지 않는다.

## Boundary(경계)

Run267DW(267DW 실행)는 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DW/runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/trade_records.csv`
- time_slice_kpi(시간구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DW/runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DW/runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DW/runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/candidate_profile_review.csv`
- candidate_init_failure_summary(후보 초기화 실패 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DW/runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/candidate_init_failure_summary.csv`
- attempt_outcome_review(시도 결과 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DW/runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/attempt_outcome_review.csv`
- performance_attribution_summary(성과 귀속 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DW/runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/performance_attribution_summary.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DW/runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures/review_result.json`
