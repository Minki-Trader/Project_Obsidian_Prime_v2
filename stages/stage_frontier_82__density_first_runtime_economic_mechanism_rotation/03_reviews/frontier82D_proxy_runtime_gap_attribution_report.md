# F82D Proxy Runtime Gap Attribution(F82D 프록시/런타임 간극 귀속)

Updated(갱신): 2026-06-18T06:00:05Z

- run id(실행 ID): `frontier82D_proxy_runtime_gap_attribution_v1`
- parent run(부모 실행): `frontier82C_mt5_runtime_materialization_v1`
- target(대상): `f82b_07295` / `extra_trees_d7_l120`
- status(상태): `f82d_runtime_gap_attributed_negative_runtime_economics_no_authority`
- judgment(판정): `signal_feature_onnx_parity_passed_runtime_economics_failed_capped_repair_or_rotation_required_no_authority`
- claim boundary(주장 경계): `gap_attribution_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Observed Change(관찰 변화)

Action(행동): F82C MT5 runtime materialization(F82C MT5 런타임 물질화)을 F82B proxy KPI(F82B 프록시 핵심 성과 지표)와 split(구간)별로 비교했다.

Effect(효과): signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 원인에서 제외하고, runtime economics(런타임 경제성) 붕괴를 다음 F82E 수리 또는 회전 입력으로 고정한다.

| split(구간) | proxy net/PF/DD(프록시 순손익/수익 팩터/손실폭) | MT5 net/PF/DD(MT5 순손익/수익 팩터/손실폭) | signal diff(신호 차이) | fill rate(체결률) | win rate proxy/runtime(승률 프록시/런타임) |
|---|---:|---:|---:|---:|---:|
| validation(검증) | `234.9537/1.2529/3.9148` | `-278.9800/0.7800/57.0000` | `0` | `0.9944` | `0.4803/0.3281` |
| OOS(표본외) | `190.9750/1.3121/2.4484` | `-55.2100/0.9300/20.3600` | `0` | `0.9993` | `0.4761/0.3677` |

## Attribution(귀속)

Primary driver(주 원인): runtime deal economics after parity(동등성 이후 런타임 거래 경제성).

Not primary drivers(주 원인 아님): feature readiness(피처 준비), signal count(신호 수), ONNX handoff(온엑스 인계).

Trade shape(거래 형태): long only(롱 전용), validation trades `1963`, OOS trades `1338`, OOS trades/day(표본외 일 거래) `6.8615`.

Next probe(다음 탐침): `F82E should decide capped repair or rotation: either deal-level entry/exit PnL reconciliation plus MT5-realized label rebuild, or rotate away from this one-sided long density branch.`

Forbidden claims(금지 주장): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
