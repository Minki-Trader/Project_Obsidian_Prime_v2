# RUN29A Unsupervised Market State Atlas MT5 Probe(RUN29A 비지도 시장 상태 지도 MT5 탐침)

- status(상태): `reviewed_unsupervised_atlas_mt5_probe_completed`
- judgment(판정): `inconclusive_unsupervised_atlas_mt5_runtime_probe_completed`
- external verification(외부 검증): `completed`
- MT5 attempts(MT5 시도): `10`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`

## Selected Atlas States(선택된 지도 상태)

- `return_volatility_shape`: state(상태) `0`, direction(방향) `long`, validation rows(검증 행) `1194`
- `trend_momentum_pressure`: state(상태) `4`, direction(방향) `long`, validation rows(검증 행) `1481`
- `session_timing_map`: state(상태) `4`, direction(방향) `long`, validation rows(검증 행) `2249`
- `macro_risk_proxy_map`: state(상태) `1`, direction(방향) `short`, validation rows(검증 행) `2877`
- `mega_cap_breadth_divergence`: state(상태) `4`, direction(방향) `long`, validation rows(검증 행) `893`

## MT5 Runtime Read(MT5 런타임 판독)

| topic(주제) | split(분할) | direction(방향) | trades(거래) | net(순손익) | PF(수익 팩터) |
|---|---:|---:|---:|---:|---:|
| `return_volatility_shape` | `validation_is` | `long` | `33` | `-508.89` | `0.44` |
| `return_volatility_shape` | `oos` | `long` | `58` | `162.82` | `1.25` |
| `trend_momentum_pressure` | `validation_is` | `long` | `41` | `-515.31` | `0.39` |
| `trend_momentum_pressure` | `oos` | `long` | `112` | `134.68` | `1.15` |
| `session_timing_map` | `validation_is` | `long` | `173` | `175.04` | `1.11` |
| `session_timing_map` | `oos` | `long` | `140` | `0.41` | `1.0` |
| `macro_risk_proxy_map` | `validation_is` | `short` | `222` | `-357.78` | `0.84` |
| `macro_risk_proxy_map` | `oos` | `short` | `166` | `-46.29` | `0.97` |
| `mega_cap_breadth_divergence` | `validation_is` | `long` | `69` | `416.77` | `1.39` |
| `mega_cap_breadth_divergence` | `oos` | `long` | `40` | `-187.69` | `0.76` |

정규화 KPI(normalized KPI, 정규화 핵심 성과 지표): records(기록) `10`, parser errors(파서 오류) `0`.

## Runtime Parity Boundary(런타임 동등성 경계)

Python(파이썬)이 cluster state(군집 상태)를 미리 계산했고, MT5(메타트레이더5)는 selected state row(선택 상태 행)만 받은 feature CSV(피처 CSV)를 실행했다.

효과(effect, 효과): 터미널에서 그 시간대만 거래했을 때의 runtime probe(런타임 탐침)는 보지만, native clustering runtime authority(원본 군집 런타임 권위)는 아니다.

## Forbidden Claims(금지 주장)

`edge(거래 우위)`, `alpha_quality(알파 품질)`, `baseline(기준선)`, `promotion(승격)`, `runtime_authority(런타임 권위)`, `live_readiness(실거래 준비)`.
