# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nfaa_s23l13_c6_l30_b

- run_id(실행 ID): `run50AA_nfaa_s23l13_c6_l30_b_logreg_deep_v1`
- variant_id(변형 ID): `nfaa_s23l13_c6_l30_b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 817 | 288.34 | 0.555556 | 38.394117 |
| oos | 589 | 308.82 | 0.571429 | 35.427736 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 228.53, mid 138.76, early -78.95` / worst(최악) `early -78.95, mid 138.76, late 228.53`
- volatility_regime: best(최상) `vol_high 299.45, vol_low 112.11, feature_missing 3.92` / worst(최악) `vol_mid -127.14, feature_missing 3.92, vol_low 112.11`
- trend_regime: best(최상) `downtrend 234.4, range_or_weak_trend 50.02, feature_missing 3.92` / worst(최악) `feature_missing 3.92, range_or_weak_trend 50.02, downtrend 234.4`
- adx_bucket: best(최상) `adx_gt25 303.81, adx_lt20 50.02, feature_missing 3.92` / worst(최악) `adx_20_25 -69.41, feature_missing 3.92, adx_lt20 50.02`
- spread_regime: best(최상) `spread_low 288.34` / worst(최악) `spread_low 288.34`

### oos
- session_slice: best(최상) `early 281.2, late 40.03, mid -12.41` / worst(최악) `mid -12.41, late 40.03, early 281.2`
- volatility_regime: best(최상) `vol_high 206.54, vol_mid 96.85, feature_missing 7.62` / worst(최악) `vol_low -2.19, feature_missing 7.62, vol_mid 96.85`
- trend_regime: best(최상) `range_or_weak_trend 234.13, downtrend 67.07, feature_missing 7.62` / worst(최악) `feature_missing 7.62, downtrend 67.07, range_or_weak_trend 234.13`
- adx_bucket: best(최상) `adx_lt20 234.13, adx_gt25 78.34, feature_missing 7.62` / worst(최악) `adx_20_25 -11.27, feature_missing 7.62, adx_gt25 78.34`
- spread_regime: best(최상) `spread_low 313.46, feature_missing -4.64` / worst(최악) `feature_missing -4.64, spread_low 313.46`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
