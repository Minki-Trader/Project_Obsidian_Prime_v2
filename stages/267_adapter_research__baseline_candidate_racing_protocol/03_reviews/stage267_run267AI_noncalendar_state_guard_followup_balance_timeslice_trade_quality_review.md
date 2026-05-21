# Stage267 Run267AI Noncalendar State Guard Follow-Up Balance/Time-Slice/Trade-Quality Review(267단계 267AI 비달력 상태 방어 후속 잔액/시간구간/거래품질 검토)

- action(행동): run267AH(267AH 실행)의 `6`개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록) 단위로 다시 읽었다.
- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 같이 본다.
- status(상태): `run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review_completed`
- judgment(판정): `diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection`
- trade_records(거래 기록): `1738`
- candidate_test_rows(후보-시험 행): `3`
- constructive_curve_rows(건설적 곡선 행): `2`
- negative_tier_a_slices(음수 Tier A 구간): `16`
- parser_errors(파서 오류): `0`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AH(267AH 실행)의 대표 숫자는 나쁘지 않다. 하지만 이 단계의 질문은 숫자 1등이 아니라, 어느 후보가 덜 깨지는지다.
Effect(효과): 이번 run267AI(267AI 실행)는 각 후보를 월별, 요일별, 세션별, 방향별, 시간 순서별로 쪼개서 약한 구간을 숨기지 않게 만든다.

Tier A+B(Tier A+B 합산)는 이번 묶음에서 fallback disabled(대체 비활성) 중복 경계다.
Effect(효과): routed robustness(라우팅 견고성) 근거로 쓰지 않고, Tier A(Tier A) 결과와 중복되는지 확인하는 감사 행으로만 쓴다.

## Candidate-Test Watchlist(후보-시험 관찰 목록)

| rank(순위) | candidate(후보) | role(역할) | test(시험) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1 | `s264_aia` | `oos_anchor` | `rep_trend_strength_adx` | 1133.77 | 1.60 | 301 | 14.73 | `2024-12` -157.55 | `weekday`/`Monday` -289.75 | `constructive_curve_watch_not_selection` |
| 2 | `s264_aia` | `oos_anchor` | `rep_volatility_atr` | 1080.68 | 1.64 | 296 | 13.77 | `2024-12` -154.93 | `weekday`/`Monday` -234.18 | `constructive_curve_watch_not_selection` |
| 3 | `s264_aih` | `challenger_core` | `abl_volatility_bandwidth` | 826.62 | 1.55 | 272 | 18.28 | `2024-12` -194.95 | `weekday`/`Monday` -243.84 | `dd_or_month_hole_uncomfortable` |

## Candidate Summary(후보 요약)

