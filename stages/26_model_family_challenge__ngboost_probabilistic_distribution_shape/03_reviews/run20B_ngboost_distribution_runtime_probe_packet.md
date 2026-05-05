# RUN20B NGBoost Distribution Runtime Probe Packet(20B 실행 NGBoost 분포 런타임 탐침 묶음)

## Judgment(판정)

- run(실행): `run20B_ngboost_distribution_runtime_probe_v1`
- status(상태): `reviewed_runtime_probe_completed`
- judgment(판정): `inconclusive_ngboost_distribution_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v02_core42_distribution_surface`
- boundary(경계): `ngboost_distribution_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): NGBoost(자연 그래디언트 부스팅)의 probability distribution(확률분포)을 direction/confidence/flat/entropy(방향/신뢰도/플랫/엔트로피) runtime features(런타임 피처)로 증류해 MT5 EA path(MT5 EA 경로)에서 읽혔는지 확인한다. native NGBoost runtime authority(원본 NGBoost 런타임 권위)는 주장하지 않는다.

## MT5 KPI(MT5 핵심 성과 지표)

- attempts(시도): `6` / `6`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10` / `6`
- normalized records(정규화 기록): `6`
- parser errors(파서 오류): `0`
- trade parser errors(거래 파서 오류): `0`

| split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 낙폭) |
|---|---:|---:|---:|---:|
| validation routed(검증 라우팅) | `-17.21` | `0.05` | `6` | `21.47` |
| OOS routed(표본외 라우팅) | `39.49` | `2.37` | `10` | `21.75` |

## Runtime Parity(런타임 동등성)

- Tier A score table parity(Tier A 점수표 동등성): `True`
- Tier B score table parity(Tier B 점수표 동등성): `True`
- known runtime difference(알려진 런타임 차이): `MT5 runtime_probe uses a distilled additive score table, not native NGBoost inference.`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
