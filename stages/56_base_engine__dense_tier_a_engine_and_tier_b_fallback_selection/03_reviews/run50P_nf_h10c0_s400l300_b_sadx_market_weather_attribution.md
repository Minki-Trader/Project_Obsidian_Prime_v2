# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nf_h10c0_s400l300_b_sadx

- run_id(실행 ID): `run50P_nf_h10c0_s400l300_b_sadx_logreg_deep_v1`
- variant_id(변형 ID): `nf_h10c0_s400l300_b_sadx`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1425 | 150.62 | 0.444444 | 43.891855 |
| oos | 1035 | -80.51 | 0.428571 | 45.338161 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 120.86, late 31.97, mid -2.21` / worst(최악) `mid -2.21, late 31.97, early 120.86`
- volatility_regime: best(최상) `vol_mid 194.5, feature_missing -9.29, vol_high -13.62` / worst(최악) `vol_low -20.97, vol_high -13.62, feature_missing -9.29`
- trend_regime: best(최상) `downtrend 180.99, feature_missing -9.29, range_or_weak_trend -21.08` / worst(최악) `range_or_weak_trend -21.08, feature_missing -9.29, downtrend 180.99`
- adx_bucket: best(최상) `adx_gt25 287.26, feature_missing -9.29, adx_lt20 -21.08` / worst(최악) `adx_20_25 -106.27, adx_lt20 -21.08, feature_missing -9.29`
- spread_regime: best(최상) `spread_low 159.03, feature_missing -8.41` / worst(최악) `feature_missing -8.41, spread_low 159.03`

### oos
- session_slice: best(최상) `early 204.2, mid -73.26, late -211.45` / worst(최악) `late -211.45, mid -73.26, early 204.2`
- volatility_regime: best(최상) `vol_high 169.46, feature_missing 11.82, vol_mid -49.49` / worst(최악) `vol_low -212.3, vol_mid -49.49, feature_missing 11.82`
- trend_regime: best(최상) `range_or_weak_trend 112.63, feature_missing 11.82, downtrend -204.96` / worst(최악) `downtrend -204.96, feature_missing 11.82, range_or_weak_trend 112.63`
- adx_bucket: best(최상) `adx_lt20 112.63, adx_20_25 75.47, feature_missing 11.82` / worst(최악) `adx_gt25 -280.43, feature_missing 11.82, adx_20_25 75.47`
- spread_regime: best(최상) `spread_low -80.51` / worst(최악) `spread_low -80.51`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
