# Stage267 Run267O Pool-Wide Balance/Time-Slice/Trade-Quality Review(267단계 267O 후보군 전체 잔액/시간구간/거래품질 검토)

- action(행동): run267N(267N 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 파싱해 balance curve diagnostics(잔액 곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 만들었다.
- effect(효과): net profit(순수익)만 보지 않고 월/요일/시간/세션/방향/초중후 구간에서 덜 깨지는 후보와 깨지는 축을 구분한다.
- status(상태): `run267O_pool_wide_balance_timeslice_trade_quality_review_completed`
- source_run(원천 실행): `run267N_stage267_pool_wide_ablation_replacement_materialization_v1`
- trade_records(거래 기록): `16484`
- curve_rows(곡선 행): `48`
- time_slice_rows(시간 구간 행): `1948`
- parser_errors(파서 오류): `0`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 해석)

run267N(267N 실행)의 KPI(핵심 성과 지표) 단서는 일부 강했다. 하지만 이번 run267O(267O 실행)는 그 숫자가 곡선과 약한 구간에서도 덜 깨지는지 확인하는 단계다.
결론은 아직 선택 후보(selected candidate, 선택 후보)가 없다는 것이다. 여러 변형이 2024 baseline(2024 기준)보다 좋아졌지만, 약한 월/구간, direct/proxy(직접/대체) 경계, 내부 feature order(피처 순서) 확인이 남아 있다.
ONNX readiness(ONNX 준비)도 주장하지 않는다. 이번 결과는 다음 run267P(267P 실행)에서 내부 피처 확인과 Adapter(어댑터) 설계를 할 재료다.

## Candidate Summary(후보 요약)

| candidate(후보) | strong clues(강한 단서) | failures(실패) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭) | best test(최고 시험) | worst month floor(최악 월 바닥) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |
| `s264_aia` | 3 | 0 | 306.874 | 1.235529 | 20.234 | `abl_volatility_bandwidth` | -74.27 | broad_constructive_watch_no_selection(넓은 건설적 관찰, 선택 아님) |
| `s264_lc` | 2 | 1 | 383.422 | 1.160043 | 26.95 | `abl_gate_variant_rule` | -106.86 | contains_failure_memory_no_selection(실패 기억 포함, 선택 아님) |
| `s264_aih` | 2 | 0 | 294.46 | 1.238505 | 20.685 | `abl_volatility_bandwidth` | -74.27 | broad_constructive_watch_no_selection(넓은 건설적 관찰, 선택 아님) |
| `s258_stc` | 1 | 0 | 283.232 | 1.189701 | 26.788 | `abl_volatility_bandwidth` | -122.87 | single_axis_clue_needs_more_pressure(단일 축 단서, 추가 압박 필요) |
| `s262_lih` | 1 | 1 | 141.518 | 1.113309 | 29.9 | `rep_volatility_atr` | -121.22 | contains_failure_memory_no_selection(실패 기억 포함, 선택 아님) |

## Top Candidate-Test Rows(상위 후보-시험 행)

