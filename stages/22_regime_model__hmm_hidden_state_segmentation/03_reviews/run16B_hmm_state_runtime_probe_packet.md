# RUN16B HMM State Runtime Probe(실행16B HMM 상태 런타임 탐침)

## Judgment(판정)

- run(실행): `run16B_hmm_state_runtime_probe_v1`
- judgment(판정): `inconclusive_hmm_state_policy_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v02_core17_4state_diag`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- boundary(경계): `hmm_state_policy_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): HMM(`Hidden Markov Model`, 은닉 마르코프 모델)의 hidden state(숨은 상태)를 MT5(`MetaTrader 5`, 메타트레이더5) `ebm_table(EBM 테이블)` backend(백엔드)로 넘겨 runtime handoff(런타임 인계)를 확인했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Runtime Read(런타임 판독)

| split(분할) | net profit(순손익) | profit factor(수익 계수) | trades(거래 수) | max DD(최대 손실) |
|---|---:|---:|---:|---:|
| validation(검증) | `-497.25` | `0.69` | `279` | `606.17` |
| OOS(표본외) | `121.96` | `1.05` | `562` | `315.22` |

## State Table Parity(상태 테이블 동등성)

- Tier A parity(Tier A 동등성): `True`; max_abs_diff(최대 절대 차이) `1.1102230246251565e-16`
- Tier B parity(Tier B 동등성): `True`; max_abs_diff(최대 절대 차이) `5.551115123125783e-17`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
