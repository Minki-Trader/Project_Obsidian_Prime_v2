# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - d390h10

- run_id(실행 ID): `run50D_d390h10_logreg_deep_v1`
- variant_id(변형 ID): `d390h10`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 748 | 341.54 | 0.666667 | 33.46123 |
| oos | 594 | 273.20 | 0.571429 | 30.372054 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 340.19, mid 76.67, late -75.32` / worst(최악) `late -75.32, mid 76.67, early 340.19`
- volatility_regime: best(최상) `vol_mid 137.76, vol_low 132.46, vol_high 92.11` / worst(최악) `feature_missing -20.79, vol_high 92.11, vol_low 132.46`
- trend_regime: best(최상) `downtrend 362.36, range_or_weak_trend -0.03, feature_missing -20.79` / worst(최악) `feature_missing -20.79, range_or_weak_trend -0.03, downtrend 362.36`
- adx_bucket: best(최상) `adx_gt25 487.32, adx_lt20 -0.03, feature_missing -20.79` / worst(최악) `adx_20_25 -124.96, feature_missing -20.79, adx_lt20 -0.03`
- spread_regime: best(최상) `spread_low 341.54` / worst(최악) `spread_low 341.54`

### oos
- session_slice: best(최상) `early 257.59, mid 76.44, late -60.83` / worst(최악) `late -60.83, mid 76.44, early 257.59`
- volatility_regime: best(최상) `vol_high 167.0, vol_low 94.86, feature_missing 48.87` / worst(최악) `vol_mid -37.53, feature_missing 48.87, vol_low 94.86`
- trend_regime: best(최상) `range_or_weak_trend 207.79, feature_missing 48.87, downtrend 16.54` / worst(최악) `downtrend 16.54, feature_missing 48.87, range_or_weak_trend 207.79`
- adx_bucket: best(최상) `adx_lt20 207.79, adx_20_25 66.83, feature_missing 48.87` / worst(최악) `adx_gt25 -50.29, feature_missing 48.87, adx_20_25 66.83`
- spread_regime: best(최상) `spread_low 273.2` / worst(최악) `spread_low 273.2`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
