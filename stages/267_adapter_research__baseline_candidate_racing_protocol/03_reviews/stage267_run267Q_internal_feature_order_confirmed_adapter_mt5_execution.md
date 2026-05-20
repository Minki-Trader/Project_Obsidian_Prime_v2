# Stage267 Run267Q Internal Feature Order Confirmed Adapter MT5 Execution(267단계 267Q 내부 피처 순서 확인 어댑터 MT5 실행)

- action(행동): `8` of `8` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): run267Q(267Q 실행)의 feature/model/set/ini(피처/모델/설정/초기화) 묶음이 실제 tester output(테스터 출력), runtime telemetry(런타임 텔레메트리), KPI(핵심 성과 지표)로 이어지는지 확인한다.
- status(상태): `run267Q_internal_feature_order_confirmed_adapter_mt5_batch_completed`
- completed_reports(완료 보고서): `8`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `8`
- candidate_aliases(후보 별칭): `s264_aia;s264_aih`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 해석)

이번 실행은 후보 선발이 아니다. run267P(267P 실행)에서 강하게 보였던 volatility/ATR(변동성/ATR) 축을 run267Q(267Q 실행)에서 내부 Adapter feature(내부 어댑터 피처)로 이름과 순서를 고정했고, 이번에는 그 파일 묶음이 MT5(MetaTrader 5, 메타트레이더5)에서 실제로 돌아가는지 본 것이다.
`s264_aih`는 core challenger(핵심 도전자), `s264_aia`는 OOS anchor(표본외 앵커)다. 효과는 두 후보가 같은 내부 feature order(피처 순서) 조건에서 덜 깨지는지 다음 review(검토)에서 비교할 수 있게 만드는 것이다.
이 결과만으로 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stage_pipelines/stage267/run267Q_internal_feature_order_confirmed_adapter_materialization.py` and `stage_pipelines/stage267/run267Q_internal_feature_order_confirmed_adapter_executor.py`.
- runtime_path(런타임 경로): EA entrypoint(EA 진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, attempt manifest(시도 목록) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/attempts.csv`.
- shared_contract(공유 계약): bar_time_server(서버 봉 시간), feature order hash(피처 순서 해시), EBM table model(EBM 표 모델), threshold(임계값), fixed historical 2024 date range(고정 2024 기간).
- known_differences(알려진 차이): source proxy score(원천 대체 점수)를 explicit internal adapter feature(명시 내부 어댑터 피처)로 rename(이름 변경)했다. raw feature ablation(원천 피처 직접 제거)은 아니다.
- parity_check(동등성 점검): compile(컴파일), Strategy Tester report(전략 테스터 보고서), runtime telemetry(런타임 텔레메트리), KPI records(KPI 기록).
- parity_identity(동등성 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/execution_result.json`, module hashes(모듈 해시)는 같은 파일에 기록했다.
- runtime_claim_boundary(런타임 주장 경계): `runtime_probe` only, no runtime authority(런타임 권위 아님).

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델 방식) `4`, date range(기간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/kpi_summary.csv`.
- trade_evidence(거래 근거): KPI records(KPI 기록) `8`, strategy reports(전략 보고서) `8`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 비용 우위는 주장하지 않는다.
- forensic_checks(포렌식 점검): settings drift(설정 드리프트), missing report(보고서 누락), runtime telemetry(런타임 텔레메트리), malformed KPI(형식 오류 KPI)를 산출물로 분리했다.
- backtest_judgment(백테스트 판정): `usable_with_boundary`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/attempts.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/internal_adapter_variant_manifest.csv`.
- producer(생산자): `stage_pipelines/stage267/run267Q_internal_feature_order_confirmed_adapter_executor.py`.
- consumer(소비자): next action(다음 행동) `run267Q_review_internal_feature_order_confirmed_adapter_mt5_results`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/backtest_forensics.csv`.
- artifact_hashes(산출물 해시): artifact_registry.csv(산출물 등록부)에 기록한다.
- registry_links(등록부 연결): artifact_registry.csv, run_registry.csv, alpha_run_ledger.csv, stage_run_ledger.csv.
- availability(가용성): tracked(추적됨) plus Common Files(공용 파일) runtime handoff(런타임 인계).
- lineage_judgment(계보 판정): `connected_with_boundary`.

## KPI Read(KPI 판독)

| candidate(후보) | test(시험) | record_view(기록 보기) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `abl_volatility_bandwidth` | `mt5_ta_s264_aih_abl_volatility_bandwidth_internal_historical_2024_tier_a_train_era_stress` | 412.57 | 1.35 | 314 | 15.9 |
| `s264_aih` | `abl_volatility_bandwidth` | `mt5_rt_s264_aih_abl_volatility_bandwidth_internal_historical_2024_tier_a_train_era_stress` | 412.57 | 1.35 | 314 | 15.9 |
| `s264_aih` | `rep_volatility_atr` | `mt5_ta_s264_aih_rep_volatility_atr_internal_historical_2024_tier_a_train_era_stress` | 412.57 | 1.35 | 314 | 15.9 |
| `s264_aih` | `rep_volatility_atr` | `mt5_rt_s264_aih_rep_volatility_atr_internal_historical_2024_tier_a_train_era_stress` | 412.57 | 1.35 | 314 | 15.9 |
| `s264_aia` | `abl_volatility_bandwidth` | `mt5_ta_s264_aia_abl_volatility_bandwidth_internal_historical_2024_tier_a_train_era_stress` | 408.29 | 1.35 | 315 | 15.85 |
| `s264_aia` | `abl_volatility_bandwidth` | `mt5_rt_s264_aia_abl_volatility_bandwidth_internal_historical_2024_tier_a_train_era_stress` | 408.29 | 1.35 | 315 | 15.85 |
| `s264_aia` | `rep_volatility_atr` | `mt5_ta_s264_aia_rep_volatility_atr_internal_historical_2024_tier_a_train_era_stress` | 408.29 | 1.35 | 315 | 15.85 |
| `s264_aia` | `rep_volatility_atr` | `mt5_rt_s264_aia_rep_volatility_atr_internal_historical_2024_tier_a_train_era_stress` | 408.29 | 1.35 | 315 | 15.85 |

## Boundary(경계)

- result_subject(결과 대상): `run267Q_internal_feature_order_confirmed_adapter_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).
- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 핵심 성과 지표) 검토, final candidate selection(최종 후보 선택), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267Q_review_internal_feature_order_confirmed_adapter_mt5_results`.
