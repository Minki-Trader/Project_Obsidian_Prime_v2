# run04G_mlp_direction_trade_shape_attribution_v1 Result Summary

- status(상태): `completed`
- judgment(판정): `inconclusive_trade_shape_attribution_completed`
- source run(원천 실행): `run04F_mlp_direction_asymmetry_runtime_probe_v1`
- boundary(경계): `trade_shape_attribution_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

## Trade Shape(거래 형태)

| view(보기) | split(분할) | trades(거래) | net(순수익) | avg win(평균 승) | avg loss(평균 패) | largest loss(최대 단일 손실) | avg hold bars(평균 보유 봉) | consec losses(연속 손실) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mt5_tier_a_long_only_validation_is | validation_is | 212 | -59.93 | 10.22 | -11.61 | -50.42 | 28.92 | 5 |
| mt5_tier_a_short_only_validation_is | validation_is | 47 | 8.36 | 10.16 | -10.24 | -62.83 | 50.49 | 5 |
| mt5_tier_a_both_no_fallback_validation_is | validation_is | 265 | -93.60 | 9.59 | -10.53 | -50.42 | 30.88 | 6 |
| mt5_tier_a_long_only_oos | oos | 159 | 83.36 | 8.79 | -8.73 | -45.71 | 15.69 | 6 |
| mt5_tier_a_short_only_oos | oos | 49 | 103.93 | 13.61 | -10.87 | -61.51 | 46.29 | 3 |
| mt5_tier_a_both_no_fallback_oos | oos | 208 | 56.67 | 9.33 | -9.51 | -56.84 | 22.23 | 7 |

## Damage Attribution(손상 기여도)

| split(분할) | separate net(분리 합산 순수익) | both net(양방향 순수익) | damage(손상) | trade delta(거래 수 차이) | DD delta(손실 차이) | driver(주된 원인) |
|---|---:|---:|---:|---:|---:|---|
| validation_is | -51.57 | -93.60 | -42.03 | 6 | -50.73 | small_trade_count_increase; long_side_deteriorated; drawdown_not_worse_than_long_only |
| oos | 187.29 | 56.67 | -130.62 | 0 | 83.27 | not_trade_count; short_side_flipped_under_both; drawdown_expanded_vs_components |

## Short OOS Fragility(숏 표본외 취약성)

- short-only OOS trades(숏 전용 표본외 거래): `49`
- net(순수익): `103.93`
- bootstrap total CI95(부트스트랩 총수익 95% 구간): `-138.35, 105.88, 328.45`
- positive bootstrap probability(부트스트랩 양수 확률): `0.808`
- positive months(양수 월): `4/7`

효과(effect, 효과): short-only OOS(숏 전용 표본외)는 좋은 단서지만, 49 trades(49개 거래)와 CI95(95% 구간) 하단 음수 때문에 alpha quality(알파 품질)로 올릴 수 없다.
