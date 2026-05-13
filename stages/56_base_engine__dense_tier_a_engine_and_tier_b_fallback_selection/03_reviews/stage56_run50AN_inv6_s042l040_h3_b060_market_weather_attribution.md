# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - inv6_s042l040_h3_b060

- run_id(실행 ID): `run50AN_inv6_s042l040_h3_b060_lgbm_fwd6_v1`
- variant_id(변형 ID): `inv6_s042l040_h3_b060`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1596 | -75.85 | 0.333333 | 9.403306 |
| oos | 1249 | -89.44 | 0.285714 | 12.552442 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 33.47, mid 27.38, late -36.58` / worst(최악) `outside_cash_session -100.12, late -36.58, mid 27.38`
- volatility_regime: best(최상) `vol_high 120.03, feature_missing 12.09, vol_low -29.29` / worst(최악) `vol_mid -178.68, vol_low -29.29, feature_missing 12.09`
- trend_regime: best(최상) `range_or_weak_trend 125.97, feature_missing 12.09, downtrend -213.91` / worst(최악) `downtrend -213.91, feature_missing 12.09, range_or_weak_trend 125.97`
- adx_bucket: best(최상) `adx_lt20 125.97, adx_20_25 94.93, feature_missing 12.09` / worst(최악) `adx_gt25 -308.84, feature_missing 12.09, adx_20_25 94.93`
- spread_regime: best(최상) `feature_missing 3.05, spread_low -78.9` / worst(최악) `spread_low -78.9, feature_missing 3.05`

### oos
- session_slice: best(최상) `late 76.59, mid 11.36, outside_cash_session -0.36` / worst(최악) `early -177.03, outside_cash_session -0.36, mid 11.36`
- volatility_regime: best(최상) `vol_high 39.83, feature_missing -10.15, vol_low -57.31` / worst(최악) `vol_mid -61.81, vol_low -57.31, feature_missing -10.15`
- trend_regime: best(최상) `range_or_weak_trend 96.81, feature_missing -10.15, downtrend -176.1` / worst(최악) `downtrend -176.1, feature_missing -10.15, range_or_weak_trend 96.81`
- adx_bucket: best(최상) `adx_lt20 96.81, feature_missing -10.15, adx_20_25 -62.72` / worst(최악) `adx_gt25 -113.38, adx_20_25 -62.72, feature_missing -10.15`
- spread_regime: best(최상) `spread_low -89.44` / worst(최악) `spread_low -89.44`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
