# Stage267 Run267AY Pool-wide State Feature Engineering Second Follow-up Balance/Time-Slice/Trade-Quality Review(267단계 267AY 후보군 전체 상태 피처 엔지니어링 2차 후속 잔액/시간구간/거래품질 검토)

- action(행동): run267AX(267AX 실행)의 `8`개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록) 단위로 다시 읽었다.
- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 같이 본다.
- status(상태): `run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review_completed`
- judgment(판정): `diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection`
- trade_records(거래 기록): `2234`
- candidate_second_rows(후보-2차 행): `8`
- watch_rows(관찰 행): `0`
- negative_tier_a_slices(음수 Tier A 구간): `35`
- parser_errors(파서 오류): `0`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AX(267AX 실행)의 8개 후보 변형은 모두 2024 구간에서 양수 KPI(핵심 성과 지표)를 만들었다.
Effect(효과): 그러나 이번 판독은 선택이 아니라 약점 노출이다. 특히 월요일(Monday, 월요일), 2024-12(2024년 12월), 순서 구간이 다시 약한지 본다.
Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 없어서 계속 blocked(차단)이다.

## Candidate Second Follow-up Watchlist(후보 2차 후속 관찰 목록)

| rank(순위) | candidate(후보) | role(역할) | source profile(원천 프로필) | second profile(2차 프로필) | net profit(순수익) | delta vs source(원천 대비 변화) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1 | `s264_aih` | `challenger_core` | `core_volatility_resilience_pressure_v2` | `core_volatility_range_interaction_v3` | 1153.72 | -118.97 | 1.74 | 275 | 16.65 | `2024-12` -232.80 | `month`/`2024-12` -232.80 | `headline_or_mixed_with_slice_hole_no_selection` |
| 2 | `s258_stc` | `stress_challenger` | `stress_challenger_trend_prune_pressure_v2` | `stress_challenger_trend_strict_prune_v3` | 1133.45 | -41.65 | 1.58 | 293 | 16.53 | `2024-12` -167.46 | `weekday`/`Monday` -283.04 | `headline_or_mixed_with_slice_hole_no_selection` |
| 3 | `s264_lc` | `defensive_control` | `defensive_control_volatility_audit_v1` | `defensive_control_repeat_audit_v2` | 1052.20 | -166.14 | 1.67 | 278 | 16.83 | `2024-12` -202.41 | `weekday`/`Monday` -233.05 | `headline_or_mixed_with_slice_hole_no_selection` |
| 4 | `s264_aia` | `oos_anchor` | `oos_anchor_dd_resilience_pressure_v2` | `oos_anchor_range_dd_conservative_v3` | 1037.60 | -27.88 | 1.64 | 287 | 14.11 | `2024-12` -137.26 | `weekday`/`Monday` -260.20 | `headline_or_mixed_with_slice_hole_no_selection` |
| 5 | `s262_lih` | `validation_heavy` | `validation_control_volatility_audit_v1` | `validation_control_repeat_audit_v2` | 1007.16 | -120.41 | 1.59 | 283 | 16.98 | `2024-12` -192.32 | `weekday`/`Monday` -245.93 | `headline_or_mixed_with_slice_hole_no_selection` |
| 6 | `s264_aia` | `oos_anchor` | `oos_anchor_shock_resilience_pressure_v2` | `oos_anchor_shock_range_conservative_v3` | 949.94 | -112.23 | 1.66 | 282 | 14.48 | `2024-12` -150.63 | `weekday`/`Monday` -192.83 | `headline_or_mixed_with_slice_hole_no_selection` |
| 7 | `s258_stc` | `stress_challenger` | `stress_challenger_volatility_prune_pressure_v2` | `stress_challenger_volatility_strict_prune_v3` | 878.20 | -27.31 | 1.57 | 255 | 16.54 | `2024-12` -88.28 | `weekday`/`Monday` -242.66 | `headline_or_mixed_with_slice_hole_no_selection` |
| 8 | `s264_aih` | `challenger_core` | `core_range_resilience_pressure_v2` | `core_range_volatility_interaction_v3` | 822.06 | -199.41 | 1.59 | 281 | 15.46 | `2024-12` -173.14 | `weekday`/`Monday` -213.14 | `headline_or_mixed_with_slice_hole_no_selection` |

