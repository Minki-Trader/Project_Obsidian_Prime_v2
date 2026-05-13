# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et20h6_r015_b

- run_id(실행 ID): `run50AT_et20h6_r015_b_logreg_deep_v1`
- variant_id(변형 ID): `et20h6_r015_b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1205 | 220.66 | 0.444444 | 19.261411 |
| oos | 926 | 312.02 | 0.714286 | 21.812095 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 147.98, early 77.19, mid -4.51` / worst(최악) `mid -4.51, early 77.19, late 147.98`
- volatility_regime: best(최상) `vol_mid 182.35, vol_high 116.93, feature_missing -13.79` / worst(최악) `vol_low -64.83, feature_missing -13.79, vol_high 116.93`
- trend_regime: best(최상) `range_or_weak_trend 131.31, downtrend 103.14, feature_missing -13.79` / worst(최악) `feature_missing -13.79, downtrend 103.14, range_or_weak_trend 131.31`
- adx_bucket: best(최상) `adx_lt20 131.31, adx_20_25 75.01, adx_gt25 28.13` / worst(최악) `feature_missing -13.79, adx_gt25 28.13, adx_20_25 75.01`
- spread_regime: best(최상) `spread_low 222.49, feature_missing -1.83` / worst(최악) `feature_missing -1.83, spread_low 222.49`

### oos
- session_slice: best(최상) `early 364.75, mid 26.49, late -79.22` / worst(최악) `late -79.22, mid 26.49, early 364.75`
- volatility_regime: best(최상) `vol_mid 227.67, vol_low 82.04, feature_missing 16.84` / worst(최악) `vol_high -14.53, feature_missing 16.84, vol_low 82.04`
- trend_regime: best(최상) `downtrend 249.97, range_or_weak_trend 45.21, feature_missing 16.84` / worst(최악) `feature_missing 16.84, range_or_weak_trend 45.21, downtrend 249.97`
- adx_bucket: best(최상) `adx_20_25 195.07, adx_gt25 54.9, adx_lt20 45.21` / worst(최악) `feature_missing 16.84, adx_lt20 45.21, adx_gt25 54.9`
- spread_regime: best(최상) `spread_low 312.02` / worst(최악) `spread_low 312.02`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
