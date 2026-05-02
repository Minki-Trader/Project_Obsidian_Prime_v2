# run04J_mlp_probability_geometry_probe_v1 결과 요약(Result Summary, 결과 요약)

- status(상태): `completed(완료)`
- judgment(판정): `inconclusive_probability_shape_stable_but_low_confidence_tail`
- recommendation(추천): `pivot_within_stage13_to_activation_or_feature_sensitivity`
- source run(원천 실행): `run04F_mlp_direction_asymmetry_runtime_probe_v1`
- boundary(경계): `probability_geometry_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

## 핵심 판독(Core Read, 핵심 판독)

- validation(검증) q90 signal(상위 10% 신호): `985` / share(비중) `0.100`.
- OOS(표본외) q90 signal(상위 10% 신호): `660` / share(비중) `0.087`.
- entropy mean(평균 엔트로피): validation(검증) `0.903`, OOS(표본외) `0.915`.
- margin mean(평균 마진): validation(검증) `0.202`, OOS(표본외) `0.194`.
- p_long mean delta(매수 확률 평균 차이, OOS-validation): `-0.014`.
- p_short mean delta(매도 확률 평균 차이, OOS-validation): `0.013`.

효과(effect, 효과): 확률 모양은 validation/OOS(검증/표본외) 사이에서 크게 무너지지는 않았지만, entropy(엔트로피)가 높고 margin(마진)이 낮아 q90 signal(상위 10% 신호)이 강한 확신보다는 얇은 tail(꼬리) 신호에 가깝다.

## q90 Clustering(q90 군집)

| split(분할) | signals(신호) | clusters(군집) | max cluster(최대 군집) | top5 cluster share(상위5 군집 비중) | max month share(최대 월 비중) |
|---|---:|---:|---:|---:|---:|
| validation_is | 985 | 359 | 63 | 0.228 | 0.508 |
| oos | 660 | 314 | 18 | 0.098 | 0.323 |

## Split Stability(분할 안정성)

| metric(지표) | validation mean(검증 평균) | OOS mean(표본외 평균) | delta(차이) | PSI(모집단 안정성 지수) |
|---|---:|---:|---:|---:|
| p_short | 0.279 | 0.292 | 0.013 | 0.017 |
| p_flat | 0.341 | 0.342 | 0.001 | 0.032 |
| p_long | 0.380 | 0.366 | -0.014 | 0.023 |
| entropy_norm | 0.903 | 0.915 | 0.012 | 0.075 |
| margin | 0.202 | 0.194 | -0.008 | 0.022 |

효과(effect, 효과): 이 결과는 probability geometry(확률 기하) 판독일 뿐이고, alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
