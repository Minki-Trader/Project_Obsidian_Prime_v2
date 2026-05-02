# run04C_mlp_activation_runtime_probe_v1 Result Summary

- status(상태): `completed`
- judgment(판정): `inconclusive_activation_runtime_probe_completed`
- boundary(경계): `activation_runtime_probe_not_alpha_quality_not_promotion_not_runtime_authority`
- no_trade_threshold(무거래 임계값): `1.01`

## Activation Behavior(활성화 동작)

| scope(범위) | split(분할) | dead units(죽은 유닛) | near-dead units(준죽은 유닛) | zero rate mean(0 비율 평균) | active units mean(활성 유닛 평균) |
|---|---:|---:|---:|---:|---:|
| Tier A validation | validation | 0 | 0 | 0.5114520901056481 | 31.26706623323852 |
| Tier A OOS | oos | 0 | 0 | 0.5138490572257384 | 31.113660337552744 |
| Tier B validation | validation | 0 | 0 | 0.5191620597870599 | 30.773628173628175 |
| Tier B OOS | oos | 0 | 0 | 0.5263651544066621 | 30.31263011797363 |

## MT5 Runtime Proxy(MT5 런타임 대리값)

| view(보기) | split(분할) | feature_ready(피처 준비) | model_ok(모델 정상) | trades(거래) |
|---|---:|---:|---:|---:|
| mt5_tier_a_activation_proxy_validation_is | validation_is | 9844 | 9844 | 0 |
| mt5_tier_b_fallback_activation_proxy_validation_is | validation_is | 2366 | 2366 | 0 |
| mt5_routed_total_validation_is | validation_is | 12210 | 12210 | 0 |
| mt5_tier_a_activation_proxy_oos | oos | 7584 | 7584 | 0 |
| mt5_tier_b_fallback_activation_proxy_oos | oos | 1062 | 1062 | 0 |
| mt5_routed_total_oos | oos | 8646 | 8646 | 0 |

효과(effect, 효과): 이번 실행은 MLP(다층 퍼셉트론)의 hidden activation(은닉 활성화) 구조와 MT5(메타트레이더5) probability proxy(확률 대리값) 인계만 확인한다.
alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
