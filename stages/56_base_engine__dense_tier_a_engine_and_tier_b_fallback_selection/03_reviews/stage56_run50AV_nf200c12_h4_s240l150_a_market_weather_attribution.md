# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nf200c12_h4_s240l150_a

- run_id(실행 ID): `run50AV_nf200c12_h4_s240l150_a_logreg_deep_v1`
- variant_id(변형 ID): `nf200c12_h4_s240l150_a`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 786 | 435.08 | 0.555556 | 22.720971 |
| oos | 593 | 7.66 | 0.571429 | 26.514429 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 307.09, mid 87.82, early 40.17` / worst(최악) `early 40.17, mid 87.82, late 307.09`
- volatility_regime: best(최상) `vol_high 265.61, vol_mid 133.75, vol_low 36.67` / worst(최악) `feature_missing -0.95, vol_low 36.67, vol_mid 133.75`
- trend_regime: best(최상) `downtrend 379.18, range_or_weak_trend 56.85, feature_missing -0.95` / worst(최악) `feature_missing -0.95, range_or_weak_trend 56.85, downtrend 379.18`
- adx_bucket: best(최상) `adx_gt25 247.4, adx_20_25 131.78, adx_lt20 56.85` / worst(최악) `feature_missing -0.95, adx_lt20 56.85, adx_20_25 131.78`
- spread_regime: best(최상) `spread_low 436.03, feature_missing -0.95` / worst(최악) `feature_missing -0.95, spread_low 436.03`

### oos
- session_slice: best(최상) `early 96.47, mid 46.23, late -135.04` / worst(최악) `late -135.04, mid 46.23, early 96.47`
- volatility_regime: best(최상) `vol_high 89.91, vol_mid 16.87, vol_low -99.12` / worst(최악) `vol_low -99.12, vol_mid 16.87, vol_high 89.91`
- trend_regime: best(최상) `downtrend 13.63, range_or_weak_trend -5.97` / worst(최악) `range_or_weak_trend -5.97, downtrend 13.63`
- adx_bucket: best(최상) `adx_gt25 35.59, adx_lt20 -5.97, adx_20_25 -21.96` / worst(최악) `adx_20_25 -21.96, adx_lt20 -5.97, adx_gt25 35.59`
- spread_regime: best(최상) `spread_low 7.66` / worst(최악) `spread_low 7.66`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