## Candidate Summary(후보 요약)

| candidate(후보) | role(역할) | tests(시험 수) | watch(관찰) | mixed(혼합) | holes(구멍) | regressions(후퇴) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | worst month net(최악 월 순수익) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_lc` | `defensive_control` | 1 | 0 | 0 | 1 | 1 | 1052.20 | 1052.20 | 16.83 | -202.41 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s262_lih` | `validation_heavy` | 1 | 0 | 0 | 1 | 1 | 1007.16 | 1007.16 | 16.98 | -192.32 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s258_stc` | `stress_challenger` | 2 | 0 | 0 | 2 | 0 | 1005.83 | 878.20 | 16.54 | -167.46 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s264_aia` | `oos_anchor` | 2 | 0 | 0 | 2 | 0 | 993.77 | 949.94 | 14.48 | -150.63 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s264_aih` | `challenger_core` | 2 | 0 | 0 | 2 | 1 | 987.89 | 822.06 | 16.65 | -232.80 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |

## Second Profile Summary(2차 프로필 요약)

| second profile(2차 프로필) | pressure group(압박 그룹) | candidates(후보 수) | watch(관찰) | holes(구멍) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | best candidate(최고 후보) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `core_volatility_range_interaction_v3` | `core_challenger_second_pressure` | 1 | 0 | 1 | 1153.72 | 1153.72 | 16.65 | `s264_aih` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `stress_challenger_trend_strict_prune_v3` | `stress_challenger_prune_or_rescue` | 1 | 0 | 1 | 1133.45 | 1133.45 | 16.53 | `s258_stc` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `defensive_control_repeat_audit_v2` | `defensive_control_repeat_audit` | 1 | 0 | 1 | 1052.20 | 1052.20 | 16.83 | `s264_lc` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `oos_anchor_range_dd_conservative_v3` | `oos_anchor_adapter_watch_gate` | 1 | 0 | 1 | 1037.60 | 1037.60 | 14.11 | `s264_aia` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `validation_control_repeat_audit_v2` | `validation_control_repeat_audit` | 1 | 0 | 1 | 1007.16 | 1007.16 | 16.98 | `s262_lih` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `oos_anchor_shock_range_conservative_v3` | `oos_anchor_adapter_watch_gate` | 1 | 0 | 1 | 949.94 | 949.94 | 14.48 | `s264_aia` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `stress_challenger_volatility_strict_prune_v3` | `stress_challenger_prune_or_rescue` | 1 | 0 | 1 | 878.20 | 878.20 | 16.54 | `s258_stc` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `core_range_volatility_interaction_v3` | `core_challenger_second_pressure` | 1 | 0 | 1 | 822.06 | 822.06 | 15.46 | `s264_aih` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |

## Worst Tier A Slices(최악 Tier A 구간)

| candidate(후보) | second profile(2차 프로필) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `s258_stc` | `stress_challenger_trend_strict_prune_v3` | `weekday` | `Monday` | -283.04 | 42 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aia` | `oos_anchor_range_dd_conservative_v3` | `weekday` | `Monday` | -260.20 | 43 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s262_lih` | `validation_control_repeat_audit_v2` | `weekday` | `Monday` | -245.93 | 44 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s258_stc` | `stress_challenger_volatility_strict_prune_v3` | `weekday` | `Monday` | -242.66 | 38 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_lc` | `defensive_control_repeat_audit_v2` | `weekday` | `Monday` | -233.05 | 43 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aih` | `core_volatility_range_interaction_v3` | `month` | `2024-12` | -232.80 | 23 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aih` | `core_volatility_range_interaction_v3` | `weekday` | `Monday` | -219.06 | 42 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aih` | `core_range_volatility_interaction_v3` | `weekday` | `Monday` | -213.14 | 42 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_lc` | `defensive_control_repeat_audit_v2` | `month` | `2024-12` | -202.41 | 23 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aia` | `oos_anchor_shock_range_conservative_v3` | `weekday` | `Monday` | -192.83 | 39 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s262_lih` | `validation_control_repeat_audit_v2` | `month` | `2024-12` | -192.32 | 23 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aih` | `core_range_volatility_interaction_v3` | `month` | `2024-12` | -173.14 | 27 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s258_stc` | `stress_challenger_trend_strict_prune_v3` | `month` | `2024-12` | -167.46 | 25 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aia` | `oos_anchor_shock_range_conservative_v3` | `month` | `2024-12` | -150.63 | 21 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |

