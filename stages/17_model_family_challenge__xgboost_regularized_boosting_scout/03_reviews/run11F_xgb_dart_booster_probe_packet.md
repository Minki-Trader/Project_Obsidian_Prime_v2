# Stage17 RUN11F XGBoost DART Booster Probe(17단계 실행11F XGBoost DART 부스터 탐침)

- run(실행): `run11F_xgb_dart_booster_probe_v1`
- judgment(판정): `inconclusive_xgboost_dart_booster_runtime_probe_completed`
- recommendation(권고): `keep_stage17_open_for_dart_followup_attribution`
- selected variant(선택 변형): `dart_v01_depth3_lowdrop`
- ONNX parity(ONNX 동등성): `True`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- trade attribution records(거래 귀속 기록): `6`

| split(분할) | routed trades(라우팅 거래 수) | net profit(순수익) | profit factor(수익 팩터) | recovery(회복 계수) |
|---|---:|---:|---:|---:|
| validation(검증) | `291` | `125.17` | `1.08` | `0.32` |
| OOS(표본 밖) | `259` | `193.23` | `1.18` | `1.09` |

- avg routed trades(평균 라우팅 거래 수): `275.0`
- trade ratio vs run11B(run11B 대비 거래 비율): `1.198257080610022`
- validation long signal share(검증 롱 신호 비중): `0.9019807008633824`
- OOS long signal share(표본 밖 롱 신호 비중): `0.8418404025880661`
- top3 changed(상위 3개 피처 변화): `True`
- new characteristic visible(새 특성 보임): `True`

효과(effect, 효과): DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅)를 기존 gbtree(기본 트리 부스팅)와 같은 데이터, threshold(임계값), MT5(`MetaTrader 5`, 메타트레이더5) 경로에서 비교했다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
