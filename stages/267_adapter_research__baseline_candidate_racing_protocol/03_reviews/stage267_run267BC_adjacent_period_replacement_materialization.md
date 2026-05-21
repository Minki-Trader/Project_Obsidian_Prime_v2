# Stage267 Run267BC Adjacent-period Replacement Materialization(267단계 267BC 인접 기간 대체 물질화)

- action(행동): run267BB(267BB 실행)의 `s264_aia` watch pair(관찰 쌍) 2개를 2023H2/2025H1/2025H2 adjacent period(인접 기간) feature frame(피처 프레임)과 MT5 attempt manifest(MT5 시도 목록)로 만들었다.
- effect(효과): 다음 run267BD(267BD 실행)에서 후보 의미를 바꾸지 않고 기간만 넓혀 덜 깨지는지 확인할 수 있다.
- status(상태): `run267BC_adjacent_period_replacement_frames_materialized_route_manifest_repair_inputs_ready_execution_pending`
- judgment(판정): `adjacent_period_attempt_inputs_materialized_no_mt5_execution_no_candidate_selection`
- periods(기간): `3`
- feature_frames(피처 프레임): `6`
- attempts(시도): `6`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

이번 실행은 성과를 낸 실행이 아니라, 성과를 검증할 재료를 만든 실행이다.
Effect(효과): `s264_aia`가 2024년에서만 좋아 보인 것인지, 2023년 후반과 2025년 구간에서도 덜 깨지는지 다음 MT5(MetaTrader 5, 메타트레이더5)에서 볼 수 있다.

좋은 후보라고 부르려면 아직 멀었다. 지금은 watch(관찰) 상태다.
Effect(효과): 숫자 몇 개가 좋았다는 이유로 Adapter(어댑터) 개발이나 ONNX(ONNX) 검토로 뛰지 않는다.

true fallback(실제 대체)은 여전히 막혀 있다.
Effect(효과): duplicate Tier A+B(중복 Tier A+B)를 actual routed total(실제 라우팅 전체)처럼 오해하지 않는다.

## Period Availability(기간 가용성)

| period(기간) | role(역할) | rows(행) | first(첫 시각) | last(마지막 시각) | split counts(스플릿 수) | status(상태) |
| --- | --- | ---: | --- | --- | --- | --- |
| `adjacent_2023_h2_train_pre_2024` | `pre_2024_train_context` | 6090 | `2023-07-05T16:40:00Z` | `2023-12-29T22:00:00Z` | `{"train": 6090}` | `usable` |
| `adjacent_2025_h1_validation_post_2024` | `post_2024_validation_context` | 6867 | `2025-01-02T16:35:00Z` | `2025-06-30T22:00:00Z` | `{"validation": 6867}` | `usable` |
| `adjacent_2025_h2_oos_followthrough` | `oos_followthrough_context` | 6486 | `2025-07-01T16:35:00Z` | `2025-12-31T22:00:00Z` | `{"oos": 3509, "validation": 2977}` | `usable` |

## Attempt Inputs(시도 입력)

| queue(큐) | test(시험) | period(기간) | rows(행) | feature hash(피처 해시) | status(상태) |
| --- | --- | --- | ---: | --- | --- |
| `run267BC_q01_s264_aia_rep_trend_strength_adx_adjacent_2023_h2_train_pre_2024` | `rep_trend_strength_adx` | `adjacent_2023_h2_train_pre_2024` | 6090 | `3fa971741f7384c060223564505aa4e6fc5a87ace83bf50c8e82bc4f01fa4a2e` | `materialized_execution_pending` |
| `run267BC_q02_s264_aia_rep_trend_strength_adx_adjacent_2025_h1_validation_post_2024` | `rep_trend_strength_adx` | `adjacent_2025_h1_validation_post_2024` | 6867 | `3fa971741f7384c060223564505aa4e6fc5a87ace83bf50c8e82bc4f01fa4a2e` | `materialized_execution_pending` |
| `run267BC_q03_s264_aia_rep_trend_strength_adx_adjacent_2025_h2_oos_followthrough` | `rep_trend_strength_adx` | `adjacent_2025_h2_oos_followthrough` | 6486 | `3fa971741f7384c060223564505aa4e6fc5a87ace83bf50c8e82bc4f01fa4a2e` | `materialized_execution_pending` |
| `run267BC_q04_s264_aia_rep_volatility_atr_adjacent_2023_h2_train_pre_2024` | `rep_volatility_atr` | `adjacent_2023_h2_train_pre_2024` | 6090 | `057a939561d360f5b6f80e7e505f4ded89da87cb4f89dec12bf23756e6199274` | `materialized_execution_pending` |
| `run267BC_q05_s264_aia_rep_volatility_atr_adjacent_2025_h1_validation_post_2024` | `rep_volatility_atr` | `adjacent_2025_h1_validation_post_2024` | 6867 | `057a939561d360f5b6f80e7e505f4ded89da87cb4f89dec12bf23756e6199274` | `materialized_execution_pending` |
| `run267BC_q06_s264_aia_rep_volatility_atr_adjacent_2025_h2_oos_followthrough` | `rep_volatility_atr` | `adjacent_2025_h2_oos_followthrough` | 6486 | `057a939561d360f5b6f80e7e505f4ded89da87cb4f89dec12bf23756e6199274` | `materialized_execution_pending` |

## Boundary(경계)

- MT5 execution(MT5 실행): `not_executed`, 다음 실행에서 확인한다.
- true fallback(실제 대체): `blocked`, route manifest(라우팅 목록) 구성요소가 아직 없다.
- Adapter(어댑터): 보류. adjacent-period(인접 기간) KPI(핵심 성과 지표), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선)를 본 뒤 판단한다.
- ONNX parity(ONNX 동등성): 금지. Goal gate(목표 게이트) 전에는 검토하지 않는다.
- next_action(다음 행동): `run267BD_execute_s264_aia_adjacent_period_replacement_mt5_batch_or_repair_materialization_gaps`.

## Artifact Lineage(산출물 계보)

- source subset review(원천 부분집합 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BB/cross_period_replacement_ready_subset_review/replacement_subset_review.csv`.
- source run267W variant manifest(원천 267W 변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/true_internal_ablation_variant_manifest.csv`.
- feature manifest(피처 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BC/adjacent_period_replacement_frame_materialization/adjacent_period_feature_frame_manifest.csv`.
- attempt manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BC/adjacent_period_replacement_frame_materialization/attempts.csv`.
- route repair inputs(라우팅 수정 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BC/adjacent_period_replacement_frame_materialization/route_manifest_repair_inputs.csv`.
