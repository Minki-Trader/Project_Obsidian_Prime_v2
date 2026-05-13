# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - c6s330l235_a_sadx

- run_id(실행 ID): `run50N_c6s330l235_a_sadx_logreg_deep_v1`
- variant_id(변형 ID): `c6s330l235_a_sadx`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1047 | 238.73 | 0.666667 | 49.875931 |
| oos | 727 | 536.95 | 0.857143 | 48.938093 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `mid 180.85, early 104.7, late -46.82` / worst(최악) `late -46.82, early 104.7, mid 180.85`
- volatility_regime: best(최상) `vol_low 114.09, vol_high 77.29, vol_mid 44.08` / worst(최악) `feature_missing 3.27, vol_mid 44.08, vol_high 77.29`
- trend_regime: best(최상) `downtrend 234.17, feature_missing 3.27, range_or_weak_trend 1.29` / worst(최악) `range_or_weak_trend 1.29, feature_missing 3.27, downtrend 234.17`
- adx_bucket: best(최상) `adx_20_25 150.85, adx_gt25 83.32, feature_missing 3.27` / worst(최악) `adx_lt20 1.29, feature_missing 3.27, adx_gt25 83.32`
- spread_regime: best(최상) `spread_low 235.46, feature_missing 3.27` / worst(최악) `feature_missing 3.27, spread_low 235.46`

### oos
- session_slice: best(최상) `early 481.4, late 47.37, mid 8.18` / worst(최악) `mid 8.18, late 47.37, early 481.4`
- volatility_regime: best(최상) `vol_mid 256.91, vol_high 212.83, vol_low 67.21` / worst(최악) `vol_low 67.21, vol_high 212.83, vol_mid 256.91`
- trend_regime: best(최상) `range_or_weak_trend 344.36, downtrend 192.59` / worst(최악) `downtrend 192.59, range_or_weak_trend 344.36`
- adx_bucket: best(최상) `adx_lt20 344.36, adx_gt25 155.76, adx_20_25 36.83` / worst(최악) `adx_20_25 36.83, adx_gt25 155.76, adx_lt20 344.36`
- spread_regime: best(최상) `spread_low 536.95` / worst(최악) `spread_low 536.95`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
