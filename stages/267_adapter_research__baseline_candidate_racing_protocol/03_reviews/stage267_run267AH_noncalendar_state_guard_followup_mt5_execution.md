# Stage267 Run267AH Noncalendar State Guard Follow-Up MT5 Execution(267단계 267AH 비달력 상태 방어 후속 MT5 실행)

- action(행동): `6` of `6` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.
- effect(효과): run267AG(267AG 실행)의 후속 pressure score table(압박 점수표)이 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 연결되는지 확인했다.
- runtime_path_repair(런타임 경로 보정): telemetry path(런타임 기록 경로)만 `OPV2/s267ah` 아래 짧은 Common Files(공통 파일) 경로로 바꿨다. Effect(효과): model(모델), feature(피처), threshold(임계값), risk(위험) 설정은 유지하고 MT5 file open error(파일 열기 오류)만 피한다.
- status(상태): `run267AH_noncalendar_state_guard_followup_mt5_batch_completed`
- completed_reports(완료 보고서): `6`
- blocked_or_missing_reports(차단 또는 누락 보고서): `0`
- kpi_records(KPI 기록): `6`
- candidates_touched(건드린 후보): `s264_aia;s264_aih`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 설명)

이번 실행은 후보를 뽑는 단계가 아니다. run267AF(267AF 실행)에서 남긴 후속/가지치기 질문을 run267AG(267AG 실행)가 6개 MT5(MetaTrader 5, 메타트레이더5) 입력으로 만들었고, run267AH(267AH 실행)는 그 입력을 실제 전략 테스터(strategy tester, 전략 테스터)에 넣어 본 단계다.
효과(effect, 효과)는 `s264_aia`의 두 replacement pressure(대체 압박)와 `s264_aih`의 core role pressure(핵심 역할 압박)가 숫자로만 좋아 보이는지, 또는 다음 balance/equity curve(잔액/평가금 곡선) 검토까지 넘길 근거가 있는지 분리하는 것이다.
Tier A+B(Tier A+B 합산)는 이번에도 fallback disabled(대체 비활성) 중복 경계로 읽는다. 따라서 runtime authority(런타임 권위)나 operating baseline(운영 기준선)은 주장하지 않는다.

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, broker symbol(브로커 심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, modeling mode(모델링 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): entrypoint(진입점) `foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.mq5`, tester set(테스터 설정) `ObsidianPrimeV2_RuntimeProbeEA.set`.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/backtest_forensics.csv`, KPI summary(KPI 요약) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/kpi_summary.csv`.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 MT5 Strategy Tester(MT5 전략 테스터)와 broker history(브로커 이력) 조건에 따른다. 별도 비용 우위 주장은 하지 않는다.
- backtest_judgment(백테스트 판정): `run267AH_noncalendar_state_guard_followup_mt5_batch_completed` with boundary(경계) `runtime_diagnostic_evidence_only_no_candidate_selection`.

## KPI Read(KPI 판독)

| candidate(후보) | source_test(원천 시험) | tier(티어) | record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aia` | `rep_trend_strength_adx` | `Tier A` | `mt5_ta_s264_aia_rep_trend_strength_adx_followup_historical_2024_tier_a_train_era_stress` | 1133.77 | 1.6 | 301 | 14.73 |
| `s264_aia` | `rep_trend_strength_adx` | `Tier A+B` | `mt5_rt_s264_aia_rep_trend_strength_adx_followup_historical_2024_tier_a_train_era_stress` | 1133.77 | 1.6 | 301 | 14.73 |
| `s264_aia` | `rep_volatility_atr` | `Tier A` | `mt5_ta_s264_aia_rep_volatility_atr_followup_historical_2024_tier_a_train_era_stress` | 1080.68 | 1.64 | 296 | 13.77 |
| `s264_aia` | `rep_volatility_atr` | `Tier A+B` | `mt5_rt_s264_aia_rep_volatility_atr_followup_historical_2024_tier_a_train_era_stress` | 1080.68 | 1.64 | 296 | 13.77 |
| `s264_aih` | `abl_volatility_bandwidth` | `Tier A` | `mt5_ta_s264_aih_abl_volatility_bandwidth_followup_historical_2024_tier_a_train_era_stress` | 826.62 | 1.55 | 272 | 18.28 |
| `s264_aih` | `abl_volatility_bandwidth` | `Tier A+B` | `mt5_rt_s264_aih_abl_volatility_bandwidth_followup_historical_2024_tier_a_train_era_stress` | 826.62 | 1.55 | 272 | 18.28 |

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AG/noncalendar_state_guard_followup_queue_materialization/run_manifest.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AG/noncalendar_state_guard_followup_queue_materialization/attempt_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AG/noncalendar_state_guard_followup_queue_materialization/followup_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AG/noncalendar_state_guard_followup_queue_materialization/runtime_contract.csv`.
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AG_noncalendar_state_guard_followup_queue_materialization.md`.
- producer(생산자): `stage_pipelines/stage267/run267AH_noncalendar_state_guard_followup_mt5_executor.py`.
- consumer(소비자): `run267AI_review_noncalendar_state_guard_followup_mt5_results`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/kpi_records.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AH/noncalendar_state_guard_followup_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AH_noncalendar_state_guard_followup_mt5_execution.md`.
- lineage_judgment(계보 판정): `connected_with_boundary`다. MT5 execution(MT5 실행)은 연결됐지만 candidate selection(후보 선택)은 없다.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267AH_noncalendar_state_guard_followup_mt5_execution`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식), execution result(실행 결과).
- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 상세 검토, time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질), 후보 탈락/유지 판정, ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.
- next_condition(다음 조건): `run267AI_review_noncalendar_state_guard_followup_mt5_results`.
