# Stage267 Run267AD Noncalendar State Guard Score Table MT5 Execution(267단계 267AD 비달력 상태 방어 점수표 MT5 실행)

- action(행동): `14` of `14` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): run267AC(267AC 실행)의 score table/model/set/ini(점수표/모델/설정/초기화)가 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 이어지는지 확인한다.
- status(상태): `run267AD_noncalendar_state_guard_score_table_mt5_batch_completed`
- completed_reports(완료 보고서): `14`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `14`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 설명)

run267AB(267AB 실행)는 약한 거래가 몰리는 시장 상태를 찾았고, run267AC(267AC 실행)는 그 상태를 직접 잘라내지 않고 점수표에 작은 soft guard(부드러운 방어 장치)로 붙였다.
run267AD(267AD 실행)는 그 입력을 MT5(MetaTrader 5, 메타트레이더5)에 실제로 넣어 본다. 효과(effect, 효과)는 숫자가 예뻐 보이는 설계와 실제 tester output(테스터 출력)을 분리하는 것이다.
이번 실행은 후보 선택(candidate selection, 후보 선택)이나 ONNX(온닉스) 검토가 아니다. 다음 review(검토)에서 거래 수, 손실폭, 곡선, 시간 구간을 따로 봐야 한다.

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, broker symbol(브로커 심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, modeling mode(모델링 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`, module hashes(모듈 해시)는 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/execution_result.json`에 기록했다.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/kpi_summary.csv`.
- trade_evidence(거래 근거): completed reports(완료 보고서) `14`, KPI records(KPI 기록) `14`, attempt manifest(시도 목록) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/attempts_executed.csv`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 MT5 Strategy Tester(MT5 전략 테스터)와 broker history(브로커 이력) 조건에 따른다. 별도 비용 우위 주장은 하지 않는다.
- forensic_checks(포렌식 확인): set/ini hash(설정/초기화 해시), runtime summary(런타임 요약), Strategy Tester report(전략 테스터 보고서), copied report hash(복사 보고서 해시)를 확인했다.
- backtest_judgment(백테스트 판정): `run267AD_noncalendar_state_guard_score_table_mt5_batch_completed` with boundary(경계) `diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| candidate(후보) | source_test(원천 시험) | tier(티어) | record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aia` | `rep_trend_strength_adx` | `Tier A` | `mt5_ta_s264_aia_rep_trend_strength_adx_state_guard_historical_2024_tier_a_train_era_stress` | 1250.12 | 1.59 | 314 | 15.75 |
| `s264_aia` | `rep_trend_strength_adx` | `Tier A+B` | `mt5_rt_s264_aia_rep_trend_strength_adx_state_guard_historical_2024_tier_a_train_era_stress` | 1250.12 | 1.59 | 314 | 15.75 |
| `s264_aia` | `rep_volatility_atr` | `Tier A` | `mt5_ta_s264_aia_rep_volatility_atr_state_guard_historical_2024_tier_a_train_era_stress` | 1097.15 | 1.57 | 317 | 15.07 |
| `s264_aia` | `rep_volatility_atr` | `Tier A+B` | `mt5_rt_s264_aia_rep_volatility_atr_state_guard_historical_2024_tier_a_train_era_stress` | 1097.15 | 1.57 | 317 | 15.07 |
| `s262_lih` | `rep_trend_strength_adx` | `Tier A` | `mt5_ta_s262_lih_rep_trend_strength_adx_state_guard_historical_2024_tier_a_train_era_stress` | 1036.02 | 1.58 | 302 | 16.67 |
| `s262_lih` | `rep_trend_strength_adx` | `Tier A+B` | `mt5_rt_s262_lih_rep_trend_strength_adx_state_guard_historical_2024_tier_a_train_era_stress` | 1036.02 | 1.58 | 302 | 16.67 |
| `s258_stc` | `abl_price_return_range` | `Tier A` | `mt5_ta_s258_stc_abl_price_return_range_state_guard_historical_2024_tier_a_train_era_stress` | 969.98 | 1.52 | 297 | 17.75 |
| `s258_stc` | `abl_price_return_range` | `Tier A+B` | `mt5_rt_s258_stc_abl_price_return_range_state_guard_historical_2024_tier_a_train_era_stress` | 969.98 | 1.52 | 297 | 17.75 |
| `s258_stc` | `abl_trend_strength_direction` | `Tier A` | `mt5_ta_s258_stc_abl_trend_strength_direction_state_guard_historical_2024_tier_a_train_era_stress` | 970.89 | 1.45 | 306 | 19.29 |
| `s258_stc` | `abl_trend_strength_direction` | `Tier A+B` | `mt5_rt_s258_stc_abl_trend_strength_direction_state_guard_historical_2024_tier_a_train_era_stress` | 970.89 | 1.45 | 306 | 19.29 |
| `s264_lc` | `abl_gate_variant_rule` | `Tier A` | `mt5_ta_s264_lc_abl_gate_variant_rule_state_guard_historical_2024_tier_a_train_era_stress` | 1620.53 | 1.49 | 378 | 21.27 |
| `s264_lc` | `abl_gate_variant_rule` | `Tier A+B` | `mt5_rt_s264_lc_abl_gate_variant_rule_state_guard_historical_2024_tier_a_train_era_stress` | 1620.53 | 1.49 | 378 | 21.27 |
| `s264_aih` | `abl_volatility_bandwidth` | `Tier A` | `mt5_ta_s264_aih_abl_volatility_bandwidth_state_guard_historical_2024_tier_a_train_era_stress` | 1037.72 | 1.54 | 297 | 16.66 |
| `s264_aih` | `abl_volatility_bandwidth` | `Tier A+B` | `mt5_rt_s264_aih_abl_volatility_bandwidth_state_guard_historical_2024_tier_a_train_era_stress` | 1037.72 | 1.54 | 297 | 16.66 |

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/run_manifest.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/attempts.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/noncalendar_state_guard_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/runtime_contract.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AD_noncalendar_state_guard_score_table_mt5_executor.py`.
- consumer(소비자): `run267AE_review_noncalendar_state_guard_score_table_mt5_results`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/kpi_records.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AD/noncalendar_state_guard_score_table_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AD_noncalendar_state_guard_score_table_mt5_execution.md`.
- lineage_judgment(계보 판정): `connected_with_boundary`이다. MT5 execution(MT5 실행)은 연결됐지만 candidate selection(후보 선택)은 없다.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267AD_noncalendar_state_guard_score_table_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식), execution result(실행 결과).
- evidence_missing(부족 근거): balance/equity curve(잔액/평가금 곡선) 상세 검토, time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 검토, 후보 탈락/유지 판단, ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- next_condition(다음 조건): `run267AE_review_noncalendar_state_guard_score_table_mt5_results`.
- user_explanation_hook(사용자 설명 핵심): 지금은 방어 점수표가 실제 MT5에서 돌아가는지 확인한 단계이고, 좋은 후보인지 여부는 다음 검토에서 곡선과 약한 구간까지 본 뒤에만 말할 수 있다.
