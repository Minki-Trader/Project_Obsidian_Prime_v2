# RUN14B GAM Runtime Handoff Probe(실행14B GAM 런타임 인계 탐침)

## Judgment(판정)

- run(실행): `run14B_gam_runtime_handoff_probe_v1`
- judgment(판정): `inconclusive_gam_piecewise_score_table_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v02_core24_smoother`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- boundary(경계): `gam_piecewise_score_table_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): GAM(`Generalized Additive Model`, 일반화 가산 모델)을 piecewise score table(구간 점수표)로 MT5(`MetaTrader 5`, 메타트레이더5)에 넘겨 runtime_probe(런타임 탐침)를 시도했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Runtime Read(런타임 판독)

| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) |
|---|---:|---:|---:|---:|
| validation(검증) | `8.65` | `1.01` | `211` | `288.52` |
| OOS(표본외) | `295.69` | `1.51` | `125` | `98.5` |

## Handoff Parity(인계 동등성)

- Tier A approximation check(Tier A 근사 점검): `True`; max_abs_diff(최대 절대 차이) `0.16040910742952552`; p95_abs_diff(95분위 절대 차이) `0.030635266081190923`
- Tier B approximation check(Tier B 근사 점검): `True`; max_abs_diff(최대 절대 차이) `0.2513191050874792`; p95_abs_diff(95분위 절대 차이) `0.010339225646583157`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
