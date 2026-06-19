# F96 Counterfactual Action Value Policy Axis(반사실 행동가치 정책 축)

- current run(현재 실행): `frontier96A_stage_open_counterfactual_action_value_policy_axis_v1`
- source closeout(원천 마감): `frontier95C_closed_bar_state_transition_repair_or_rotation_decision_v1`
- status(상태): pending formal open(정식 개방 대기)
- authority(권위): not_claimed(주장 없음)

## Question(질문)

Can closed-bar features learn long/short/abstain counterfactual action value with adverse-excursion risk before direction mapping, producing side-balanced 5-10 trades/day candidates with lower DD?

## Hypothesis(가설)

Learn cost-adjusted path utility, adverse excursion, recovery/DD, and trade-density-aware action values directly for long, short, and abstain, rather than clustering states first and mapping actions later.

## Novelty Delta(신규성 차이)

- objective(목적함수): action-value/regret-first instead of unsupervised state-first
- label(라벨): counterfactual long/short/abstain path utility with adverse excursion penalties
- trade shape(거래 형태): side-symmetric risk-first action eligibility
- validation philosophy(검증 철학): risk/density/side-balance before PF-only selection
- runtime boundary(런타임 경계): runtime probe required in same packet if a runnable ONNX/EA/set claim appears

## Boundary(경계)

This scaffold(골격)는 pending-open(개방 대기) record(기록) only(전용)이다. No selected baseline(선택 기준선), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed(주장됨).
