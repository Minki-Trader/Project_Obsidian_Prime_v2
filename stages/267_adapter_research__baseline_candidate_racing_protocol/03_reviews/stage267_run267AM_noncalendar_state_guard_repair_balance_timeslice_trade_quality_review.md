# Stage267 Run267AM Noncalendar State Guard Repair Balance/Time-Slice/Trade-Quality Review(267단계 267AM 비달력 상태 방어 수리 잔액/시간구간/거래품질 검토)

- action(행동): run267AL(267AL 실행)의 `4`개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록) 단위로 다시 읽었다.
- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 repair(수리)가 Monday(월요일), 2024-12(2024년 12월), session(세션), chron segment(시간 순서 구간)에서 덜 깨지는지 확인했다.
- status(상태): `run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review_completed`
- judgment(판정): `diagnostic_repair_curve_timeslice_trade_quality_review_completed_no_candidate_selection`
- trade_records(거래 기록): `1160`
- candidate_test_rows(후보-시험 행): `2`
- baseline_comparison_rows(기준 비교 행): `2`
- negative_tier_a_slices(음수 Tier A 구간): `9`
- parser_errors(파서 오류): `0`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AL(267AL 실행)의 대표 숫자는 좋아 보인다. 하지만 이번 goal(목표)은 숫자만 보는 것이 아니라 누가 덜 깨지는지 보는 것이다.
Effect(효과): run267AM(267AM 실행)은 run267AI(267AI 실행)의 약점 기준과 비교해 수리 후에도 Monday(월요일)와 December(12월) 구멍이 남는지 확인한다.
Tier A+B(Tier A+B 합산)는 fallback disabled(대체 비활성) 중복 경계다. 따라서 routed robustness(라우팅 견고성)이나 runtime authority(런타임 권위)는 주장하지 않는다.

## Repair Comparison(수리 비교)

| candidate(후보) | test(시험) | net delta(순수익 변화) | PF delta(PF 변화) | trade delta(거래 변화) | DD delta(손실폭 변화) | Monday delta(월요일 변화) | Dec delta(12월 변화) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_aia` | `rep_volatility_atr` | -62.30 | 0.02 | -6 | -1.39 | 14.18 | 28.35 | `headline_survives_but_named_weak_slice_gate_incomplete` |
| `s264_aia` | `rep_trend_strength_adx` | -116.66 | -0.01 | -11 | -0.71 | 25.92 | 22.16 | `headline_survives_but_named_weak_slice_gate_incomplete` |

## Candidate-Test Watchlist(후보-시험 관찰 목록)

| rank(순위) | candidate(후보) | test(시험) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1 | `s264_aia` | `rep_volatility_atr` | 1018.38 | 1.66 | 290 | 12.38 | `2024-12` -126.58 | `weekday`/`Monday` -220.00 | `constructive_curve_watch_not_selection` |
| 2 | `s264_aia` | `rep_trend_strength_adx` | 1017.11 | 1.59 | 290 | 14.02 | `2024-12` -135.39 | `weekday`/`Monday` -263.83 | `constructive_curve_watch_not_selection` |

## Worst Tier A Slices(최악 Tier A 구간)

| candidate(후보) | test(시험) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `s264_aia` | `rep_trend_strength_adx` | `weekday` | `Monday` | -263.83 | 43 | `deep_negative_or_dd_slice` |
| `s264_aia` | `rep_volatility_atr` | `weekday` | `Monday` | -220.00 | 43 | `deep_negative_or_dd_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `month` | `2024-12` | -135.39 | 23 | `deep_negative_or_dd_slice` |
| `s264_aia` | `rep_volatility_atr` | `month` | `2024-12` | -126.58 | 21 | `deep_negative_or_dd_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `session_report` | `session_07_12_report_time` | -87.50 | 3 | `negative_fragile_slice` |
| `s264_aia` | `rep_volatility_atr` | `session_report` | `session_07_12_report_time` | -81.82 | 3 | `negative_fragile_slice` |
| `s264_aia` | `rep_volatility_atr` | `month` | `2024-07` | -35.17 | 39 | `minor_negative_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `month` | `2024-06` | -26.24 | 10 | `minor_negative_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `month` | `2024-07` | -4.15 | 36 | `minor_negative_slice` |

## Performance Attribution(성과 귀인)

- observed_change(관찰 변화): repair(수리) 후 대표 KPI(핵심 성과 지표)는 net profit(순수익) 1017~1018, PF(수익 팩터) 1.59~1.66, trade count(거래 수) 290으로 유지됐다.
- comparison_baseline(비교 기준): run267AI(267AI 실행)의 s264_aia Tier A follow-up rows(후속 행)를 기준으로 삼았다.
- likely_drivers(가능 원인): 새 학습이 아니라 score table guard terms(점수표 방어 항) 변경이므로, 성능 변화는 decision surface(결정 표면)의 일부 상태 구간 억제에서 온 것으로 본다.
- segment_checks(구간 확인): month(월), weekday(요일), hour(시간), session(세션), direction(방향), chron segment(시간 순서 구간)를 확인했다.
- trade_shape(거래 형태): trade count(거래 수), expectancy(기대값), win rate(승률), payoff ratio(손익비), drawdown(손실폭), underwater(회복 전 체류)를 기록했다.
- alternative_explanations(대체 설명): 2024 단일 기간 stress(압박)라서 우연 적합 가능성이 남고, Tier A+B(Tier A+B 합산)는 실제 fallback(대체) 검증이 아니다.
- attribution_confidence(귀인 신뢰도): `medium_diagnostic_only`.
- next_probe(다음 탐침): `run267AN_design_noncalendar_state_guard_repair_followup_or_prune`.

## Forensics Boundary(포렌식 경계)

- tester_identity(테스터 정체성): terminal count(터미널 수) `1`, symbol(심볼) `US100`, timeframe(시간 프레임) `M5`, date range(날짜 범위) `2024.01.02` to `2025.01.01`.
- trade_evidence(거래 근거): trade records(거래 기록) `1160`, parser checks(파서 확인) `4`.
- cost_assumptions(비용 가정): `MT5 tester broker-history costs; no separate cost authority claimed`.
- backtest_judgment(백테스트 판정): `usable_with_boundary`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AL/noncalendar_state_guard_repair_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AL/noncalendar_state_guard_repair_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AL/noncalendar_state_guard_repair_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AL/noncalendar_state_guard_repair_mt5_execution/attempts_executed.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AI/noncalendar_state_guard_followup_balance_timeslice_trade_quality_review/candidate_test_review.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review.py`.
- consumer(소비자): `run267AN_design_noncalendar_state_guard_repair_followup_or_prune`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AM/noncalendar_state_guard_repair_balance_timeslice_trade_quality_review/trade_records.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AM/noncalendar_state_guard_repair_balance_timeslice_trade_quality_review/time_slice_kpi.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AM/noncalendar_state_guard_repair_balance_timeslice_trade_quality_review/curve_diagnostics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AM/noncalendar_state_guard_repair_balance_timeslice_trade_quality_review/run267AI_baseline_comparison.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AM/noncalendar_state_guard_repair_balance_timeslice_trade_quality_review/review_result.json`.
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Boundary(경계)

- positive_claim(긍정 주장): `none`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- missing_required(필수 누락): broader period pressure(더 넓은 기간 압박), real fallback/routed robustness(실제 대체 라우팅 견고성), Adapter follow-up(어댑터 후속), ONNX parity(ONNX 동등성).
- next_action(다음 행동): `run267AN_design_noncalendar_state_guard_repair_followup_or_prune`.
