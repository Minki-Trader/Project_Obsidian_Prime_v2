# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et40c12_h4_s220l140_b

- run_id(실행 ID): `run50AV_et40c12_h4_s220l140_b_logreg_deep_v1`
- variant_id(변형 ID): `et40c12_h4_s220l140_b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 637 | -9.26 | 0.333333 | 15.926897 |
| oos | 521 | 184.80 | 0.571429 | 12.779271 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 72.15, early -6.75, mid -74.66` / worst(최악) `mid -74.66, early -6.75, late 72.15`
- volatility_regime: best(최상) `vol_mid 25.99, vol_low 2.56, feature_missing -2.23` / worst(최악) `vol_high -35.58, feature_missing -2.23, vol_low 2.56`
- trend_regime: best(최상) `downtrend 36.78, feature_missing -2.23, range_or_weak_trend -43.81` / worst(최악) `range_or_weak_trend -43.81, feature_missing -2.23, downtrend 36.78`
- adx_bucket: best(최상) `adx_gt25 94.11, feature_missing -2.23, adx_lt20 -43.81` / worst(최악) `adx_20_25 -57.33, adx_lt20 -43.81, feature_missing -2.23`
- spread_regime: best(최상) `spread_low -9.26` / worst(최악) `spread_low -9.26`

### oos
- session_slice: best(최상) `early 170.94, late 24.72, mid -10.86` / worst(최악) `mid -10.86, late 24.72, early 170.94`
- volatility_regime: best(최상) `vol_mid 60.62, vol_high 55.27, vol_low 45.64` / worst(최악) `feature_missing 23.27, vol_low 45.64, vol_high 55.27`
- trend_regime: best(최상) `downtrend 155.81, feature_missing 23.27, range_or_weak_trend 5.72` / worst(최악) `range_or_weak_trend 5.72, feature_missing 23.27, downtrend 155.81`
- adx_bucket: best(최상) `adx_gt25 104.35, adx_20_25 51.46, feature_missing 23.27` / worst(최악) `adx_lt20 5.72, feature_missing 23.27, adx_20_25 51.46`
- spread_regime: best(최상) `spread_low 184.8` / worst(최악) `spread_low 184.8`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
