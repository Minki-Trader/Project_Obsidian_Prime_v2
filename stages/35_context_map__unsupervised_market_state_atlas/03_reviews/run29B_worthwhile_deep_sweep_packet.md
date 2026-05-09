# RUN29B Worthwhile Deep Sweep MT5 Probe(29B 실행 더 파볼 축 깊은 훑기 MT5 탐침)

- status(상태): `reviewed_stage35_worthwhile_deep_sweep_mt5_completed`
- judgment(판정): `inconclusive_stage35_worthwhile_deep_sweep_mt5_completed`
- external verification(외부 검증): `completed`
- variants(변형 수): `19`
- planned MT5 attempts(계획 MT5 시도): `32`
- MT5 attempts(MT5 시도): `32`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `32`
- skipped empty feature files(빈 피처 파일 제외): `4`

## Why This Run Exists(이 실행의 이유)

RUN29A(29A 실행)에서 그나마 볼 만한 단서는 session timing(세션 시간), return-volatility state(수익률/변동성 상태), trend-momentum state(추세/모멘텀 상태)였다. RUN29B(29B 실행)는 그 안에서 더 파볼 만한 축을 전부 MT5(`MetaTrader 5`, 메타트레이더5)에 넘겨 확인했다.

효과(effect, 효과): 좋은 단서와 버릴 단서를 한 번에 분리한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Python Proxy Variants(Python 대리 측정 변형)

| variant(변형) | family(계열) | direction(방향) | validation rows(검증 행) | validation PF(검증 수익 팩터) | OOS rows(표본외 행) | OOS PF(표본외 수익 팩터) |
|---|---:|---:|---:|---:|---:|---:|
| `session_cash_open_0_30` | `session_timing` | `long` | `809` | `1.2755189296392104` | `542` | `0.9555398579553835` |
| `session_cash_open_30_90` | `session_timing` | `short` | `1910` | `1.0355802123428257` | `1392` | `1.1852557786182296` |
| `session_cash_open_90_180` | `session_timing` | `short` | `2728` | `1.0626429503301384` | `2218` | `0.9952868871515669` |
| `session_cash_mid_180_330` | `session_timing` | `long` | `4225` | `1.064586845315016` | `3309` | `0.9444830139432073` |
| `session_cash_late_30` | `session_timing` | `long` | `0` | `None` | `0` | `None` |
| `session_cash_only` | `session_timing` | `long` | `9844` | `1.033786549343557` | `7584` | `0.935432844169344` |
| `session_non_cash_only` | `session_timing` | `long` | `0` | `None` | `0` | `None` |
| `return_volatility_shape_state0` | `return_volatility` | `long` | `1194` | `1.3319286504494905` | `750` | `1.046576245582107` |
| `return_volatility_shape_state1` | `return_volatility` | `short` | `3107` | `1.1347383091831236` | `2047` | `1.292645540438892` |
| `return_volatility_shape_state2` | `return_volatility` | `long` | `748` | `1.1431267158208194` | `465` | `0.7403836902148829` |
| `return_volatility_shape_state3` | `return_volatility` | `long` | `3072` | `1.0239282998425376` | `3392` | `1.0284155336896308` |
| `return_volatility_shape_state4` | `return_volatility` | `short` | `1723` | `1.065745295263461` | `930` | `1.202535272888246` |
| `trend_momentum_pressure_state0` | `trend_momentum` | `short` | `1946` | `1.0619050019955862` | `1397` | `0.985995696515031` |
| `trend_momentum_pressure_state1` | `trend_momentum` | `long` | `2619` | `1.0313640503341148` | `1869` | `0.9829428769247855` |
| `trend_momentum_pressure_state2` | `trend_momentum` | `short` | `2250` | `1.0026192913727008` | `1657` | `0.8577032531982193` |
| `trend_momentum_pressure_state3` | `trend_momentum` | `long` | `1548` | `1.013588265489468` | `1210` | `0.6581788694951133` |
| `trend_momentum_pressure_state4` | `trend_momentum` | `long` | `1481` | `1.2316892226875935` | `1451` | `0.9308645863819206` |
| `return_volatility_shape_state0_no_oct2025` | `return_volatility_drift` | `long` | `1194` | `1.3319286504494905` | `605` | `1.0604703657985972` |
| `trend_momentum_pressure_state4_no_oct2025` | `trend_momentum_drift` | `long` | `1481` | `1.2316892226875935` | `1210` | `0.8758727092718298` |

