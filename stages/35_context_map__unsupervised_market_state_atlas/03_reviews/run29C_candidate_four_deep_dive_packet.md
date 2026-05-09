# RUN29C Candidate Four Deep Dive MT5 Probe(29C 실행 후보 4개 심화 MT5 탐침)

- status(상태): `reviewed_stage35_candidate_four_deep_dive_mt5_completed`
- judgment(판정): `inconclusive_stage35_candidate_four_deep_dive_mt5_completed`
- external verification(외부 검증): `completed`
- candidates(후보): `4`
- planned MT5 attempts(계획 MT5 시도): `36`
- MT5 attempts(MT5 시도): `36`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `36`

## Easy Read(쉬운 판독)

| rank(순위) | candidate(후보) | read(판독) | base val(기본 검증) | base OOS(기본 표본외) | no Oct OOS(10월 제외 표본외) | first/second half(전반/후반) |
|---:|---|---|---:|---:|---:|---:|
| `1` | `return_volatility_shape_state2` | `base_positive_only` | `310.59` / `1.29` | `86.46` / `1.14` | `-155.03` / `0.76` | `141.34` / `1.52` ; `-75.34` / `0.81` |
| `2` | `trend_momentum_pressure_state1` | `failed_base_recheck` | `-496.68` / `0.5` | `55.96` / `1.04` | `-12.09` / `0.99` | `57.79` / `1.1` ; `-92.77` / `0.88` |
| `3` | `session_cash_open_0_30` | `base_positive_only` | `331.08` / `1.39` | `19.44` / `1.02` | `-0.81` / `1.0` | `8.74` / `1.02` ; `-49.55` / `0.89` |
| `4` | `session_cash_mid_180_330` | `failed_base_recheck` | `272.13` / `1.13` | `-6.24` / `1.0` | `-21.27` / `0.98` | `12.64` / `1.02` ; `-3.74` / `1.0` |

## Full MT5 Stress Table(전체 MT5 압박 표)

| candidate(후보) | stress(압박) | hold(보유) | trades(거래) | net(순손익) | PF(수익 팩터) |
|---|---|---:|---:|---:|---:|
| `return_volatility_shape_state2` | `validation_h6` | `6` | `107` | `74.62` | `1.05` |
| `return_volatility_shape_state2` | `oos_h6` | `6` | `67` | `50.77` | `1.05` |
| `return_volatility_shape_state2` | `validation_h12` | `12` | `58` | `310.59` | `1.29` |
| `return_volatility_shape_state2` | `oos_h12` | `12` | `36` | `86.46` | `1.14` |
| `return_volatility_shape_state2` | `validation_h24` | `24` | `15` | `-507.95` | `0.24` |
| `return_volatility_shape_state2` | `oos_h24` | `24` | `19` | `-0.75` | `1.0` |
| `return_volatility_shape_state2` | `oos_no_oct2025_h12` | `12` | `31` | `-155.03` | `0.76` |
| `return_volatility_shape_state2` | `oos_first_half_h12` | `12` | `18` | `141.34` | `1.52` |
| `return_volatility_shape_state2` | `oos_second_half_h12` | `12` | `18` | `-75.34` | `0.81` |
| `trend_momentum_pressure_state1` | `validation_h6` | `6` | `375` | `152.04` | `1.1` |
| `trend_momentum_pressure_state1` | `oos_h6` | `6` | `267` | `-159.79` | `0.9` |
| `trend_momentum_pressure_state1` | `validation_h12` | `12` | `67` | `-496.68` | `0.5` |
| `trend_momentum_pressure_state1` | `oos_h12` | `12` | `144` | `55.96` | `1.04` |
| `trend_momentum_pressure_state1` | `validation_h24` | `24` | `105` | `279.19` | `1.28` |
| `trend_momentum_pressure_state1` | `oos_h24` | `24` | `75` | `-60.51` | `0.94` |
| `trend_momentum_pressure_state1` | `oos_no_oct2025_h12` | `12` | `115` | `-12.09` | `0.99` |
| `trend_momentum_pressure_state1` | `oos_first_half_h12` | `12` | `72` | `57.79` | `1.1` |
| `trend_momentum_pressure_state1` | `oos_second_half_h12` | `12` | `72` | `-92.77` | `0.88` |
| `session_cash_open_0_30` | `validation_h6` | `6` | `35` | `-497.03` | `0.4` |
| `session_cash_open_0_30` | `oos_h6` | `6` | `78` | `29.77` | `1.03` |
| `session_cash_open_0_30` | `validation_h12` | `12` | `63` | `331.08` | `1.39` |
| `session_cash_open_0_30` | `oos_h12` | `12` | `42` | `19.44` | `1.02` |
| `session_cash_open_0_30` | `validation_h24` | `24` | `10` | `-496.58` | `0.21` |
| `session_cash_open_0_30` | `oos_h24` | `24` | `22` | `-46.14` | `0.89` |
| `session_cash_open_0_30` | `oos_no_oct2025_h12` | `12` | `35` | `-0.81` | `1.0` |
| `session_cash_open_0_30` | `oos_first_half_h12` | `12` | `21` | `8.74` | `1.02` |
| `session_cash_open_0_30` | `oos_second_half_h12` | `12` | `21` | `-49.55` | `0.89` |
| `session_cash_mid_180_330` | `validation_h6` | `6` | `604` | `135.98` | `1.06` |
| `session_cash_mid_180_330` | `oos_h6` | `6` | `473` | `46.98` | `1.03` |
| `session_cash_mid_180_330` | `validation_h12` | `12` | `325` | `272.13` | `1.13` |
| `session_cash_mid_180_330` | `oos_h12` | `12` | `255` | `-6.24` | `1.0` |
| `session_cash_mid_180_330` | `validation_h24` | `24` | `169` | `488.68` | `1.35` |
| `session_cash_mid_180_330` | `oos_h24` | `24` | `133` | `-121.11` | `0.92` |
| `session_cash_mid_180_330` | `oos_no_oct2025_h12` | `12` | `211` | `-21.27` | `0.98` |
| `session_cash_mid_180_330` | `oos_first_half_h12` | `12` | `128` | `12.64` | `1.02` |
| `session_cash_mid_180_330` | `oos_second_half_h12` | `12` | `128` | `-3.74` | `1.0` |

## Boundary(경계)

`stage35_candidate_four_deep_dive_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority`

runtime_probe(런타임 탐침)일 뿐이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
