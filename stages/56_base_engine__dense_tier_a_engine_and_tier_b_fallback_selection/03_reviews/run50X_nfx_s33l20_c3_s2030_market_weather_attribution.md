# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nfx_s33l20_c3_s2030

- run_id(실행 ID): `run50X_nfx_s33l20_c3_s2030_logreg_deep_v1`
- variant_id(변형 ID): `nfx_s33l20_c3_s2030`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1317 | 451.99 | 0.666667 | 32.165624 |
| oos | 986 | 251.32 | 0.571429 | 34.314402 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 334.14, early 79.75, mid 38.1` / worst(최악) `mid 38.1, early 79.75, late 334.14`
- volatility_regime: best(최상) `vol_high 236.23, vol_mid 114.57, vol_low 107.31` / worst(최악) `feature_missing -6.12, vol_low 107.31, vol_mid 114.57`
- trend_regime: best(최상) `downtrend 304.42, range_or_weak_trend 153.69, feature_missing -6.12` / worst(최악) `feature_missing -6.12, range_or_weak_trend 153.69, downtrend 304.42`
- adx_bucket: best(최상) `adx_gt25 312.63, adx_lt20 153.69, feature_missing -6.12` / worst(최악) `adx_20_25 -8.21, feature_missing -6.12, adx_lt20 153.69`
- spread_regime: best(최상) `spread_low 451.99` / worst(최악) `spread_low 451.99`

### oos
- session_slice: best(최상) `early 214.45, late 62.38, mid -25.51` / worst(최악) `mid -25.51, late 62.38, early 214.45`
- volatility_regime: best(최상) `vol_mid 271.41, vol_high 115.27, feature_missing 6.05` / worst(최악) `vol_low -141.41, feature_missing 6.05, vol_high 115.27`
- trend_regime: best(최상) `range_or_weak_trend 192.14, downtrend 53.13, feature_missing 6.05` / worst(최악) `feature_missing 6.05, downtrend 53.13, range_or_weak_trend 192.14`
- adx_bucket: best(최상) `adx_lt20 192.14, adx_gt25 164.24, feature_missing 6.05` / worst(최악) `adx_20_25 -111.11, feature_missing 6.05, adx_gt25 164.24`
- spread_regime: best(최상) `spread_low 251.32` / worst(최악) `spread_low 251.32`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
