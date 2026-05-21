# Stage267 Run267AP Pool-wide State Feature Engineering MT5 Execution(267단계 267AP 후보군 전체 상태 피처 엔지니어링 MT5 실행)

- action(행동): `40` of `40` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): run267AO(267AO 실행)의 후보 5개 x 상태 피처 4개 score table/model(점수표/모델)을 실제 tester output(테스터 출력), runtime telemetry(런타임 기록), KPI(핵심 성과 지표)로 연결했다.
- status(상태): `run267AP_pool_wide_state_feature_engineering_mt5_batch_completed`
- completed_reports(완료 보고서): `40`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `40`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 설명)

이번 실행은 후보를 고르는 단계가 아니다. run267AO(267AO 실행)에서 만든 네 가지 state feature(상태 피처) 축을 다섯 Baseline candidates(기준 후보군)에 붙여 MT5(MetaTrader 5, 메타트레이더5)에서 실제로 돌린 단계다.
Effect(효과): 다음 review(검토)에서 누가 더 좋은 숫자인지가 아니라, 누가 덜 깨지고 balance/equity curve(잔액/평가금 곡선)가 덜 지저분한지 볼 수 있다.

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, broker symbol(브로커 심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, modeling mode(모델링 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/kpi_summary.csv`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 MT5 Strategy Tester(MT5 전략 테스터)의 broker history(브로커 이력) 조건을 따른다.
- backtest_judgment(백테스트 판정): `run267AP_pool_wide_state_feature_engineering_mt5_batch_completed` with boundary(경계) `runtime_diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| candidate(후보) | state_profile(상태 프로필) | tier(티어) | record_view(기록 보기) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `return_shock_absorption` | `Tier A` | `mt5_ta_s264_aih_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 1145.81 | 1.59 | 317 | 17.23 |
| `s264_aih` | `return_shock_absorption` | `Tier A+B` | `mt5_rt_s264_aih_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 1145.81 | 1.59 | 317 | 17.23 |
| `s264_aih` | `volatility_regime_expansion` | `Tier A` | `mt5_ta_s264_aih_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1297.57 | 1.62 | 309 | 18.54 |
| `s264_aih` | `volatility_regime_expansion` | `Tier A+B` | `mt5_rt_s264_aih_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1297.57 | 1.62 | 309 | 18.54 |
| `s264_aih` | `range_expansion_pressure` | `Tier A` | `mt5_ta_s264_aih_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 1297.62 | 1.64 | 312 | 17.55 |
| `s264_aih` | `range_expansion_pressure` | `Tier A+B` | `mt5_rt_s264_aih_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 1297.62 | 1.64 | 312 | 17.55 |
| `s264_aih` | `trend_strength_disagreement` | `Tier A` | `mt5_ta_s264_aih_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 844.71 | 1.55 | 280 | 15.09 |
| `s264_aih` | `trend_strength_disagreement` | `Tier A+B` | `mt5_rt_s264_aih_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 844.71 | 1.55 | 280 | 15.09 |
| `s264_lc` | `return_shock_absorption` | `Tier A` | `mt5_ta_s264_lc_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 1104.84 | 1.57 | 314 | 16.89 |
| `s264_lc` | `return_shock_absorption` | `Tier A+B` | `mt5_rt_s264_lc_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 1104.84 | 1.57 | 314 | 16.89 |
| `s264_lc` | `volatility_regime_expansion` | `Tier A` | `mt5_ta_s264_lc_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1145.2 | 1.57 | 309 | 18.4 |
| `s264_lc` | `volatility_regime_expansion` | `Tier A+B` | `mt5_rt_s264_lc_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1145.2 | 1.57 | 309 | 18.4 |
| `s264_lc` | `range_expansion_pressure` | `Tier A` | `mt5_ta_s264_lc_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 1062.29 | 1.56 | 309 | 17.26 |
| `s264_lc` | `range_expansion_pressure` | `Tier A+B` | `mt5_rt_s264_lc_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 1062.29 | 1.56 | 309 | 17.26 |
| `s264_lc` | `trend_strength_disagreement` | `Tier A` | `mt5_ta_s264_lc_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 1091.82 | 1.52 | 317 | 17.62 |
| `s264_lc` | `trend_strength_disagreement` | `Tier A+B` | `mt5_rt_s264_lc_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 1091.82 | 1.52 | 317 | 17.62 |
| `s262_lih` | `return_shock_absorption` | `Tier A` | `mt5_ta_s262_lih_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 1117.68 | 1.57 | 305 | 17.71 |
| `s262_lih` | `return_shock_absorption` | `Tier A+B` | `mt5_rt_s262_lih_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 1117.68 | 1.57 | 305 | 17.71 |
| `s262_lih` | `volatility_regime_expansion` | `Tier A` | `mt5_ta_s262_lih_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1196.86 | 1.59 | 298 | 17.89 |
| `s262_lih` | `volatility_regime_expansion` | `Tier A+B` | `mt5_rt_s262_lih_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1196.86 | 1.59 | 298 | 17.89 |
| `s262_lih` | `range_expansion_pressure` | `Tier A` | `mt5_ta_s262_lih_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 1136.4 | 1.58 | 300 | 17.92 |
| `s262_lih` | `range_expansion_pressure` | `Tier A+B` | `mt5_rt_s262_lih_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 1136.4 | 1.58 | 300 | 17.92 |
| `s262_lih` | `trend_strength_disagreement` | `Tier A` | `mt5_ta_s262_lih_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 962.36 | 1.52 | 300 | 17.93 |
| `s262_lih` | `trend_strength_disagreement` | `Tier A+B` | `mt5_rt_s262_lih_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 962.36 | 1.52 | 300 | 17.93 |
| `s264_aia` | `return_shock_absorption` | `Tier A` | `mt5_ta_s264_aia_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 1119.25 | 1.6 | 310 | 14.77 |
| `s264_aia` | `return_shock_absorption` | `Tier A+B` | `mt5_rt_s264_aia_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 1119.25 | 1.6 | 310 | 14.77 |
| `s264_aia` | `volatility_regime_expansion` | `Tier A` | `mt5_ta_s264_aia_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1167.06 | 1.59 | 305 | 17.48 |
| `s264_aia` | `volatility_regime_expansion` | `Tier A+B` | `mt5_rt_s264_aia_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1167.06 | 1.59 | 305 | 17.48 |
| `s264_aia` | `range_expansion_pressure` | `Tier A` | `mt5_ta_s264_aia_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 1151.94 | 1.61 | 309 | 15.07 |
| `s264_aia` | `range_expansion_pressure` | `Tier A+B` | `mt5_rt_s264_aia_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 1151.94 | 1.61 | 309 | 15.07 |
| `s264_aia` | `trend_strength_disagreement` | `Tier A` | `mt5_ta_s264_aia_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 1015.1 | 1.49 | 314 | 19.11 |
| `s264_aia` | `trend_strength_disagreement` | `Tier A+B` | `mt5_rt_s264_aia_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 1015.1 | 1.49 | 314 | 19.11 |
| `s258_stc` | `return_shock_absorption` | `Tier A` | `mt5_ta_s258_stc_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 885.68 | 1.48 | 298 | 17.67 |
| `s258_stc` | `return_shock_absorption` | `Tier A+B` | `mt5_rt_s258_stc_return_shock_absorption_historical_2024_tier_a_train_era_stress` | 885.68 | 1.48 | 298 | 17.67 |
| `s258_stc` | `volatility_regime_expansion` | `Tier A` | `mt5_ta_s258_stc_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1450.57 | 1.59 | 303 | 18.01 |
| `s258_stc` | `volatility_regime_expansion` | `Tier A+B` | `mt5_rt_s258_stc_volatility_regime_expansion_historical_2024_tier_a_train_era_stress` | 1450.57 | 1.59 | 303 | 18.01 |
| `s258_stc` | `range_expansion_pressure` | `Tier A` | `mt5_ta_s258_stc_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 907.51 | 1.49 | 294 | 18.03 |
| `s258_stc` | `range_expansion_pressure` | `Tier A+B` | `mt5_rt_s258_stc_range_expansion_pressure_historical_2024_tier_a_train_era_stress` | 907.51 | 1.49 | 294 | 18.03 |
| `s258_stc` | `trend_strength_disagreement` | `Tier A` | `mt5_ta_s258_stc_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 1385.53 | 1.54 | 321 | 18.75 |
| `s258_stc` | `trend_strength_disagreement` | `Tier A+B` | `mt5_rt_s258_stc_trend_strength_disagreement_historical_2024_tier_a_train_era_stress` | 1385.53 | 1.54 | 321 | 18.75 |

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/run_manifest.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/attempts.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/state_feature_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/runtime_contract.csv`.
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AO_pool_wide_state_feature_engineering_materialization.md`.
- producer(생산자): `stage_pipelines/stage267/run267AP_pool_wide_state_feature_engineering_mt5_executor.py`.
- consumer(소비자): `run267AQ_review_pool_wide_state_feature_engineering_mt5_results`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/kpi_records.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AP/pool_wide_state_feature_engineering_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AP_pool_wide_state_feature_engineering_mt5_execution.md`.
- lineage_judgment(계보 판정): `connected_with_boundary`. MT5 execution(MT5 실행)은 연결됐지만 candidate selection(후보 선택)은 없다.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267AP_pool_wide_state_feature_engineering_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식), execution result(실행 결과).
- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 KPI), trade quality(거래 품질), 후보 탈락/유지 판정, ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- next_condition(다음 조건): `run267AQ_review_pool_wide_state_feature_engineering_mt5_results`.
