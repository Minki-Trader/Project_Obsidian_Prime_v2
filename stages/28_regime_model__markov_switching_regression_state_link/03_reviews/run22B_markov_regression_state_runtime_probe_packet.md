# RUN22B Markov Regression State Runtime Probe Packet(22B 실행 마르코프 회귀 상태 런타임 탐침 묶음)

## Judgment(판정)

- run(실행): `run22B_markov_regression_state_runtime_probe_v1`
- status(상태): `reviewed_runtime_probe_completed`
- judgment(판정): `inconclusive_markov_regression_state_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v01_return_2state_switchvar`
- boundary(경계): `markov_regression_state_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Markov regression(마르코프 회귀) state sequence(상태 순서)를 score-table handoff(점수표 인계)로 MT5 EA path(MT5 전문가 자문 경로)에서 읽히는지 확인한다. native statsmodels runtime authority(원본 스탯스모델 런타임 권위)는 주장하지 않는다.

## MT5 KPI(MT5 핵심 성과 지표)

- attempts(시도): `6` / `6`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10` / `10`
- normalized records(정규화 기록): `6`
- parser errors(파서 오류): `0`
- trade parser errors(거래 파서 오류): `0`

| split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실폭) |
|---|---:|---:|---:|---:|
| validation routed(검증 라우팅) | `244.08` | `1.77` | `190` | `74.31` |
| OOS routed(표본외 라우팅) | `111.27` | `1.31` | `118` | `90.63` |

## Runtime Parity(런타임 동등성)

- Tier A score table parity(Tier A 점수표 동등성): `True`
- Tier B score table parity(Tier B 점수표 동등성): `True`
- known runtime difference(알려진 런타임 차이): `MT5 runtime_probe uses sampled Markov state-table handoff, not native statsmodels MarkovRegression inference.`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
