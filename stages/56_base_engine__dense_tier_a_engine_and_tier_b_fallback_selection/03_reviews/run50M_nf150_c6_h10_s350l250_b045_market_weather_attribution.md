# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nf150_c6_h10_s350l250_b045

- run_id(실행 ID): `run50M_nf150_c6_h10_s350l250_b045_logreg_deep_v1`
- variant_id(변형 ID): `nf150_c6_h10_s350l250_b045`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1264 | 26.31 | 0.666667 | 36.417009 |
| oos | 864 | 590.30 | 0.714286 | 39.008094 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `mid 102.38, early 101.86, late -177.93` / worst(최악) `late -177.93, early 101.86, mid 102.38`
- volatility_regime: best(최상) `vol_low 35.33, vol_high 21.81, feature_missing 9.24` / worst(최악) `vol_mid -40.07, feature_missing 9.24, vol_high 21.81`
- trend_regime: best(최상) `downtrend 93.88, feature_missing 9.24, range_or_weak_trend -76.81` / worst(최악) `range_or_weak_trend -76.81, feature_missing 9.24, downtrend 93.88`
- adx_bucket: best(최상) `adx_gt25 207.84, feature_missing 9.24, adx_lt20 -76.81` / worst(최악) `adx_20_25 -113.96, adx_lt20 -76.81, feature_missing 9.24`
- spread_regime: best(최상) `spread_low 23.04, feature_missing 3.27` / worst(최악) `feature_missing 3.27, spread_low 23.04`

### oos
- session_slice: best(최상) `late 275.04, early 216.85, mid 98.41` / worst(최악) `mid 98.41, early 216.85, late 275.04`
- volatility_regime: best(최상) `vol_high 342.49, vol_mid 169.13, vol_low 94.3` / worst(최악) `feature_missing -15.62, vol_low 94.3, vol_mid 169.13`
- trend_regime: best(최상) `range_or_weak_trend 542.96, downtrend 62.96, feature_missing -15.62` / worst(최악) `feature_missing -15.62, downtrend 62.96, range_or_weak_trend 542.96`
- adx_bucket: best(최상) `adx_lt20 542.96, adx_gt25 106.17, feature_missing -15.62` / worst(최악) `adx_20_25 -43.21, feature_missing -15.62, adx_gt25 106.17`
- spread_regime: best(최상) `spread_low 590.3` / worst(최악) `spread_low 590.3`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
