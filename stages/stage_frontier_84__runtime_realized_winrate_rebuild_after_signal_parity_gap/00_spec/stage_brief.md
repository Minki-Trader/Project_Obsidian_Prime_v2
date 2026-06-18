# F84 Stage Brief(F84 단계 개요)

Stage ID(단계 ID): `stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap`

Prepared by(작성 실행): `frontier83G_runtime_realized_outcome_repair_or_rotation_decision_v1`

Next run(다음 실행): `frontier84A_stage_open_runtime_realized_winrate_rebuild_after_signal_parity_gap_v1`

Status(상태): `handoff_scaffold_not_opened(인계 뼈대, 아직 개방 아님)`

## Question(질문)

Can runtime-realized win/loss and stop-touch/fill-path labels(런타임 실현 승패 및 손절·익절 터치/체결 경로 라벨)이 signal parity after proxy success(프록시 성공 뒤 신호 동등성)에서도 actual MT5 win rate(실제 MT5 승률)를 보존하는 exportable ONNX candidate(내보내기 가능 온엑스 후보)를 만들 수 있는가?

## Action And Effect(행동과 효과)

Action(행동): F84는 F83 same-surface threshold/filter repair(F83 동일 표면 임계값/필터 수리)를 반복하지 않고 runtime-realized win/loss and stop-touch/fill-path label(런타임 실현 승패 및 손절·익절 터치/체결 경로 라벨)을 새 hypothesis lifecycle(가설 생명주기)로 연다.

Effect(효과): F83F의 primary cause(주 원인)인 runtime win-rate erosion(런타임 승률 침식)을 다음 모델 학습 목표로 직접 겨냥한다.

## Seed Axes(씨앗 축)

- Use F83E/F83F runtime deal outcome as teacher surface(F83E/F83F 런타임 거래 결과를 교사 표면으로 사용)
- Train label around realized win/loss, stop-touch, and fill path(실현 승패/손절·익절 터치/체결 경로 중심 라벨 학습)
- Segment by session/regime before threshold search(임계값 탐색 전 세션/장세 분할)
- Require MT5 materialization once a meaningful candidate appears(의미 있는 후보가 나오면 MT5 물질화 필수)

## Boundary(경계)

This file(이 파일)은 F84 open evidence(F84 개방 근거)가 아니라 handoff scaffold(인계 뼈대)다. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
