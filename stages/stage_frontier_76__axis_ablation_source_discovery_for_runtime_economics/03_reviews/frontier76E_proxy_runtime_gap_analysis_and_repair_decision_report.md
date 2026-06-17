# Frontier76E Proxy/Runtime Gap Analysis and Repair Decision(F76E 프록시/런타임 간극 분석 및 수리 결정)

Updated(갱신): 2026-06-17T06:22:52Z

- status(상태): `gap_analysis_completed_lifecycle_repair_proxy_required_no_authority`
- judgment(판정): `runtime_probe_gap_traced_to_same_direction_hold_compression_no_authority`
- primary gap cause(주 간극 원인): `same_direction_hold_compression_after_signal_parity`
- next action(다음 행동): `frontier76F_lifecycle_aware_density_repair_proxy_v1`
- claim boundary(주장 경계): `gap_analysis_and_repair_decision_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Gap Rows(간극 행)

| split(분할) | signal(신호) | orders(주문) | trades(거래) | order/signal(주문/신호) | hold_same_direction(동방향 보유) | proxy tpd(프록시 일거래) | runtime tpd(런타임 일거래) | proxy PF(프록시 수익 팩터) | runtime PF(런타임 수익 팩터) | proxy DD%(프록시 손실폭) | runtime DD%(런타임 손실폭) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `validation` | `194` | `100` | `50` | `0.5155` | `144` | `1.0601092896174864` | `0.18382352941176472` | `1.594854315978897` | `2.08` | `6.4446875` | `6.6` |
| `oos` | `154` | `76` | `38` | `0.4935` | `116` | `1.1755725190839694` | `0.19487179487179487` | `1.6893374882536825` | `1.47` | `7.8916796875` | `10.04` |

## Repair Decision(수리 결정)

Action(행동): F76F에서 lifecycle-aware proxy(생명주기 인식 프록시)를 새로 실행한다.

Effect(효과): 독립 신호마다 거래로 계산하던 F76B proxy(프록시)를 런타임처럼 single-position max-hold12(단일 포지션 12봉 최대 보유) 구조로 다시 점수화한다.

Repair axes(수리 축):

- feature set/model/target(피처 묶음/모델/목표)은 F76B 축을 재사용한다.
- session/threshold(세션/임계값)는 density(거래 밀도)를 위해 다시 넓힌다.
- runtime claim(런타임 주장)은 만들지 않고, 의미 신호가 생기면 Grok review(Grok 검토) 뒤 MT5 Runtime Probe(MT5 런타임 탐침)로 보낸다.
