# Stage267 Run267AE Noncalendar State Guard Balance/Time-Slice/Trade-Quality Review(267단계 267AE 비달력 상태 방어 잔액/시간구간/거래품질 검토)

- action(행동): run267AD(267AD 실행)의 14개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록) 단위로 다시 읽었다.
- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 같이 본다.
- status(상태): `run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review_completed`
- judgment(판정): `diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection`
- trade_records(거래 기록): `4422`
- candidate_test_rows(후보-시험 행): `7`
- constructive_curve_rows(건설적 곡선 행): `2`
- negative_tier_a_slices(음수 Tier A 구간): `52`
- parser_errors(파서 오류): `0`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 해석)

run267AE(267AE 실행)는 run267AD(267AD 실행)의 좋은 숫자가 실제 곡선과 약한 구간에서도 덜 깨지는지 확인했다.
Effect(효과): 다음 run267AF(267AF 실행)는 숫자 1등을 고르는 대신, 어떤 guard axis(방어 축)를 더 누르고 어떤 분기는 prune(가지치기)할지 정할 수 있다.

Tier A+B(Tier A+B 합산)는 이번 묶음에서 fallback disabled(대체 비활성)라 Tier A(Tier A)와 중복이다.
Effect(효과): 이 결과를 routed robustness(라우팅 견고성) 근거로 쓰지 않고, duplicate boundary(중복 경계)로만 기록한다.

## Candidate-Test Watchlist(후보-시험 관찰 목록)

| rank(순위) | candidate(후보) | role(역할) | test(시험) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실률) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1 | `s264_aia` | `oos_anchor` | `rep_trend_strength_adx` | 1250.12 | 1.59 | 314 | 15.75 | `2024-12` -177.43 | `weekday`/`Monday` -272.43 | `constructive_curve_watch_not_selection` |
| 2 | `s264_aia` | `oos_anchor` | `rep_volatility_atr` | 1097.15 | 1.57 | 317 | 15.07 | `2024-12` -161.24 | `weekday`/`Monday` -259.52 | `constructive_curve_watch_not_selection` |
| 3 | `s264_lc` | `defensive_control` | `abl_gate_variant_rule` | 1620.53 | 1.49 | 378 | 21.27 | `2024-12` -297.93 | `month`/`2024-12` -297.93 | `dd_or_month_hole_uncomfortable` |
| 4 | `s264_aih` | `challenger_core` | `abl_volatility_bandwidth` | 1037.72 | 1.54 | 297 | 16.66 | `2024-12` -197.01 | `weekday`/`Monday` -314.12 | `dd_or_month_hole_uncomfortable` |
| 5 | `s262_lih` | `validation_heavy` | `rep_trend_strength_adx` | 1036.02 | 1.58 | 302 | 16.67 | `2024-12` -184.63 | `weekday`/`Monday` -252.02 | `dd_or_month_hole_uncomfortable` |
| 6 | `s258_stc` | `stress_challenger` | `abl_trend_strength_direction` | 970.89 | 1.45 | 306 | 19.29 | `2024-12` -180.43 | `weekday`/`Monday` -247.77 | `dd_or_month_hole_uncomfortable` |
| 7 | `s258_stc` | `stress_challenger` | `abl_price_return_range` | 969.98 | 1.52 | 297 | 17.75 | `2024-12` -159.01 | `weekday`/`Monday` -252.12 | `mixed_constructive_needs_more_pressure` |

## Candidate Summary(후보 요약)

