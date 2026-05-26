# run336L Feature Handoff Repair Decision(336L 피처 인계 수리 결정)

- run_id(실행 ID): `run336L_review_fresh_mt5_runtime_probe_and_repair_or_rebuild_decision_v1`
- status(상태): `completed_live_safe_feature_handoff_repair_decision_no_forward_decision`
- judgment(판정): `repair_feasible_for_macro48_and_us100_only_core56_requires_equity_refresh`
- decision(결정): `stage336L_run336M_live_safe_feature_handoff_repair_queue_ready_no_selection`
- latest US100 close(최신 US100 종가): `2026-05-26T17:15:00+00:00`
- repair feasible(수리 가능): `macro48_no_equity_breadth_or_top3;us100_technical42_no_external`
- repair blocked(수리 차단): `core56_no_top3_weight_features`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Finding(발견)

run336K(336K 실행)의 proxy expected value(프록시 예상값)는 MT5 telemetry(메타트레이더5 기록)와 signal count(신호 수) 기준 `matched(일치)`였다. Effect(효과): 기존 feature handoff rows(피처 인계 행)에서는 runtime signal parity(런타임 신호 동등성) 진단에 쓸 수 있다.

하지만 모든 attempt(시도)가 latest broker bars(최신 브로커 봉)에서 `feature_csv_timestamp_not_found`로 끝났다. Effect(효과): Forward Passed/Failed(전진 통과/실패)에는 아직 쓸 수 없다.

live-safe overnight_return(실시간 안전 야간 수익률) 수리는 과거 overlap rows(겹친 행)에서 기존 값과 `0` 차이였다. Effect(효과): complete session(완료 세션)의 학습/검증 의미를 바꾸지 않고 current partial session(현재 부분 세션)의 feature handoff gap(피처 인계 공백)을 줄일 수 있다.

## Decision(결정)

macro48_no_equity_breadth_or_top3(거시48)와 us100_technical42_no_external(US100 기술42)는 run336M(336M 실행)에서 no-retune(무재튜닝) live-safe feature handoff repair(실시간 안전 피처 인계 수리)로 보낸다.

core56_no_top3_weight_features(핵심56)는 equity symbols(주식 심볼) AAPL/AMD/AMZN/GOOGL/META/MSFT/NVDA/TSLA가 `2026-05-22T23:00:00Z`에서 멈춰 최신 close(종가)를 덮지 못한다. Effect(효과): equity refresh(주식 데이터 갱신) 전에는 run336M 대상에서 제외한다.

## Boundary(경계)

`research_development_only_stage336L_feature_handoff_repair_decision_no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
