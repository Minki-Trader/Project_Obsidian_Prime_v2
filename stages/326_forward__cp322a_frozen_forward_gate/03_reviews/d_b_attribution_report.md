# D/B Attribution Report(D/B 귀속 보고서)

## Status(상태)

`blocked_forward_signal_handoff_missing`(전진 신호 인계 누락).

## Evidence(근거)

- frozen ONNX(고정 오닉스) input(입력): `run322b_route_signal`
- source feature files(원천 피처 파일): `24` old validation/OOS(과거 검증/표본외) files only.
- forward route signal files(전진 경로 신호 파일): `0`
- effect(효과): D source(D 원천), B source(B 원천), D+B attribution(D+B 귀속), long/short attribution(롱/숏 귀속)을 forward window(전진 구간)에서 계산하지 않았다.

## Boundary(경계)

새 데이터로 score threshold(점수 임계값), D/B rule(D/B 규칙), source priority(원천 우선순위)를 다시 맞추지 않았다.