## MT5 Runtime Read(MT5 런타임 판독)

| variant(변형) | split(분할) | direction(방향) | trades(거래) | net(순손익) | PF(수익 팩터) |
|---|---:|---:|---:|---:|---:|
| `session_cash_open_0_30` | `validation_is` | `long` | `63` | `373.88` | `1.45` |
| `session_cash_open_0_30` | `oos` | `long` | `42` | `50.12` | `1.06` |
| `session_cash_open_30_90` | `validation_is` | `short` | `147` | `-336.54` | `0.81` |
| `session_cash_open_30_90` | `oos` | `short` | `108` | `-282.61` | `0.8` |
| `session_cash_open_90_180` | `validation_is` | `short` | `203` | `-494.1` | `0.77` |
| `session_cash_open_90_180` | `oos` | `short` | `171` | `16.91` | `1.01` |
| `session_cash_mid_180_330` | `validation_is` | `long` | `325` | `314.11` | `1.15` |
| `session_cash_mid_180_330` | `oos` | `long` | `255` | `25.62` | `1.01` |
| `session_cash_only` | `validation_is` | `long` | `758` | `114.66` | `1.04` |
| `session_cash_only` | `oos` | `long` | `584` | `-117.31` | `0.96` |
| `return_volatility_shape_state0` | `validation_is` | `long` | `33` | `-508.89` | `0.44` |
| `return_volatility_shape_state0` | `oos` | `long` | `58` | `162.82` | `1.25` |
| `return_volatility_shape_state1` | `validation_is` | `short` | `239` | `-451.9` | `0.72` |
| `return_volatility_shape_state1` | `oos` | `short` | `158` | `-50.12` | `0.95` |
| `return_volatility_shape_state2` | `validation_is` | `long` | `58` | `352.39` | `1.34` |
| `return_volatility_shape_state2` | `oos` | `long` | `36` | `149.46` | `1.25` |
| `return_volatility_shape_state3` | `validation_is` | `long` | `237` | `397.16` | `1.23` |
| `return_volatility_shape_state3` | `oos` | `long` | `261` | `-117.01` | `0.94` |
| `return_volatility_shape_state4` | `validation_is` | `short` | `133` | `-354.3` | `0.75` |
| `return_volatility_shape_state4` | `oos` | `short` | `72` | `-113.69` | `0.86` |
| `trend_momentum_pressure_state0` | `validation_is` | `short` | `150` | `-321.31` | `0.81` |
| `trend_momentum_pressure_state0` | `oos` | `short` | `108` | `-150.26` | `0.89` |
| `trend_momentum_pressure_state1` | `validation_is` | `long` | `202` | `178.19` | `1.13` |
| `trend_momentum_pressure_state1` | `oos` | `long` | `144` | `85.13` | `1.07` |
| `trend_momentum_pressure_state2` | `validation_is` | `short` | `174` | `-451.08` | `0.76` |
| `trend_momentum_pressure_state2` | `oos` | `short` | `128` | `-211.66` | `0.85` |
| `trend_momentum_pressure_state3` | `validation_is` | `long` | `60` | `-499.83` | `0.37` |
| `trend_momentum_pressure_state3` | `oos` | `long` | `94` | `91.62` | `1.09` |
| `trend_momentum_pressure_state4` | `validation_is` | `long` | `41` | `-515.31` | `0.39` |
| `trend_momentum_pressure_state4` | `oos` | `long` | `112` | `134.68` | `1.15` |
| `return_volatility_shape_state0_no_oct2025` | `oos` | `long` | `47` | `-36.42` | `0.95` |
| `trend_momentum_pressure_state4_no_oct2025` | `oos` | `long` | `94` | `-257.45` | `0.71` |

