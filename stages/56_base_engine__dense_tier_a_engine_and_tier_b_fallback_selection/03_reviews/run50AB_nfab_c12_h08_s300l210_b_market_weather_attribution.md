# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nfab_c12_h08_s300l210_b

- run_id(실행 ID): `run50AB_nfab_c12_h08_s300l210_b_logreg_deep_v1`
- variant_id(변형 ID): `nfab_c12_h08_s300l210_b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 925 | 71.06 | 0.444444 | 34.803236 |
| oos | 669 | 139.42 | 0.428571 | 36.022377 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 100.44, mid 47.31, early -76.69` / worst(최악) `early -76.69, mid 47.31, late 100.44`
- volatility_regime: best(최상) `vol_mid 65.2, vol_high 54.84, feature_missing 1.37` / worst(최악) `vol_low -50.35, feature_missing 1.37, vol_high 54.84`
- trend_regime: best(최상) `downtrend 101.25, feature_missing 1.37, range_or_weak_trend -31.56` / worst(최악) `range_or_weak_trend -31.56, feature_missing 1.37, downtrend 101.25`
- adx_bucket: best(최상) `adx_gt25 141.89, feature_missing 1.37, adx_lt20 -31.56` / worst(최악) `adx_20_25 -40.64, adx_lt20 -31.56, feature_missing 1.37`
- spread_regime: best(최상) `spread_low 71.06` / worst(최악) `spread_low 71.06`

### oos
- session_slice: best(최상) `late 111.87, early 58.28, mid -30.73` / worst(최악) `mid -30.73, early 58.28, late 111.87`
- volatility_regime: best(최상) `vol_high 101.26, vol_mid 32.67, vol_low 15.11` / worst(최악) `feature_missing -9.62, vol_low 15.11, vol_mid 32.67`
- trend_regime: best(최상) `range_or_weak_trend 204.37, feature_missing -9.62, downtrend -55.33` / worst(최악) `downtrend -55.33, feature_missing -9.62, range_or_weak_trend 204.37`
- adx_bucket: best(최상) `adx_lt20 204.37, feature_missing -9.62, adx_20_25 -22.81` / worst(최악) `adx_gt25 -32.52, adx_20_25 -22.81, feature_missing -9.62`
- spread_regime: best(최상) `spread_low 142.04, feature_missing -2.62` / worst(최악) `feature_missing -2.62, spread_low 142.04`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
