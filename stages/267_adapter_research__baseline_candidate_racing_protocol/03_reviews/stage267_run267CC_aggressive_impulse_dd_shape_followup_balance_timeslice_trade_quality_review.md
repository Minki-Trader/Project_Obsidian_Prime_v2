# Stage267 Run267CC Aggressive Impulse Follow-up Balance/Time-slice/Trade-quality Review(267단계 267CC 공격형 임펄스 후속 잔액/시간구간/거래품질 검토)

## Summary(요약)

- run_id(실행 ID): `run267CC_stage267_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review_v1`
- source_run(원천 실행): `run267CB_stage267_aggressive_impulse_dd_shape_followup_mt5_execution_v1`
- status(상태): `run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review_completed`
- trade_records(거래 기록): `300`
- time_slice_rows(시간 구간 행): `55`
- negative_slices(음수 구간): `6`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267CB(267CB 실행)의 2개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 읽고, s264_aih/s258_stc의 2025H2 후속 형태를 분해했다.
Effect(효과): headline KPI(대표 핵심 성과 지표)가 모두 양수여도 DD(drawdown, 손실폭), 약한 월, 후반 구간, 시간 구간 구멍을 숨기지 않는다.

## Candidate Summary(후보 요약)

| candidate(후보) | total net(총 순수익) | min PF(최저 수익 팩터) | worst DD%(최악 손실폭 %) | trades(거래 수) | worst period(최악 기간) | read(판독) |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `s264_aih` | 415.11 | 1.648457 | 15.52 | 151 | `2025H2` 415.11 | `single_period_followup_dd_watch_no_selection(단일 기간 후속 관찰, 선택 아님)` |
| `s258_stc` | 394.51 | 1.622904 | 16.08 | 149 | `2025H2` 394.51 | `single_period_followup_dd_watch_no_selection(단일 기간 후속 관찰, 선택 아님)` |

## Period Summary(기간 요약)

| period(기간) | total net(총 순수익) | mean PF(평균 수익 팩터) | worst DD%(최악 손실폭 %) | weakest candidate(가장 약한 후보) | read(판독) |
| --- | ---: | ---: | ---: | --- | --- |
| `2025H2` | 809.62 | 1.635681 | 16.08 | `s258_stc` 394.51 | `dd_watch_period(손실폭 관찰 기간)` |

## Candidate/Period Review(후보/기간 검토)

| candidate(후보) | period(기간) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst month(최악 월) | curve read(곡선 판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s258_stc` | `2025H2` | 394.51 | 1.622904 | 149 | 16.08 | `2025-10` 4.6 | `positive_but_shape_watch_no_selection(양수지만 형태 관찰, 선택 아님)` |
| `s264_aih` | `2025H2` | 415.11 | 1.648457 | 151 | 15.52 | `2025-10` 18.81 | `positive_but_shape_watch_no_selection(양수지만 형태 관찰, 선택 아님)` |

## Worst Negative Slices(최악 음수 구간)

| candidate(후보) | period(기간) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | DD%(손실폭 %) |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `s264_aih` | `2025H2` | `close_hour_report` | `22` | 3 | -18.64 | 5.314922 |
| `s264_aih` | `2025H2` | `weekday` | `Monday` | 20 | -16.99 | 12.489418 |
| `s264_aih` | `2025H2` | `session_report` | `session_21_23_report_time` | 9 | -15.08 | 6.790966 |
| `s258_stc` | `2025H2` | `weekday` | `Monday` | 20 | -11.47 | 13.703739 |
| `s264_aih` | `2025H2` | `close_hour_report` | `19` | 3 | -3.88 | 1.206 |
| `s258_stc` | `2025H2` | `close_hour_report` | `19` | 3 | -3.86 | 1.258 |

## Judgment Boundary(판정 경계)

- run267CC(267CC 실행)는 review evidence(검토 근거)이며 candidate selection(후보 선택)이 아니다.
- all-positive(전부 양수) 결과는 좋은 단서지만, 두 후보 모두 DD watch(손실폭 관찰)에 걸리면 repair loop(수리 반복)를 길게 끌지 않는다.
- ONNX parity(ONNX 동등성)와 ONNX conversion(ONNX 변환)은 시작하지 않는다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CC/aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간 구간 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CC/aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CC/aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_period_review(후보 기간 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CC/aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review/candidate_period_review.csv`
- candidate_summary(후보 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CC/aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review/candidate_followup_summary.csv`
- period_summary(기간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CC/aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review/period_summary.csv`
- followup_queue(후속 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CC/aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review/followup_queue.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CC/aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review/failure_memory.csv`
- next_action(다음 행동): `run267CD_design_aggressive_impulse_dd_shape_followup_prune_or_pivot`
