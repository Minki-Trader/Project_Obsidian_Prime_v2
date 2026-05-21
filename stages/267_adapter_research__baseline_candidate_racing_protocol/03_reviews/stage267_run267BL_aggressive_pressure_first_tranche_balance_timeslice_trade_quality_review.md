# Stage267 Run267BL Aggressive Pressure First Tranche Balance/Time-Slice/Trade-Quality Review(267단계 267BL 공격형 압박 첫 묶음 잔액/시간구간/거래품질 검토)

- action(행동): run267BK(267BK 실행)의 `4`개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록) 단위로 다시 읽었다.
- effect(효과): headline KPI(겉 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 같이 본다.
- status(상태): `run267BL_aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review_completed`
- judgment(판정): `diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection`
- trade_records(거래 기록): `1910`
- aggressive_variant_rows(공격형 변형 행): `4`
- watch_rows(관찰 행): `2`
- negative_tier_a_slices(음수 Tier A 구간): `15`
- parser_errors(파서 오류): `0`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267BK(267BK 실행)의 숫자는 확실히 눈에 띈다. 특히 `explode_opportunity_recall`과 `anti_overconstraint_prune`은 net profit(순수익), PF(수익 팩터), trade count(거래 수)가 좋다.
하지만 이 단계의 baseline(기준 후보)은 operating baseline(운영 기준선)이 아니라 R&D racing research candidate(연구개발 경주용 연구 후보)다.
Effect(효과): 숫자가 좋아도 월별 구멍, 후반 구간 붕괴, 손실폭, 거래 품질을 확인하기 전에는 선택하지 않는다.

## Aggressive Variant Review(공격형 변형 검토)

| rank(순위) | variant(변형) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst month(최악 월) | worst slice(최악 구간) | late net(후반 순수익) | read(판독) |
| ---: | --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| 1 | `anti_overconstraint_prune` | 6887.04 | 1.81 | 495 | 16.53 | `2024-06` 35.29 | `session_report`/`session_07_12_report_time` -266.96 | 4789.16 | `aggressive_watch_not_selection(공격형 관찰, 선택 아님)` |
| 2 | `state_acceleration_interaction` | 2128.47 | 1.61 | 409 | 11.47 | `2024-06` -196.49 | `weekday`/`Monday` -214.38 | 1062.76 | `constructive_but_needs_wider_pressure(건설적이나 더 넓은 압박 필요)` |
| 3 | `explode_opportunity_recall` | 9213.54 | 1.78 | 670 | 11.45 | `2024-06` -137.44 | `session_report`/`session_07_12_report_time` -327.45 | 6803.07 | `headline_strong_but_uncomfortable_no_selection(겉 숫자는 강하지만 불편, 선택 아님)` |
| 4 | `payoff_convexity_push` | 6021.35 | 1.52 | 336 | 27.99 | `2024-12` -753.17 | `weekday`/`Monday` -755.76 | 3304.06 | `headline_strong_but_uncomfortable_no_selection(겉 숫자는 강하지만 불편, 선택 아님)` |

## Candidate Summary(후보 요약)

| candidate(후보) | role(역할) | variants(변형 수) | aggressive watch(공격형 관찰) | constructive(건설적) | uncomfortable(불편) | net mean(평균 순수익) | net max(최대 순수익) | worst DD%(최악 손실폭) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_aih` | `core_challenger` | 4 | 1 | 1 | 2 | 6062.60 | 9213.54 | 27.99 | `aggressive_branch_has_watch_rows_no_selection(공격형 분기 관찰 행 있음, 선택 아님)` |

## Worst Tier A Slices(최악 Tier A 구간)

| variant(변형) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |
| --- | --- | --- | ---: | ---: | --- |
| `payoff_convexity_push` | `weekday` | `Monday` | -755.76 | 52 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `payoff_convexity_push` | `month` | `2024-12` | -753.17 | 26 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `payoff_convexity_push` | `close_hour_report` | `16` | -601.17 | 33 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `payoff_convexity_push` | `close_hour_report` | `22` | -337.29 | 11 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `explode_opportunity_recall` | `session_report` | `session_07_12_report_time` | -327.45 | 4 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `explode_opportunity_recall` | `weekday` | `Monday` | -297.89 | 104 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `anti_overconstraint_prune` | `session_report` | `session_07_12_report_time` | -266.96 | 3 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `payoff_convexity_push` | `month` | `2024-06` | -249.26 | 14 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `state_acceleration_interaction` | `weekday` | `Monday` | -214.38 | 58 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `anti_overconstraint_prune` | `weekday` | `Monday` | -210.43 | 79 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `state_acceleration_interaction` | `month` | `2024-06` | -196.49 | 15 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `state_acceleration_interaction` | `session_report` | `session_07_12_report_time` | -148.37 | 3 | `negative_fragile_slice(음수 취약 구간)` |
| `explode_opportunity_recall` | `month` | `2024-06` | -137.44 | 31 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `explode_opportunity_recall` | `close_hour_report` | `22` | -118.24 | 13 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |

## Forensics Boundary(포렌식 경계)

- tester_identity(테스터 정체성): terminal count(터미널 수) `1`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, date range(날짜 범위) `2024.01.02` to `2025.01.01`.
- trade_evidence(거래 근거): trade records(거래 기록) `1910`, parser checks(파서 확인) `4`.
- cost_assumptions(비용 가정): `MT5 tester broker-history costs; no separate cost authority claimed(MT5 테스터 브로커 이력 비용 조건, 별도 비용 권위 주장 없음)`.
- backtest_judgment(백테스트 판정): `usable_with_boundary(경계부 사용 가능)`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BK/aggressive_pressure_first_tranche_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BK/aggressive_pressure_first_tranche_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BK/aggressive_pressure_first_tranche_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BJ/aggressive_pressure_first_tranche_materialization/first_tranche_queue.csv`.
- source_profile_encoding(원천 프로필 인코딩): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BK/aggressive_pressure_first_tranche_mt5_execution/profile_encoding_receipt.csv`.
- source_runtime_parity(원천 런타임 동등성): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BK/aggressive_pressure_first_tranche_mt5_execution/runtime_parity_receipt.csv`.
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BK_aggressive_pressure_first_tranche_mt5_execution.md`.
- producer(생산자): `stage_pipelines/stage267/run267BL_aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review.py`.
- consumer(소비자): `run267BM_design_aggressive_pressure_second_tranche_or_cross_period_validation`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BL/aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review/trade_records.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BL/aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review/time_slice_kpi.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BL/aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review/curve_diagnostics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BL/aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review/review_result.json`.
- lineage_judgment(계보 판정): `connected_with_boundary(경계부 연결)`.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267BL_aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), parsed trade list(파싱된 거래 목록), curve diagnostics(곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표).
- evidence_missing(빠진 근거): broader period pressure(더 넓은 기간 압박), Tier B fallback routed total(Tier B 대체 실제 라우팅 전체), Adapter follow-up(어댑터 후속), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- selected_candidate(선택 후보): `none`.
- selected_research_baseline(선택 연구 기준선): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_condition(다음 조건): `run267BM_design_aggressive_pressure_second_tranche_or_cross_period_validation`.
