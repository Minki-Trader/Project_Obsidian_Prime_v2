# Stage267 Run267N Pool-Wide P0 MT5 Execution(267단계 267N 후보군 전체 P0 MT5 실행)

- action(행동): `48` of `48` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): run267M(267M 실행)의 P0 queue(P0 큐)와 run267N(267N 실행)의 feature/model/set/ini(피처/모델/설정/초기화) 묶음이 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 연결되는지 확인한다.
- status(상태): `run267N_pool_wide_ablation_replacement_mt5_batch_completed`
- completed_reports(완료 보고서): `48`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `48`
- direct_runtime_surface_attempts(직접 런타임 표면 시도): `6`
- proxy_adapter_attempts(대체 어댑터 시도): `42`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 해석)

이번 실행은 후보 선발이 아니다. 효과는 다섯 Baseline candidates(기준 후보)의 P0 ablation/replacement(우선 제거/대체) 변형이 MT5(MetaTrader 5, 메타트레이더5)에서 실제로 돌아가는지 확인하는 것이다.
direct runtime surface(직접 런타임 표면) 변형과 proxy adapter(대체 어댑터) 변형은 같은 의미가 아니다. 효과는 내부 feature(피처) 직접 제거와 우회적 score table(점수표) 변형을 섞어 과장하지 않게 하는 것이다.
이 실행은 ONNX(모델 교환 형식) 검토가 아니다. 효과는 다음 review(검토)에서 누가 덜 깨졌는지 볼 수 있는 재료를 만드는 것이다.

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`, runtime module hashes(런타임 모듈 해시)는 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/execution_result.json`에 기록했다.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/kpi_summary.csv`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건에 따른다. 별도 비용 우위는 주장하지 않는다.
- backtest_judgment(백테스트 판정): `run267N_pool_wide_ablation_replacement_mt5_batch_completed` with boundary(경계) `diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| candidate(후보) | test(시험) | boundary(경계) | record_view(기록 보기) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_aih_abl_volatility_bandwidth_historical_2024_tier_a_train_era_stress` | 412.57 | 1.35 | 314 | 15.9 |
| `s264_aih` | `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_aih_abl_volatility_bandwidth_historical_2024_tier_a_train_era_stress` | 412.57 | 1.35 | 314 | 15.9 |
| `s264_aih` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_aih_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 176.35 | 1.13 | 340 | 25.47 |
| `s264_aih` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_aih_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 176.35 | 1.13 | 340 | 25.47 |
| `s264_aih` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_aih_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 176.35 | 1.13 | 340 | 25.47 |
| `s264_aih` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_aih_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 176.35 | 1.13 | 340 | 25.47 |
| `s264_aih` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_aih_rep_volatility_atr_historical_2024_tier_a_train_era_stress` | 412.57 | 1.35 | 314 | 15.9 |
| `s264_aih` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_aih_rep_volatility_atr_historical_2024_tier_a_train_era_stress` | 412.57 | 1.35 | 314 | 15.9 |
| `s264_lc` | `abl_gate_rank_bucket` | `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | `mt5_ta_s264_lc_abl_gate_rank_bucket_historical_2024_tier_a_train_era_stress` | -32.52 | 0.98 | 350 | 42.67 |
| `s264_lc` | `abl_gate_rank_bucket` | `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | `mt5_rt_s264_lc_abl_gate_rank_bucket_historical_2024_tier_a_train_era_stress` | -32.52 | 0.98 | 350 | 42.67 |
| `s264_lc` | `abl_gate_variant_rule` | `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | `mt5_ta_s264_lc_abl_gate_variant_rule_historical_2024_tier_a_train_era_stress` | 1227.99 | 1.24 | 516 | 22.97 |
| `s264_lc` | `abl_gate_variant_rule` | `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | `mt5_rt_s264_lc_abl_gate_variant_rule_historical_2024_tier_a_train_era_stress` | 1227.99 | 1.24 | 516 | 22.97 |
| `s264_lc` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_lc_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 162.73 | 1.12 | 337 | 26.15 |
| `s264_lc` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_lc_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 162.73 | 1.12 | 337 | 26.15 |
| `s264_lc` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_lc_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 162.73 | 1.12 | 337 | 26.15 |
| `s264_lc` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_lc_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 162.73 | 1.12 | 337 | 26.15 |
| `s264_lc` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_lc_rep_volatility_atr_historical_2024_tier_a_train_era_stress` | 396.18 | 1.34 | 312 | 16.81 |
| `s264_lc` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_lc_rep_volatility_atr_historical_2024_tier_a_train_era_stress` | 396.18 | 1.34 | 312 | 16.81 |
| `s262_lih` | `abl_gate_rank_bucket` | `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | `mt5_ta_s262_lih_abl_gate_rank_bucket_historical_2024_tier_a_train_era_stress` | -51.96 | 0.97 | 352 | 45.33 |
| `s262_lih` | `abl_gate_rank_bucket` | `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | `mt5_rt_s262_lih_abl_gate_rank_bucket_historical_2024_tier_a_train_era_stress` | -51.96 | 0.97 | 352 | 45.33 |
| `s262_lih` | `abl_ma_trend` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s262_lih_abl_ma_trend_historical_2024_tier_a_train_era_stress` | 98.52 | 1.07 | 345 | 31.12 |
| `s262_lih` | `abl_ma_trend` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s262_lih_abl_ma_trend_historical_2024_tier_a_train_era_stress` | 98.52 | 1.07 | 345 | 31.12 |
| `s262_lih` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s262_lih_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 140.02 | 1.1 | 339 | 27.5 |
| `s262_lih` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s262_lih_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 140.02 | 1.1 | 339 | 27.5 |
| `s262_lih` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s262_lih_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 140.02 | 1.1 | 339 | 27.5 |
| `s262_lih` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s262_lih_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 140.02 | 1.1 | 339 | 27.5 |
| `s262_lih` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s262_lih_rep_volatility_atr_historical_2024_tier_a_train_era_stress` | 380.99 | 1.33 | 313 | 18.05 |
| `s262_lih` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s262_lih_rep_volatility_atr_historical_2024_tier_a_train_era_stress` | 380.99 | 1.33 | 313 | 18.05 |
| `s264_aia` | `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_aia_abl_volatility_bandwidth_historical_2024_tier_a_train_era_stress` | 408.29 | 1.35 | 315 | 15.85 |
| `s264_aia` | `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_aia_abl_volatility_bandwidth_historical_2024_tier_a_train_era_stress` | 408.29 | 1.35 | 315 | 15.85 |
| `s264_aia` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_aia_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 176.35 | 1.13 | 340 | 25.47 |
| `s264_aia` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_aia_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 176.35 | 1.13 | 340 | 25.47 |
| `s264_aia` | `abl_session_timing` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_aia_abl_session_timing_historical_2024_tier_a_train_era_stress` | 365.09 | 1.23 | 332 | 18.53 |
| `s264_aia` | `abl_session_timing` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_aia_abl_session_timing_historical_2024_tier_a_train_era_stress` | 365.09 | 1.23 | 332 | 18.53 |
| `s264_aia` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_aia_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 176.35 | 1.13 | 340 | 25.47 |
| `s264_aia` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_aia_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 176.35 | 1.13 | 340 | 25.47 |
| `s264_aia` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s264_aia_rep_volatility_atr_historical_2024_tier_a_train_era_stress` | 408.29 | 1.35 | 315 | 15.85 |
| `s264_aia` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s264_aia_rep_volatility_atr_historical_2024_tier_a_train_era_stress` | 408.29 | 1.35 | 315 | 15.85 |
| `s258_stc` | `abl_price_return_range` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s258_stc_abl_price_return_range_historical_2024_tier_a_train_era_stress` | 265.82 | 1.19 | 335 | 27.03 |
| `s258_stc` | `abl_price_return_range` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s258_stc_abl_price_return_range_historical_2024_tier_a_train_era_stress` | 265.82 | 1.19 | 335 | 27.03 |
| `s258_stc` | `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s258_stc_abl_volatility_bandwidth_historical_2024_tier_a_train_era_stress` | 442.13 | 1.33 | 335 | 19.33 |
| `s258_stc` | `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s258_stc_abl_volatility_bandwidth_historical_2024_tier_a_train_era_stress` | 442.13 | 1.33 | 335 | 19.33 |
| `s258_stc` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s258_stc_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 195.44 | 1.12 | 364 | 31.04 |
| `s258_stc` | `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s258_stc_abl_trend_strength_directi_historical_2024_tier_a_train_era_stress` | 195.44 | 1.12 | 364 | 31.04 |
| `s258_stc` | `abl_session_timing` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s258_stc_abl_session_timing_historical_2024_tier_a_train_era_stress` | 317.33 | 1.18 | 354 | 25.5 |
| `s258_stc` | `abl_session_timing` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s258_stc_abl_session_timing_historical_2024_tier_a_train_era_stress` | 317.33 | 1.18 | 354 | 25.5 |
| `s258_stc` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_ta_s258_stc_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 195.44 | 1.12 | 364 | 31.04 |
| `s258_stc` | `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | `mt5_rt_s258_stc_rep_trend_strength_adx_historical_2024_tier_a_train_era_stress` | 195.44 | 1.12 | 364 | 31.04 |

## Boundary(경계)

- result_subject(결과 대상): `run267N_pool_wide_ablation_replacement_p0_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).
- evidence_missing(빠진 근거): full batch completion(전체 묶음 완료)이 partial(부분)일 수 있음, balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 핵심 성과 지표) 검토, ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267N_review_pool_wide_ablation_replacement_p0_mt5_results`.
