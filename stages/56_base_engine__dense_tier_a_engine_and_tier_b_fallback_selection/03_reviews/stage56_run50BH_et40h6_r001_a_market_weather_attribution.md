# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et40h6_r001_a

- run_id(실행 ID): `run50BH_et40h6_r001_a_logreg_deep_v1`
- variant_id(변형 ID): `et40h6_r001_a`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1253 | 313.49 | 0.333333 | 20.119713 |
| oos | 995 | 613.58 | 0.857143 | 20.38794 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 182.2, late 94.3, mid 36.99` / worst(최악) `mid 36.99, late 94.3, early 182.2`
- volatility_regime: best(최상) `vol_high 233.22, vol_low 52.34, vol_mid 27.93` / worst(최악) `vol_mid 27.93, vol_low 52.34, vol_high 233.22`
- trend_regime: best(최상) `downtrend 293.44, range_or_weak_trend 20.05` / worst(최악) `range_or_weak_trend 20.05, downtrend 293.44`
- adx_bucket: best(최상) `adx_gt25 283.07, adx_lt20 20.05, adx_20_25 10.37` / worst(최악) `adx_20_25 10.37, adx_lt20 20.05, adx_gt25 283.07`
- spread_regime: best(최상) `spread_low 313.49` / worst(최악) `spread_low 313.49`

### oos
- session_slice: best(최상) `early 341.63, late 273.0, mid -1.05` / worst(최악) `mid -1.05, late 273.0, early 341.63`
- volatility_regime: best(최상) `vol_mid 352.71, vol_high 150.27, vol_low 110.6` / worst(최악) `vol_low 110.6, vol_high 150.27, vol_mid 352.71`
- trend_regime: best(최상) `downtrend 366.18, range_or_weak_trend 247.4` / worst(최악) `range_or_weak_trend 247.4, downtrend 366.18`
- adx_bucket: best(최상) `adx_lt20 247.4, adx_20_25 185.79, adx_gt25 180.39` / worst(최악) `adx_gt25 180.39, adx_20_25 185.79, adx_lt20 247.4`
- spread_regime: best(최상) `spread_low 613.58` / worst(최악) `spread_low 613.58`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
