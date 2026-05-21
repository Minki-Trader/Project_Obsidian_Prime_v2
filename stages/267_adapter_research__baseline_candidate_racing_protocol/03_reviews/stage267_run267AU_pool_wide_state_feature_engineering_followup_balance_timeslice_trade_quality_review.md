# Stage267 Run267AU Pool-wide State Feature Engineering Follow-up Balance/Time-Slice/Trade-Quality Review(267단계 267AU 후보군 전체 상태 피처 엔지니어링 후속 잔액/시간구간/거래품질 검토)

- action(행동): run267AT(267AT 실행)의 `16`개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록) 단위로 다시 읽었다.
- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 같이 본다.
- status(상태): `run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review_completed`
- judgment(판정): `diagnostic_curve_timeslice_trade_quality_review_completed_no_candidate_selection`
- trade_records(거래 기록): `4668`
- candidate_followup_rows(후보-후속 행): `8`
- watch_rows(관찰 행): `0`
- negative_tier_a_slices(음수 Tier A 구간): `38`
- parser_errors(파서 오류): `0`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AT(267AT 실행)의 숫자는 전체적으로 좋아 보인다. 하지만 이 단계의 질문은 '누가 제일 큰 숫자인가'가 아니다.
Effect(효과): 후보별로 어느 월, 어느 요일, 어느 세션, 어느 순서 구간에서 깨지는지 확인해서 다음 run267AV(267AV 실행)의 설계 재료로 쓴다.

Tier A+B(Tier A+B 합산)는 이번에도 duplicate boundary(중복 경계)다.
Effect(효과): 실제 fallback routing(대체 라우팅) 강건성으로 과장하지 않고, Tier A(티어 A) 결과가 반복됐는지 확인하는 감사 근거로만 둔다.

## Candidate Follow-up Watchlist(후보 후속 관찰 목록)

| rank(순위) | candidate(후보) | role(역할) | followup_profile(후속 프로필) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1 | `s264_aih` | `challenger_core` | `core_volatility_resilience_pressure_v2` | 1272.69 | 1.68 | 296 | 17.76 | `2024-12` -270.97 | `month`/`2024-12` -270.97 | `headline_or_mixed_with_slice_hole_no_selection` |
| 2 | `s264_lc` | `defensive_control` | `defensive_control_volatility_audit_v1` | 1218.34 | 1.69 | 289 | 17.00 | `2024-12` -222.70 | `weekday`/`Monday` -268.37 | `headline_or_mixed_with_slice_hole_no_selection` |
| 3 | `s258_stc` | `stress_challenger` | `stress_challenger_trend_prune_pressure_v2` | 1175.10 | 1.57 | 303 | 17.13 | `2024-12` -183.11 | `weekday`/`Monday` -267.44 | `headline_or_mixed_with_slice_hole_no_selection` |
| 4 | `s262_lih` | `validation_heavy` | `validation_control_volatility_audit_v1` | 1127.57 | 1.61 | 288 | 17.24 | `2024-12` -216.59 | `weekday`/`Monday` -272.80 | `headline_or_mixed_with_slice_hole_no_selection` |
| 5 | `s264_aia` | `oos_anchor` | `oos_anchor_dd_resilience_pressure_v2` | 1065.48 | 1.63 | 296 | 14.57 | `2024-12` -145.72 | `weekday`/`Monday` -259.92 | `headline_or_mixed_with_slice_hole_no_selection` |
| 6 | `s264_aia` | `oos_anchor` | `oos_anchor_shock_resilience_pressure_v2` | 1062.17 | 1.65 | 293 | 13.71 | `2024-12` -141.61 | `weekday`/`Monday` -227.89 | `headline_or_mixed_with_slice_hole_no_selection` |
| 7 | `s264_aih` | `challenger_core` | `core_range_resilience_pressure_v2` | 1021.47 | 1.59 | 301 | 16.64 | `2024-12` -216.75 | `weekday`/`Monday` -231.65 | `headline_or_mixed_with_slice_hole_no_selection` |
| 8 | `s258_stc` | `stress_challenger` | `stress_challenger_volatility_prune_pressure_v2` | 905.51 | 1.50 | 268 | 19.87 | `2024-12` -195.06 | `weekday`/`Monday` -285.54 | `headline_or_mixed_with_slice_hole_no_selection` |

