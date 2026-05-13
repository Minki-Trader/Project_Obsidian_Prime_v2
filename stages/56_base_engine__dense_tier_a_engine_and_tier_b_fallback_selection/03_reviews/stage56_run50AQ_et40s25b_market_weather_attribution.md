# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et40s25b

- run_id(실행 ID): `run50AQ_et40s25b_logreg_deep_v1`
- variant_id(변형 ID): `et40s25b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 836 | 0.05 | 0.444444 | 28.708142 |
| oos | 661 | 540.59 | 1.0 | 23.239032 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 111.26, early -34.94, mid -76.27` / worst(최악) `mid -76.27, early -34.94, late 111.26`
- volatility_regime: best(최상) `vol_mid 126.42, feature_missing -8.44, vol_high -22.3` / worst(최악) `vol_low -95.63, vol_high -22.3, feature_missing -8.44`
- trend_regime: best(최상) `downtrend 130.24, feature_missing -8.44, range_or_weak_trend -121.75` / worst(최악) `range_or_weak_trend -121.75, feature_missing -8.44, downtrend 130.24`
- adx_bucket: best(최상) `adx_gt25 203.92, feature_missing -8.44, adx_20_25 -73.68` / worst(최악) `adx_lt20 -121.75, adx_20_25 -73.68, feature_missing -8.44`
- spread_regime: best(최상) `spread_low 0.05` / worst(최악) `spread_low 0.05`

### oos
- session_slice: best(최상) `early 418.19, late 140.47, mid -18.07` / worst(최악) `mid -18.07, late 140.47, early 418.19`
- volatility_regime: best(최상) `vol_mid 268.94, vol_high 130.55, vol_low 109.87` / worst(최악) `feature_missing 31.23, vol_low 109.87, vol_high 130.55`
- trend_regime: best(최상) `downtrend 265.72, range_or_weak_trend 243.64, feature_missing 31.23` / worst(최악) `feature_missing 31.23, range_or_weak_trend 243.64, downtrend 265.72`
- adx_bucket: best(최상) `adx_lt20 243.64, adx_20_25 139.59, adx_gt25 126.13` / worst(최악) `feature_missing 31.23, adx_gt25 126.13, adx_20_25 139.59`
- spread_regime: best(최상) `spread_low 540.59` / worst(최악) `spread_low 540.59`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