| candidate(후보) | test(시험) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | weakest month(가장 약한 월) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s264_lc` | `abl_gate_variant_rule` | 1227.99 | 1.240707 | 22.97 | 516 | `2024-07` -86.87 | strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요) |
| `s258_stc` | `abl_volatility_bandwidth` | 442.13 | 1.331409 | 19.33 | 335 | `2024-06` -46.68 | strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요) |
| `s264_aih` | `abl_volatility_bandwidth` | 412.57 | 1.349864 | 15.9 | 314 | `2024-06` -32.73 | strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요) |
| `s264_aih` | `rep_volatility_atr` | 412.57 | 1.349864 | 15.9 | 314 | `2024-06` -32.73 | strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요) |
| `s264_aia` | `abl_volatility_bandwidth` | 408.29 | 1.347088 | 15.85 | 315 | `2024-06` -32.37 | strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요) |
| `s264_aia` | `rep_volatility_atr` | 408.29 | 1.347088 | 15.85 | 315 | `2024-06` -32.37 | strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요) |
| `s264_lc` | `rep_volatility_atr` | 396.18 | 1.339745 | 16.81 | 312 | `2024-06` -32.37 | strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요) |
| `s262_lih` | `rep_volatility_atr` | 380.99 | 1.327002 | 18.05 | 313 | `2024-06` -32.37 | strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요) |
| `s264_aia` | `abl_session_timing` | 365.09 | 1.229175 | 18.53 | 332 | `2024-07` -72.07 | strong_curve_clue_needs_internal_confirmation(강한 곡선 단서, 내부 확인 필요) |
| `s258_stc` | `abl_session_timing` | 317.33 | 1.178887 | 25.5 | 354 | `2024-07` -117.58 | constructive_but_not_adapter_ready(건설적이나 어댑터 준비 아님) |
| `s258_stc` | `abl_price_return_range` | 265.82 | 1.194602 | 27.03 | 335 | `2024-04` -78.2 | constructive_but_not_adapter_ready(건설적이나 어댑터 준비 아님) |
| `s258_stc` | `abl_trend_strength_direction` | 195.44 | 1.121804 | 31.04 | 364 | `2024-07` -122.87 | mixed_or_insufficient_curve_evidence(혼합 또는 곡선 근거 부족) |

## Weak Slices(약한 구간)

| candidate(후보) | test(시험) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_lc` | `abl_gate_variant_rule` | `session_report` | `session_07_12_report_time` | 6 | -219.59 | 0.0 | 43.918 |
| `s264_lc` | `abl_gate_variant_rule` | `close_hour_report` | `22` | 17 | -150.91 | 0.660678 | 57.510833 |
| `s262_lih` | `abl_gate_rank_bucket` | `chron_segment` | `chron_mid` | 118 | -137.62 | 0.753245 | 39.56 |
| `s262_lih` | `abl_trend_strength_direction` | `chron_segment` | `chron_mid` | 113 | -135.85 | 0.73251 | 34.328 |
| `s262_lih` | `rep_trend_strength_adx` | `chron_segment` | `chron_mid` | 113 | -135.85 | 0.73251 | 34.328 |
| `s258_stc` | `abl_session_timing` | `weekday` | `Monday` | 63 | -130.54 | 0.673952 | 33.011412 |
| `s258_stc` | `abl_trend_strength_direction` | `chron_segment` | `chron_mid` | 122 | -130.18 | 0.796572 | 41.005107 |
| `s258_stc` | `rep_trend_strength_adx` | `chron_segment` | `chron_mid` | 122 | -130.18 | 0.796572 | 41.005107 |
| `s262_lih` | `abl_gate_rank_bucket` | `weekday` | `Friday` | 84 | -129.13 | 0.692986 | 34.27534 |
| `s262_lih` | `abl_gate_rank_bucket` | `direction` | `sell` | 207 | -126.83 | 0.891824 | 50.162264 |
| `s264_lc` | `abl_gate_rank_bucket` | `weekday` | `Monday` | 60 | -124.85 | 0.604179 | 27.464831 |
| `s264_lc` | `abl_gate_rank_bucket` | `chron_segment` | `chron_mid` | 117 | -123.29 | 0.77782 | 36.667857 |
| `s258_stc` | `abl_trend_strength_direction` | `month` | `2024-07` | 39 | -122.87 | 0.484562 | 26.268474 |
| `s258_stc` | `rep_trend_strength_adx` | `month` | `2024-07` | 39 | -122.87 | 0.484562 | 26.268474 |
| `s262_lih` | `abl_gate_rank_bucket` | `weekday` | `Monday` | 60 | -122.64 | 0.603364 | 27.229378 |

## Performance Attribution(성과 귀인)

- observed_change(관측 변화): run267N(267N 실행)의 일부 proxy adapter(대체 어댑터)와 direct gate(직접 게이트) 변형은 2024 baseline(2024 기준) 대비 net profit(순수익), PF(profit factor, 수익 팩터), DD(drawdown, 손실폭)를 동시에 개선했다.
- likely_drivers(가능한 원인): volatility/ATR(변동성/ATR) proxy axis(대체 축)는 여러 후보에서 손실폭을 낮췄고, `s264_lc`의 gate variant(게이트 변형)는 매우 큰 순수익 단서를 냈다.
- alternative_explanations(대안 설명): proxy adapter(대체 어댑터)는 true internal feature ablation(진짜 내부 피처 제거)이 아니므로 feature order(피처 순서)와 runtime surface(런타임 표면) 확인 전에는 구조적 견고성으로 볼 수 없다.
- attribution_confidence(귀인 신뢰도): `medium_to_low(중간~낮음)`. MT5 거래 목록 근거는 생겼지만 내부 피처 확인과 더 넓은 기간 검증은 남았다.

## Backtest Forensics(백테스트 포렌식)

- source_execution_result(원천 실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/execution_result.json`
- source_kpi_summary(원천 KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/kpi_summary.csv`
- source_forensics(원천 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/backtest_forensics.csv`
- source_reports(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/mt5/reports`
- tester_scope(테스터 범위): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 비용 우위를 주장하지 않는다.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267O_pool_wide_balance_timeslice_trade_quality_review.py`
- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간 구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_test_review(후보-시험 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/candidate_test_review.csv`
- candidate_summary(후보 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/candidate_balance_timeslice_summary.csv`
- test_axis_summary(시험 축 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/test_axis_balance_timeslice_summary.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
- parser_checks(파서 점검): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/parser_checks.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267O/pool_wide_balance_timeslice_trade_quality_review/review_result.json`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267O_pool_wide_balance_timeslice_trade_quality_review`.
- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design`.
