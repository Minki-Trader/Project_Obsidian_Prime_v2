# F80 Input Boundary(F80 입력 경계)

Created(생성): 2026-06-17T12:05:00Z

## Source Inputs(원천 입력)

- F79 closeout report(F79 마감 보고서): `stages/stage_frontier_79__runtime_native_trade_shape_labeling_from_fill_path/03_reviews/stage_closeout_report.md`
- Current truth(현재 진실): `docs/workspace/workspace_state.yaml`, `docs/context/current_working_state.md`
- Task Force registry(태스크포스 등록부): `docs/agent_control/codex_task_force_registry.yaml`
- Frontier governance(전선 거버넌스): `docs/policies/frontier_governance.md`

## Boundary(경계)

Action(행동): F79(전선79)는 fixed prior evidence(고정 이전 근거)로만 읽는다.

Effect(효과): F80(전선80)이 F79/F79A(전선79/79A)를 다시 여는 작업으로 오해되지 않는다.

## Required Preflight(필수 사전 점검)

- data identity(데이터 정체성)
- time axis(시간축)
- closed-bar feature rule(확정봉 피처 규칙)
- feature order/hash(피처 순서/해시)
- label fill-path semantics(라벨 체결경로 의미)
- split boundary(분할 경계)
- Python/MT5 parity boundary(파이썬/MT5 동등성 경계)

Preflight(사전 점검)는 conclusion(결론)이 아니다. MT5 evidence(MT5 근거)는 Codex debate(코덱스 토론)로 대체하지 않는다.
