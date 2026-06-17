# F80E Proxy/Runtime Gap Attribution(F80E 프록시/런타임 간극 귀속)

Updated(갱신): 2026-06-17T15:41:05Z

- run id(실행 ID): `frontier80E_proxy_runtime_gap_attribution_v1`
- target(대상): `f80b_13315` / `extra_trees_d6_l120`
- claim boundary(주장 경계): `stage_closeout_runtime_probe_quality_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Action(행동)

F80D(전선80D)의 MT5 runtime probe(MT5 런타임 탐침)를 F80B/F80C proxy(프록시) 기대와 비교했다.

Effect(효과): signal count(신호 수), feature readiness(피처 준비), ONNX handoff(온엑스 인계)가 맞아도 MT5 economics(MT5 경제성)가 깨질 수 있음을 F80의 closeout(마감) 근거로 고정한다.

## KPI Gap(KPI 간극)

| metric(지표) | proxy validation(프록시 검증) | MT5 validation(MT5 검증) | runtime - proxy(런타임-프록시) |
|---|---:|---:|---:|
| net profit(순손익) | `89.72893373785989` | `-14.61` | `-104.33893373785989` |
| profit factor(수익 팩터) | `1.3786494266857832` | `0.95` | `-0.4286494266857832` |
| DD %(손실폭 %) | `4.056337901607913` | `6.09` | `2.033662098392087` |
| signal count(신호 수) | `396.0` | `396.0` | `0.0` |

## Attribution(귀속)

Primary cause(주 원인): `runtime_order_economics_after_parity(동등성 이후 런타임 주문 경제성)`.

Not the cause(원인 아님): feature readiness(피처 준비), signal count(신호 수), ONNX handoff(온엑스 인계).

Boundary(경계): This is runtime probe quality closeout material(런타임 탐침 품질 마감 근거) only.
