# Stage18 CatBoost Follow-up MT5 KPI Batch(18단계 캣부스트 후속 MT5 KPI 배치)

- judgment(판정): `inconclusive_catboost_followup_batch_mt5_kpi_completed`
- boundary(경계): `runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- completed runs(완료 실행): `10` / `10`
- total attempts(전체 시도): `48`
- total MT5 KPI records(전체 MT5 KPI 기록): `132`
- total normalized KPI records(전체 정규화 KPI 기록): `132`

| run(실행) | topic(주제) | strength(강도) | attempts/KPI(시도/KPI) | best OOS(최고 OOS) | worst OOS(최저 OOS) |
|---|---|---|---:|---:|---:|
| `run12D` | `volatility_regime_split` | `volatility_regime_split_visible` | `4/12` | `mt5_routed_low_vol_oos: 398.8` | `mt5_routed_high_vol_oos: 146.36` |
| `run12E` | `cash_session_timing_split` | `cash_session_timing_split_visible` | `6/18` | `mt5_routed_session_mid_oos: 279.66` | `mt5_routed_session_early_oos: 8.47` |
| `run12F` | `feature_driver_masking` | `feature_driver_masking_visible` | `6/18` | `mt5_routed_mask_historical_vol_20_oos: 290.15` | `mt5_routed_mask_minutes_from_cash_open_oos: 152.55` |
| `run12G` | `probability_confidence_band` | `probability_confidence_band_visible` | `4/12` | `mt5_routed_high_conf_oos: 157.15` | `mt5_routed_mid_conf_oos: -494.71` |
| `run12H` | `probability_margin_geometry` | `probability_margin_geometry_visible` | `4/12` | `mt5_routed_high_margin_oos: 203.64` | `mt5_routed_low_margin_oos: -51.8` |
| `run12I` | `long_bias_source_split` | `long_bias_source_split_visible` | `6/18` | `mt5_routed_long_high_vol_oos: 56.22` | `mt5_routed_long_other_oos: -2.73` |
| `run12J` | `tier_b_fallback_subtype_anatomy` | `tier_b_fallback_subtype_anatomy_visible` | `6/6` | `mt5_tier_b_b_core_or_outside_oos: 0.0` | `mt5_tier_b_b_macro_missing_oos: -94.57` |
| `run12K` | `trade_shape_hold_time_stress` | `trade_shape_hold_time_stress_visible` | `4/12` | `mt5_routed_hold_6_oos: 211.53` | `mt5_routed_hold_18_oos: 52.87` |
| `run12L` | `ordered_vs_plain_boosting_contrast` | `ordered_vs_plain_boosting_contrast_visible` | `2/6` | `mt5_routed_plain_control_oos: 413.75` | `mt5_routed_plain_control_oos: 413.75` |
| `run12M` | `threshold_surface_q70_q85_q95` | `threshold_surface_q70_q85_q95_visible` | `6/18` | `mt5_routed_q85_oos: 293.95` | `mt5_routed_q70_oos: 133.39` |

효과(effect, 효과): 10개 후속 주제를 각각 다른 질문으로 나눠 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) 모델 특성을 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 연결했다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
