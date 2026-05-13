# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et40h6_r015_a

- run_id(실행 ID): `run50AS_et40h6_r015_a_logreg_deep_v1`
- variant_id(변형 ID): `et40h6_r015_a`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1094 | 317.78 | 0.333333 | 20.091301 |
| oos | 833 | 632.50 | 0.714286 | 21.585834 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 190.3, mid 112.15, late 15.33` / worst(최악) `late 15.33, mid 112.15, early 190.3`
- volatility_regime: best(최상) `vol_high 264.37, vol_low 80.24, feature_missing 2.22` / worst(최악) `vol_mid -29.05, feature_missing 2.22, vol_low 80.24`
- trend_regime: best(최상) `downtrend 280.12, range_or_weak_trend 35.44, feature_missing 2.22` / worst(최악) `feature_missing 2.22, range_or_weak_trend 35.44, downtrend 280.12`
- adx_bucket: best(최상) `adx_gt25 227.26, adx_20_25 52.86, adx_lt20 35.44` / worst(최악) `feature_missing 2.22, adx_lt20 35.44, adx_20_25 52.86`
- spread_regime: best(최상) `spread_low 315.56, feature_missing 2.22` / worst(최악) `feature_missing 2.22, spread_low 315.56`

### oos
- session_slice: best(최상) `late 306.41, early 256.35, mid 69.74` / worst(최악) `mid 69.74, early 256.35, late 306.41`
- volatility_regime: best(최상) `vol_mid 412.75, vol_low 154.71, vol_high 65.04` / worst(최악) `vol_high 65.04, vol_low 154.71, vol_mid 412.75`
- trend_regime: best(최상) `downtrend 371.17, range_or_weak_trend 261.33` / worst(최악) `range_or_weak_trend 261.33, downtrend 371.17`
- adx_bucket: best(최상) `adx_lt20 261.33, adx_gt25 197.22, adx_20_25 173.95` / worst(최악) `adx_20_25 173.95, adx_gt25 197.22, adx_lt20 261.33`
- spread_regime: best(최상) `spread_low 632.5` / worst(최악) `spread_low 632.5`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
