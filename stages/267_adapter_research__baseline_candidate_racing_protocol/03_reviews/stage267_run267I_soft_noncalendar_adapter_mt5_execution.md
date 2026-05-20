# Stage267 Run267I Soft Non-Calendar Adapter MT5 Execution(267단계 267I 부드러운 비달력 어댑터 MT5 실행)

- action(행동): `4` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): `s264_aih`, `s264_lc`의 `adx_atr_soft_score` feature/model/set/ini(피처/모델/설정/초기화) 묶음이 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 연결됐는지 확인한다.
- status(상태): `run267I_p0_soft_noncalendar_adapter_mt5_batch_completed`
- completed_reports(완료 보고서): `4`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `4`
- model_materialization_type(모델 물질화 유형): `research_score_table_extension_not_retrained`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 해석)

이번 실행은 후보 선발이 아니다. 물질화된 soft feature(부드러운 피처)가 실제 MT5(MetaTrader 5, 메타트레이더5) 테스터에서 깨지지 않고 돌아가는지 보는 확인이다.
`s264_aih`는 core challenger(핵심 도전자), `s264_lc`는 defensive control(방어 기준)이다. 둘을 같이 돌리는 효과는 공격 후보와 안정 후보가 같은 feature engineering(피처 엔지니어링) 변화에서 어떻게 달라지는지 비교할 수 있다는 점이다.
이 모델은 true retrain(진짜 재학습)이 아니라 research score-table extension(연구용 점수표 확장)이다. 효과는 ONNX(모델 교환 형식) 검토가 아니라 다음 R&D racing(연구개발 경주) 방향 판단에만 쓰는 것이다.

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`, runtime module hashes(런타임 모듈 해시)는 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/execution_result.json`에 기록했다.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267I/p0_soft_noncalendar_adapter_materialization/kpi_summary.csv`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건에 따른다. 별도 비용 우위는 주장하지 않는다.
- backtest_judgment(백테스트 판정): `run267I_p0_soft_noncalendar_adapter_mt5_batch_completed` with boundary(경계) `diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| candidate(후보) | role(역할) | record_view(기록 보기) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `challenger_core` | `mt5_ta_s264_aih_adxatrsoft_historical_2024_tier_a_train_era_stress` | 170.14 | 1.1 | 350 | 30.3 |
| `s264_aih` | `challenger_core` | `mt5_rt_s264_aih_adxatrsoft_historical_2024_tier_a_train_era_stress` | 170.14 | 1.1 | 350 | 30.3 |
| `s264_lc` | `defensive_control` | `mt5_ta_s264_lc_adxatrsoft_historical_2024_tier_a_train_era_stress` | 148.03 | 1.09 | 347 | 31.41 |
| `s264_lc` | `defensive_control` | `mt5_rt_s264_lc_adxatrsoft_historical_2024_tier_a_train_era_stress` | 148.03 | 1.09 | 347 | 31.41 |

## Boundary(경계)

- result_subject(결과 대상): `run267I_p0_soft_noncalendar_adapter_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).
- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 핵심 성과 지표) 검토, feature ablation/replacement(피처 제거/대체) 재검증, ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267I_review_p0_soft_noncalendar_adapter_mt5_results`.
