# Stage267 Run267T Pool-Wide Orthogonal Stability MT5 Execution(267단계 267T 후보군 전체 직교 안정성 MT5 실행)

- action(행동): `34` of `34` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): run267S(267S 실행)의 orthogonal stability matrix(직교 안정성 행렬)와 run267T(267T 실행)의 set/ini(설정/초기화) 묶음이 실제 tester output(테스터 출력), runtime telemetry(런타임 기록), KPI(핵심 성과 지표)로 이어지는지 확인한다.
- status(상태): `run267T_pool_wide_orthogonal_stability_mt5_batch_completed`
- completed_reports(완료 보고서): `34`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `34`
- candidates_touched(건드린 후보 수): `5`
- axes_touched(건드린 축 수): `2`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 해석)

이번 실행은 candidate selection(후보 선택)이 아니다. 효과는 후보군 전체 ablation/replacement(제거/대체)와 weak-slice resilience(약점 구간 견고성) 축이 MT5(MetaTrader 5, 메타트레이더5)에서 실제로 돌아가는지 먼저 확인하는 것이다.
small tranche(작은 묶음)로 실행했다면, 효과는 고장난 batch(묶음)를 오래 밀지 않고 terminal/report/runtime(터미널/보고서/런타임) 경로를 먼저 확인하는 것이다.
따라서 selected_candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 안 함)이다.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stage_pipelines/stage267/run267T_build_pool_wide_orthogonal_stability_mt5_attempts.py` and `stage_pipelines/stage267/run267T_pool_wide_orthogonal_stability_executor.py`.
- runtime_path(런타임 경로): EA entrypoint(EA 진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, attempt manifest(시도 목록) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/attempts.csv`.
- shared_contract(공유 계약): bar_time_server(서버 봉 시간), feature order hash(피처 순서 해시), CSV model table(CSV 모델 표), threshold(임계값), historical 2024 date range(2024 과거 기간).
- known_differences(알려진 차이): axis03 prune/restore(가지치기/복귀) 축은 MT5 실행 축이 아니라 decision-only(판정 전용) 축이라 gap register(공백 등록부)에 남아 있다.
- parity_check(동등성 확인): compile(컴파일), Strategy Tester report(전략 테스터 보고서), runtime telemetry(런타임 기록), KPI records(KPI 기록).
- parity_identity(동등성 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/execution_result.json`, runtime module hashes(런타임 모듈 해시)는 같은 파일에 기록했다.
- runtime_claim_boundary(런타임 주장 경계): `runtime_probe(런타임 탐침)` only; runtime authority(런타임 권위)는 주장하지 않는다.

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델 방식) `4`, date range(기간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/kpi_summary.csv`.
- trade_evidence(거래 근거): KPI records(KPI 기록) `34`, strategy reports(전략 보고서) `34`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 비용 우위는 주장하지 않는다.
- forensic_checks(포렌식 확인): settings drift(설정 이탈), missing report(보고서 누락), runtime telemetry(런타임 기록), malformed KPI(형식 오류 KPI)를 산출물로 분리했다.
- backtest_judgment(백테스트 판정): `usable_with_boundary`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/attempts.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/orthogonal_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/runtime_contract.csv`.
- producer(생산자): `stage_pipelines/stage267/run267T_pool_wide_orthogonal_stability_executor.py`.
- consumer(소비자): next action(다음 행동) `run267T_review_pool_wide_orthogonal_stability_mt5_results`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/attempts_executed.csv`.
- artifact_hashes(산출물 해시): artifact_registry.csv(산출물 등록부)에 기록한다.
- registry_links(등록부 연결): artifact_registry.csv, run_registry.csv, alpha_run_ledger.csv, stage_run_ledger.csv.
- availability(가용성): tracked(추적됨) plus Common Files(공통 파일) runtime handoff(런타임 인계).
- lineage_judgment(계보 판정): `connected_with_boundary`.

## KPI Read(KPI 판독)

| candidate(후보) | axis(축) | test(시험) | record_view(기록 보기) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `run267S_axis01_pool_wide_variant_distinguishability` | `abl_volatility_bandwidth` | `mt5_ta_s264_aih_abl_volatility_bandwidth_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_aih` | `run267S_axis01_pool_wide_variant_distinguishability` | `abl_volatility_bandwidth` | `mt5_rt_s264_aih_abl_volatility_bandwidth_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_aih` | `run267S_axis01_pool_wide_variant_distinguishability` | `rep_volatility_atr` | `mt5_ta_s264_aih_rep_volatility_atr_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_aih` | `run267S_axis01_pool_wide_variant_distinguishability` | `rep_volatility_atr` | `mt5_rt_s264_aih_rep_volatility_atr_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_aih` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_ta_s264_aih_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_aih` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_rt_s264_aih_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_aih` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_ta_s264_aih_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_aih` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_rt_s264_aih_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_lc` | `run267S_axis01_pool_wide_variant_distinguishability` | `rep_volatility_atr` | `mt5_ta_s264_lc_rep_volatility_atr_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_lc` | `run267S_axis01_pool_wide_variant_distinguishability` | `rep_volatility_atr` | `mt5_rt_s264_lc_rep_volatility_atr_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_lc` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_ta_s264_lc_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_lc` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_rt_s264_lc_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_lc` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_ta_s264_lc_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_lc` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_rt_s264_lc_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s262_lih` | `run267S_axis01_pool_wide_variant_distinguishability` | `rep_volatility_atr` | `mt5_ta_s262_lih_rep_volatility_atr_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s262_lih` | `run267S_axis01_pool_wide_variant_distinguishability` | `rep_volatility_atr` | `mt5_rt_s262_lih_rep_volatility_atr_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s262_lih` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_ta_s262_lih_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s262_lih` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_rt_s262_lih_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s262_lih` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_ta_s262_lih_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s262_lih` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_rt_s262_lih_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_aia` | `run267S_axis01_pool_wide_variant_distinguishability` | `abl_volatility_bandwidth` | `mt5_ta_s264_aia_abl_volatility_bandwidth_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_aia` | `run267S_axis01_pool_wide_variant_distinguishability` | `abl_volatility_bandwidth` | `mt5_rt_s264_aia_abl_volatility_bandwidth_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_aia` | `run267S_axis01_pool_wide_variant_distinguishability` | `rep_volatility_atr` | `mt5_ta_s264_aia_rep_volatility_atr_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_aia` | `run267S_axis01_pool_wide_variant_distinguishability` | `rep_volatility_atr` | `mt5_rt_s264_aia_rep_volatility_atr_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s264_aia` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_ta_s264_aia_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_aia` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_rt_s264_aia_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_aia` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_ta_s264_aia_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s264_aia` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_rt_s264_aia_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s258_stc` | `run267S_axis01_pool_wide_variant_distinguishability` | `abl_volatility_bandwidth` | `mt5_ta_s258_stc_abl_volatility_bandwidth_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s258_stc` | `run267S_axis01_pool_wide_variant_distinguishability` | `abl_volatility_bandwidth` | `mt5_rt_s258_stc_abl_volatility_bandwidth_run267t_historical_2024_tier_a_train_era_stress` | 236.31 | 1.3 | 454 | 12.88 |
| `s258_stc` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_ta_s258_stc_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s258_stc` | `run267S_axis02_non_calendar_weak_slice_resilience` | `abl_trend_strength_direction` | `mt5_rt_s258_stc_abl_trend_strength_direction_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s258_stc` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_ta_s258_stc_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |
| `s258_stc` | `run267S_axis02_non_calendar_weak_slice_resilience` | `rep_trend_strength_adx` | `mt5_rt_s258_stc_rep_trend_strength_adx_run267t_historical_2024_tier_a_train_era_stress` | 177.49 | 1.2 | 486 | 12.68 |

## Boundary(경계)

- result_subject(결과 대상): `run267T_pool_wide_orthogonal_stability_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).
- evidence_missing(빠진 근거): full batch completion(전체 묶음 완료) if partial(부분 실행이면), balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 핵심 성과 지표) 검토, final candidate selection(최종 후보 선택), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267T_review_pool_wide_orthogonal_stability_mt5_results`.
