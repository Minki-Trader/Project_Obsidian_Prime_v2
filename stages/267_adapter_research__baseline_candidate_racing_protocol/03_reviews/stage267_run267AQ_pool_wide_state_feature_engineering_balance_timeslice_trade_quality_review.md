# Stage267 Run267AQ Pool-wide State Feature Engineering Balance/Time-Slice/Trade-Quality Review(267단계 267AQ 후보군 전체 상태 피처 엔지니어링 잔액/시간구간/거래품질 검토)

- action(행동): run267AP(267AP 실행)의 `40` MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 거래 단위로 다시 파싱했다.
- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고, balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 같이 본다.
- status(상태): `run267AQ_pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review_completed`
- judgment(판정): `diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection`
- trade_records(거래 기록): `12248`
- candidate_profile_rows(후보-상태프로필 행): `20`
- followup_watch_rows(후속 관찰 행): `0`
- negative_tier_a_slices(음수 Tier A 구간): `99`
- parser_errors(파서 오류): `0`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 해석)

이번 결과는 좋아 보이는 숫자가 꽤 많다. 하지만 이것은 선택이 아니다.
Effect(효과): 다음 run267AR(267AR 실행)에서는 강한 축을 더 압박하거나, 구간 구멍이 큰 축은 과감히 가지치기할 수 있다.

Tier A+B(Tier A+B 합산)는 이번에도 duplicate boundary(중복 경계)다.
Effect(효과): routed fallback robustness(라우팅 대체 견고성) 근거가 아니라 Tier A(티어 A)와 같은 결과가 반복됐는지 확인하는 감사 근거로만 쓴다.

## Candidate-Profile Watchlist(후보-상태프로필 관찰 목록)

| rank(순위) | candidate(후보) | state_profile(상태 프로필) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1 | `s258_stc` | `volatility_regime_expansion` | 1450.57 | 1.59 | 303 | 18.01 | `2024-12` -241.73 | `weekday`/`Monday` -394.14 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |
| 2 | `s258_stc` | `trend_strength_disagreement` | 1385.53 | 1.54 | 321 | 18.75 | `2024-12` -239.82 | `month`/`2024-12` -239.82 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |
| 3 | `s264_aih` | `range_expansion_pressure` | 1297.62 | 1.64 | 312 | 17.55 | `2024-12` -270.78 | `month`/`2024-12` -270.78 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |
| 4 | `s264_aih` | `volatility_regime_expansion` | 1297.57 | 1.62 | 309 | 18.54 | `2024-12` -289.49 | `month`/`2024-12` -289.49 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |
| 5 | `s262_lih` | `volatility_regime_expansion` | 1196.86 | 1.59 | 298 | 17.89 | `2024-12` -227.68 | `weekday`/`Monday` -283.73 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |
| 6 | `s264_aia` | `volatility_regime_expansion` | 1167.06 | 1.59 | 305 | 17.48 | `2024-12` -220.35 | `weekday`/`Monday` -279.00 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |
| 7 | `s264_aia` | `range_expansion_pressure` | 1151.94 | 1.61 | 309 | 15.07 | `2024-12` -161.26 | `weekday`/`Monday` -278.42 | `constructive_but_slice_pressure_needed(건설적이나 구간 압박 필요)` |
| 8 | `s264_aih` | `return_shock_absorption` | 1145.81 | 1.59 | 317 | 17.23 | `2024-12` -245.88 | `weekday`/`Monday` -248.98 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |
| 9 | `s264_lc` | `volatility_regime_expansion` | 1145.20 | 1.57 | 309 | 18.40 | `2024-12` -258.48 | `weekday`/`Monday` -280.51 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |
| 10 | `s262_lih` | `range_expansion_pressure` | 1136.40 | 1.58 | 300 | 17.92 | `2024-12` -222.02 | `weekday`/`Monday` -275.19 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |
| 11 | `s264_aia` | `return_shock_absorption` | 1119.25 | 1.60 | 310 | 14.77 | `2024-12` -154.12 | `weekday`/`Monday` -273.11 | `constructive_but_slice_pressure_needed(건설적이나 구간 압박 필요)` |
| 12 | `s262_lih` | `return_shock_absorption` | 1117.68 | 1.57 | 305 | 17.71 | `2024-12` -217.57 | `weekday`/`Monday` -274.62 | `needs_pressure_or_prune(추가 압박 또는 가지치기 필요)` |

## Candidate Summary(후보 요약)

