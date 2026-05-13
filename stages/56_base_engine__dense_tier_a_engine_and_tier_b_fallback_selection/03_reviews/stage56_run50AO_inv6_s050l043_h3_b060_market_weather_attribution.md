# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - inv6_s050l043_h3_b060

- run_id(실행 ID): `run50AO_inv6_s050l043_h3_b060_lgbm_fwd6_v1`
- variant_id(변형 ID): `inv6_s050l043_h3_b060`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 966 | 318.69 | 0.666667 | 11.930759 |
| oos | 717 | 179.25 | 0.714286 | 13.196653 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 183.27, outside_cash_session 130.06, early 105.16` / worst(최악) `mid -99.8, early 105.16, outside_cash_session 130.06`
- volatility_regime: best(최상) `vol_high 357.45, vol_low 2.89, feature_missing 1.59` / worst(최악) `vol_mid -43.24, feature_missing 1.59, vol_low 2.89`
- trend_regime: best(최상) `range_or_weak_trend 349.41, feature_missing 1.59, downtrend -32.31` / worst(최악) `downtrend -32.31, feature_missing 1.59, range_or_weak_trend 349.41`
- adx_bucket: best(최상) `adx_lt20 349.41, adx_20_25 159.97, feature_missing 1.59` / worst(최악) `adx_gt25 -192.28, feature_missing 1.59, adx_20_25 159.97`
- spread_regime: best(최상) `spread_low 317.1, feature_missing 1.59` / worst(최악) `feature_missing 1.59, spread_low 317.1`

### oos
- session_slice: best(최상) `mid 78.04, outside_cash_session 62.19, late 52.6` / worst(최악) `early -13.58, late 52.6, outside_cash_session 62.19`
- volatility_regime: best(최상) `vol_high 90.6, vol_low 45.96, vol_mid 43.23` / worst(최악) `feature_missing -0.54, vol_mid 43.23, vol_low 45.96`
- trend_regime: best(최상) `downtrend 104.71, range_or_weak_trend 75.08, feature_missing -0.54` / worst(최악) `feature_missing -0.54, range_or_weak_trend 75.08, downtrend 104.71`
- adx_bucket: best(최상) `adx_gt25 144.67, adx_lt20 75.08, feature_missing -0.54` / worst(최악) `adx_20_25 -39.96, feature_missing -0.54, adx_lt20 75.08`
- spread_regime: best(최상) `spread_low 179.25` / worst(최악) `spread_low 179.25`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
