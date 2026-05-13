# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nf_h10c1_s390l280_b_sadx

- run_id(실행 ID): `run50Q_nf_h10c1_s390l280_b_sadx_logreg_deep_v1`
- variant_id(변형 ID): `nf_h10c1_s390l280_b_sadx`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1378 | -8.43 | 0.333333 | 42.093045 |
| oos | 995 | 99.37 | 0.428571 | 44.642204 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 22.17, late 16.35, mid -46.95` / worst(최악) `mid -46.95, late 16.35, early 22.17`
- volatility_regime: best(최상) `vol_mid 288.73, feature_missing -8.34, vol_low -99.56` / worst(최악) `vol_high -189.26, vol_low -99.56, feature_missing -8.34`
- trend_regime: best(최상) `downtrend 114.95, feature_missing -8.34, range_or_weak_trend -115.04` / worst(최악) `range_or_weak_trend -115.04, feature_missing -8.34, downtrend 114.95`
- adx_bucket: best(최상) `adx_gt25 228.54, feature_missing -8.34, adx_20_25 -113.59` / worst(최악) `adx_lt20 -115.04, adx_20_25 -113.59, feature_missing -8.34`
- spread_regime: best(최상) `spread_low -8.43` / worst(최악) `spread_low -8.43`

### oos
- session_slice: best(최상) `early 223.07, late -36.63, mid -87.07` / worst(최악) `mid -87.07, late -36.63, early 223.07`
- volatility_regime: best(최상) `vol_high 221.61, vol_mid 33.53, feature_missing -4.35` / worst(최악) `vol_low -151.42, feature_missing -4.35, vol_mid 33.53`
- trend_regime: best(최상) `range_or_weak_trend 100.85, downtrend 2.87, feature_missing -4.35` / worst(최악) `feature_missing -4.35, downtrend 2.87, range_or_weak_trend 100.85`
- adx_bucket: best(최상) `adx_lt20 100.85, adx_gt25 84.38, feature_missing -4.35` / worst(최악) `adx_20_25 -81.51, feature_missing -4.35, adx_gt25 84.38`
- spread_regime: best(최상) `spread_low 99.37` / worst(최악) `spread_low 99.37`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
