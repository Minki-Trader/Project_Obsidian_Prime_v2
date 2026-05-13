# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nf_adxblk_c0_s380l270_b

- run_id(실행 ID): `run50R_nf_adxblk_c0_s380l270_b_logreg_deep_v1`
- variant_id(변형 ID): `nf_adxblk_c0_s380l270_b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1401 | 1.24 | 0.333333 | 40.131489 |
| oos | 1007 | 67.89 | 0.428571 | 45.696124 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `mid 71.93, late 49.54, early -120.23` / worst(최악) `early -120.23, late 49.54, mid 71.93`
- volatility_regime: best(최상) `vol_mid 128.59, vol_low -2.54, feature_missing -14.64` / worst(최악) `vol_high -110.17, feature_missing -14.64, vol_low -2.54`
- trend_regime: best(최상) `downtrend 206.52, feature_missing -14.64, range_or_weak_trend -190.64` / worst(최악) `range_or_weak_trend -190.64, feature_missing -14.64, downtrend 206.52`
- adx_bucket: best(최상) `adx_gt25 206.52, feature_missing -14.64, adx_lt20 -190.64` / worst(최악) `adx_lt20 -190.64, feature_missing -14.64, adx_gt25 206.52`
- spread_regime: best(최상) `spread_low 1.24` / worst(최악) `spread_low 1.24`

### oos
- session_slice: best(최상) `early 183.13, late -40.8, mid -74.44` / worst(최악) `mid -74.44, late -40.8, early 183.13`
- volatility_regime: best(최상) `vol_high 236.59, feature_missing 4.9, vol_mid -4.64` / worst(최악) `vol_low -168.96, vol_mid -4.64, feature_missing 4.9`
- trend_regime: best(최상) `range_or_weak_trend 196.4, feature_missing 4.9, downtrend -133.41` / worst(최악) `downtrend -133.41, feature_missing 4.9, range_or_weak_trend 196.4`
- adx_bucket: best(최상) `adx_lt20 196.4, feature_missing 4.9, adx_gt25 -133.41` / worst(최악) `adx_gt25 -133.41, feature_missing 4.9, adx_lt20 196.4`
- spread_regime: best(최상) `spread_low 67.89` / worst(최악) `spread_low 67.89`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
