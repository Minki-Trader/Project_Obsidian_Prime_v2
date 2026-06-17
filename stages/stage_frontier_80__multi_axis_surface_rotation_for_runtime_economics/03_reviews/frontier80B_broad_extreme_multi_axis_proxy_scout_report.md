# F80B Broad Extreme Multi-Axis Proxy Scout Report(F80B 넓은/극단 다축 프록시 탐색 보고서)

Updated(갱신): 2026-06-17T15:02:14Z

- run id(실행 ID): `frontier80B_broad_extreme_multi_axis_proxy_scout_v1`
- parent run(부모 실행): `frontier80A_stage_open_multi_axis_surface_rotation_v1`
- claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve_no_parity_only_economics`
- candidate rows(후보 행): `50400`
- scout clue count(탐색 단서 수): `2372`
- materialization candidate count(물질화 후보 수): `519`
- meaningful signal count(의미 신호 수): `21`
- final-like reference count(최종 유사 참고 수): `0`
- best candidate(최선 후보): `f80b_11473` `order_intent_swing` val net/PF/DD/tpd/trades(검증 순손익/수익 팩터/손실폭/일 거래/거래) `120.8359/1.3546/4.0572/2.0849/565`, OOS(표본외) `128.8703/1.4007/3.3248/2.8144/546`

## Signal Count Boundary(신호 수 경계)

Signal count(신호 수)는 diagnostic only(진단 전용)다. Effect(효과): raw signal count(원시 신호 수)나 lifecycle trade count(생명주기 거래 수)가 많아도 MT5 economics(MT5 경제성), runtime authority(런타임 권위), or selected baseline(선택 기준선)을 만들지 않는다.

## Top Candidates(상위 후보)

| candidate(후보) | surface(표면) | model(모델) | feature(피처) | regime/risk/cooldown(장세/위험/쿨다운) | val net/PF/DD/tpd/trades(검증) | OOS net/PF/DD/tpd/trades(표본외) | scout/material/meaningful/final-like(탐색/물질/의미/최종유사) |
|---|---|---|---|---|---:|---:|---:|
| `f80b_11473` | `order_intent_swing` | `histgbm_shallow` | `runtime_fill_context` | `high_vol/order_intent_guard/0` | `120.8359/1.3546/4.0572/2.0849/565` | `128.8703/1.4007/3.3248/2.8144/546` | `1/1/1/0` |
| `f80b_15073` | `order_intent_swing` | `histgbm_shallow` | `compact_exportable_28` | `high_vol/order_intent_guard/0` | `120.8359/1.3546/4.0572/2.0849/565` | `128.8703/1.4007/3.3248/2.8144/546` | `1/1/1/0` |
| `f80b_11410` | `order_intent_swing` | `histgbm_shallow` | `runtime_fill_context` | `all/liquidity_release/0` | `127.5955/1.4067/4.0572/1.9520/529` | `114.8630/1.3903/3.3248/2.5670/498` | `1/1/1/0` |
| `f80b_11470` | `order_intent_swing` | `histgbm_shallow` | `runtime_fill_context` | `high_vol/liquidity_release/0` | `127.5955/1.4067/4.0572/1.9520/529` | `114.8630/1.3903/3.3248/2.5670/498` | `1/1/1/0` |
| `f80b_15010` | `order_intent_swing` | `histgbm_shallow` | `compact_exportable_28` | `all/liquidity_release/0` | `127.5955/1.4067/4.0572/1.9520/529` | `114.8630/1.3903/3.3248/2.5670/498` | `1/1/1/0` |
| `f80b_15070` | `order_intent_swing` | `histgbm_shallow` | `compact_exportable_28` | `high_vol/liquidity_release/0` | `127.5955/1.4067/4.0572/1.9520/529` | `114.8630/1.3903/3.3248/2.5670/498` | `1/1/1/0` |
| `f80b_12193` | `order_intent_swing` | `histgbm_shallow` | `price_vol_session` | `high_vol/order_intent_guard/0` | `120.7276/1.4342/3.0942/1.7454/473` | `83.6443/1.3717/3.2468/1.9536/379` | `1/1/1/0` |
| `f80b_11395` | `order_intent_swing` | `histgbm_shallow` | `runtime_fill_context` | `chop/liquidity_release/0` | `92.4878/1.4477/2.2035/1.3026/353` | `66.7806/1.4484/4.1410/1.3196/256` | `1/1/1/0` |
| `f80b_11398` | `order_intent_swing` | `histgbm_shallow` | `runtime_fill_context` | `chop/order_intent_guard/0` | `92.4878/1.4477/2.2035/1.3026/353` | `66.7806/1.4484/4.1410/1.3196/256` | `1/1/1/0` |
| `f80b_14995` | `order_intent_swing` | `histgbm_shallow` | `compact_exportable_28` | `chop/liquidity_release/0` | `92.4878/1.4477/2.2035/1.3026/353` | `66.7806/1.4484/4.1410/1.3196/256` | `1/1/1/0` |
| `f80b_14998` | `order_intent_swing` | `histgbm_shallow` | `compact_exportable_28` | `chop/order_intent_guard/0` | `92.4878/1.4477/2.2035/1.3026/353` | `66.7806/1.4484/4.1410/1.3196/256` | `1/1/1/0` |
| `f80b_13481` | `order_intent_swing` | `histgbm_shallow` | `micro_reversal` | `cash_mid/liquidity_release/4` | `99.6502/1.4954/3.3181/1.2878/349` | `60.1851/1.3729/2.8813/1.4021/272` | `1/1/1/0` |

## Tier Record(티어 기록)

Tier A separate(티어 A 분리)는 proxy scout(프록시 탐색)로 기록했다. Tier B separate(티어 B 분리)는 `missing_required(필수 누락)`, Tier A+B combined(티어 A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`로 기록했다.

## Next Boundary(다음 경계)

Next run(다음 실행): `frontier80C_wfo_aware_surface_selection_v1`.

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), parity-only economics(동등성 단독 경제성)를 만들지 않는다.
