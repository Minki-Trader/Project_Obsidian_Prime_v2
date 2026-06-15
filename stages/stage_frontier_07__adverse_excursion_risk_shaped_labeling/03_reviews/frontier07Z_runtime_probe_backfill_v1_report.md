# Frontier07 Runtime Probe Backfill(전선07 런타임 탐침 소급)

Updated(갱신): 2026-06-15T14:16:13Z

Status(상태): `runtime_probe_backfill_observation_no_authority`

Judgment(판정): `runtime_probe_observation(런타임 탐침 관찰)`

Action(행동): existing candidate ONNX(기존 후보 온엑스)를 MT5 runtime probe(MT5 런타임 탐침)로 실행했습니다.

Effect(효과): proxy-only gap(프록시 전용 공백)을 실제 tester KPI(테스터 지표) 관찰로 보강하되 authority(권위)는 만들지 않습니다.

| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | signal diff(신호 차이) |
|---|---:|---:|---:|---:|---:|---:|
| `validation_is` | `completed` | `completed` | 0.99 | 55.93 | 272 | 0 |
| `oos` | `completed` | `completed` | 0.97 | 30.32 | 165 | 0 |

Candidate(후보): `f07b_time_to_adverse_penalty_v1_lt0p90_st0p90_lc0p60_sc0p60_q90__v02_rw01`
Decision mode(결정 방식): `argmax`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
