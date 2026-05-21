# Stage267 Run267AX Pool-wide State Feature Engineering Second Follow-up MT5 Execution(267단계 267AX 후보군 전체 상태 피처 엔지니어링 2차 후속 MT5 실행)

- action(행동): run267AW(267AW 실행)의 `8` / `8` Tier A(티어 A) MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): materialization(물질화)만 있던 2차 후속 압박을 tester output(테스터 출력), runtime telemetry(런타임 기록), KPI(핵심 성과 지표), backtest forensics(백테스트 포렌식)로 바꿨다.
- runtime_path_repair(런타임 경로 보정): feature/model/telemetry path(피처/모델/기록 경로)를 `OPV2/s267ax` 아래 짧은 Common Files(공통 파일) 경로로 바꿨다.
- effect(효과): threshold(문턱값), risk/ATR(위험/ATR), score table(점수표) 내용은 유지하고 MT5 file open error(파일 열기 오류) 위험만 줄인다.
- status(상태): `run267AX_pool_wide_state_feature_engineering_second_followup_mt5_batch_completed`
- completed_reports(완료 보고서): `8`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `8`
- candidates_touched(건드린 후보): `s258_stc;s262_lih;s264_aia;s264_aih;s264_lc`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 설명)

이번 실행은 후보를 고르는 단계가 아니다. run267AW(267AW 실행)가 만든 8개 Tier A(티어 A) 실험 입력을 실제 MT5(MetaTrader 5, 메타트레이더5)에 넣어 숫자와 파일 근거가 생기는지 확인하는 단계다.
Effect(효과): 다음 run267AY(267AY 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 후보별로 다시 읽을 수 있다.
Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 `Tier_B_and_actual_routed_total_blocked_until_true_fallback_manifest_exists`로 남긴다. Effect(효과): 합성 합산을 combined result(합산 결과)처럼 과장하지 않는다.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/run_manifest.json`.
- runtime_path(런타임 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution`.
- shared_contract(공유 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/runtime_contract.csv`.
- known_differences(알려진 차이): feature/model/telemetry path(피처/모델/기록 경로)만 짧은 Common Files(공통 파일) 경로로 보정했다.
- parity_check(동등성 점검): feature/model/set/ini(피처/모델/설정/초기화) 입력과 module hash(모듈 해시)를 실행 결과에 연결했다.
- runtime_claim_boundary(런타임 주장 경계): `runtime_diagnostic_evidence_only_no_candidate_selection`.

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, broker symbol(브로커 심볼) `US100`, timeframe(시간 프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, modeling mode(모델링 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/kpi_summary.csv`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/미끄러짐/스왑)은 MT5 Strategy Tester(MT5 전략 테스터)와 broker history(브로커 이력) 조건을 따른다.
- backtest_judgment(백테스트 판정): `run267AX_pool_wide_state_feature_engineering_second_followup_mt5_batch_completed` with boundary(경계) `runtime_diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| candidate(후보) | second_profile(2차 프로필) | tier(티어) | record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `core_range_volatility_interaction_v3` | `Tier A` | `mt5_ta_s264_aih_range_expansion_pressure_aw_historical_2024_tier_a_train_era_stress` | 822.06 | 1.59 | 281 | 15.46 |
| `s264_aih` | `core_volatility_range_interaction_v3` | `Tier A` | `mt5_ta_s264_aih_volatility_regime_expans_aw_historical_2024_tier_a_train_era_stress` | 1153.72 | 1.74 | 275 | 16.65 |
| `s264_aia` | `oos_anchor_range_dd_conservative_v3` | `Tier A` | `mt5_ta_s264_aia_range_expansion_pressure_aw_historical_2024_tier_a_train_era_stress` | 1037.6 | 1.64 | 287 | 14.11 |
| `s264_aia` | `oos_anchor_shock_range_conservative_v3` | `Tier A` | `mt5_ta_s264_aia_return_shock_absorption_aw_historical_2024_tier_a_train_era_stress` | 949.94 | 1.66 | 282 | 14.48 |
| `s264_lc` | `defensive_control_repeat_audit_v2` | `Tier A` | `mt5_ta_s264_lc_volatility_regime_expans_aw_historical_2024_tier_a_train_era_stress` | 1052.2 | 1.67 | 278 | 16.83 |
| `s262_lih` | `validation_control_repeat_audit_v2` | `Tier A` | `mt5_ta_s262_lih_volatility_regime_expans_aw_historical_2024_tier_a_train_era_stress` | 1007.16 | 1.59 | 283 | 16.98 |
| `s258_stc` | `stress_challenger_volatility_strict_prune_v3` | `Tier A` | `mt5_ta_s258_stc_volatility_regime_expans_aw_historical_2024_tier_a_train_era_stress` | 878.2 | 1.57 | 255 | 16.54 |
| `s258_stc` | `stress_challenger_trend_strict_prune_v3` | `Tier A` | `mt5_ta_s258_stc_trend_strength_disagreem_aw_historical_2024_tier_a_train_era_stress` | 1133.45 | 1.58 | 293 | 16.53 |

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/run_manifest.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/attempt_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/second_followup_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/runtime_contract.csv`.
- source_audits(원천 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/route_gap_audit.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/tier_record_requirement_audit.csv`.
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AW_pool_wide_state_feature_engineering_second_followup_materialization.md`.
- producer(생산자): `stage_pipelines/stage267/run267AX_pool_wide_state_feature_engineering_second_followup_mt5_executor.py`.
- consumer(소비자): `run267AY_review_pool_wide_state_feature_engineering_second_followup_mt5_results`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/kpi_records.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution.md`.
- lineage_judgment(계보 판정): `connected_with_boundary`. MT5 execution(MT5 실행)은 연결됐지만 candidate selection(후보 선택)은 없다.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식), execution result(실행 결과).
- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 상세 검토, time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질), 후보 탈락/유지 판정, ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- next_condition(다음 조건): `run267AY_review_pool_wide_state_feature_engineering_second_followup_mt5_results`.
