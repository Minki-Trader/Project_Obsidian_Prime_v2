# run24B Runtime Probe Packet(run24B 런타임 탐침 묶음)

## Judgment(판정)

- run(실행): `run24B_probability_calibration_abstention_runtime_probe_v1`
- status(상태): `reviewed_runtime_probe_completed`
- judgment(판정): `inconclusive_stage30_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v02_isotonic_margin_abstention`
- boundary(경계): `stage30_exploration_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage30(30단계) topic surface(주제 표면)를 MT5 score-table handoff(MT5 점수표 인계)로 관찰한다. native package runtime authority(원본 패키지 런타임 권위)는 주장하지 않는다.

## MT5 KPI(MT5 핵심 성과 지표)

- attempts(시도): `6` / `6`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10` / `10`
- normalized records(정규화 기록): `6`
- parser errors(파서 오류): `0`
- trade parser errors(거래 파서 오류): `0`

| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) |
|---|---:|---:|---:|---:|
| validation routed(검증 라우팅) | `-5.44` | `0.99` | `231` | `106.38` |
| OOS routed(표본외 라우팅) | `130.07` | `1.37` | `204` | `75.98` |

## Runtime Parity(런타임 동등성)

- Tier A score table parity(Tier A 점수표 동등성): `True`
- Tier B score table parity(Tier B 점수표 동등성): `True`
- known runtime difference(알려진 런타임 차이): `MT5 runtime_probe(MT5 런타임 탐침)는 native package runtime(원본 패키지 런타임)이 아니라 distilled score-table handoff(증류 점수표 인계)다. native calibration package(원본 보정 패키지) not required; sklearn isotonic(사이킷런 등위 회귀) used.`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
