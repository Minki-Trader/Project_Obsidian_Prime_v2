# F81D Proxy Runtime Gap Attribution(F81D 프록시/런타임 간극 귀속)

Updated(갱신): 2026-06-18T04:01:42Z

- run id(실행 ID): `frontier81D_proxy_runtime_gap_attribution_v1`
- parent run(부모 실행): `frontier81C_mt5_runtime_materialization_v1`
- target(대상): `f81b_01107` / `extra_trees_d6_l160`
- status(상태): `f81d_runtime_gap_attributed_negative_runtime_economics_no_authority`
- judgment(판정): `signal_feature_onnx_parity_passed_runtime_economics_failed_repair_or_rotation_required_no_authority`
- claim boundary(주장 경계): `gap_attribution_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Observed Change(관찰 변화)

Action(행동): F81C MT5 runtime materialization(F81C MT5 런타임 물질화)을 F81B proxy KPI(F81B 프록시 핵심 성과 지표)와 split(구간)별로 비교했다.

Effect(효과): signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 원인에서 제외하고, runtime economics(런타임 경제성) 붕괴를 다음 F81E 수리 또는 회전 입력으로 고정한다.

| split(구간) | proxy net/PF/DD(프록시 순손익/수익 팩터/손실폭) | MT5 net/PF/DD(MT5 순손익/수익 팩터/손실폭) | signal diff(신호 차이) | fill rate(체결률) | win rate proxy/runtime(승률 프록시/런타임) |
|---|---:|---:|---:|---:|---:|
| validation(검증) | `131.0659/1.4029/4.0842` | `-147.0200/0.6800/30.9800` | `0` | `0.9929` | `0.4340/0.2410` |
| OOS(표본외) | `120.8997/1.3961/2.0510` | `-115.7100/0.7300/23.7200` | `0` | `1.0000` | `0.4164/0.2537` |

## Attribution(귀속)

Primary driver(주 원인): runtime deal economics after parity(동등성 이후 런타임 거래 경제성).

Not primary drivers(주 원인 아님): feature readiness(피처 준비), signal count(신호 수), ONNX handoff(온엑스 인계).

Trade shape(거래 형태): long only(롱 전용), validation trades `697`, OOS trades `670`, OOS trades/day(표본외 일 거래) `3.4359`.

Next probe(다음 탐침): `F81E should do capped repair or rotation: either deal-level entry/exit PnL reconciliation and MT5-realized label rebuild, or rotate away from this one-sided long cost-shape branch.`

Forbidden claims(금지 주장): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
