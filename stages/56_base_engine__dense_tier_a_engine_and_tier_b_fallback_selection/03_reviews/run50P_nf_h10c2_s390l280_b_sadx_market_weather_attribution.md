# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nf_h10c2_s390l280_b_sadx

- run_id(실행 ID): `run50P_nf_h10c2_s390l280_b_sadx_logreg_deep_v1`
- variant_id(변형 ID): `nf_h10c2_s390l280_b_sadx`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1306 | 116.66 | 0.444444 | 44.77352 |
| oos | 928 | 140.04 | 0.428571 | 42.05926 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 64.1, early 36.77, mid 15.79` / worst(최악) `mid 15.79, early 36.77, late 64.1`
- volatility_regime: best(최상) `vol_mid 181.07, feature_missing -5.12, vol_low -13.71` / worst(최악) `vol_high -45.58, vol_low -13.71, feature_missing -5.12`
- trend_regime: best(최상) `downtrend 238.13, feature_missing -5.12, range_or_weak_trend -116.35` / worst(최악) `range_or_weak_trend -116.35, feature_missing -5.12, downtrend 238.13`
- adx_bucket: best(최상) `adx_gt25 159.37, adx_20_25 78.76, feature_missing -5.12` / worst(최악) `adx_lt20 -116.35, feature_missing -5.12, adx_20_25 78.76`
- spread_regime: best(최상) `spread_low 116.66` / worst(최악) `spread_low 116.66`

### oos
- session_slice: best(최상) `early 155.14, late 91.52, mid -106.62` / worst(최악) `mid -106.62, late 91.52, early 155.14`
- volatility_regime: best(최상) `vol_high 219.42, vol_mid 84.25, feature_missing -17.68` / worst(최악) `vol_low -145.95, feature_missing -17.68, vol_mid 84.25`
- trend_regime: best(최상) `range_or_weak_trend 86.61, downtrend 71.11, feature_missing -17.68` / worst(최악) `feature_missing -17.68, downtrend 71.11, range_or_weak_trend 86.61`
- adx_bucket: best(최상) `adx_lt20 86.61, adx_gt25 70.08, adx_20_25 1.03` / worst(최악) `feature_missing -17.68, adx_20_25 1.03, adx_gt25 70.08`
- spread_regime: best(최상) `spread_low 140.04` / worst(최악) `spread_low 140.04`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
