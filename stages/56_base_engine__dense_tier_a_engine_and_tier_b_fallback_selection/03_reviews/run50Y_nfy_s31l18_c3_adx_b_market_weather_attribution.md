# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nfy_s31l18_c3_adx_b

- run_id(실행 ID): `run50Y_nfy_s31l18_c3_adx_b_logreg_deep_v1`
- variant_id(변형 ID): `nfy_s31l18_c3_adx_b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 708 | 166.36 | 0.555556 | 42.391243 |
| oos | 512 | 378.86 | 0.571429 | 48.917969 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 255.62, mid 44.26, early -133.52` / worst(최악) `early -133.52, mid 44.26, late 255.62`
- volatility_regime: best(최상) `vol_high 134.74, vol_low 119.37, feature_missing 3.92` / worst(최악) `vol_mid -91.67, feature_missing 3.92, vol_low 119.37`
- trend_regime: best(최상) `range_or_weak_trend 98.7, downtrend 63.74, feature_missing 3.92` / worst(최악) `feature_missing 3.92, downtrend 63.74, range_or_weak_trend 98.7`
- adx_bucket: best(최상) `adx_lt20 98.7, adx_gt25 63.74, feature_missing 3.92` / worst(최악) `feature_missing 3.92, adx_gt25 63.74, adx_lt20 98.7`
- spread_regime: best(최상) `spread_low 166.36` / worst(최악) `spread_low 166.36`

### oos
- session_slice: best(최상) `early 147.51, late 131.69, mid 99.66` / worst(최악) `mid 99.66, late 131.69, early 147.51`
- volatility_regime: best(최상) `vol_high 191.09, vol_mid 116.99, vol_low 85.34` / worst(최악) `feature_missing -14.56, vol_low 85.34, vol_mid 116.99`
- trend_regime: best(최상) `downtrend 205.89, range_or_weak_trend 187.53, feature_missing -14.56` / worst(최악) `feature_missing -14.56, range_or_weak_trend 187.53, downtrend 205.89`
- adx_bucket: best(최상) `adx_gt25 205.89, adx_lt20 187.53, feature_missing -14.56` / worst(최악) `feature_missing -14.56, adx_lt20 187.53, adx_gt25 205.89`
- spread_regime: best(최상) `spread_low 378.86` / worst(최악) `spread_low 378.86`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
