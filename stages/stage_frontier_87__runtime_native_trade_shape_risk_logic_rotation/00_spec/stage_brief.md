# F87 Runtime-Native Trade Shape/Risk Logic Rotation(F87 런타임 네이티브 거래 형태/위험 로직 회전)

Status(상태): `f87b_trade_shape_risk_proxy_weak_or_negative_repair_or_rotation_required_no_authority`

Latest completed run(최근 완료 실행): `frontier87B_trade_shape_risk_proxy_scout_v1`

Current run(현재 실행): `frontier87C_trade_shape_risk_repair_or_rotation_decision_v1`

Action(행동): F87B built a trade-shape/risk proxy surface(F87B가 거래 형태/위험 프록시 표면 생성).

Effect(효과): F86 first-touch prediction repair(F86 첫 터치 예측 수리)를 반복하지 않고, MFE/MAE/shape score(최대 유리 이동/최대 불리 이동/형태 점수) 기반 후보 판단으로 이동했다.

Claim boundary(주장 경계): `f87b_trade_shape_risk_proxy_scout_only_no_strategy_tester_runtime_economics_no_runtime_authority_no_goal_achieve`.
<!-- frontier87C_trade_shape_risk_repair_or_rotation_decision_v1 -->

## F87C decision update(결정 갱신)

- Action(행동): F87B weak trade-shape/risk proxy(약한 거래 형태/위험 프록시) 때문에 same-axis repair(동일 축 수리)를 capped(상한 처리)했다.
- Effect(효과): next run(다음 실행)은 `frontier87D_stage_closeout_or_f88_rotation_handoff_v1`이며, 같은 top-percent threshold retune(상위 퍼센트 임계값 재조정)로 이어지지 않는다.
