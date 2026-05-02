# run04L_mlp_feature_sensitivity_probe_v1 결과 요약(Result Summary, 결과 요약)

- status(상태): `completed(완료)`
- judgment(판정): `inconclusive_feature_sensitivity_stable_top_drivers`
- recommendation(추천): `one_shallow_followup_on_top_feature_groups_if_staying_in_stage13`
- source run(원천 실행): `run04F_mlp_direction_asymmetry_runtime_probe_v1`
- boundary(경계): `feature_sensitivity_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

## Core Read(핵심 판독)

- top5 feature overlap(상위 5개 피처 겹침): `1.000`.
- top10 feature overlap(상위 10개 피처 겹침): `0.900`.
- validation top1(검증 1위): `hl_range` / group(그룹) `volatility_range` / l1 delta(L1 변화) `0.1538`.
- OOS top1(표본외 1위): `hl_range`.

효과(effect, 효과): 한 feature(피처)를 validation median(검증 중앙값)으로 가렸을 때 probability(확률) 표면이 얼마나 바뀌는지 본다. 새 학습이나 threshold search(기준값 탐색)는 없다.

## Top Features(상위 피처)

| split(분할) | rank(순위) | feature(피처) | group(그룹) | L1 delta(L1 변화) | decision flip(결정 뒤집힘) | signal drop(신호 소실) |
|---|---:|---|---|---:|---:|---:|
| validation_is | 1 | hl_range | volatility_range | 0.1538 | 0.0345 | 0.0295 |
| validation_is | 2 | minutes_from_cash_open | session | 0.1041 | 0.0361 | 0.0193 |
| validation_is | 3 | ema50_ema200_diff | trend_structure | 0.1031 | 0.0577 | 0.0161 |
| validation_is | 4 | hl_zscore_50 | volatility_range | 0.1017 | 0.0485 | 0.0093 |
| validation_is | 5 | atr_14 | volatility_range | 0.0965 | 0.0584 | 0.0474 |
| validation_is | 6 | ema20_ema50_diff | trend_structure | 0.0837 | 0.0331 | 0.0127 |
| validation_is | 7 | return_1_over_atr_14 | volatility_range | 0.0835 | 0.0387 | 0.0126 |
| validation_is | 8 | bb_position_20 | volatility_range | 0.0798 | 0.0356 | 0.0113 |
| validation_is | 9 | close_open_ratio | session | 0.0753 | 0.0400 | 0.0156 |
| validation_is | 10 | ema9_ema20_diff | trend_structure | 0.0715 | 0.0422 | 0.0163 |
| oos | 1 | hl_range | volatility_range | 0.1485 | 0.0353 | 0.0310 |
| oos | 2 | ema50_ema200_diff | trend_structure | 0.1229 | 0.0847 | 0.0196 |
| oos | 3 | atr_14 | volatility_range | 0.1100 | 0.0674 | 0.0554 |
| oos | 4 | hl_zscore_50 | volatility_range | 0.1082 | 0.0562 | 0.0108 |
| oos | 5 | minutes_from_cash_open | session | 0.1080 | 0.0421 | 0.0315 |
| oos | 6 | ema20_ema50_diff | trend_structure | 0.1005 | 0.0406 | 0.0154 |
| oos | 7 | ema9_ema20_diff | trend_structure | 0.0848 | 0.0564 | 0.0248 |
| oos | 8 | return_1_over_atr_14 | volatility_range | 0.0825 | 0.0431 | 0.0179 |
| oos | 9 | bb_position_20 | volatility_range | 0.0799 | 0.0380 | 0.0125 |
| oos | 10 | atr_50 | volatility_range | 0.0796 | 0.0392 | 0.0186 |
