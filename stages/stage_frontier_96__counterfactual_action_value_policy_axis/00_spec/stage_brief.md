# F96 Counterfactual Action Value Policy Axis(반사실 행동가치 정책 축)

- current run(현재 실행): `frontier96B_counterfactual_action_value_policy_proxy_scout_v1`
- latest completed run(최근 완료 실행): `frontier96A_stage_open_counterfactual_action_value_policy_axis_v1`
- source closeout(원천 마감): `frontier95C_closed_bar_state_transition_repair_or_rotation_decision_v1`
- status(상태): design-only formal open recorded(설계 전용 정식 개방 기록)
- authority(권위): not_claimed(주장 없음)

## Question(질문)

Can closed-bar features(확정 봉 피처) learn long/short/abstain(롱/숏/관망) counterfactual action value(반사실 행동가치) with adverse-excursion risk(불리한 변동 위험) before direction mapping(방향 매핑), producing side-balanced(방향 균형) 5-10 trades/day(일 5-10 거래) scout clues(정찰 단서)?

## Hypothesis(가설)

Closed-bar features can learn long/short/abstain counterfactual action value with adverse-excursion and cost penalties, producing a risk-first trade surface that avoids the F95 state-cluster long-only collapse.

## Novelty Delta(신규성 차이)

- objective(목적함수): action-value/regret-first(행동가치/후회 우선) instead of unsupervised state-first clustering(비지도 상태 우선 군집)
- label(라벨): counterfactual long/short/abstain path utility(반사실 롱/숏/관망 경로 효용) with adverse excursion penalties(불리 변동 벌점)
- trade shape(거래 형태): side-symmetric risk-first action eligibility(양방향 대칭 위험 우선 행동 자격)
- validation philosophy(검증 철학): utility/regret/DD/recovery/side-balance(효용/후회/손실폭/회복/방향 균형) before PF-only selection(PF 단독 선정)
- runtime boundary(런타임 경계): same-packet MT5 Strategy Tester probe(같은 묶음 MT5 전략 테스터 탐침) is required if a runnable ONNX/EA/set claim(실행 가능한 온엑스/전문가 자문/설정 주장) appears

## Boundary(경계)

F96A is design-only formal open(설계 전용 정식 개방) evidence(근거) only. No selected baseline(선택 기준선), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed(주장됨).
