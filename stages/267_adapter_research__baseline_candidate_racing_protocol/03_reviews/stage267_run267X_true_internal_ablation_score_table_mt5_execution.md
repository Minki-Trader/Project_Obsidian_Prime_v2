# Stage267 Run267X True Internal Ablation Score Table MT5 Execution(267단계 267X 진짜 내부 제거 점수표 MT5 실행)

- action(행동): `48` of `48` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): run267W(267W 실행)의 score table/model(점수표/모델)이 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 이어지는지 확인한다.
- status(상태): `run267X_true_internal_ablation_score_table_mt5_batch_completed`
- completed_reports(완료 보고서): `48`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `48`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stage_pipelines/stage267/run267W_true_internal_ablation_score_table_materialization.py` and `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267W_true_internal_ablation_score_table_materialization.md`.
- runtime_path(런타임 경로): `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, source attempts(원천 시도) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/attempts.csv`, execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/execution_result.json`.
- shared_contract(공유 계약): US100 M5, 2024 historical stress window(2024 과거 압박 구간), true internal feature order(진짜 내부 피처 순서), supervised EBM score table(지도학습 EBM 점수표), set/ini identity(설정/초기화 정체성).
- known_differences(알려진 차이): score table(점수표)은 true internal feature order(진짜 내부 피처 순서)로 재학습됐고, 이전 proxy adapter(대체 어댑터) 결과와 같은 의미가 아니다.
- parity_check(동등성 확인): score table parity(점수표 동등성)는 run267W(267W 실행)에서 24/24 통과했고, 이번 실행은 MT5 tester output(테스터 출력) 연결 확인이다.
- runtime_claim_boundary(런타임 주장 경계): `runtime_probe(런타임 탐침)` only, no runtime authority(런타임 권위 없음).

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`, module hashes(모듈 해시) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/execution_result.json`.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/kpi_summary.csv`.
- cost_assumptions(비용 가정): Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 spread/commission/slippage(스프레드/수수료/슬리피지) 우위 주장은 하지 않는다.
- backtest_judgment(백테스트 판정): `run267X_true_internal_ablation_score_table_mt5_batch_completed` with boundary(경계) `diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| candidate(후보) | test(시험) | record_view(기록 보기) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `abl_volatility_bandwidth` | `mt5_ta_s264_aih_abl_volatility_bandwidth_true_historical_2024_tier_a_train_era_stress` | 1269.97 | 1.53 | 323 | 17.52 |
| `s264_aih` | `abl_volatility_bandwidth` | `mt5_rt_s264_aih_abl_volatility_bandwidth_true_historical_2024_tier_a_train_era_stress` | 1269.97 | 1.53 | 323 | 17.52 |
| `s264_aih` | `abl_trend_strength_direction` | `mt5_ta_s264_aih_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 1130.52 | 1.44 | 354 | 19.46 |
| `s264_aih` | `abl_trend_strength_direction` | `mt5_rt_s264_aih_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 1130.52 | 1.44 | 354 | 19.46 |
| `s264_aih` | `rep_trend_strength_adx` | `mt5_ta_s264_aih_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1097.96 | 1.51 | 308 | 18.19 |
| `s264_aih` | `rep_trend_strength_adx` | `mt5_rt_s264_aih_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1097.96 | 1.51 | 308 | 18.19 |
| `s264_aih` | `rep_volatility_atr` | `mt5_ta_s264_aih_rep_volatility_atr_true_historical_2024_tier_a_train_era_stress` | 1177.35 | 1.52 | 337 | 17.25 |
| `s264_aih` | `rep_volatility_atr` | `mt5_rt_s264_aih_rep_volatility_atr_true_historical_2024_tier_a_train_era_stress` | 1177.35 | 1.52 | 337 | 17.25 |
| `s264_lc` | `abl_gate_rank_bucket` | `mt5_ta_s264_lc_abl_gate_rank_bucket_true_historical_2024_tier_a_train_era_stress` | 52.75 | 1.09 | 165 | 20.42 |
| `s264_lc` | `abl_gate_rank_bucket` | `mt5_rt_s264_lc_abl_gate_rank_bucket_true_historical_2024_tier_a_train_era_stress` | 52.75 | 1.09 | 165 | 20.42 |
| `s264_lc` | `abl_gate_variant_rule` | `mt5_ta_s264_lc_abl_gate_variant_rule_true_historical_2024_tier_a_train_era_stress` | 1700.94 | 1.47 | 400 | 19.42 |
| `s264_lc` | `abl_gate_variant_rule` | `mt5_rt_s264_lc_abl_gate_variant_rule_true_historical_2024_tier_a_train_era_stress` | 1700.94 | 1.47 | 400 | 19.42 |
| `s264_lc` | `abl_trend_strength_direction` | `mt5_ta_s264_lc_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 1166.55 | 1.51 | 330 | 18.28 |
| `s264_lc` | `abl_trend_strength_direction` | `mt5_rt_s264_lc_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 1166.55 | 1.51 | 330 | 18.28 |
| `s264_lc` | `rep_trend_strength_adx` | `mt5_ta_s264_lc_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1108.83 | 1.46 | 343 | 16.92 |
| `s264_lc` | `rep_trend_strength_adx` | `mt5_rt_s264_lc_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1108.83 | 1.46 | 343 | 16.92 |
| `s264_lc` | `rep_volatility_atr` | `mt5_ta_s264_lc_rep_volatility_atr_true_historical_2024_tier_a_train_era_stress` | 1204.36 | 1.51 | 330 | 18.86 |
| `s264_lc` | `rep_volatility_atr` | `mt5_rt_s264_lc_rep_volatility_atr_true_historical_2024_tier_a_train_era_stress` | 1204.36 | 1.51 | 330 | 18.86 |
| `s262_lih` | `abl_gate_rank_bucket` | `mt5_ta_s262_lih_abl_gate_rank_bucket_true_historical_2024_tier_a_train_era_stress` | 34.85 | 1.06 | 167 | 22.36 |
| `s262_lih` | `abl_gate_rank_bucket` | `mt5_rt_s262_lih_abl_gate_rank_bucket_true_historical_2024_tier_a_train_era_stress` | 34.85 | 1.06 | 167 | 22.36 |
| `s262_lih` | `abl_ma_trend` | `mt5_ta_s262_lih_abl_ma_trend_true_historical_2024_tier_a_train_era_stress` | 834.52 | 1.41 | 309 | 19.05 |
| `s262_lih` | `abl_ma_trend` | `mt5_rt_s262_lih_abl_ma_trend_true_historical_2024_tier_a_train_era_stress` | 834.52 | 1.41 | 309 | 19.05 |
| `s262_lih` | `abl_trend_strength_direction` | `mt5_ta_s262_lih_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 1111.75 | 1.46 | 343 | 20.34 |
| `s262_lih` | `abl_trend_strength_direction` | `mt5_rt_s262_lih_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 1111.75 | 1.46 | 343 | 20.34 |
| `s262_lih` | `rep_trend_strength_adx` | `mt5_ta_s262_lih_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1116.28 | 1.52 | 331 | 17.88 |
| `s262_lih` | `rep_trend_strength_adx` | `mt5_rt_s262_lih_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1116.28 | 1.52 | 331 | 17.88 |
| `s262_lih` | `rep_volatility_atr` | `mt5_ta_s262_lih_rep_volatility_atr_true_historical_2024_tier_a_train_era_stress` | 1259.93 | 1.53 | 325 | 16.85 |
| `s262_lih` | `rep_volatility_atr` | `mt5_rt_s262_lih_rep_volatility_atr_true_historical_2024_tier_a_train_era_stress` | 1259.93 | 1.53 | 325 | 16.85 |
| `s264_aia` | `abl_volatility_bandwidth` | `mt5_ta_s264_aia_abl_volatility_bandwidth_true_historical_2024_tier_a_train_era_stress` | 1093.77 | 1.53 | 290 | 18.4 |
| `s264_aia` | `abl_volatility_bandwidth` | `mt5_rt_s264_aia_abl_volatility_bandwidth_true_historical_2024_tier_a_train_era_stress` | 1093.77 | 1.53 | 290 | 18.4 |
| `s264_aia` | `abl_trend_strength_direction` | `mt5_ta_s264_aia_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 1237.02 | 1.5 | 329 | 20.98 |
| `s264_aia` | `abl_trend_strength_direction` | `mt5_rt_s264_aia_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 1237.02 | 1.5 | 329 | 20.98 |
| `s264_aia` | `abl_session_timing` | `mt5_ta_s264_aia_abl_session_timing_true_historical_2024_tier_a_train_era_stress` | 1275.28 | 1.53 | 330 | 19.17 |
| `s264_aia` | `abl_session_timing` | `mt5_rt_s264_aia_abl_session_timing_true_historical_2024_tier_a_train_era_stress` | 1275.28 | 1.53 | 330 | 19.17 |
| `s264_aia` | `rep_trend_strength_adx` | `mt5_ta_s264_aia_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1390.83 | 1.56 | 332 | 15.44 |
| `s264_aia` | `rep_trend_strength_adx` | `mt5_rt_s264_aia_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1390.83 | 1.56 | 332 | 15.44 |
| `s264_aia` | `rep_volatility_atr` | `mt5_ta_s264_aia_rep_volatility_atr_true_historical_2024_tier_a_train_era_stress` | 1191.32 | 1.53 | 339 | 16.07 |
| `s264_aia` | `rep_volatility_atr` | `mt5_rt_s264_aia_rep_volatility_atr_true_historical_2024_tier_a_train_era_stress` | 1191.32 | 1.53 | 339 | 16.07 |
| `s258_stc` | `abl_price_return_range` | `mt5_ta_s258_stc_abl_price_return_range_true_historical_2024_tier_a_train_era_stress` | 1002.4 | 1.46 | 315 | 19.01 |
| `s258_stc` | `abl_price_return_range` | `mt5_rt_s258_stc_abl_price_return_range_true_historical_2024_tier_a_train_era_stress` | 1002.4 | 1.46 | 315 | 19.01 |
| `s258_stc` | `abl_volatility_bandwidth` | `mt5_ta_s258_stc_abl_volatility_bandwidth_true_historical_2024_tier_a_train_era_stress` | 1393.91 | 1.5 | 336 | 18.57 |
| `s258_stc` | `abl_volatility_bandwidth` | `mt5_rt_s258_stc_abl_volatility_bandwidth_true_historical_2024_tier_a_train_era_stress` | 1393.91 | 1.5 | 336 | 18.57 |
| `s258_stc` | `abl_trend_strength_direction` | `mt5_ta_s258_stc_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 906.92 | 1.38 | 325 | 21.43 |
| `s258_stc` | `abl_trend_strength_direction` | `mt5_rt_s258_stc_abl_trend_strength_directi_true_historical_2024_tier_a_train_era_stress` | 906.92 | 1.38 | 325 | 21.43 |
| `s258_stc` | `abl_session_timing` | `mt5_ta_s258_stc_abl_session_timing_true_historical_2024_tier_a_train_era_stress` | 1136.16 | 1.47 | 348 | 17.79 |
| `s258_stc` | `abl_session_timing` | `mt5_rt_s258_stc_abl_session_timing_true_historical_2024_tier_a_train_era_stress` | 1136.16 | 1.47 | 348 | 17.79 |
| `s258_stc` | `rep_trend_strength_adx` | `mt5_ta_s258_stc_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1413.66 | 1.49 | 340 | 19.15 |
| `s258_stc` | `rep_trend_strength_adx` | `mt5_rt_s258_stc_rep_trend_strength_adx_true_historical_2024_tier_a_train_era_stress` | 1413.66 | 1.49 | 340 | 19.15 |

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/run_manifest.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/true_internal_ablation_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/runtime_contract.csv`.
- producer(생산자): `stage_pipelines/stage267/run267X_true_internal_ablation_score_table_executor.py`.
- consumer(소비자): `run267Y_review_true_internal_ablation_score_table_mt5_results`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267X/true_internal_ablation_score_table_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267X_true_internal_ablation_score_table_mt5_execution.md`.
- availability(가용성): tracked after commit(커밋 후 추적 가능).
- lineage_judgment(계보 판정): `connected_with_boundary` because MT5 execution(실행)은 되었더라도 candidate selection(후보 선택)은 없다.

## Boundary(경계)

- result_subject(결과 대상): `run267X_true_internal_ablation_score_table_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).
- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 KPI) 검토, candidate elimination/update(후보 탈락/갱신), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- next_action(다음 행동): `run267Y_review_true_internal_ablation_score_table_mt5_results`.
