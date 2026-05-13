# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nf_vollow_h06_s350l240_b

- run_id(실행 ID): `run50T_nf_vollow_h06_s350l240_b_logreg_deep_v1`
- variant_id(변형 ID): `nf_vollow_h06_s350l240_b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1338 | 116.61 | 0.666667 | 22.783266 |
| oos | 1067 | 146.50 | 0.571429 | 24.671978 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 131.5, early 40.44, mid -55.33` / worst(최악) `mid -55.33, early 40.44, late 131.5`
- volatility_regime: best(최상) `vol_high 249.4, feature_missing 7.0, vol_mid -139.79` / worst(최악) `vol_mid -139.79, feature_missing 7.0, vol_high 249.4`
- trend_regime: best(최상) `downtrend 136.65, feature_missing 7.0, range_or_weak_trend -27.04` / worst(최악) `range_or_weak_trend -27.04, feature_missing 7.0, downtrend 136.65`
- adx_bucket: best(최상) `adx_gt25 294.76, feature_missing 7.0, adx_lt20 -27.04` / worst(최악) `adx_20_25 -158.11, adx_lt20 -27.04, feature_missing 7.0`
- spread_regime: best(최상) `spread_low 116.61` / worst(최악) `spread_low 116.61`

### oos
- session_slice: best(최상) `early 136.56, late 20.61, mid -10.67` / worst(최악) `mid -10.67, late 20.61, early 136.56`
- volatility_regime: best(최상) `vol_high 128.02, vol_mid 20.08, feature_missing -1.6` / worst(최악) `feature_missing -1.6, vol_mid 20.08, vol_high 128.02`
- trend_regime: best(최상) `range_or_weak_trend 187.36, feature_missing -1.6, downtrend -39.26` / worst(최악) `downtrend -39.26, feature_missing -1.6, range_or_weak_trend 187.36`
- adx_bucket: best(최상) `adx_lt20 187.36, adx_20_25 121.9, feature_missing -1.6` / worst(최악) `adx_gt25 -161.16, feature_missing -1.6, adx_20_25 121.9`
- spread_regime: best(최상) `spread_low 146.5` / worst(최악) `spread_low 146.5`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
