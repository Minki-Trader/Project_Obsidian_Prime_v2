# Stage17 RUN11D XGBoost Trade Shape Attribution(17단계 실행11D XGBoost 거래 모양 귀속)

- source run(원천 실행): `run11C_xgb_q80_direction_asymmetry_probe_v1`
- judgment(판정): `inconclusive_xgboost_trade_shape_attribution_completed`
- external verification(외부 검증): `completed_reused_run11C_mt5_evidence`
- characteristic strength(특성 강도): `xgboost_trade_shape_probability_skew_visible`
- recommendation(권고): `keep_stage17_open_for_probability_feature_driver_probe`
- boundary(경계): `xgboost_trade_shape_attribution_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| side/split(방향/분할) | trades(거래수) | net(순손익) | avg hold(평균 보유) | MFE | MAE | positive months(양수 월 비율) |
|---|---:|---:|---:|---:|---:|---:|
| long/validation | `224` | `-24.28000000000003` | `41.356621874999995` | `9.596482142857143` | `11.928294642857143` | `0.3333333333333333` |
| short/validation | `73` | `-253.75999999999996` | `56.95890410958904` | `10.48676712328767` | `15.85882191780822` | `0.2222222222222222` |
| long/oos | `191` | `-8.439999999999976` | `37.31937172774869` | `9.099596858638744` | `10.568371727748692` | `0.42857142857142855` |
| short/oos | `73` | `66.91` | `32.054794520547944` | `10.471534246575343` | `8.677945205479451` | `0.7142857142857143` |

- validation long signal share(검증 롱 신호 비율): `0.8439334637964775`
- OOS long signal share(표본외 롱 신호 비율): `0.7446254071661238`
- hold contrast bars(보유 시간 차이): `5.168852513694148`
- positive month ratio contrast(양수 월 비율 차이): `0.08730158730158732`
- new characteristic visible(새 특성 보임): `True`

효과(effect, 효과): 이 run(실행)은 run11C의 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심성과지표) 근거를 재사용해 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅)의 방향 비대칭이 거래 모양과 확률 신호 쏠림으로도 보이는지 확인했다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
