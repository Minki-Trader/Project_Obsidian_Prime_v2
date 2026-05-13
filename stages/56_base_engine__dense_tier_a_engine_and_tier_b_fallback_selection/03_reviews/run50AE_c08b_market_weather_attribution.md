# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - c08b

- run_id(실행 ID): `run50AE_c08b_logreg_deep_v1`
- variant_id(변형 ID): `c08b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 791 | 118.68 | 0.666667 | 32.632111 |
| oos | 615 | 330.59 | 0.857143 | 30.260163 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 105.8, mid 43.47, late -30.59` / worst(최악) `late -30.59, mid 43.47, early 105.8`
- volatility_regime: best(최상) `vol_mid 103.0, vol_high 78.25, feature_missing 11.09` / worst(최악) `vol_low -73.66, feature_missing 11.09, vol_high 78.25`
- trend_regime: best(최상) `downtrend 60.45, range_or_weak_trend 47.14, feature_missing 11.09` / worst(최악) `feature_missing 11.09, range_or_weak_trend 47.14, downtrend 60.45`
- adx_bucket: best(최상) `adx_gt25 148.28, adx_lt20 47.14, feature_missing 11.09` / worst(최악) `adx_20_25 -87.83, feature_missing 11.09, adx_lt20 47.14`
- spread_regime: best(최상) `spread_low 118.68` / worst(최악) `spread_low 118.68`

### oos
- session_slice: best(최상) `late 198.26, early 131.45, mid 0.88` / worst(최악) `mid 0.88, early 131.45, late 198.26`
- volatility_regime: best(최상) `vol_low 153.21, vol_high 123.33, vol_mid 38.3` / worst(최악) `feature_missing 15.75, vol_mid 38.3, vol_high 123.33`
- trend_regime: best(최상) `range_or_weak_trend 235.15, downtrend 79.69, feature_missing 15.75` / worst(최악) `feature_missing 15.75, downtrend 79.69, range_or_weak_trend 235.15`
- adx_bucket: best(최상) `adx_lt20 235.15, adx_gt25 42.53, adx_20_25 37.16` / worst(최악) `feature_missing 15.75, adx_20_25 37.16, adx_gt25 42.53`
- spread_regime: best(최상) `spread_low 330.59` / worst(최악) `spread_low 330.59`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