| candidate(후보) | profiles(프로필 수) | followup(후속 관찰) | holes(구멍) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | worst month net(최악 월 순수익) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s258_stc` | 4 | 0 | 4 | 1157.32 | 885.68 | 18.75 | -241.73 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s264_aih` | 4 | 0 | 4 | 1146.43 | 844.71 | 18.54 | -289.49 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s264_aia` | 4 | 0 | 4 | 1113.34 | 1015.10 | 19.11 | -220.90 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s262_lih` | 4 | 0 | 4 | 1103.33 | 962.36 | 17.93 | -227.68 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s264_lc` | 4 | 0 | 4 | 1101.04 | 1062.29 | 18.40 | -258.48 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |

## State Profile Summary(상태 프로필 요약)

| state_profile(상태 프로필) | source_test_id(원천 시험 ID) | followup(후속 관찰) | holes(구멍) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | best candidate(최고 후보) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `volatility_regime_expansion` | `abl_volatility_bandwidth` | 0 | 1 | 1450.57 | 1450.57 | 18.01 | `s258_stc` | `weak_or_fragile_state_profile(약하거나 취약한 상태 프로필)` |
| `volatility_regime_expansion` | `rep_volatility_atr` | 0 | 4 | 1201.67 | 1145.20 | 18.54 | `s264_aih` | `weak_or_fragile_state_profile(약하거나 취약한 상태 프로필)` |
| `range_expansion_pressure` | `rep_volatility_atr` | 0 | 4 | 1162.06 | 1062.29 | 17.92 | `s264_aih` | `weak_or_fragile_state_profile(약하거나 취약한 상태 프로필)` |
| `return_shock_absorption` | `rep_volatility_atr` | 0 | 4 | 1121.89 | 1104.84 | 17.71 | `s264_aih` | `weak_or_fragile_state_profile(약하거나 취약한 상태 프로필)` |
| `trend_strength_disagreement` | `rep_trend_strength_adx` | 0 | 5 | 1059.90 | 844.71 | 19.11 | `s258_stc` | `weak_or_fragile_state_profile(약하거나 취약한 상태 프로필)` |
| `range_expansion_pressure` | `abl_price_return_range` | 0 | 1 | 907.51 | 907.51 | 18.03 | `s258_stc` | `weak_or_fragile_state_profile(약하거나 취약한 상태 프로필)` |
| `return_shock_absorption` | `abl_price_return_range` | 0 | 1 | 885.68 | 885.68 | 17.67 | `s258_stc` | `weak_or_fragile_state_profile(약하거나 취약한 상태 프로필)` |

## Worst Tier A Slices(최악 Tier A 구간)

| candidate(후보) | state_profile(상태 프로필) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `s258_stc` | `volatility_regime_expansion` | `weekday` | `Monday` | -394.14 | 44 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aia` | `trend_strength_disagreement` | `weekday` | `Monday` | -330.16 | 46 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s258_stc` | `range_expansion_pressure` | `weekday` | `Monday` | -291.27 | 42 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aih` | `volatility_regime_expansion` | `month` | `2024-12` | -289.49 | 27 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s262_lih` | `volatility_regime_expansion` | `weekday` | `Monday` | -283.73 | 46 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s258_stc` | `return_shock_absorption` | `weekday` | `Monday` | -283.01 | 44 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_lc` | `range_expansion_pressure` | `weekday` | `Monday` | -281.82 | 47 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_lc` | `return_shock_absorption` | `weekday` | `Monday` | -281.69 | 47 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_lc` | `volatility_regime_expansion` | `weekday` | `Monday` | -280.51 | 46 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aia` | `volatility_regime_expansion` | `weekday` | `Monday` | -279.00 | 45 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aia` | `range_expansion_pressure` | `weekday` | `Monday` | -278.42 | 45 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s262_lih` | `range_expansion_pressure` | `weekday` | `Monday` | -275.19 | 46 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s262_lih` | `return_shock_absorption` | `weekday` | `Monday` | -274.62 | 47 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aia` | `return_shock_absorption` | `weekday` | `Monday` | -273.11 | 46 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |

## Forensics Boundary(포렌식 경계)

- tester_identity(테스터 정체성): terminal count(터미널 수) `1`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, date range(날짜 범위) `2024.01.02` to `2025.01.01`.
- trade_evidence(거래 근거): trade records(거래 기록) `12248`, parser checks(파서 확인) `40`.
- cost_assumptions(비용 가정): `spread_commission_slippage_follow_strategy_tester_report_no_cost_edge_claim(스프레드/수수료/슬리피지는 전략 테스터 보고서를 따르며 비용 우위 주장은 없음)`.
- backtest_judgment(백테스트 판정): `usable_with_boundary(경계부 사용 가능)`.

## Attribution(성과 귀속)

- observed_change(관측 변화): run267B(267B 실행) 2024 base(기준)보다 headline KPI(대표 KPI)는 크게 좋아졌다.
- comparison_baseline(비교 기준): run267B historical 2024(2024 과거 압박) MT5 KPI(MT5 핵심 성과 지표)와 curve diagnostics(곡선 진단).
- likely_drivers(가능 동인): state feature score table extension(상태 피처 점수표 확장)과 threshold surface(임계값 표면) 변화다. 재학습(retraining, 재학습)은 아니다.
- alternative_explanations(대안 설명): 2024 단일 기간 적합, 중복 Tier A+B 경계, state feature(상태 피처) 점수표 항 추가에 따른 우연 적합 가능성이 남아 있다.
- attribution_confidence(귀속 신뢰도): `medium_for_2024_diagnostic_only(2024 진단 한정 중간)`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/state_feature_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/runtime_contract.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AQ_pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review.py`.
- consumer(소비자): `run267AR_design_pool_wide_state_feature_engineering_followup_or_adapter_branch`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AQ/pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review/trade_records.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AQ/pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review/time_slice_kpi.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AQ/pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review/curve_diagnostics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AQ/pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review/review_result.json`.
- lineage_judgment(계보 판정): `connected_with_boundary(경계부 연결)`.

## Boundary(경계)

- positive_claim(긍정 주장): `none(없음)`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- missing_required(필수 누락): real fallback/routed robustness(실제 대체 라우팅 견고성), broader period pressure(더 넓은 기간 압박), Adapter follow-up(어댑터 후속), ONNX parity(ONNX 동등성).
- next_action(다음 행동): `run267AR_design_pool_wide_state_feature_engineering_followup_or_adapter_branch`.
