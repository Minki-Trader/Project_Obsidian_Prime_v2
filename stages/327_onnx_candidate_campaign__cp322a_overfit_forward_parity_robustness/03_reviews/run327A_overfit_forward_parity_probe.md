# run327A Overfit/Forward/Parity Probe(327A 과적합/전진/동등성 탐침)

## Decision(판정)

- status(상태): `completed_overfit_forward_parity_probe_forward_signal_blocked`
- judgment(판정): `blocked_repair_required_no_goal_achieve`
- decision(결정): `forward_usability_unresolved_due_signal_contract_and_overfit_risk`
- effect(효과): cp322A는 연구 산출물(research artifact, 연구 산출물)로 보존하지만, forward usability(전진 사용 가능성)과 Goal Achieve(목표 달성)는 주장하지 않는다.

## What Held(유지된 것)

- ONNX parity(온닉스 동등성): `True`; mismatch(불일치)=`0`
- Runtime parity(런타임 동등성): `True`; compared rows(비교 행)=`78`
- Forward data(전진 데이터): `core_data_available`

## What Did Not Hold(유지되지 않은 것)

- ONNX model(온닉스 모델)은 live-computable feature model(실시간 계산 피처 모델)이 아니라 `run322b_route_signal` identity surface(정체성 표면)다.
- Stage326(326단계) 기준 최신 forward(전진) 구간에는 `run322b_route_signal` handoff(인계)가 없다.
- naive forward signal generation(순진한 전진 신호 생성)은 split rank(분할 순위)와 outcome distillation(결과 증류) 위험 때문에 금지한다.

## KPI Context(핵심 지표 문맥)

- validation net/PF/trades(검증 순수익/수익 팩터/거래수): `472738.31` / `1.64` / `919`
- OOS net/PF/trades(표본외 순수익/수익 팩터/거래수): `237627.93` / `1.51` / `637`
- OOS/validation ratio(OOS/검증 비율): net=`0.5027`, PF=`0.9207`, trades=`0.6931`
- effect(효과): 숫자는 참고 문맥일 뿐이고, 이번 판정은 forward handoff(전진 인계)와 overfit risk(과적합 위험)를 우선한다.

## Risk Matrix(위험 행렬)

- R1: identity_onnx_over_precomputed_signal(사전 계산 신호 위 정체성 ONNX) -> high / 새 forward(전진) 구간에서는 route signal(경로 신호)이 없으면 모델이 판단하지 못한다.
- R2: split_local_rank_threshold(분할 내부 순위 임계값) -> high / forward(전진) 전체 분포를 본 뒤 순위를 만들면 미래 정보 누수(leakage, 누수)가 된다.
- R3: actual_outcome_distillation(실제 결과 증류) -> high / 성과 좋은 과거 거래 모양을 다시 맞추는 overfit(과적합) 위험이 크다.
- R4: actual_mt5_gate_selection_pressure(실제 MT5 관문 선택 압력) -> medium_high / 검증/표본외 구간 자체에 selection pressure(선택 압력)가 쌓인다.
- R5: runtime_reproduction_not_forward_authority(런타임 재현은 전진 권위가 아님) -> high / 기존 parity pass(동등성 통과)는 최신 forward(전진) 사용 가능성을 증명하지 않는다.

## Forward Feasibility(전진 가능성)

- forward_market_data(전진 시장 데이터): available_with_timezone_boundary(시간대 경계 포함 사용 가능) / Effect(효과): US100/VIX/USDX/US10YR forward(전진) 데이터는 핵심 차단이 아니다.
- runtime_feature_order(런타임 피처 순서): single_route_signal_required(단일 경로 신호 필요) / Effect(효과): `run322b_route_signal` 없이는 ONNX(온닉스)가 독립 판단을 못 한다.
- forward_route_signal_handoff(전진 경로 신호 인계): blocked_forward_signal_handoff_missing(전진 신호 인계 누락 차단) / Effect(효과): MT5 forward result(MT5 전진 결과)를 아직 만들 수 없다.
- naive_signal_generation(순진한 신호 생성): unsafe(불안전) / Effect(효과): split-local rank(분할 내부 순위)를 forward(전진)에 그대로 적용하면 leakage(누수)가 된다.
- safe_next_probe(안전한 다음 탐침): stage328_required(328단계 필요) / Effect(효과): 과거 기준 창에서 얼린 signal contract(신호 계약)만 추출하고 새 데이터 튜닝은 금지한다.

## Selection Pressure(선택 압력)

- run_registry rows(실행 등록부 행): `342`
- noted attempts(기록된 시도): `1797`
- noted MT5 KPI records(기록된 MT5 핵심 지표): `1404`
- interpretation(해석): `high_multiple_testing_pressure(높은 다중 시험 압력)`

## Next(다음)

Stage328(328단계)는 frozen signal contract extraction(고정 신호 계약 추출)을 설계한다. Effect(효과): 새 forward(전진) 데이터로 threshold(임계값)를 맞추지 않고, 과거 기준으로 얼린 규칙만 전진에 적용 가능한지 검증한다.
