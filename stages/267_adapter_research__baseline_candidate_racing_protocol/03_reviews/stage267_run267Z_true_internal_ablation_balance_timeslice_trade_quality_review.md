# Stage267 Run267Z True Internal Ablation Balance/Time-Slice/Trade-Quality Review(267단계 267Z 진짜 내부 제거 잔액/시간구간/거래품질 검토)

- action(행동): run267X(267X 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 거래 단위로 다시 파싱했다.
- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고, balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 같이 본다.
- status(상태): `run267Z_true_internal_ablation_balance_timeslice_trade_quality_review_completed`
- judgment(판정): `diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection`
- trade_records(거래 기록): `15298`
- candidate_test_rows(후보-시험 행): `24`
- constructive_curve_rows(건설적 곡선 행): `5`
- negative_tier_a_slices(음수 Tier A 구간): `120`
- parser_errors(파서 오류): `0`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 해석)

run267Y(267Y 실행)는 24개 true internal KPI signature(진짜 내부 핵심 성과 지표 서명)를 확인했다.
이번 run267Z(267Z 실행)는 그 숫자를 곡선과 약한 구간으로 펼쳐봤다.
Effect(효과): 숫자가 좋은 후보라도 특정 월, 요일, 세션, 후반 구간에서 깊게 파이면 바로 드러난다.

현재 constructive_curve_watch_not_selection(건설적 곡선 관찰, 선택 아님) 행은 단서일 뿐이다.
Effect(효과): Adapter(어댑터) 설계나 후속 압박으로 넘길 수는 있지만, selected candidate(선택 후보)나 ONNX(ONNX) 검토로 넘기지는 않는다.

Tier A+B(Tier A+B 합산)는 여전히 fallback disabled(대체 비활성) 중복 경계다.
Effect(효과): routed robustness(라우팅 견고성) 근거가 아니라 Tier A(Tier A) 결과의 중복 확인으로만 읽는다.

## Candidate-Test Watchlist(후보-시험 관찰 목록)

| rank(순위) | candidate(후보) | test(시험) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1 | `s264_aia` | `rep_trend_strength_adx` | 1390.83 | 1.56 | 332 | 15.44 | `2024-12` -177.31 | `weekday`/`Monday` -319.36 | `constructive_curve_watch_not_selection` |
| 2 | `s264_aia` | `rep_volatility_atr` | 1191.32 | 1.53 | 339 | 16.07 | `2024-12` -153.18 | `weekday`/`Monday` -269.98 | `constructive_curve_watch_not_selection` |
| 3 | `s262_lih` | `rep_trend_strength_adx` | 1116.28 | 1.52 | 331 | 17.88 | `2024-12` -163.35 | `weekday`/`Monday` -241.72 | `constructive_curve_watch_not_selection` |
| 4 | `s258_stc` | `abl_price_return_range` | 1002.40 | 1.46 | 315 | 19.01 | `2024-12` -172.35 | `weekday`/`Monday` -282.30 | `constructive_curve_watch_not_selection` |
| 5 | `s258_stc` | `abl_trend_strength_direction` | 906.92 | 1.38 | 325 | 21.43 | `2024-12` -170.77 | `weekday`/`Monday` -304.16 | `constructive_curve_watch_not_selection` |
| 6 | `s264_lc` | `abl_gate_variant_rule` | 1700.94 | 1.47 | 400 | 19.42 | `2024-12` -237.38 | `weekday`/`Monday` -283.80 | `dd_or_month_hole_uncomfortable` |
| 7 | `s258_stc` | `rep_trend_strength_adx` | 1413.66 | 1.49 | 340 | 19.15 | `2024-12` -230.09 | `weekday`/`Monday` -276.83 | `dd_or_month_hole_uncomfortable` |
| 8 | `s258_stc` | `abl_volatility_bandwidth` | 1393.91 | 1.50 | 336 | 18.57 | `2024-12` -289.36 | `weekday`/`Monday` -437.18 | `dd_or_month_hole_uncomfortable` |
| 9 | `s264_aia` | `abl_session_timing` | 1275.28 | 1.53 | 330 | 19.17 | `2024-12` -275.63 | `weekday`/`Monday` -276.73 | `dd_or_month_hole_uncomfortable` |
| 10 | `s264_aih` | `abl_volatility_bandwidth` | 1269.97 | 1.53 | 323 | 17.52 | `2024-12` -227.63 | `weekday`/`Monday` -292.57 | `dd_or_month_hole_uncomfortable` |

## Candidate Summary(후보 요약)

