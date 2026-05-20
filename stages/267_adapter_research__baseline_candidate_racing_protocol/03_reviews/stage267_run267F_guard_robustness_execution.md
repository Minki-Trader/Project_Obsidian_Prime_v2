# Stage267 Run267F Non-Calendar Guard MT5 Execution(267단계 267F 비달력 방어 MT5 실행)

- action(행동): `20` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): ADX 20-25(추세 강도 20-25)와 DI-low q33(DI 낮은 33%) guard(방어)를 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 비교할 수 있게 했다.
- status(상태): `run267F_non_calendar_guard_mt5_batch_completed`
- completed_reports(완료 보고서): `20`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `20`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델링 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`, runtime module hashes(런타임 모듈 해시)는 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/execution_result.json`에 기록했다.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267F/atrcomp_guard_robustness/kpi_summary.csv`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 Strategy Tester(전략 테스터) 설정과 broker history(브로커 이력) 조건에 따른다. 별도 비용 우위를 주장하지 않는다.
- forensic_checks(포렌식 점검): set/ini(설정/초기화), report path(보고서 경로), runtime summary(런타임 요약), feature/model path(피처/모델 경로), module hash(모듈 해시)를 연결했다.
- backtest_judgment(백테스트 판정): `run267F_non_calendar_guard_mt5_batch_completed` with boundary(경계) `diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| record_view(기록 보기) | role(역할) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | ---: | ---: | ---: | ---: |
| `mt5_ta_s264_aih_adx2025_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 304.93 | 1.23 | 253 | 27.89 |
| `mt5_rt_s264_aih_adx2025_historical_2024_tier_a_train_era_stress` | `routed_total` | 304.93 | 1.23 | 253 | 27.89 |
| `mt5_ta_s264_aia_adx2025_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 304.93 | 1.23 | 253 | 27.89 |
| `mt5_rt_s264_aia_adx2025_historical_2024_tier_a_train_era_stress` | `routed_total` | 304.93 | 1.23 | 253 | 27.89 |
| `mt5_ta_s258_stc_adx2025_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 322.21 | 1.21 | 270 | 27.97 |
| `mt5_rt_s258_stc_adx2025_historical_2024_tier_a_train_era_stress` | `routed_total` | 322.21 | 1.21 | 270 | 27.97 |
| `mt5_ta_s264_lc_adx2025_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 285.74 | 1.22 | 250 | 27.96 |
| `mt5_rt_s264_lc_adx2025_historical_2024_tier_a_train_era_stress` | `routed_total` | 285.74 | 1.22 | 250 | 27.96 |
| `mt5_ta_s262_lih_adx2025_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 243.01 | 1.19 | 252 | 29.67 |
| `mt5_rt_s262_lih_adx2025_historical_2024_tier_a_train_era_stress` | `routed_total` | 243.01 | 1.19 | 252 | 29.67 |
| `mt5_ta_s264_aih_dilowq33_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 50.71 | 1.05 | 223 | 31.6 |
| `mt5_rt_s264_aih_dilowq33_historical_2024_tier_a_train_era_stress` | `routed_total` | 50.71 | 1.05 | 223 | 31.6 |
| `mt5_ta_s264_aia_dilowq33_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 50.71 | 1.05 | 223 | 31.6 |
| `mt5_rt_s264_aia_dilowq33_historical_2024_tier_a_train_era_stress` | `routed_total` | 50.71 | 1.05 | 223 | 31.6 |
| `mt5_ta_s258_stc_dilowq33_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 27.44 | 1.02 | 240 | 36.22 |
| `mt5_rt_s258_stc_dilowq33_historical_2024_tier_a_train_era_stress` | `routed_total` | 27.44 | 1.02 | 240 | 36.22 |
| `mt5_ta_s264_lc_dilowq33_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 42.22 | 1.04 | 221 | 32.65 |
| `mt5_rt_s264_lc_dilowq33_historical_2024_tier_a_train_era_stress` | `routed_total` | 42.22 | 1.04 | 221 | 32.65 |
| `mt5_ta_s262_lih_dilowq33_historical_2024_tier_a_train_era_stress` | `tier_only_total` | 12.83 | 1.01 | 223 | 36.09 |
| `mt5_rt_s262_lih_dilowq33_historical_2024_tier_a_train_era_stress` | `routed_total` | 12.83 | 1.01 | 223 | 36.09 |

## Boundary(경계)

- result_subject(결과 대상): `run267F_non_calendar_guard_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).
- evidence_missing(빠진 근거): guard comparison review(방어 비교 검토), time-slice review(시간 구간 검토), curve diagnostics(곡선 진단), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267F_review_non_calendar_guard_mt5_results`.