## Best OOS Clues(가장 나은 표본외 단서)

| rank(순위) | variant(변형) | trades(거래) | net(순손익) | PF(수익 팩터) |
|---:|---|---:|---:|---:|
| `1` | `return_volatility_shape_state0` | `58` | `162.82` | `1.25` |
| `2` | `return_volatility_shape_state2` | `36` | `149.46` | `1.25` |
| `3` | `trend_momentum_pressure_state4` | `112` | `134.68` | `1.15` |
| `4` | `trend_momentum_pressure_state3` | `94` | `91.62` | `1.09` |
| `5` | `trend_momentum_pressure_state1` | `144` | `85.13` | `1.07` |
| `6` | `session_cash_open_0_30` | `42` | `50.12` | `1.06` |
| `7` | `session_cash_mid_180_330` | `255` | `25.62` | `1.01` |
| `8` | `session_cash_open_90_180` | `171` | `16.91` | `1.01` |

## Easy Read(쉬운 판독)

| read(판독) | variant(변형) | val net/PF(검증 순손익/수익 팩터) | OOS net/PF(표본외 순손익/수익 팩터) |
|---|---|---:|---:|
| `both_positive` | `return_volatility_shape_state2` | `352.39` / `1.34` | `149.46` / `1.25` |
| `both_positive` | `trend_momentum_pressure_state1` | `178.19` / `1.13` | `85.13` / `1.07` |
| `both_positive` | `session_cash_open_0_30` | `373.88` / `1.45` | `50.12` / `1.06` |
| `both_positive` | `session_cash_mid_180_330` | `314.11` / `1.15` | `25.62` / `1.01` |
| `oos_only` | `return_volatility_shape_state0` | `-508.89` / `0.44` | `162.82` / `1.25` |
| `oos_only` | `trend_momentum_pressure_state4` | `-515.31` / `0.39` | `134.68` / `1.15` |
| `oos_only` | `trend_momentum_pressure_state3` | `-499.83` / `0.37` | `91.62` / `1.09` |
| `oos_only` | `session_cash_open_90_180` | `-494.1` / `0.77` | `16.91` / `1.01` |
| `validation_only` | `session_cash_only` | `114.66` / `1.04` | `-117.31` / `0.96` |
| `validation_only` | `return_volatility_shape_state3` | `397.16` / `1.23` | `-117.01` / `0.94` |
| `weak_or_negative` | `return_volatility_shape_state0_no_oct2025` | `None` / `None` | `-36.42` / `0.95` |
| `weak_or_negative` | `return_volatility_shape_state1` | `-451.9` / `0.72` | `-50.12` / `0.95` |
| `weak_or_negative` | `trend_momentum_pressure_state0` | `-321.31` / `0.81` | `-150.26` / `0.89` |
| `weak_or_negative` | `return_volatility_shape_state4` | `-354.3` / `0.75` | `-113.69` / `0.86` |
| `weak_or_negative` | `trend_momentum_pressure_state2` | `-451.08` / `0.76` | `-211.66` / `0.85` |
| `weak_or_negative` | `session_cash_open_30_90` | `-336.54` / `0.81` | `-282.61` / `0.8` |
| `weak_or_negative` | `trend_momentum_pressure_state4_no_oct2025` | `None` / `None` | `-257.45` / `0.71` |

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `completed`
- Tier B separate(Tier B 분리): `out_of_scope_by_claim_stage35_tier_a_runtime_probe_only`
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim_stage35_tier_a_runtime_probe_only`

## Boundary(경계)

`stage35_worthwhile_deep_sweep_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority`

runtime_probe(런타임 탐침)일 뿐이다. edge(거래 우위), alpha_quality(알파 품질), baseline(기준선), promotion(승격), runtime_authority(런타임 권위), live_readiness(실거래 준비)는 금지 주장이다.