## Candidate Summary(후보 요약)

| candidate(후보) | role(역할) | tests(시험 수) | watch(관찰) | mixed(혼합) | holes(구멍) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | worst month net(최악 월 순수익) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_lc` | `defensive_control` | 1 | 0 | 0 | 1 | 1218.34 | 1218.34 | 17.00 | -222.70 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s264_aih` | `challenger_core` | 2 | 0 | 0 | 2 | 1147.08 | 1021.47 | 17.76 | -270.97 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s262_lih` | `validation_heavy` | 1 | 0 | 0 | 1 | 1127.57 | 1127.57 | 17.24 | -216.59 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s264_aia` | `oos_anchor` | 2 | 0 | 0 | 2 | 1063.83 | 1062.17 | 14.57 | -145.72 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |
| `s258_stc` | `stress_challenger` | 2 | 0 | 0 | 2 | 1040.30 | 905.51 | 19.87 | -195.06 | `candidate_has_slice_holes_no_selection(구간 구멍 있음, 선택 아님)` |

## Follow-up Profile Summary(후속 프로필 요약)

| followup_profile(후속 프로필) | pressure_group(압박 그룹) | candidates(후보 수) | watch(관찰) | holes(구멍) | net mean(평균 순수익) | net min(최소 순수익) | worst DD%(최악 손실폭) | best candidate(최고 후보) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `core_volatility_resilience_pressure_v2` | `core_challenger_slice_pressure` | 1 | 0 | 1 | 1272.69 | 1272.69 | 17.76 | `s264_aih` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `defensive_control_volatility_audit_v1` | `defensive_control_audit` | 1 | 0 | 1 | 1218.34 | 1218.34 | 17.00 | `s264_lc` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `stress_challenger_trend_prune_pressure_v2` | `stress_challenger_prune_or_rescue` | 1 | 0 | 1 | 1175.10 | 1175.10 | 17.13 | `s258_stc` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `validation_control_volatility_audit_v1` | `validation_control_audit` | 1 | 0 | 1 | 1127.57 | 1127.57 | 17.24 | `s262_lih` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `oos_anchor_dd_resilience_pressure_v2` | `oos_anchor_watch_gate` | 1 | 0 | 1 | 1065.48 | 1065.48 | 14.57 | `s264_aia` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `oos_anchor_shock_resilience_pressure_v2` | `oos_anchor_watch_gate` | 1 | 0 | 1 | 1062.17 | 1062.17 | 13.71 | `s264_aia` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `core_range_resilience_pressure_v2` | `core_challenger_slice_pressure` | 1 | 0 | 1 | 1021.47 | 1021.47 | 16.64 | `s264_aih` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |
| `stress_challenger_volatility_prune_pressure_v2` | `stress_challenger_prune_or_rescue` | 1 | 0 | 1 | 905.51 | 905.51 | 19.87 | `s258_stc` | `profile_needs_pressure_or_prune(압박 또는 가지치기 필요)` |

## Worst Tier A Slices(최악 Tier A 구간)

