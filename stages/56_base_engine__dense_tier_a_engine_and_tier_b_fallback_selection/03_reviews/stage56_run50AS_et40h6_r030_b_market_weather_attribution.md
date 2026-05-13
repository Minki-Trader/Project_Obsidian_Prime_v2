# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et40h6_r030_b

- run_id(실행 ID): `run50AS_et40h6_r030_b_logreg_deep_v1`
- variant_id(변형 ID): `et40h6_r030_b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1022 | 385.93 | 0.333333 | 19.688845 |
| oos | 759 | 639.18 | 0.857143 | 20.736495 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 190.35, mid 127.69, late 67.89` / worst(최악) `late 67.89, mid 127.69, early 190.35`
- volatility_regime: best(최상) `vol_high 388.83, vol_low 75.97, feature_missing -7.72` / worst(최악) `vol_mid -71.15, feature_missing -7.72, vol_low 75.97`
- trend_regime: best(최상) `downtrend 308.59, range_or_weak_trend 85.06, feature_missing -7.72` / worst(최악) `feature_missing -7.72, range_or_weak_trend 85.06, downtrend 308.59`
- adx_bucket: best(최상) `adx_gt25 275.6, adx_lt20 85.06, adx_20_25 32.99` / worst(최악) `feature_missing -7.72, adx_20_25 32.99, adx_lt20 85.06`
- spread_regime: best(최상) `spread_low 385.93` / worst(최악) `spread_low 385.93`

### oos
- session_slice: best(최상) `late 338.41, early 280.2, mid 20.57` / worst(최악) `mid 20.57, early 280.2, late 338.41`
- volatility_regime: best(최상) `vol_mid 397.7, vol_low 199.28, feature_missing 24.75` / worst(최악) `vol_high 17.45, feature_missing 24.75, vol_low 199.28`
- trend_regime: best(최상) `downtrend 338.07, range_or_weak_trend 276.36, feature_missing 24.75` / worst(최악) `feature_missing 24.75, range_or_weak_trend 276.36, downtrend 338.07`
- adx_bucket: best(최상) `adx_lt20 276.36, adx_gt25 197.37, adx_20_25 140.7` / worst(최악) `feature_missing 24.75, adx_20_25 140.7, adx_gt25 197.37`
- spread_regime: best(최상) `spread_low 639.18` / worst(최악) `spread_low 639.18`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
