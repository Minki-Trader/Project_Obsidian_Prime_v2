# run04D_mlp_convergence_threshold_feasibility_probe_v1 Result Summary

- status(상태): `completed`
- judgment(판정): `inconclusive_convergence_threshold_feasibility_probe_completed`
- boundary(경계): `convergence_threshold_feasibility_probe_not_alpha_quality_not_promotion_not_runtime_authority`
- representative threshold(대표 임계값): `q90_m000`

## Convergence(수렴)

| scope(범위) | n_iter(반복) | max_iter(최대 반복) | loss first(초기 손실) | loss last(마지막 손실) | validation best(검증 최고) | label(라벨) |
|---|---:|---:|---:|---:|---:|---|
| Tier A | 44 | 180 | 1.13656 | 1.00743 | 0.457371 | early_stopping_triggered |
| Tier B | 91 | 180 | 1.13373 | 0.994472 | 0.476222 | early_stopping_triggered |

## Threshold Feasibility(임계값 가능성)

| scope(범위) | validation signals(검증 신호) | validation coverage(검증 비율) | OOS signals(표본외 신호) | OOS coverage(표본외 비율) | density label(밀도 라벨) |
|---|---:|---:|---:|---:|---|
| Tier A | 985 | 0.100061 | 660 | 0.0870253 | usable_density_band |
| Tier B | 1221 | 0.1 | 1041 | 0.120402 | usable_density_band |
| Tier A+B | 1222 | 0.100082 | 887 | 0.102591 | usable_density_band |

## MT5 No-Trade Handoff(MT5 무거래 인계)

| view(보기) | split(분할) | feature_ready(피처 준비) | model_ok(모델 정상) | trades(거래) |
|---|---:|---:|---:|---:|
| mt5_tier_a_convergence_threshold_proxy_validation_is | validation_is | 9844 | 9844 | 0 |
| mt5_tier_b_fallback_convergence_threshold_proxy_validation_is | validation_is | 2366 | 2366 | 0 |
| mt5_routed_total_validation_is | validation_is | 12210 | 12210 | 0 |
| mt5_tier_a_convergence_threshold_proxy_oos | oos | 7584 | 7584 | 0 |
| mt5_tier_b_fallback_convergence_threshold_proxy_oos | oos | 1062 | 1062 | 0 |
| mt5_routed_total_oos | oos | 8646 | 8646 | 0 |

효과(effect, 효과): 이번 실행(run, 실행)은 MLP(다층 퍼셉트론)의 수렴 곡선과 확률 임계값 밀도를 함께 본다.
alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
