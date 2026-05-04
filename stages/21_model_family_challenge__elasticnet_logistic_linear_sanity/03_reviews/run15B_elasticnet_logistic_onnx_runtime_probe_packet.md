# RUN15B ElasticNet Logistic ONNX Runtime Probe(실행15B 엘라스틱넷 로지스틱 온닉스 런타임 탐침)

## Judgment(판정)

- run(실행): `run15B_elasticnet_logistic_onnx_runtime_probe_v1`
- judgment(판정): `inconclusive_elasticnet_logistic_onnx_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v01_core42_balanced_enet025`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- boundary(경계): `elasticnet_logistic_onnx_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): ElasticNet Logistic(엘라스틱넷 로지스틱)을 ONNX(온닉스) handoff(인계)로 MT5(`MetaTrader 5`, 메타트레이더5)에서 실행했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Runtime Read(런타임 판독)

| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) |
|---|---:|---:|---:|---:|
| validation(검증) | `-113.11` | `0.9` | `173` | `273.73` |
| OOS(표본외) | `-49.77` | `0.94` | `130` | `159.63` |

## ONNX Parity(온닉스 동등성)

- Tier A parity(Tier A 동등성): `True`; max_abs_diff(최대 절대 차이) `5.999363719144668e-07`
- Tier B parity(Tier B 동등성): `True`; max_abs_diff(최대 절대 차이) `2.888406099299523e-07`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
