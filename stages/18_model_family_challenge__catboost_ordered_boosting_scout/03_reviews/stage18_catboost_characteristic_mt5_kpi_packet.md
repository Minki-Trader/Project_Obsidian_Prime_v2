# Stage18 CatBoost Characteristic MT5 KPI Aggregate(18단계 캣부스트 특성 MT5 핵심 성과 지표 종합)

- judgment(판정): `inconclusive_catboost_model_characteristic_mt5_kpi_completed`
- recommendation(권고): `keep_stage18_open_for_catboost_attribution_or_regime_probe`
- boundary(경계): `runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| run(실행) | topic(주제) | strength(강도) | validation net/PF/trades(검증 순수익/수익 팩터/거래) | OOS net/PF/trades(표본외 순수익/수익 팩터/거래) |
|---|---|---|---:|---:|
| `run12A` | `ordered_boosting_probability_shape` | `ordered_probability_shape_visible` | `206.56 / 1.27 / 146` | `203.52 / 1.49 / 99` |
| `run12B` | `q80_signal_density_pressure` | `q80_density_visible_risk_warning` | `-496.86 / 0.56 / 160` | `298.27 / 1.3 / 222` |
| `run12C` | `direction_balance_long_short_split` | `direction_balance_or_asymmetry_visible` | `long 4.15 / 1.0 / 231; short -178.55 / 0.51 / 45` | `long 153.1 / 1.18 / 180; short 91.63 / 1.51 / 41` |

- visible topic count(보이는 주제 수): `3`
- run12B density ratio vs run12A(run12A 대비 run12B 밀도 비율): `2.242424242424242`
- risk warning runs(위험 경고 실행): `['run12A', 'run12B']`

효과(effect, 효과): Stage18(18단계)는 CatBoost(캣부스트)의 ordered boosting(순서 부스팅), q80 signal density(q80 신호 밀도), direction balance(방향 균형)를 MT5(`MetaTrader 5`, 메타트레이더5)까지 확인했다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
