# RUN21B Quantile Boosting Tail Runtime Probe Packet(21B 실행 분위수 부스팅 꼬리 런타임 탐침 묶음)

## Judgment(판정)

- run(실행): `run21B_quantile_boosting_tail_risk_runtime_probe_v1`
- status(상태): `reviewed_runtime_probe_completed`
- judgment(판정): `inconclusive_quantile_boosting_tail_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v02_core42_tail_risk_surface`
- boundary(경계): `quantile_boosting_tail_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): quantile boosting(분위수 부스팅)의 tail surface(꼬리 표면)를 direction/width/asymmetry/pressure(방향/폭/비대칭/압력) runtime features(런타임 피처)로 증류해 MT5 EA path(MT5 EA 경로)에서 읽히는지 확인한다. native quantile boosting runtime authority(원본 분위수 부스팅 런타임 권위)는 주장하지 않는다.

## MT5 KPI(MT5 핵심 성과 지표)

- attempts(시도): `6` / `6`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10` / `6`
- normalized records(정규화 기록): `6`
- parser errors(파서 오류): `0`
- trade parser errors(거래 파서 오류): `0`

| split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 낙폭) |
|---|---:|---:|---:|---:|
| validation routed(검증 라우팅) | `-38.2` | `0.97` | `665` | `307.66` |
| OOS routed(표본외 라우팅) | `79.17` | `1.07` | `576` | `241.7` |

## Runtime Parity(런타임 동등성)

- Tier A score table parity(Tier A 점수표 동등성): `True`
- Tier B score table parity(Tier B 점수표 동등성): `True`
- known runtime difference(알려진 런타임 차이): `MT5 runtime_probe uses a distilled additive score table, not native quantile boosting inference.`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
