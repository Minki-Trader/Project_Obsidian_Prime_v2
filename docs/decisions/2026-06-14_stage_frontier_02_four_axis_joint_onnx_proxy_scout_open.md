# Decision: Open Stage Frontier 02(결정: 전선 02단계 개방)

Date(날짜): 2026-06-14

Stage id(단계 ID): `stage_frontier_02__four_axis_joint_onnx_proxy_scout`

Run id(실행 ID): `frontier02A_proxy_score_spec_v1`

## Decision(결정)

Open Frontier 02(전선 02)를 four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색)로 연다.

Action(행동): Frontier 01(전선 01)의 proposal(제안) `density_quality_scout(밀도 품질 탐색)`을 그대로 쓰지 않고, Grok review(그록 검토) 지적을 반영해 `four_axis_joint_onnx_proxy_scout(네 축 동시 온엑스 프록시 탐색)`로 조정한다.

Effect(효과): 새 stage name(단계 이름)이 density-only(밀도 전용)처럼 읽히지 않고, 네 축 동시 목적을 명확히 한다.

## Evidence(근거)

- `docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md`
- `stages/stage_frontier_01__archive_synthesis_and_new_axis_lock/04_selected/next_frontier_proposal.md`
- `stages/stage_frontier_01__archive_synthesis_and_new_axis_lock/01_inputs/do_not_repeat_list.md`
- `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/01_inputs/proxy_score_plan.md`

## Claim Boundary(주장 경계)

This decision(이 결정)은 stage-open design(단계 개방 설계)만 닫는다.

Not claimed(주장 안 함): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성), selected candidate(선택 후보).
