# Stage267 Run267AT Pool-wide State Feature Engineering Follow-up MT5 Execution(267단계 267AT 후보군 전체 상태 피처 엔지니어링 후속 MT5 실행)

- action(행동): `16` of `16` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): run267AS(267AS 실행)의 8개 follow-up variant(후속 변형)와 16개 MT5(MetaTrader 5, 메타트레이더5) 시도를 실제 tester output(테스터 출력), runtime telemetry(런타임 기록), KPI(핵심 성과 지표)와 연결한다.
- runtime_path_repair(런타임 경로 보정): telemetry path(기록 경로)만 `OPV2/s267at` 아래 짧은 Common Files(공통 파일) 경로로 바꿨다.
- effect(효과): model(모델), feature(피처), threshold(문턱값), risk(위험) 설정은 유지하고 MT5 file open error(파일 열기 오류) 위험만 줄인다.
- status(상태): `run267AT_pool_wide_state_feature_engineering_followup_mt5_batch_completed`
- completed_reports(완료 보고서): `16`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `16`
- candidates_touched(건드린 후보): `s258_stc;s262_lih;s264_aia;s264_aih;s264_lc`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 설명)

이번 실행은 후보를 고르는 단계가 아니다. run267AS(267AS 실행)가 만든 follow-up pressure(후속 압박) 입력을 MT5(MetaTrader 5, 메타트레이더5)에 넣어 실제 거래 결과가 생기는지 확인하는 단계다.
Effect(효과): 다음 run267AU(267AU 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 후보별로 다시 읽을 수 있다.
Tier A+B(Tier A+B 합산)는 이번에도 duplicate boundary(중복 경계)로만 읽는다. Effect(효과): synthetic sum(합성 합산)을 combined result(합산 결과)처럼 과장하지 않는다.

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, broker symbol(브로커 심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, modeling mode(모델링 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/kpi_summary.csv`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 MT5 Strategy Tester(MT5 전략 테스터)의 broker history(브로커 이력) 조건을 따른다.
- backtest_judgment(백테스트 판정): `run267AT_pool_wide_state_feature_engineering_followup_mt5_batch_completed` with boundary(경계) `runtime_diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| candidate(후보) | profile(프로필) | tier(티어) | record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `core_range_resilience_pressure_v2` | `Tier A` | `mt5_ta_s264_aih_range_expansion_pressure_as_historical_2024_tier_a_train_era_stress` | 1021.47 | 1.59 | 301 | 16.64 |
| `s264_aih` | `core_range_resilience_pressure_v2` | `Tier A+B` | `mt5_rt_s264_aih_range_expansion_pressure_as_historical_2024_tier_a_train_era_stress` | 1021.47 | 1.59 | 301 | 16.64 |
| `s264_aih` | `core_volatility_resilience_pressure_v2` | `Tier A` | `mt5_ta_s264_aih_volatility_regime_expans_as_historical_2024_tier_a_train_era_stress` | 1272.69 | 1.68 | 296 | 17.76 |
| `s264_aih` | `core_volatility_resilience_pressure_v2` | `Tier A+B` | `mt5_rt_s264_aih_volatility_regime_expans_as_historical_2024_tier_a_train_era_stress` | 1272.69 | 1.68 | 296 | 17.76 |
| `s264_aia` | `oos_anchor_dd_resilience_pressure_v2` | `Tier A` | `mt5_ta_s264_aia_range_expansion_pressure_as_historical_2024_tier_a_train_era_stress` | 1065.48 | 1.63 | 296 | 14.57 |
| `s264_aia` | `oos_anchor_dd_resilience_pressure_v2` | `Tier A+B` | `mt5_rt_s264_aia_range_expansion_pressure_as_historical_2024_tier_a_train_era_stress` | 1065.48 | 1.63 | 296 | 14.57 |
| `s264_aia` | `oos_anchor_shock_resilience_pressure_v2` | `Tier A` | `mt5_ta_s264_aia_return_shock_absorption_as_historical_2024_tier_a_train_era_stress` | 1062.17 | 1.65 | 293 | 13.71 |
| `s264_aia` | `oos_anchor_shock_resilience_pressure_v2` | `Tier A+B` | `mt5_rt_s264_aia_return_shock_absorption_as_historical_2024_tier_a_train_era_stress` | 1062.17 | 1.65 | 293 | 13.71 |
| `s258_stc` | `stress_challenger_volatility_prune_pressure_v2` | `Tier A` | `mt5_ta_s258_stc_volatility_regime_expans_as_historical_2024_tier_a_train_era_stress` | 905.51 | 1.5 | 268 | 19.87 |
| `s258_stc` | `stress_challenger_volatility_prune_pressure_v2` | `Tier A+B` | `mt5_rt_s258_stc_volatility_regime_expans_as_historical_2024_tier_a_train_era_stress` | 905.51 | 1.5 | 268 | 19.87 |
| `s258_stc` | `stress_challenger_trend_prune_pressure_v2` | `Tier A` | `mt5_ta_s258_stc_trend_strength_disagreem_as_historical_2024_tier_a_train_era_stress` | 1175.1 | 1.57 | 303 | 17.13 |
| `s258_stc` | `stress_challenger_trend_prune_pressure_v2` | `Tier A+B` | `mt5_rt_s258_stc_trend_strength_disagreem_as_historical_2024_tier_a_train_era_stress` | 1175.1 | 1.57 | 303 | 17.13 |
| `s264_lc` | `defensive_control_volatility_audit_v1` | `Tier A` | `mt5_ta_s264_lc_volatility_regime_expans_as_historical_2024_tier_a_train_era_stress` | 1218.34 | 1.69 | 289 | 17.0 |
| `s264_lc` | `defensive_control_volatility_audit_v1` | `Tier A+B` | `mt5_rt_s264_lc_volatility_regime_expans_as_historical_2024_tier_a_train_era_stress` | 1218.34 | 1.69 | 289 | 17.0 |
| `s262_lih` | `validation_control_volatility_audit_v1` | `Tier A` | `mt5_ta_s262_lih_volatility_regime_expans_as_historical_2024_tier_a_train_era_stress` | 1127.57 | 1.61 | 288 | 17.24 |
| `s262_lih` | `validation_control_volatility_audit_v1` | `Tier A+B` | `mt5_rt_s262_lih_volatility_regime_expans_as_historical_2024_tier_a_train_era_stress` | 1127.57 | 1.61 | 288 | 17.24 |

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/run_manifest.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/attempt_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/followup_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/runtime_contract.csv`.
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AS_pool_wide_state_feature_engineering_followup_materialization.md`.
- producer(생산자): `stage_pipelines/stage267/run267AT_pool_wide_state_feature_engineering_followup_mt5_executor.py`.
- consumer(소비자): `run267AU_review_pool_wide_state_feature_engineering_followup_mt5_results`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/kpi_records.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AT_pool_wide_state_feature_engineering_followup_mt5_execution.md`.
- lineage_judgment(계보 판정): `connected_with_boundary`. MT5 execution(MT5 실행)은 연결됐지만 candidate selection(후보 선택)은 없다.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267AT_pool_wide_state_feature_engineering_followup_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식), execution result(실행 결과).
- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 상세 검토, time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질), 후보 탈락/유지 판정, ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- next_condition(다음 조건): `run267AU_review_pool_wide_state_feature_engineering_followup_mt5_results`.
