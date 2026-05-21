# Stage267 run267BQ Anti-overconstraint Cross-period Balance/Time-slice/Trade-quality Review(과제약 제거 확장 기간 잔액/시간구간/거래품질 검토)

## Summary(요약)

- run_id(실행 ID): `run267BQ_stage267_anti_overconstraint_cross_period_balance_timeslice_trade_quality_v1`
- source_gap_run(원천 공백 실행): `run267BP_stage267_state_acceleration_zero_trade_gap_classification_v1`
- source_mt5_run(원천 MT5 실행): `run267BO_stage267_aggressive_second_tranche_cross_period_mt5_execution_v1`
- status(상태): `run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality_review_completed`
- trade_records(거래 기록): `812`
- time_slice_rows(시간 구간 행): `92`
- negative_slices(음수 구간): `18`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BP(267BP 실행)에서 usable(사용 가능)로 분류된 anti_overconstraint_prune(과제약 제거) 3개 기간을 trade list(거래 목록)로 다시 읽었다.
Effect(효과): 2023H2의 강한 headline KPI(겉 핵심 성과 지표)가 2025H1/2025H2에서도 덜 깨지는지 월/요일/시간/세션/방향/초중후반 구간으로 확인한다.

## Cross-period Summary(확장 기간 요약)

| period(기간) | trades(거래) | net(순수익) | PF(수익 팩터) | expectancy(기대값) | closed DD%(폐쇄 손실폭 %) | worst month(최악 월) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `2023H2` | 221 | 998.53 | 1.920915 | 4.518235 | 13.794638 | `2023-07` 3.56 | `constructive_watch_not_selection(건설적 관찰, 선택 아님)` |
| `2025H1` | 372 | 113.39 | 1.077543 | 0.304812 | 22.118133 | `2025-05` -76.7 | `positive_but_uncomfortable_holes(양수지만 불편한 구멍)` |
| `2025H2` | 219 | 55.79 | 1.049843 | 0.254749 | 28.148763 | `2025-12` -69.07 | `positive_but_uncomfortable_holes(양수지만 불편한 구멍)` |

## Worst Negative Slices(최악 음수 구간)

| period(기간) | axis(축) | bucket(구간) | trades(거래) | net(순수익) | DD%(손실폭 %) |
| --- | --- | --- | ---: | ---: | ---: |
| `2025H1` | `direction` | `sell` | 119 | -267.91 | 58.120113 |
| `2025H1` | `close_hour_report` | `16` | 64 | -185.24 | 39.391139 |
| `2025H1` | `weekday` | `Wednesday` | 71 | -127.18 | 31.068514 |
| `2025H1` | `chron_segment` | `chron_late` | 124 | -102.01 | 30.714131 |
| `2025H1` | `month` | `2025-05` | 39 | -76.7 | 26.629109 |
| `2025H2` | `chron_segment` | `chron_late` | 73 | -74.79 | 29.577414 |
| `2025H2` | `month` | `2025-12` | 41 | -69.07 | 21.032 |
| `2025H2` | `weekday` | `Monday` | 28 | -63.28 | 20.030292 |
| `2025H2` | `close_hour_report` | `19` | 18 | -59.78 | 11.956 |
| `2025H2` | `close_hour_report` | `20` | 14 | -58.35 | 13.498639 |
| `2025H1` | `close_hour_report` | `20` | 47 | -57.45 | 13.783363 |
| `2025H2` | `direction` | `sell` | 127 | -45.17 | 33.173744 |

## Excluded Gap Attempts(제외 공백 시도)

| attempt(시도) | variant(변형) | period(기간) | reason(이유) |
| --- | --- | --- | --- |
| `run267bn_04_s264_aih_state_acceleration_interaction_2025h1` | `state_acceleration_interaction` | `2025H1` | `zero_trade_report_completed_runtime_csv_absent` |

## Boundary(경계)

- 이 실행은 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 진단이다.
- 2023H2가 좋아도 2025H1/2025H2 약화와 음수 구간을 숨기지 않는다.
- candidate selection(후보 선택), selected research baseline(선택 연구 기준선), ONNX conversion(ONNX 변환), Goal Achieve(목표 달성)는 주장하지 않는다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BQ/anti_overconstraint_cross_period_balance_timeslice_trade_quality/trade_records.csv`
- time_slice_kpi(시간 구간 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BQ/anti_overconstraint_cross_period_balance_timeslice_trade_quality/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BQ/anti_overconstraint_cross_period_balance_timeslice_trade_quality/curve_diagnostics.csv`
- cross_period_summary(확장 기간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BQ/anti_overconstraint_cross_period_balance_timeslice_trade_quality/cross_period_summary.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BQ/anti_overconstraint_cross_period_balance_timeslice_trade_quality/negative_slice_summary.csv`
- next_action(다음 행동): `run267BR_design_anti_overconstraint_cross_period_followup_or_prune`
