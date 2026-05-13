# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et40s25a

- run_id(실행 ID): `run50AQ_et40s25a_logreg_deep_v1`
- variant_id(변형 ID): `et40s25a`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 831 | -6.12 | 0.444444 | 28.685929 |
| oos | 639 | 473.93 | 1.0 | 24.388106 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 82.91, early -24.06, mid -64.97` / worst(최악) `mid -64.97, early -24.06, late 82.91`
- volatility_regime: best(최상) `vol_mid 83.3, vol_high -10.28, vol_low -79.14` / worst(최악) `vol_low -79.14, vol_high -10.28, vol_mid 83.3`
- trend_regime: best(최상) `downtrend 158.98, range_or_weak_trend -165.1` / worst(최악) `range_or_weak_trend -165.1, downtrend 158.98`
- adx_bucket: best(최상) `adx_gt25 226.07, adx_20_25 -67.09, adx_lt20 -165.1` / worst(최악) `adx_lt20 -165.1, adx_20_25 -67.09, adx_gt25 226.07`
- spread_regime: best(최상) `spread_low -6.12` / worst(최악) `spread_low -6.12`

### oos
- session_slice: best(최상) `early 296.32, late 235.65, mid -58.04` / worst(최악) `mid -58.04, late 235.65, early 296.32`
- volatility_regime: best(최상) `vol_mid 218.05, vol_low 145.76, vol_high 110.12` / worst(최악) `vol_high 110.12, vol_low 145.76, vol_mid 218.05`
- trend_regime: best(최상) `downtrend 248.06, range_or_weak_trend 225.87` / worst(최악) `range_or_weak_trend 225.87, downtrend 248.06`
- adx_bucket: best(최상) `adx_lt20 225.87, adx_gt25 144.85, adx_20_25 103.21` / worst(최악) `adx_20_25 103.21, adx_gt25 144.85, adx_lt20 225.87`
- spread_regime: best(최상) `spread_low 473.93` / worst(최악) `spread_low 473.93`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
