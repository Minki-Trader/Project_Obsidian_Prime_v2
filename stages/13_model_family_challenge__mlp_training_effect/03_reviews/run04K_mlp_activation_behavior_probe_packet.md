# run04K_mlp_activation_behavior_probe_v1 결과 요약(Result Summary, 결과 요약)

- status(상태): `completed(완료)`
- judgment(판정): `inconclusive_activation_distributed_and_split_stable`
- recommendation(추천): `move_to_feature_sensitivity_or_new_stage13_topic`
- source run(원천 실행): `run04F_mlp_direction_asymmetry_runtime_probe_v1`
- boundary(경계): `activation_behavior_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

## Core Read(핵심 판독)

- validation(검증) mean active units(평균 활성 유닛): `32.86` / 64.
- OOS(표본외) mean active units(평균 활성 유닛): `32.76` / 64.
- dead units(죽은 유닛): validation(검증) `0`, OOS(표본외) `0`.
- top10 activation share(상위 10개 활성 비중): validation(검증) `0.247`, OOS(표본외) `0.271`.
- top10 unit overlap(상위 10개 유닛 겹침): `0.800`.

효과(effect, 효과): hidden activation(은닉층 활성화)은 한두 유닛에 과도하게 몰린 붕괴라기보다 넓게 퍼진 구조다.

## Signal Contrast(신호 대비)

| split(분할) | group(그룹) | rows(행) | active units(활성 유닛) | activation L1(활성 L1) | entropy(엔트로피) | margin(마진) |
|---|---|---:|---:|---:|---:|---:|
| validation_is | flat | 8859 | 33.246 | 25.326 | 0.933 | 0.164 |
| validation_is | any_signal | 985 | 29.429 | 50.413 | 0.630 | 0.543 |
| validation_is | long_signal | 903 | 29.415 | 50.899 | 0.617 | 0.554 |
| validation_is | short_signal | 82 | 29.585 | 45.060 | 0.765 | 0.423 |
| oos | flat | 6924 | 33.051 | 26.327 | 0.930 | 0.170 |
| oos | any_signal | 660 | 29.658 | 38.468 | 0.750 | 0.443 |
| oos | long_signal | 557 | 29.603 | 36.216 | 0.751 | 0.448 |
| oos | short_signal | 103 | 29.951 | 50.649 | 0.745 | 0.417 |
