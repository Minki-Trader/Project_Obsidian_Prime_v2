# F81B MT5 Native Order Intent Cost Shape Proxy Scout Report(F81B MT5 원형 주문 의도 비용 형태 프록시 탐색 보고서)

Updated(갱신): 2026-06-18T03:40:10Z

- run id(실행 ID): `frontier81B_mt5_native_order_intent_cost_shape_proxy_scout_v1`
- parent run(부모 실행): `frontier81A_stage_open_mt5_native_order_intent_cost_shape_rebuild_v1`
- claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve_no_parity_only_economics`
- candidate rows(후보 행): `4800`
- scout clue count(탐색 단서 수): `1862`
- materialization candidate count(물질화 후보 수): `1013`
- meaningful signal count(의미 신호 수): `162`
- final-like reference count(최종 유사 참고 수): `0`
- best candidate(최선 후보): `f81b_04147` `smooth_density_cost_shape` val net/PF/DD/tpd/trades(검증 순손익/수익 팩터/손실폭/일 거래/거래) `145.2984/1.3886/3.3316/2.5387/688`, OOS(표본외) `128.0462/1.4583/2.1716/2.7423/532`

## Hypothesis Boundary(가설 경계)

Hypothesis(가설): F80 runtime gap(F80 런타임 간극)은 parity(동등성) 부족만이 아니라 spread pressure/exit efficiency/cost shape(스프레드 압력/청산 효율/비용 형태)를 label(라벨)에서 충분히 벌하지 못한 데서 생겼을 수 있다.

Effect(효과): 이번 run(실행)은 같은 threshold/filter/parameter(임계값/필터/파라미터) 반복이 아니라 MT5-native order intent(MT5 원형 주문 의도)와 cost shape(비용 형태)를 같이 압박한다.

## Signal Count Boundary(신호 수 경계)

Signal count(신호 수)는 diagnostic only(진단 전용)다. Effect(효과): raw signal count(원시 신호 수)나 lifecycle trade count(생명주기 거래 수)가 많아도 MT5 economics(MT5 경제성), runtime authority(런타임 권위), or selected baseline(선택 기준선)을 만들지 않는다.

## Top Candidates(상위 후보)

| candidate(후보) | surface(표면) | model(모델) | feature(피처) | regime/risk/cooldown(장세/위험/쿨다운) | val net/PF/DD/tpd/trades(검증) | OOS net/PF/DD/tpd/trades(표본외) | scout/material/meaningful/final-like(탐색/물질/의미/최종유사) |
|---|---|---|---|---|---:|---:|---:|
| `f81b_04147` | `smooth_density_cost_shape` | `histgbm_cost_shape_shallow` | `trend_order_intent` | `cash_open/none/0` | `145.2984/1.3886/3.3316/2.5387/688` | `128.0462/1.4583/2.1716/2.7423/532` | `1/1/1/0` |
| `f81b_03937` | `smooth_density_cost_shape` | `histgbm_cost_shape_shallow` | `runtime_fill_context` | `cash_open/none/0` | `158.1525/1.4877/4.0460/2.2731/616` | `121.1756/1.4312/2.4555/2.7371/531` | `1/1/1/0` |
| `f81b_04297` | `smooth_density_cost_shape` | `histgbm_cost_shape_shallow` | `compact_exportable_28` | `cash_open/none/0` | `158.1525/1.4877/4.0460/2.2731/616` | `121.1756/1.4312/2.4555/2.7371/531` | `1/1/1/0` |
| `f81b_01107` | `order_intent_exit_efficiency` | `extra_trees_d6_l160` | `price_vol_session` | `trend/liquidity_release/0` | `131.0659/1.4029/4.0842/2.6015/705` | `120.8997/1.3961/2.0510/3.4536/670` | `1/1/1/0` |
| `f81b_03083` | `intent_cost_asymmetry` | `histgbm_cost_shape_shallow` | `price_vol_session` | `high_vol/order_intent_guard/0` | `254.5852/1.4949/3.3639/3.3137/898` | `269.2933/1.6574/2.5548/3.9021/757` | `1/1/1/0` |
| `f81b_03065` | `intent_cost_asymmetry` | `histgbm_cost_shape_shallow` | `price_vol_session` | `all/order_intent_guard/0` | `247.0626/1.4523/3.9458/3.4760/942` | `262.6223/1.5740/2.5548/4.2629/827` | `1/1/1/0` |
| `f81b_03063` | `intent_cost_asymmetry` | `histgbm_cost_shape_shallow` | `price_vol_session` | `all/liquidity_release/0` | `253.9110/1.5327/3.3639/3.1033/841` | `209.5828/1.5501/3.3639/3.5258/684` | `1/1/1/0` |
| `f81b_03081` | `intent_cost_asymmetry` | `histgbm_cost_shape_shallow` | `price_vol_session` | `high_vol/liquidity_release/0` | `253.9110/1.5327/3.3639/3.1033/841` | `209.5828/1.5501/3.3639/3.5258/684` | `1/1/1/0` |
| `f81b_01133` | `order_intent_exit_efficiency` | `extra_trees_d6_l160` | `price_vol_session` | `high_vol/order_intent_guard/0` | `192.7164/1.4863/2.7873/3.2509/881` | `201.2086/1.6600/2.7039/3.7165/721` | `1/1/1/0` |
| `f81b_04085` | `smooth_density_cost_shape` | `extra_trees_d6_l160` | `trend_order_intent` | `all/order_intent_guard/0` | `365.6603/1.3837/4.6306/6.4576/1750` | `275.9057/1.3983/2.5761/6.6546/1291` | `1/1/1/0` |
| `f81b_01113` | `order_intent_exit_efficiency` | `extra_trees_d6_l160` | `price_vol_session` | `all/liquidity_release/0` | `194.6813/1.5213/3.0262/3.0959/839` | `184.2296/1.6390/2.5406/3.4948/678` | `1/1/1/0` |
| `f81b_01131` | `order_intent_exit_efficiency` | `extra_trees_d6_l160` | `price_vol_session` | `high_vol/liquidity_release/0` | `194.6813/1.5213/3.0262/3.0959/839` | `184.2296/1.6390/2.5406/3.4948/678` | `1/1/1/0` |

## Tier Record(티어 기록)

Tier A separate(티어 A 분리)는 proxy scout(프록시 탐색)로 기록했다. Tier B separate(티어 B 분리)는 `missing_required(필수 누락)`, Tier A+B combined(티어 A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`로 기록했다.

## Next Boundary(다음 경계)

Next run(다음 실행): `frontier81C_mt5_runtime_materialization_v1`.

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), parity-only economics(동등성 단독 경제성)를 만들지 않는다.