| candidate(후보) | role(역할) | tests(시험 수) | constructive(건설적 수) | holes(구멍 수) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실률) | worst month net(최악 월 순수익) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_aia` | `oos_anchor` | 2 | 2 | 2 | 1173.63 | 1097.15 | 15.75 | -177.43 | `candidate_has_constructive_clues_but_not_selected` |
| `s264_lc` | `defensive_control` | 1 | 0 | 1 | 1620.53 | 1620.53 | 21.27 | -297.93 | `candidate_needs_pressure_or_prune` |
| `s264_aih` | `challenger_core` | 1 | 0 | 1 | 1037.72 | 1037.72 | 16.66 | -197.01 | `candidate_needs_pressure_or_prune` |
| `s262_lih` | `validation_heavy` | 1 | 0 | 1 | 1036.02 | 1036.02 | 16.67 | -184.63 | `candidate_needs_pressure_or_prune` |
| `s258_stc` | `stress_challenger` | 2 | 0 | 2 | 970.43 | 969.98 | 19.29 | -180.43 | `candidate_needs_pressure_or_prune` |

## Worst Tier A Slices(최악 Tier A 구간)

| candidate(후보) | test(시험) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `s264_aih` | `abl_volatility_bandwidth` | `weekday` | `Monday` | -314.12 | 43 | `negative_deep_drawdown_slice` |
| `s264_lc` | `abl_gate_variant_rule` | `month` | `2024-12` | -297.93 | 31 | `negative_deep_drawdown_slice` |
| `s264_lc` | `abl_gate_variant_rule` | `weekday` | `Monday` | -275.09 | 62 | `negative_deep_drawdown_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `weekday` | `Monday` | -272.43 | 45 | `negative_deep_drawdown_slice` |
| `s264_aia` | `rep_volatility_atr` | `weekday` | `Monday` | -259.52 | 47 | `negative_deep_drawdown_slice` |
| `s258_stc` | `abl_price_return_range` | `weekday` | `Monday` | -252.12 | 44 | `negative_deep_drawdown_slice` |
| `s262_lih` | `rep_trend_strength_adx` | `weekday` | `Monday` | -252.02 | 43 | `negative_deep_drawdown_slice` |
| `s258_stc` | `abl_trend_strength_direction` | `weekday` | `Monday` | -247.77 | 45 | `negative_deep_drawdown_slice` |
| `s264_aih` | `abl_volatility_bandwidth` | `month` | `2024-12` | -197.01 | 25 | `negative_deep_drawdown_slice` |
| `s262_lih` | `rep_trend_strength_adx` | `month` | `2024-12` | -184.63 | 24 | `negative_deep_drawdown_slice` |
| `s258_stc` | `abl_trend_strength_direction` | `month` | `2024-12` | -180.43 | 27 | `negative_deep_drawdown_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `month` | `2024-12` | -177.43 | 24 | `negative_deep_drawdown_slice` |

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): noncalendar state guard(비달력 상태 방어)는 여러 후보에서 2024 순수익을 유지하거나 키웠지만, 최악 월과 최악 구간은 여전히 후보별로 다르다.
- comparison_baseline(비교 기준): run267AD(267AD 실행)의 Tier A(Tier A) MT5(MetaTrader 5, 메타트레이더5) 결과만 1차 판독으로 쓰고, Tier A+B(Tier A+B 합산)는 중복 경계로 둔다.
- likely_drivers(가능 원인): guard_rule_family(방어 규칙 계열)가 특정 달력 조건이 아니라 상태 기반 진입 필터로 작동해 거래 수를 크게 줄이지 않은 점은 긍정 단서다.
- segment_checks(구간 점검): month(월), weekday(요일), session(세션), hour(시간), direction(방향), chron segment(시간순 구간)를 따로 저장했다.
- alternative_explanations(대안 설명): 2024 단일 historical stress(과거 스트레스) 구간의 우연 적합이나 HTML parser(HTML 파서) 해석 문제는 parser_checks(파서 점검)로만 좁게 통제했다.
- attribution_confidence(귀속 신뢰도): `medium_diagnostic_only`.
- next_probe(다음 탐침): run267AF(267AF 실행)에서 constructive axis(건설적 축)는 follow-up(후속)하고 deep slice hole(깊은 구간 구멍)은 prune/repair(가지치기/수리) 경계로 나눈다.

## Forensics Boundary(포렌식 경계)

- tester_identity(테스터 정체성): terminal count(터미널 수) `1`, symbol(심볼) `US100`, timeframe(시간대) `M5`, date range(날짜 범위) `2024.01.02` to `2025.01.01`.
- trade_evidence(거래 근거): trade records(거래 기록) `4422`, parser checks(파서 점검) `14`.
- cost_assumptions(비용 가정): `spread_commission_slippage_follow_strategy_tester_report_no_cost_edge_claim`.
- backtest_judgment(백테스트 판정): `usable_with_boundary`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/attempts_executed.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review.py`.
- consumer(소비자): `run267AF_noncalendar_state_guard_followup_or_prune_design`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AE/noncalendar_state_guard_balance_timeslice_trade_quality_review/trade_records.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AE/noncalendar_state_guard_balance_timeslice_trade_quality_review/time_slice_kpi.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AE/noncalendar_state_guard_balance_timeslice_trade_quality_review/curve_diagnostics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AE/noncalendar_state_guard_balance_timeslice_trade_quality_review/review_result.json`.
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Boundary(경계)

- positive_claim(긍정 주장): `none`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- missing_required(필수 누락): broader period pressure(더 넓은 기간 압박), real fallback/routed robustness(실제 대체/라우팅 견고성), Adapter follow-up(어댑터 후속).
- next_action(다음 행동): `run267AF_noncalendar_state_guard_followup_or_prune_design`.