| candidate(후보) | tests(시험 수) | constructive(건설적 행) | holes(구멍 수) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | worst month net(최악 월 순수익) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_aia` | 5 | 2 | 5 | 1237.64 | 1093.77 | 20.98 | -302.52 | `candidate_has_constructive_clues_but_not_selected` |
| `s258_stc` | 5 | 2 | 5 | 1170.61 | 906.92 | 21.43 | -289.36 | `candidate_has_constructive_clues_but_not_selected` |
| `s262_lih` | 5 | 1 | 4 | 871.47 | 34.85 | 22.36 | -283.07 | `candidate_has_constructive_clues_but_not_selected` |
| `s264_aih` | 4 | 0 | 4 | 1168.95 | 1097.96 | 19.46 | -280.42 | `candidate_needs_pressure_or_prune` |
| `s264_lc` | 5 | 0 | 4 | 1046.69 | 52.75 | 20.42 | -246.12 | `candidate_needs_pressure_or_prune` |

## Worst Tier A Slices(최악 Tier A 구간)

| candidate(후보) | test(시험) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `s258_stc` | `abl_volatility_bandwidth` | `weekday` | `Monday` | -437.18 | 51 | `deep_negative_or_dd_slice` |
| `s264_aia` | `abl_volatility_bandwidth` | `weekday` | `Monday` | -378.04 | 46 | `deep_negative_or_dd_slice` |
| `s264_aia` | `rep_trend_strength_adx` | `weekday` | `Monday` | -319.36 | 49 | `deep_negative_or_dd_slice` |
| `s264_aia` | `abl_trend_strength_direction` | `weekday` | `Monday` | -319.19 | 48 | `deep_negative_or_dd_slice` |
| `s262_lih` | `rep_volatility_atr` | `weekday` | `Monday` | -312.35 | 50 | `deep_negative_or_dd_slice` |
| `s258_stc` | `abl_trend_strength_direction` | `weekday` | `Monday` | -304.16 | 47 | `deep_negative_or_dd_slice` |
| `s264_aia` | `abl_trend_strength_direction` | `month` | `2024-12` | -302.52 | 27 | `deep_negative_or_dd_slice` |
| `s264_aih` | `rep_trend_strength_adx` | `weekday` | `Monday` | -294.38 | 48 | `deep_negative_or_dd_slice` |
| `s264_aih` | `abl_volatility_bandwidth` | `weekday` | `Monday` | -292.57 | 49 | `deep_negative_or_dd_slice` |
| `s262_lih` | `abl_trend_strength_direction` | `weekday` | `Monday` | -289.77 | 49 | `deep_negative_or_dd_slice` |
| `s258_stc` | `abl_volatility_bandwidth` | `month` | `2024-12` | -289.36 | 28 | `deep_negative_or_dd_slice` |
| `s264_lc` | `abl_gate_variant_rule` | `weekday` | `Monday` | -283.80 | 68 | `deep_negative_or_dd_slice` |

## Forensics Boundary(포렌식 경계)

- tester_identity(테스터 정체성): terminal count(터미널 수) `1`, symbol(심볼) `US100`, timeframe(시간봉) `M5`, date range(날짜 범위) `2024.01.02` to `2025.01.01`.
- trade_evidence(거래 근거): trade records(거래 기록) `15298`, parser checks(파서 점검) `48`.
- cost_assumptions(비용 가정): `spread_commission_slippage_follow_strategy_tester_report_no_cost_edge_claim`.
- backtest_judgment(백테스트 판정): `usable_with_boundary`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Y/true_internal_ablation_kpi_signature_review/review_result.json`.
- producer(생산자): `stage_pipelines/stage267/run267Z_true_internal_ablation_balance_timeslice_trade_quality_review.py`.
- consumer(소비자): `run267AA_true_internal_ablation_followup_or_adapter_design`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Z/true_internal_ablation_balance_timeslice_trade_quality_review/trade_records.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Z/true_internal_ablation_balance_timeslice_trade_quality_review/time_slice_kpi.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Z/true_internal_ablation_balance_timeslice_trade_quality_review/curve_diagnostics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Z/true_internal_ablation_balance_timeslice_trade_quality_review/review_result.json`.
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Boundary(경계)

- positive_claim(긍정 주장): `none`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- missing_required(필수 누락): real fallback/routed robustness(실제 대체/라우팅 견고성), broader period pressure(더 넓은 기간 압박), Adapter follow-up(어댑터 후속).
- next_action(다음 행동): `run267AA_true_internal_ablation_followup_or_adapter_design`.
