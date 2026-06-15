# Frontier06 Runtime Probe Backfill(전선06 런타임 탐침 소급)

Updated(갱신): 2026-06-15T14:16:13Z

Status(상태): `runtime_probe_backfill_observation_no_authority`

Judgment(판정): `runtime_probe_observation(런타임 탐침 관찰)`

Action(행동): existing candidate ONNX(기존 후보 온엑스)를 MT5 runtime probe(MT5 런타임 탐침)로 실행했습니다.

Effect(효과): proxy-only gap(프록시 전용 공백)을 실제 tester KPI(테스터 지표) 관찰로 보강하되 authority(권위)는 만들지 않습니다.

| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | signal diff(신호 차이) |
|---|---:|---:|---:|---:|---:|---:|
| `validation_is` | `completed` | `completed` | 1.12 | 36.15 | 415 | 0 |
| `oos` | `completed` | `completed` | 0.89 | 61.28 | 312 | 0 |

Candidate(후보): `rf_depth5_leaf80_balanced_argmax__directional_margin__flat1p01__margin0p00__d4p0`
Decision mode(결정 방식): `edge_margin`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
