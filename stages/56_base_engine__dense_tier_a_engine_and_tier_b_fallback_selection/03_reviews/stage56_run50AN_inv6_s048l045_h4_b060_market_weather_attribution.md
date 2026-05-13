# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - inv6_s048l045_h4_b060

- run_id(실행 ID): `run50AN_inv6_s048l045_h4_b060_lgbm_fwd6_v1`
- variant_id(변형 ID): `inv6_s048l045_h4_b060`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 762 | 223.57 | 0.666667 | 11.335958 |
| oos | 549 | 258.00 | 0.571429 | 20.870777 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 174.74, outside_cash_session 86.55, mid 4.06` / worst(최악) `early -41.78, mid 4.06, outside_cash_session 86.55`
- volatility_regime: best(최상) `vol_high 296.78, vol_low 0.49, vol_mid -73.7` / worst(최악) `vol_mid -73.7, vol_low 0.49, vol_high 296.78`
- trend_regime: best(최상) `range_or_weak_trend 303.64, downtrend -80.07` / worst(최악) `downtrend -80.07, range_or_weak_trend 303.64`
- adx_bucket: best(최상) `adx_lt20 303.64, adx_20_25 101.34, adx_gt25 -181.41` / worst(최악) `adx_gt25 -181.41, adx_20_25 101.34, adx_lt20 303.64`
- spread_regime: best(최상) `spread_low 223.57` / worst(최악) `spread_low 223.57`

### oos
- session_slice: best(최상) `late 100.79, mid 100.23, early 57.19` / worst(최악) `outside_cash_session -0.21, early 57.19, mid 100.23`
- volatility_regime: best(최상) `vol_high 285.1, vol_mid 10.17, vol_low -37.27` / worst(최악) `vol_low -37.27, vol_mid 10.17, vol_high 285.1`
- trend_regime: best(최상) `range_or_weak_trend 133.46, downtrend 124.54` / worst(최악) `downtrend 124.54, range_or_weak_trend 133.46`
- adx_bucket: best(최상) `adx_gt25 135.78, adx_lt20 133.46, adx_20_25 -11.24` / worst(최악) `adx_20_25 -11.24, adx_lt20 133.46, adx_gt25 135.78`
- spread_regime: best(최상) `spread_low 258.0` / worst(최악) `spread_low 258.0`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