## Forensics Boundary(포렌식 경계)

- tester_identity(테스터 정체성): terminal count(터미널 수) `1`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, date range(날짜 범위) `2024.01.02` to `2025.01.01`.
- trade_evidence(거래 근거): trade records(거래 기록) `2234`, parser checks(파서 확인) `8`.
- cost_assumptions(비용 가정): `MT5 tester broker-history costs; no separate cost authority claimed(MT5 테스터 브로커 이력 비용 조건, 별도 비용 권위 주장 없음)`.
- backtest_judgment(백테스트 판정): `usable_with_boundary(경계부 사용 가능)`.

## Attribution(성과 귀속)

- observed_change(관찰 변화): 2차 후속 압박(second follow-up pressure, 2차 후속 압박)은 일부 후보에서 net profit(순수익)을 유지하거나 개선했지만 일부는 원천 후속보다 후퇴했다.
- comparison_baseline(비교 기준): run267AU(267AU 실행) source follow-up review(원천 후속 검토)와 run267B historical 2024(2024 과거 압박) KPI(핵심 성과 지표).
- likely_drivers(가능 동인): retraining(재학습)이 아니라 state feature interaction(상태 피처 상호작용), strict prune(엄격 가지치기), conservative DD gate(보수적 손실폭 게이트) 변화다.
- segment_checks(구간 확인): month/weekday/session/hour/direction/chron_segment(월/요일/세션/시간/방향/순서 구간)을 확인했다.
- trade_shape(거래 형태): trade count(거래 수), expectancy(기대값), PF(수익 팩터), closed-balance drawdown(종가 기준 손실폭), losing streak(연속 손실)을 기록했다.
- alternative_explanations(대체 설명): 2024 단일 기간 적합, Tier B(티어 B) 부재, score table(점수표) 확장에 따른 우연 적합 가능성이 남아 있다.
- attribution_confidence(귀속 신뢰도): `medium_for_2024_diagnostic_only(2024 진단 한정 중간)`. 운영 의미는 없다.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AX/pool_wide_state_feature_engineering_second_followup_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/second_followup_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/runtime_contract.csv`.
- source_route_gap(원천 라우팅 공백): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/route_gap_audit.csv`.
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution.md`.
- producer(생산자): `stage_pipelines/stage267/run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review.py`.
- consumer(소비자): `run267AZ_design_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_from_run267AY_review`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AY/pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review/trade_records.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AY/pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review/time_slice_kpi.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AY/pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review/curve_diagnostics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AY/pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review/review_result.json`.
- lineage_judgment(계보 판정): `connected_with_boundary(경계부 연결)`.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review`.
- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), parsed trade list(파싱된 거래 목록), curve diagnostics(곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표).
- evidence_missing(빠진 근거): broader period pressure(더 넓은 기간 압박), Tier B fallback routed total(Tier B 대체 실제 라우팅 전체), Adapter follow-up(어댑터 후속), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_condition(다음 조건): `run267AZ_design_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_from_run267AY_review`.
