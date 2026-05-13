# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et20h6_r030_b

- run_id(실행 ID): `run50AT_et20h6_r030_b_logreg_deep_v1`
- variant_id(변형 ID): `et20h6_r030_b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1095 | 346.02 | 0.444444 | 21.209132 |
| oos | 833 | 249.83 | 0.714286 | 22.266507 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 198.25, early 123.57, mid 24.2` / worst(최악) `mid 24.2, early 123.57, late 198.25`
- volatility_regime: best(최상) `vol_high 211.11, vol_mid 138.47, vol_low 10.23` / worst(최악) `feature_missing -13.79, vol_low 10.23, vol_mid 138.47`
- trend_regime: best(최상) `downtrend 222.54, range_or_weak_trend 137.27, feature_missing -13.79` / worst(최악) `feature_missing -13.79, range_or_weak_trend 137.27, downtrend 222.54`
- adx_bucket: best(최상) `adx_lt20 137.27, adx_gt25 119.29, adx_20_25 103.25` / worst(최악) `feature_missing -13.79, adx_20_25 103.25, adx_gt25 119.29`
- spread_regime: best(최상) `spread_low 347.85, feature_missing -1.83` / worst(최악) `feature_missing -1.83, spread_low 347.85`

### oos
- session_slice: best(최상) `early 249.78, mid 1.86, late -1.81` / worst(최악) `late -1.81, mid 1.86, early 249.78`
- volatility_regime: best(최상) `vol_mid 167.32, vol_low 81.58, feature_missing 16.84` / worst(최악) `vol_high -15.91, feature_missing 16.84, vol_low 81.58`
- trend_regime: best(최상) `range_or_weak_trend 152.48, downtrend 80.51, feature_missing 16.84` / worst(최악) `feature_missing 16.84, downtrend 80.51, range_or_weak_trend 152.48`
- adx_bucket: best(최상) `adx_20_25 175.72, adx_lt20 152.48, feature_missing 16.84` / worst(최악) `adx_gt25 -95.21, feature_missing 16.84, adx_lt20 152.48`
- spread_regime: best(최상) `spread_low 249.83` / worst(최악) `spread_low 249.83`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
