# run04E_mlp_q90_threshold_trading_runtime_probe_v1 Result Summary

- status(상태): `completed`
- judgment(판정): `inconclusive_q90_threshold_trading_runtime_probe_completed`
- source run(원천 실행): `run04D_mlp_convergence_threshold_feasibility_probe_v1`
- threshold(임계값): Tier A `0.5919602995462544`, Tier B fallback `0.4895868680769523`
- boundary(경계): `q90_threshold_trading_runtime_probe_not_alpha_quality_not_promotion_not_runtime_authority`

| view(보기) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실) | trades(거래) |
|---|---:|---:|---:|---:|---:|
| mt5_tier_a_q90_trading_validation_is | validation_is | -93.6 | 0.93 | 304.12 | 265 |
| mt5_tier_b_fallback_q90_trading_validation_is | validation_is | -153.5 | 0.78 | 284.11 | 76 |
| mt5_routed_total_validation_is | validation_is | -175.2 | 0.89 | 324.86 | 351 |
| mt5_tier_a_q90_trading_oos | oos | 56.67 | 1.06 | 248.58 | 208 |
| mt5_tier_b_fallback_q90_trading_oos | oos | -190.58 | 0.77 | 361.88 | 64 |
| mt5_routed_total_oos | oos | 182.18 | 1.16 | 196.89 | 285 |

효과(effect, 효과): RUN04D(실행 04D)의 q90 threshold(90분위 임계값)를 실제 거래 runtime_probe(런타임 탐침)에 연결했다.
alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
