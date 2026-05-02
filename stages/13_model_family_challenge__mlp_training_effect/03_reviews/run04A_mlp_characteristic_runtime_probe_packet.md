# run04A_mlp_characteristic_runtime_probe_v1 Result Summary

- status(상태): `completed`
- judgment(판정): `inconclusive_mlp_characteristic_runtime_probe_completed`
- selected variant(선택 변형): `v02_wide_relu_l2`
- boundary(경계): `runtime_probe_mlp_characteristic_not_alpha_quality_not_promotion_not_runtime_authority`

| view(보기) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실) | trades(거래 수) |
|---|---:|---:|---:|---:|---:|
| mt5_tier_a_only_validation_is | validation_is | -276.82 | 0.83 | 334.65 | 307 |
| mt5_tier_b_fallback_only_validation_is | validation_is | -78.22 | 0.41 | 116.82 | 19 |
| mt5_routed_total_validation_is | validation_is | -250.67 | 0.84 | 316.89 | 325 |
| mt5_tier_a_only_oos | oos | 321.54 | 1.38 | 87.79 | 229 |
| mt5_tier_b_fallback_only_oos | oos | -127.58 | 0.43 | 152.94 | 19 |
| mt5_routed_total_oos | oos | 414.82 | 1.49 | 84.81 | 247 |

효과(effect, 효과): 이 결과는 MLP model(다층 퍼셉트론 모델)의 얕은 runtime_probe(런타임 탐침)이다.
alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 만들지 않는다.
