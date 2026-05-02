# run04F_mlp_direction_asymmetry_runtime_probe_v1 Result Summary

- status(상태): `completed`
- judgment(판정): `inconclusive_direction_asymmetry_runtime_probe_completed`
- source run(원천 실행): `run04E_mlp_q90_threshold_trading_runtime_probe_v1`
- threshold(임계값): Tier A `0.5919602995462544`
- boundary(경계): `direction_asymmetry_runtime_probe_not_alpha_quality_not_promotion_not_runtime_authority`

| view(보기) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실) | trades(거래) | long/short(롱/숏) |
|---|---:|---:|---:|---:|---:|---:|
| mt5_tier_a_long_only_validation_is | validation_is | -59.93 | 0.95 | 354.85 | 212 | 212/0 |
| mt5_tier_a_short_only_validation_is | validation_is | 8.36 | 1.04 | 170.02 | 47 | 0/47 |
| mt5_tier_a_both_no_fallback_validation_is | validation_is | -93.6 | 0.93 | 304.12 | 265 | 216/49 |
| mt5_tier_a_long_only_oos | oos | 83.36 | 1.13 | 165.31 | 159 | 159/0 |
| mt5_tier_a_short_only_oos | oos | 103.93 | 1.42 | 100.09 | 49 | 0/49 |
| mt5_tier_a_both_no_fallback_oos | oos | 56.67 | 1.06 | 248.58 | 208 | 159/49 |

효과(effect, 효과): RUN04E(실행 04E)의 q90 threshold(90분위 임계값)를 Tier A(티어 A) 방향별로 분해했다.
Tier B(티어 B)와 routed total(라우팅 전체)은 이번 주장 범위 밖(out_of_scope_by_claim, 주장 범위 밖)이다.
alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
