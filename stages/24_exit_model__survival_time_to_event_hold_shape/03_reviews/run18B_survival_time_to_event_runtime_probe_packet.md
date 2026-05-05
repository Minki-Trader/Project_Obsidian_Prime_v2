# RUN18B Survival Time-To-Event Runtime Probe(실행18B 생존 시간-사건 런타임 탐침)

## Judgment(판정)

- run(실행): `run18B_survival_time_to_event_runtime_probe_v1`
- judgment(판정): `inconclusive_survival_permission_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v04_weibull_aft_core24_abs_move_3x`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- boundary(경계): `survival_permission_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Survival model(생존 모델)의 risk score(위험 점수)를 flat/close pressure(평탄/청산 압력)로 넘기는 runtime_probe(런타임 탐침)를 수행했다. direction_proxy(방향 대리값)는 단순 closed-bar cue(닫힌 봉 단서)일 뿐이며 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Runtime Read(런타임 판독)

| split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실폭) |
|---|---:|---:|---:|---:|
| validation(검증) | `-157.74` | `0.9` | `2195` | `315.57` |
| OOS(표본외) | `-98.54` | `0.88` | `1100` | `141.34` |

## Runtime Parity(런타임 동등성)

- Tier A table parity(Tier A 테이블 동등성): `True`; max_abs_diff(최대 절대 차이) `0.10748847807900863`
- Tier B table parity(Tier B 테이블 동등성): `True`; max_abs_diff(최대 절대 차이) `0.06256716760342185`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
