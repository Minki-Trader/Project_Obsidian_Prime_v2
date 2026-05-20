# Stage267 Run267D Adapter/P2 MT5 Execution(267단계 267D 어댑터/2차 대체 MT5 실행)

- action(행동): `30` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): Adapter prototype(어댑터 원형)과 P2 replacement(2차 대체)를 실제 tester output(테스터 출력)으로 확인해, 다음 review(검토)가 말이 아니라 KPI(핵심 성과 지표)와 curve evidence(곡선 근거)를 보게 했다.
- status(상태): `run267D_adapter_p2_mt5_batch_completed`
- completed_reports(완료 보고서): `30`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `30`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델링) `4`, date range(기간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`, runtime module hashes(런타임 모듈 해시)는 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267D/adapter_p2_materialization/execution_result.json`에 기록했다.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267D/adapter_p2_materialization/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267D/adapter_p2_materialization/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267D/adapter_p2_materialization/kpi_summary.csv`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 Strategy Tester(전략 테스터) 설정과 브로커 히스토리 조건에 의존하며, 별도 완화 주장은 하지 않는다.
- forensic_checks(포렌식 점검): set/ini(설정/초기화), report path(보고서 경로), runtime summary(런타임 요약), feature/model path(피처/모델 경로), module hash(모듈 해시)를 연결했다.
- backtest_judgment(백테스트 판정): `run267D_adapter_p2_mt5_batch_completed` with boundary(경계) `diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| record_view(기록 보기) | axis(축) | role(역할) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `mt5_ta_s264_aih_late21_historical_2024_tier_a_train_era_stress` | `late21` | `tier_only_total` | 198.2 | 1.12 | 312 | 22.86 |
| `mt5_rt_s264_aih_late21_historical_2024_tier_a_train_era_stress` | `late21` | `routed_total` | 198.2 | 1.12 | 312 | 22.86 |
| `mt5_ta_s264_lc_late21_historical_2024_tier_a_train_era_stress` | `late21` | `tier_only_total` | 173.26 | 1.11 | 309 | 22.86 |
| `mt5_rt_s264_lc_late21_historical_2024_tier_a_train_era_stress` | `late21` | `routed_total` | 173.26 | 1.11 | 309 | 22.86 |
| `mt5_ta_s262_lih_late21_historical_2024_tier_a_train_era_stress` | `late21` | `tier_only_total` | 142.76 | 1.09 | 311 | 25.89 |
| `mt5_rt_s262_lih_late21_historical_2024_tier_a_train_era_stress` | `late21` | `routed_total` | 142.76 | 1.09 | 311 | 25.89 |
| `mt5_ta_s258_stc_late21_historical_2024_tier_a_train_era_stress` | `late21` | `tier_only_total` | 190.46 | 1.11 | 332 | 26.42 |
| `mt5_rt_s258_stc_late21_historical_2024_tier_a_train_era_stress` | `late21` | `routed_total` | 190.46 | 1.11 | 332 | 26.42 |
| `mt5_ta_s264_aia_late21_historical_2024_tier_a_train_era_stress` | `late21` | `tier_only_total` | 189.67 | 1.12 | 313 | 22.88 |
| `mt5_rt_s264_aia_late21_historical_2024_tier_a_train_era_stress` | `late21` | `routed_total` | 189.67 | 1.12 | 313 | 22.88 |
| `mt5_ta_s264_aih_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `tier_only_total` | 269.2 | 1.16 | 314 | 28.73 |
| `mt5_rt_s264_aih_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `routed_total` | 269.2 | 1.16 | 314 | 28.73 |
| `mt5_ta_s264_aia_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `tier_only_total` | 261.08 | 1.16 | 315 | 28.89 |
| `mt5_rt_s264_aia_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `routed_total` | 261.08 | 1.16 | 315 | 28.89 |
| `mt5_ta_s258_stc_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `tier_only_total` | 260.91 | 1.14 | 334 | 29.99 |
| `mt5_rt_s258_stc_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `routed_total` | 260.91 | 1.14 | 334 | 29.99 |
| `mt5_ta_s264_lc_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `tier_only_total` | 240.12 | 1.15 | 311 | 28.78 |
| `mt5_rt_s264_lc_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `routed_total` | 240.12 | 1.15 | 311 | 28.78 |
| `mt5_ta_s258_stc_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `tier_only_total` | 203.28 | 1.1 | 357 | 39.62 |
| `mt5_rt_s258_stc_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `routed_total` | 203.28 | 1.1 | 357 | 39.62 |
| `mt5_ta_s262_lih_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `tier_only_total` | 201.92 | 1.12 | 313 | 30.48 |
| `mt5_rt_s262_lih_atrcomp_historical_2024_tier_a_train_era_stress` | `atrcomp` | `routed_total` | 201.92 | 1.12 | 313 | 30.48 |
| `mt5_ta_s264_aih_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `tier_only_total` | 196.82 | 1.11 | 334 | 34.07 |
| `mt5_rt_s264_aih_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `routed_total` | 196.82 | 1.11 | 334 | 34.07 |
| `mt5_ta_s264_aia_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `tier_only_total` | 196.82 | 1.11 | 334 | 34.07 |
| `mt5_rt_s264_aia_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `routed_total` | 196.82 | 1.11 | 334 | 34.07 |
| `mt5_ta_s264_lc_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `tier_only_total` | 175.16 | 1.1 | 331 | 34.39 |
| `mt5_rt_s264_lc_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `routed_total` | 175.16 | 1.1 | 331 | 34.39 |
| `mt5_ta_s262_lih_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `tier_only_total` | 142.27 | 1.08 | 333 | 36.43 |
| `mt5_rt_s262_lih_vlowadx_historical_2024_tier_a_train_era_stress` | `vlowadx` | `routed_total` | 142.27 | 1.08 | 333 | 36.43 |

## Boundary(경계)

- result_subject(결과 대상): `run267D_adapter_p2_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).
- evidence_missing(빠진 근거): zoomed balance/equity review(확대 잔액/평가금 검토), time-slice review(시간 구간 검토), Adapter stability judgment(어댑터 안정성 판정), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비도): `not_claimed`.
- next_action(다음 행동): `run267D_review_adapter_p2_mt5_results`.
