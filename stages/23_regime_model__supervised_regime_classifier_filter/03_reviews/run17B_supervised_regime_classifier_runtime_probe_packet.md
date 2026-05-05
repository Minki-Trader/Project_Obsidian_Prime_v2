# RUN17B Supervised Regime Classifier Runtime Probe(실행17B 지도 국면 분류기 런타임 탐침)

## Judgment(판정)

- run(실행): `run17B_supervised_regime_classifier_runtime_probe_v1`
- judgment(판정): `inconclusive_supervised_regime_classifier_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v05_logistic_core24_compact_filter`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- boundary(경계): `supervised_regime_classifier_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): supervised regime classifier(지도 국면 분류기)를 direct entry model(직접 진입 모델)이 아니라 permission/filter(허용/필터) runtime_probe(런타임 탐침)로 MT5(`MetaTrader 5`, 메타트레이더5)에 인계했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Runtime Read(런타임 판독)

| split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) |
|---|---:|---:|---:|---:|
| validation(검증) | `324.75` | `1.16` | `476` | `301.5` |
| OOS(표본외) | `254.63` | `1.19` | `345` | `153.14` |

## ONNX Parity(온닉스 동등성)

- Tier A parity(Tier A 동등성): `True`; max_abs_diff(최대 절대 차이) `6.690947950138693e-07`
- Tier B parity(Tier B 동등성): `True`; max_abs_diff(최대 절대 차이) `2.693215265248128e-07`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
