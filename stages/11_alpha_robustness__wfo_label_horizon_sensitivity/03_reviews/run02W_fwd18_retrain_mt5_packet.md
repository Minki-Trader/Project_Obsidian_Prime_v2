# RUN02W fwd18 Retrain MT5 Packet

## Result

`RUN02W(실행 02W)`는 fwd18 label horizon(90분 라벨 예측수평선)으로 LGBM(`LightGBM`, 라이트GBM)을 재학습하고 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터)까지 연결했다.

| View(보기) | Validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | Read(판독) |
|---|---:|---:|---|
| Tier A only(Tier A 단독) | `-495.84 / 0.28` | `-132.97 / 0.75` | negative(부정) |
| Tier B fallback-only(Tier B 대체 단독) | `197.17 / 8.31` | `-105.73 / 0.70` | validation-only(검증만 양수) |
| Routed total(라우팅 전체) | `-496.25 / 0.28` | `-216.12 / 0.67` | negative(부정) |

## Python Surface

| View(보기) | Rows(행) | Signals(신호) | Short/Long(숏/롱) | Coverage(커버리지) |
|---|---:|---:|---:|---:|
| Tier A separate(Tier A 분리) | `2884` | `843` | `172/671` | `0.292302` |
| Tier B separate(Tier B 분리) | `696` | `131` | `18/113` | `0.188218` |
| Tier A+B combined(Tier A+B 합산) | `3580` | `974` | `190/784` | `0.272067` |

## Runtime Evidence

- ONNX probability parity(온닉스 확률 동등성): passed(통과), Tier A max abs diff(Tier A 최대 절대 차이) `0.000000199064`, Tier B `0.000000221100`
- MT5 routed validation(라우팅 검증): `21` trades(거래), max DD(최대 손실) `587.48`, recovery(회복계수) `-0.84`
- MT5 routed OOS(라우팅 표본외): `33` trades(거래), max DD(최대 손실) `401.55`, recovery(회복계수) `-0.54`
- Tier B fallback used(Tier B 대체 사용): validation(검증) `32`, OOS(표본외) `64`

## Judgment

판정(judgment, 판정): `inconclusive_label_horizon_fwd18_retrain_scout_mt5_runtime_probe_completed`.

해석(read, 판독): fwd18(90분) 자체는 구조 탐침에서 좋아 보였지만, 일반 LGBM 재학습과 기존 run01Y threshold(임계값)로 MT5에 연결하면 거래 품질이 회복되지 않는다. 효과(effect, 효과)는 “fwd18만 바꾸면 된다”는 단순 가설을 낮추고, 다음 탐색을 fwd18 + context/rank threshold(문맥/순위 임계값)로 좁히는 것이다.

## Boundary

이 결과는 negative runtime_probe(부정 런타임 탐침)로 읽는다. invalid(무효)는 아니다. alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위)는 아니다.
