# Stage17 RUN11E XGBoost Feature Driver Saturation(17단계 실행11E XGBoost 피처 동인 포화)

- judgment(판정): `closed_inconclusive_xgboost_regularized_boosting_characteristics_exhausted`
- recommendation(권고): `close_stage17_no_new_feature_driver_after_run11E`
- selected variant(선택 변형): `v03_depth4_l1_l2_slow`
- top3 features(상위 3개 피처): `['hl_range', 'historical_vol_20', 'is_first_30m_after_open']`
- min top10 overlap(최소 상위10 겹침): `1.0`
- new feature driver visible(새 피처 동인 보임): `False`
- boundary(경계): `xgboost_feature_driver_saturation_closeout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| source run(원천 실행) | score(점수) | threshold(임계값) | top10 gain share(상위10 gain 비중) |
|---|---:|---:|---:|
| `run11A_xgb_regularized_boosting_characteristic_scout_v1` | `0.9542046856635382` | `0.4672216027975082` | `0.3446187256324587` |
| `run11B_xgb_threshold_q80_frequency_pressure_closeout_v1` | `0.7329091620874055` | `0.4302987039089203` | `0.3446187256324587` |
| `run11C_xgb_q80_direction_asymmetry_probe_v1` | `0.7329091620874055` | `0.4302987039089203` | `0.3446187256324587` |

효과(effect, 효과): run11A부터 run11D까지 나온 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) 특성 단서를 feature driver(피처 동인) 관점에서 다시 봤고, 새 피처 축이 더 나오지 않아 Stage17(17단계)을 closeout(마감)한다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
