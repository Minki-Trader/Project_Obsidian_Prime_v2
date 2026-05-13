# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - inv6_s045l045_h3_b060

- run_id(실행 ID): `run50AN_inv6_s045l045_h3_b060_lgbm_fwd6_v1`
- variant_id(변형 ID): `inv6_s045l045_h3_b060`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 983 | 265.28 | 0.555556 | 8.819149 |
| oos | 707 | 84.42 | 0.428571 | 14.077713 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 246.12, late 82.16, mid -26.91` / worst(최악) `outside_cash_session -36.09, mid -26.91, late 82.16`
- volatility_regime: best(최상) `vol_high 331.42, vol_mid 12.95, feature_missing -5.18` / worst(최악) `vol_low -73.91, feature_missing -5.18, vol_mid 12.95`
- trend_regime: best(최상) `range_or_weak_trend 238.37, downtrend 32.09, feature_missing -5.18` / worst(최악) `feature_missing -5.18, downtrend 32.09, range_or_weak_trend 238.37`
- adx_bucket: best(최상) `adx_lt20 238.37, adx_20_25 189.85, feature_missing -5.18` / worst(최악) `adx_gt25 -157.76, feature_missing -5.18, adx_20_25 189.85`
- spread_regime: best(최상) `spread_low 265.28` / worst(최악) `spread_low 265.28`

### oos
- session_slice: best(최상) `outside_cash_session 94.65, mid 86.82, late 85.03` / worst(최악) `early -182.08, late 85.03, mid 86.82`
- volatility_regime: best(최상) `vol_high 178.88, feature_missing 7.94, vol_low -12.87` / worst(최악) `vol_mid -89.53, vol_low -12.87, feature_missing 7.94`
- trend_regime: best(최상) `range_or_weak_trend 75.92, feature_missing 7.94, downtrend 0.56` / worst(최악) `downtrend 0.56, feature_missing 7.94, range_or_weak_trend 75.92`
- adx_bucket: best(최상) `adx_lt20 75.92, adx_20_25 8.19, feature_missing 7.94` / worst(최악) `adx_gt25 -7.63, feature_missing 7.94, adx_20_25 8.19`
- spread_regime: best(최상) `spread_low 75.6, feature_missing 8.82` / worst(최악) `feature_missing 8.82, spread_low 75.6`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