| candidate(후보) | followup_profile(후속 프로필) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |
| --- | --- | --- | --- | ---: | ---: | --- |
| `s258_stc` | `stress_challenger_volatility_prune_pressure_v2` | `weekday` | `Monday` | -285.54 | 39 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s262_lih` | `validation_control_volatility_audit_v1` | `weekday` | `Monday` | -272.80 | 45 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aih` | `core_volatility_resilience_pressure_v2` | `month` | `2024-12` | -270.97 | 27 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_lc` | `defensive_control_volatility_audit_v1` | `weekday` | `Monday` | -268.37 | 46 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s258_stc` | `stress_challenger_trend_prune_pressure_v2` | `weekday` | `Monday` | -267.44 | 45 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aia` | `oos_anchor_dd_resilience_pressure_v2` | `weekday` | `Monday` | -259.92 | 44 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aih` | `core_volatility_resilience_pressure_v2` | `weekday` | `Monday` | -244.05 | 44 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aih` | `core_range_resilience_pressure_v2` | `weekday` | `Monday` | -231.65 | 43 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aia` | `oos_anchor_shock_resilience_pressure_v2` | `weekday` | `Monday` | -227.89 | 42 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_lc` | `defensive_control_volatility_audit_v1` | `month` | `2024-12` | -222.70 | 25 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s264_aih` | `core_range_resilience_pressure_v2` | `month` | `2024-12` | -216.75 | 27 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s262_lih` | `validation_control_volatility_audit_v1` | `month` | `2024-12` | -216.59 | 24 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s258_stc` | `stress_challenger_volatility_prune_pressure_v2` | `month` | `2024-12` | -195.06 | 24 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |
| `s258_stc` | `stress_challenger_trend_prune_pressure_v2` | `month` | `2024-12` | -183.11 | 25 | `deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)` |

## Forensics Boundary(포렌식 경계)

- tester_identity(테스터 정체성): terminal count(터미널 수) `1`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, date range(날짜 범위) `2024.01.02` to `2025.01.01`.
- trade_evidence(거래 근거): trade records(거래 기록) `4668`, parser checks(파서 확인) `16`.
- cost_assumptions(비용 가정): `MT5 tester broker-history costs; no separate cost authority claimed(MT5 테스터 브로커 이력 비용 조건, 별도 비용 권위 주장 없음)`.
- backtest_judgment(백테스트 판정): `usable_with_boundary(경계부 사용 가능)`.

## Attribution(성과 귀속)

- observed_change(관찰 변화): run267AS/run267AT(267AS/267AT 실행)의 follow-up pressure(후속 압박) 변형들이 2024 구간에서 양수 KPI(핵심 성과 지표)를 만들었다.
- comparison_baseline(비교 기준): run267B historical 2024(2024 과거 압박) MT5 KPI(MT5 핵심 성과 지표)와 curve diagnostics(곡선 진단).
- likely_drivers(가능 동인): retraining(재학습)이 아니라 state feature score table extension(상태 피처 점수표 확장)과 pressure term(압박 항) 변화다.
- alternative_explanations(대체 설명): 2024 단일 기간 적합, duplicate Tier A+B boundary(중복 Tier A+B 경계), score table(점수표) 확장에 따른 우연 적합 가능성이 남아 있다.
- attribution_confidence(귀속 신뢰도): `medium_for_2024_diagnostic_only(2024 진단 한정 중간)`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/execution_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/kpi_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AT/pool_wide_state_feature_engineering_followup_mt5_execution/backtest_forensics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/followup_variant_manifest.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/runtime_contract.csv`.
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AT_pool_wide_state_feature_engineering_followup_mt5_execution.md`.
- producer(생산자): `stage_pipelines/stage267/run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review.py`.
- consumer(소비자): `run267AV_design_pool_wide_state_feature_engineering_followup_or_adapter_branch_from_run267AU_review`.
- artifact_paths(산출물 경로): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AU/pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review/trade_records.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AU/pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review/time_slice_kpi.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AU/pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review/curve_diagnostics.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AU/pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review/review_result.json`.
- lineage_judgment(계보 판정): `connected_with_boundary(경계부 연결)`.

## Boundary(경계)

- positive_claim(긍정 주장): `none(없음)`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- missing_required(필수 누락): broader period pressure(더 넓은 기간 압박), Adapter follow-up(어댑터 후속), true fallback/routed robustness(실제 대체 라우팅 강건성), ONNX parity(ONNX 동등성).
- next_action(다음 행동): `run267AV_design_pool_wide_state_feature_engineering_followup_or_adapter_branch_from_run267AU_review`.
