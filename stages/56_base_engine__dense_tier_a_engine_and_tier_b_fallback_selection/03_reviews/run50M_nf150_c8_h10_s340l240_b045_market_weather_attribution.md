# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nf150_c8_h10_s340l240_b045

- run_id(실행 ID): `run50M_nf150_c8_h10_s340l240_b045_logreg_deep_v1`
- variant_id(변형 ID): `nf150_c8_h10_s340l240_b045`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1174 | 91.64 | 0.666667 | 38.58111 |
| oos | 793 | 233.06 | 0.571429 | 44.678436 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `mid 77.72, late 55.82, early -41.9` / worst(최악) `early -41.9, late 55.82, mid 77.72`
- volatility_regime: best(최상) `vol_mid 157.37, feature_missing 5.39, vol_high -23.13` / worst(최악) `vol_low -47.99, vol_high -23.13, feature_missing 5.39`
- trend_regime: best(최상) `downtrend 285.46, feature_missing 5.39, range_or_weak_trend -199.21` / worst(최악) `range_or_weak_trend -199.21, feature_missing 5.39, downtrend 285.46`
- adx_bucket: best(최상) `adx_gt25 265.23, adx_20_25 20.23, feature_missing 5.39` / worst(최악) `adx_lt20 -199.21, feature_missing 5.39, adx_20_25 20.23`
- spread_regime: best(최상) `spread_low 91.64` / worst(최악) `spread_low 91.64`

### oos
- session_slice: best(최상) `early 172.62, late 32.08, mid 28.36` / worst(최악) `mid 28.36, late 32.08, early 172.62`
- volatility_regime: best(최상) `vol_mid 155.52, vol_high 153.19, feature_missing 29.17` / worst(최악) `vol_low -104.82, feature_missing 29.17, vol_high 153.19`
- trend_regime: best(최상) `range_or_weak_trend 255.35, feature_missing 29.17, downtrend -51.46` / worst(최악) `downtrend -51.46, feature_missing 29.17, range_or_weak_trend 255.35`
- adx_bucket: best(최상) `adx_lt20 255.35, feature_missing 29.17, adx_gt25 -21.31` / worst(최악) `adx_20_25 -30.15, adx_gt25 -21.31, feature_missing 29.17`
- spread_regime: best(최상) `spread_low 233.06` / worst(최악) `spread_low 233.06`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
