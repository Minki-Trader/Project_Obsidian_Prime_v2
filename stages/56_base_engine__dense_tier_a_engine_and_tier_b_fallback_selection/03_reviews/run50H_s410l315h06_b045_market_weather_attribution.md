# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - s410l315h06_b045

- run_id(실행 ID): `run50H_s410l315h06_b045_logreg_deep_v1`
- variant_id(변형 ID): `s410l315h06_b045`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1033 | 240.62 | 0.777778 | 18.89062 |
| oos | 834 | 145.24 | 0.285714 | 20.139089 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 252.66, late 40.37, mid -52.41` / worst(최악) `mid -52.41, late 40.37, early 252.66`
- volatility_regime: best(최상) `vol_low 110.21, vol_high 89.73, vol_mid 41.13` / worst(최악) `feature_missing -0.45, vol_mid 41.13, vol_high 89.73`
- trend_regime: best(최상) `downtrend 162.94, range_or_weak_trend 78.13, feature_missing -0.45` / worst(최악) `feature_missing -0.45, range_or_weak_trend 78.13, downtrend 162.94`
- adx_bucket: best(최상) `adx_gt25 239.42, adx_lt20 78.13, feature_missing -0.45` / worst(최악) `adx_20_25 -76.48, feature_missing -0.45, adx_lt20 78.13`
- spread_regime: best(최상) `spread_low 240.62` / worst(최악) `spread_low 240.62`

### oos
- session_slice: best(최상) `early 174.22, mid 23.35, late -52.33` / worst(최악) `late -52.33, mid 23.35, early 174.22`
- volatility_regime: best(최상) `vol_mid 93.37, vol_high 54.74, feature_missing 25.46` / worst(최악) `vol_low -28.33, feature_missing 25.46, vol_high 54.74`
- trend_regime: best(최상) `range_or_weak_trend 118.83, feature_missing 25.46, downtrend 0.95` / worst(최악) `downtrend 0.95, feature_missing 25.46, range_or_weak_trend 118.83`
- adx_bucket: best(최상) `adx_lt20 118.83, adx_20_25 47.18, feature_missing 25.46` / worst(최악) `adx_gt25 -46.23, feature_missing 25.46, adx_20_25 47.18`
- spread_regime: best(최상) `spread_low 145.24` / worst(최악) `spread_low 145.24`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
