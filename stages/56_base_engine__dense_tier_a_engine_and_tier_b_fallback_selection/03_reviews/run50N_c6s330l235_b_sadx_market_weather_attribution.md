# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - c6s330l235_b_sadx

- run_id(실행 ID): `run50N_c6s330l235_b_sadx_logreg_deep_v1`
- variant_id(변형 ID): `c6s330l235_b_sadx`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1134 | 256.42 | 0.444444 | 40.769929 |
| oos | 781 | 508.97 | 0.714286 | 43.051216 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 166.09, late 98.27, mid -7.94` / worst(최악) `mid -7.94, late 98.27, early 166.09`
- volatility_regime: best(최상) `vol_low 178.04, vol_high 109.48, feature_missing 11.99` / worst(최악) `vol_mid -43.09, feature_missing 11.99, vol_high 109.48`
- trend_regime: best(최상) `downtrend 422.43, feature_missing 11.99, range_or_weak_trend -178.0` / worst(최악) `range_or_weak_trend -178.0, feature_missing 11.99, downtrend 422.43`
- adx_bucket: best(최상) `adx_20_25 233.77, adx_gt25 188.66, feature_missing 11.99` / worst(최악) `adx_lt20 -178.0, feature_missing 11.99, adx_gt25 188.66`
- spread_regime: best(최상) `spread_low 253.15, feature_missing 3.27` / worst(최악) `feature_missing 3.27, spread_low 253.15`

### oos
- session_slice: best(최상) `early 265.6, late 180.84, mid 62.53` / worst(최악) `mid 62.53, late 180.84, early 265.6`
- volatility_regime: best(최상) `vol_mid 267.09, vol_high 228.89, vol_low 27.93` / worst(최악) `feature_missing -14.94, vol_low 27.93, vol_high 228.89`
- trend_regime: best(최상) `range_or_weak_trend 482.74, downtrend 41.17, feature_missing -14.94` / worst(최악) `feature_missing -14.94, downtrend 41.17, range_or_weak_trend 482.74`
- adx_bucket: best(최상) `adx_lt20 482.74, adx_gt25 87.03, feature_missing -14.94` / worst(최악) `adx_20_25 -45.86, feature_missing -14.94, adx_gt25 87.03`
- spread_regime: best(최상) `spread_low 508.97` / worst(최악) `spread_low 508.97`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