| candidate(후보) | role(역할) | tests(시험 수) | constructive(건설적) | holes(구멍 수) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | worst month net(최악 월 순수익) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_aia` | `oos_anchor` | 2 | 2 | 0 | 1107.22 | 1080.68 | 14.73 | -157.55 | `constructive_watch_not_selection` |
| `s264_aih` | `challenger_core` | 1 | 0 | 1 | 826.62 | 826.62 | 18.28 | -194.95 | `fragile_or_prune_pressure` |

## Worst Tier A Slices(최악 Tier A 구간)

| candidate(후보) | test(시험) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `s264_aia` | `rep_trend_strength_adx` | `weekday` | `Monday` | -289.75 | 44 | `deep_negative_or_dd_slice` |
| `s264_aih` | `abl_volatility_bandwidth` | `weekday` | `Monday` | -243.84 | 42 | `deep_negative_or_dd_slice` |
| `s264_aia` | `rep_volatility_atr` | `weekday` | `Monday` | -234.18 | 44 | `deep_negative_or_dd_slice` |
| `s264_aih` | `abl_volatility_bandwidth` | `month` | `2024-12` | -194.95 | 23 | `deep_negative_or_dd_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `month` | `2024-12` | -157.55 | 23 | `deep_negative_or_dd_slice` |
| `s264_aia` | `rep_volatility_atr` | `month` | `2024-12` | -154.93 | 23 | `deep_negative_or_dd_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `session_report` | `session_07_12_report_time` | -97.91 | 3 | `negative_fragile_slice` |
| `s264_aia` | `rep_volatility_atr` | `session_report` | `session_07_12_report_time` | -91.94 | 3 | `negative_fragile_slice` |
| `s264_aih` | `abl_volatility_bandwidth` | `session_report` | `session_07_12_report_time` | -83.05 | 3 | `negative_fragile_slice` |
| `s264_aia` | `rep_volatility_atr` | `month` | `2024-07` | -38.65 | 39 | `minor_negative_slice` |
| `s264_aih` | `abl_volatility_bandwidth` | `close_hour_report` | `20` | -36.92 | 15 | `minor_negative_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `month` | `2024-06` | -32.08 | 10 | `minor_negative_slice` |

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): s264_aia(264 AIA)는 두 replacement pressure(대체 압박)에서 2024 순수익과 PF(수익 팩터)가 유지됐고, s264_aih(264 AIH)는 core role pressure(핵심 역할 압박)에서 순수익은 낮고 DD(drawdown, 손실폭)는 더 불편하다.
- comparison_baseline(비교 기준): run267AH(267AH 실행)의 Tier A(Tier A) MT5 결과를 1차 판독으로 쓰고, Tier A+B(Tier A+B 합산)는 fallback disabled(대체 비활성) 중복 경계로 둔다.
- likely_drivers(가능 원인): follow-up pressure(후속 압박)는 새 재학습이 아니라 score table(점수표) 확장이므로, 개선처럼 보이는 수치는 state guard(상태 방어)와 기존 decision surface(결정 표면)의 상호작용일 가능성이 크다.
- segment_checks(구간 점검): month(월), weekday(요일), session(세션), hour(시간), direction(방향), chron segment(시간 순서 구간)를 따로 저장했다.
- trade_shape(거래 형태): trade count(거래 수), expectancy(기대값), win rate(승률), payoff ratio(손익비), drawdown(손실폭), underwater(회복 전 체류)를 같이 기록했다.
- alternative_explanations(대체 설명): 2024 단일 historical stress(과거 압박) 구간이라 우연 적합이 남아 있고, real fallback(실제 대체) 검증은 아직 아니다.
- attribution_confidence(귀속 신뢰도): `medium_diagnostic_only`.
- next_probe(다음 탐침): `run267AJ_design_followup_from_run267AI_curve_time_slice_review`.

## Forensics Boundary(포렌식 경계)

- tester_identity(테스터 정체성): terminal count(터미널 수) `1`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, date range(날짜 범위) `2024.01.02` to `2025.01.01`.
- trade_evidence(거래 근거): trade records(거래 기록) `1738`, parser checks(파서 점검) `6`.
- cost_assumptions(비용 가정): `MT5 tester broker-history costs; no separate cost authority claimed`.
- backtest_judgment(백테스트 판정): `usable_with_boundary`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/attempts_executed.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review.py`.
- consumer(소비자): `run267AJ_design_followup_from_run267AI_curve_time_slice_review`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AI/noncalendar_state_guard_followup_balance_timeslice_trade_quality_review/trade_records.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AI/noncalendar_state_guard_followup_balance_timeslice_trade_quality_review/time_slice_kpi.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AI/noncalendar_state_guard_followup_balance_timeslice_trade_quality_review/curve_diagnostics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AI/noncalendar_state_guard_followup_balance_timeslice_trade_quality_review/review_result.json`.
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Boundary(경계)

- positive_claim(긍정 주장): `none`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- missing_required(필수 누락): broader period pressure(더 넓은 기간 압박), real fallback/routed robustness(실제 대체/라우팅 견고성), Adapter follow-up(어댑터 후속), ONNX parity(ONNX 동등성).
- next_action(다음 행동): `run267AJ_design_followup_from_run267AI_curve_time_slice_review`.
