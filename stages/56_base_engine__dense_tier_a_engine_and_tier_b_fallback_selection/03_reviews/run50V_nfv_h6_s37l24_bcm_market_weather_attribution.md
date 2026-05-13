# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nfv_h6_s37l24_bcm

- run_id(실행 ID): `run50V_nfv_h6_s37l24_bcm_logreg_deep_v1`
- variant_id(변형 ID): `nfv_h6_s37l24_bcm`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1291 | 153.96 | 0.666667 | 23.93804 |
| oos | 1033 | 107.69 | 0.428571 | 24.569216 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 139.94, early 50.73, mid -36.71` / worst(최악) `mid -36.71, early 50.73, late 139.94`
- volatility_regime: best(최상) `vol_high 189.08, feature_missing 2.56, vol_mid -37.68` / worst(최악) `vol_mid -37.68, feature_missing 2.56, vol_high 189.08`
- trend_regime: best(최상) `downtrend 150.68, feature_missing 2.56, range_or_weak_trend 0.72` / worst(최악) `range_or_weak_trend 0.72, feature_missing 2.56, downtrend 150.68`
- adx_bucket: best(최상) `adx_gt25 250.09, feature_missing 2.56, adx_lt20 0.72` / worst(최악) `adx_20_25 -99.41, adx_lt20 0.72, feature_missing 2.56`
- spread_regime: best(최상) `spread_low 153.96` / worst(최악) `spread_low 153.96`

### oos
- session_slice: best(최상) `early 109.76, late 9.71, mid -11.78` / worst(최악) `mid -11.78, late 9.71, early 109.76`
- volatility_regime: best(최상) `vol_high 102.65, feature_missing 6.42, vol_mid -1.38` / worst(최악) `vol_mid -1.38, feature_missing 6.42, vol_high 102.65`
- trend_regime: best(최상) `range_or_weak_trend 134.54, feature_missing 6.42, downtrend -33.27` / worst(최악) `downtrend -33.27, feature_missing 6.42, range_or_weak_trend 134.54`
- adx_bucket: best(최상) `adx_lt20 134.54, feature_missing 6.42, adx_20_25 0.18` / worst(최악) `adx_gt25 -33.45, adx_20_25 0.18, feature_missing 6.42`
- spread_regime: best(최상) `spread_low 107.69` / worst(최악) `spread_low 107.69`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
