# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nfw_s35l22_c2_sadx

- run_id(실행 ID): `run50W_nfw_s35l22_c2_sadx_logreg_deep_v1`
- variant_id(변형 ID): `nfw_s35l22_c2_sadx`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1498 | 600.73 | 0.777778 | 31.174301 |
| oos | 1137 | 139.96 | 0.571429 | 36.267364 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 270.34, early 257.54, mid 72.85` / worst(최악) `mid 72.85, early 257.54, late 270.34`
- volatility_regime: best(최상) `vol_high 454.53, vol_mid 78.69, vol_low 74.88` / worst(최악) `feature_missing -7.37, vol_low 74.88, vol_mid 78.69`
- trend_regime: best(최상) `downtrend 583.64, range_or_weak_trend 24.46, feature_missing -7.37` / worst(최악) `feature_missing -7.37, range_or_weak_trend 24.46, downtrend 583.64`
- adx_bucket: best(최상) `adx_gt25 433.37, adx_20_25 150.27, adx_lt20 24.46` / worst(최악) `feature_missing -7.37, adx_lt20 24.46, adx_20_25 150.27`
- spread_regime: best(최상) `spread_low 605.34, feature_missing -4.61` / worst(최악) `feature_missing -4.61, spread_low 605.34`

### oos
- session_slice: best(최상) `early 147.01, late 40.61, mid -47.66` / worst(최악) `mid -47.66, late 40.61, early 147.01`
- volatility_regime: best(최상) `vol_mid 128.21, feature_missing 29.34, vol_high 13.36` / worst(최악) `vol_low -30.95, vol_high 13.36, feature_missing 29.34`
- trend_regime: best(최상) `range_or_weak_trend 229.7, feature_missing 29.34, downtrend -119.08` / worst(최악) `downtrend -119.08, feature_missing 29.34, range_or_weak_trend 229.7`
- adx_bucket: best(최상) `adx_lt20 229.7, feature_missing 29.34, adx_20_25 -21.91` / worst(최악) `adx_gt25 -97.17, adx_20_25 -21.91, feature_missing 29.34`
- spread_regime: best(최상) `spread_low 139.96` / worst(최악) `spread_low 139.96`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
