# RUN19B Hazard Runtime Probe Packet(실행19B 위험률 런타임 탐침 묶음)

## Judgment(판정)

- run(실행): `run19B_hazard_trade_lifecycle_runtime_probe_v1`
- judgment(판정): `inconclusive_hazard_permission_runtime_probe_completed`
- external verification(외부 검증): `completed`
- selected variant(선택 변형): `v04_logit_core24_reversal_after_favorable_1x`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- boundary(경계): `hazard_permission_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Hazard model(위험률 모델)의 fixed elapsed-bar risk(고정 경과 봉 위험)를 flat/close pressure(평탄/청산 압력)로 넘기는 MT5 runtime_probe(MT5 런타임 탐침)를 수행했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Runtime Read(런타임 판독)

| split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실폭) |
|---|---:|---:|---:|---:|
| validation(검증) | `-89.59` | `0.94` | `2145` | `187.51` |
| OOS(표본외) | `-174.49` | `0.83` | `1210` | `206.31` |

## Runtime Parity(런타임 동등성)

- Tier A table parity(Tier A 점수표 동등성): `True`; max_abs_diff(최대 절대 차이) `0.03188428583454417`
- Tier B table parity(Tier B 점수표 동등성): `True`; max_abs_diff(최대 절대 차이) `0.03593360493368214`
- known difference(알려진 차이): MT5 runtime_probe(MT5 런타임 탐침)는 fixed elapsed-bar snapshot(고정 경과 봉 스냅샷)을 쓰며 dynamic position-age hazard clock(동적 포지션 나이 위험률 시계)은 아니다.

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
