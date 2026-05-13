# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - lv26b

- run_id(실행 ID): `run50AD_lv26b_logreg_deep_v1`
- variant_id(변형 ID): `lv26b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 702 | 23.40 | 0.555556 | 28.649573 |
| oos | 494 | 312.41 | 0.714286 | 31.842105 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `mid 89.48, early -24.16, late -41.92` / worst(최악) `late -41.92, early -24.16, mid 89.48`
- volatility_regime: best(최상) `vol_low 39.17, vol_mid 29.69, feature_missing -1.63` / worst(최악) `vol_high -43.83, feature_missing -1.63, vol_mid 29.69`
- trend_regime: best(최상) `range_or_weak_trend 41.22, feature_missing -1.63, downtrend -16.19` / worst(최악) `downtrend -16.19, feature_missing -1.63, range_or_weak_trend 41.22`
- adx_bucket: best(최상) `adx_gt25 53.24, adx_lt20 41.22, feature_missing -1.63` / worst(최악) `adx_20_25 -69.43, feature_missing -1.63, adx_lt20 41.22`
- spread_regime: best(최상) `spread_low 23.4` / worst(최악) `spread_low 23.4`

### oos
- session_slice: best(최상) `early 213.26, late 82.82, mid 16.33` / worst(최악) `mid 16.33, late 82.82, early 213.26`
- volatility_regime: best(최상) `vol_high 256.21, vol_low 70.99, feature_missing -5.47` / worst(최악) `vol_mid -9.32, feature_missing -5.47, vol_low 70.99`
- trend_regime: best(최상) `downtrend 163.14, range_or_weak_trend 154.74, feature_missing -5.47` / worst(최악) `feature_missing -5.47, range_or_weak_trend 154.74, downtrend 163.14`
- adx_bucket: best(최상) `adx_lt20 154.74, adx_20_25 151.93, adx_gt25 11.21` / worst(최악) `feature_missing -5.47, adx_gt25 11.21, adx_20_25 151.93`
- spread_regime: best(최상) `spread_low 312.41` / worst(최악) `spread_low 312.41`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
