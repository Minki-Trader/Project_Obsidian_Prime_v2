# Stage267 Run267BY Aggressive Impulse Cross-period Balance/Time-slice/Trade-quality Review(267단계 267BY 공격형 임펄스 확장 기간 잔액/시간구간/거래품질 검토)

## Summary(요약)

- run_id(실행 ID): `run267BY_stage267_aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review_v1`
- source_run(원천 실행): `run267BX_stage267_aggressive_impulse_dd_shape_cross_period_mt5_execution_v1`
- status(상태): `run267BY_aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review_completed`
- trade_records(거래 기록): `1637`
- time_slice_rows(시간 구간 행): `294`
- negative_slices(음수 구간): `22`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BX(267BX 실행)의 9개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 읽고, 후보별 2023H2/2025H1/2025H2 기간 형태를 분해했다.
Effect(효과): headline KPI(대표 핵심 성과 지표)가 모두 양수여도 DD(drawdown, 손실폭), 약한 월, 후반 구간, 시간 구간 구멍을 숨기지 않는다.

## Candidate Summary(후보 요약)

| candidate(후보) | total net(총 순수익) | min PF(최저 수익 팩터) | worst DD%(최악 손실폭 %) | trades(거래 수) | worst period(최악 기간) | read(판독) |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `s258_stc` | 1952.09 | 1.471409 | 15.96 | 571 | `2025H2` 572.02 | `positive_but_dd_or_late_watch_no_selection(양수지만 손실폭/후반 관찰, 선택 아님)` |
| `s264_aih` | 1812.06 | 1.613865 | 13.717068 | 531 | `2025H2` 476.4 | `constructive_but_needs_more_pressure_no_selection(건설적이나 추가 압박 필요, 선택 아님)` |
| `s264_aia` | 1777.83 | 1.580338 | 15.84 | 535 | `2025H2` 451.56 | `positive_but_dd_or_late_watch_no_selection(양수지만 손실폭/후반 관찰, 선택 아님)` |

## Period Summary(기간 요약)

| period(기간) | total net(총 순수익) | mean PF(평균 수익 팩터) | worst DD%(최악 손실폭 %) | weakest candidate(가장 약한 후보) | read(판독) |
| --- | ---: | ---: | ---: | --- | --- |
| `2023H2` | 1848.98 | 1.834443 | 15.318265 | `s264_aih` 539.33 | `dd_watch_period(손실폭 관찰 기간)` |
| `2025H1` | 2193.02 | 1.555204 | 12.965217 | `s258_stc` 630.58 | `constructive_period_watch(건설적 기간 관찰)` |
| `2025H2` | 1499.98 | 1.662842 | 15.96 | `s264_aia` 451.56 | `dd_watch_period(손실폭 관찰 기간)` |

## Candidate/Period Review(후보/기간 검토)

| candidate(후보) | period(기간) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst month(최악 월) | curve read(곡선 판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s258_stc` | `2023H2` | 749.49 | 1.906868 | 178 | 10.63 | `2023-07` -3.93 | `positive_but_shape_watch_no_selection(양수지만 형태 관찰, 선택 아님)` |
| `s258_stc` | `2025H1` | 630.58 | 1.471409 | 226 | 11.68 | `2025-05` -5.58 | `mixed_watch_no_selection(혼합 관찰, 선택 아님)` |
| `s258_stc` | `2025H2` | 572.02 | 1.686624 | 167 | 15.96 | `2025-09` 13.97 | `positive_but_shape_watch_no_selection(양수지만 형태 관찰, 선택 아님)` |
| `s264_aia` | `2023H2` | 560.16 | 1.80837 | 165 | 9.74 | `2023-07` -3.44 | `constructive_watch_no_selection(건설적 관찰, 선택 아님)` |
| `s264_aia` | `2025H1` | 766.11 | 1.580338 | 216 | 11.74 | `2025-05` -1.83 | `constructive_watch_no_selection(건설적 관찰, 선택 아님)` |
| `s264_aia` | `2025H2` | 451.56 | 1.632641 | 154 | 15.84 | `2025-12` 14.16 | `positive_but_shape_watch_no_selection(양수지만 형태 관찰, 선택 아님)` |
| `s264_aih` | `2023H2` | 539.33 | 1.788091 | 164 | 9.6 | `2023-07` -3.44 | `constructive_watch_no_selection(건설적 관찰, 선택 아님)` |
| `s264_aih` | `2025H1` | 796.33 | 1.613865 | 215 | 11.74 | `2025-05` 25.97 | `constructive_watch_no_selection(건설적 관찰, 선택 아님)` |
| `s264_aih` | `2025H2` | 476.4 | 1.669261 | 152 | 12.19 | `2025-12` 14.03 | `constructive_watch_no_selection(건설적 관찰, 선택 아님)` |

## Worst Negative Slices(최악 음수 구간)

| candidate(후보) | period(기간) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | DD%(손실폭 %) |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `s258_stc` | `2025H2` | `close_hour_report` | `22` | 5 | -66.79 | 15.596384 |
| `s258_stc` | `2025H2` | `session_report` | `session_21_23_report_time` | 11 | -62.63 | 16.159641 |
| `s264_aih` | `2025H2` | `close_hour_report` | `22` | 4 | -46.54 | 11.651015 |
| `s264_aia` | `2025H2` | `close_hour_report` | `22` | 4 | -45.77 | 11.500994 |
| `s264_aih` | `2025H2` | `session_report` | `session_21_23_report_time` | 10 | -43.34 | 12.39977 |
| `s264_aia` | `2025H2` | `session_report` | `session_21_23_report_time` | 10 | -42.63 | 12.263572 |
| `s264_aia` | `2025H1` | `close_hour_report` | `21` | 19 | -14.07 | 7.236712 |
| `s264_aih` | `2025H1` | `close_hour_report` | `21` | 19 | -14.06 | 7.236712 |
| `s264_aia` | `2025H2` | `weekday` | `Monday` | 21 | -12.83 | 13.000241 |
| `s258_stc` | `2025H1` | `close_hour_report` | `21` | 19 | -12.76 | 6.558935 |
| `s258_stc` | `2025H1` | `month` | `2025-05` | 32 | -5.58 | 16.457575 |
| `s258_stc` | `2023H2` | `session_report` | `session_00_06_report_time` | 3 | -4.48 | 6.598 |

## Judgment Boundary(판정 경계)

- run267BY(267BY 실행)는 review evidence(검토 근거)이며 candidate selection(후보 선택)이 아니다.
- all-positive(전부 양수) 결과는 좋은 단서지만, Tier B(티어 B), actual routed total(실제 라우팅 전체), Adapter(어댑터) 구조, curve zoom(곡선 확대)이 아직 없다.
- ONNX parity(ONNX 동등성)와 ONNX conversion(ONNX 변환)은 시작하지 않는다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BY/aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간 구간 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BY/aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BY/aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_period_review(후보 기간 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BY/aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review/candidate_period_review.csv`
- candidate_summary(후보 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BY/aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review/candidate_cross_period_summary.csv`
- period_summary(기간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BY/aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review/period_summary.csv`
- followup_queue(후속 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BY/aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review/followup_queue.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BY/aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review/failure_memory.csv`
- next_action(다음 행동): `run267BZ_design_aggressive_impulse_dd_shape_cross_period_followup_or_prune`
