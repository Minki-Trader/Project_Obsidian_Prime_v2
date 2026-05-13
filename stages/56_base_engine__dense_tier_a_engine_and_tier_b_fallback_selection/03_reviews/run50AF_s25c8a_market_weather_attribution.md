# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - s25c8a

- run_id(실행 ID): `run50AF_s25c8a_logreg_deep_v1`
- variant_id(변형 ID): `s25c8a`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 979 | 466.64 | 0.666667 | 40.755175 |
| oos | 711 | 417.57 | 0.714286 | 42.203929 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 210.03, early 167.94, mid 88.67` / worst(최악) `mid 88.67, early 167.94, late 210.03`
- volatility_regime: best(최상) `vol_high 317.92, vol_low 98.05, vol_mid 50.67` / worst(최악) `vol_mid 50.67, vol_low 98.05, vol_high 317.92`
- trend_regime: best(최상) `downtrend 343.31, range_or_weak_trend 123.33` / worst(최악) `range_or_weak_trend 123.33, downtrend 343.31`
- adx_bucket: best(최상) `adx_20_25 258.31, adx_lt20 123.33, adx_gt25 85.0` / worst(최악) `adx_gt25 85.0, adx_lt20 123.33, adx_20_25 258.31`
- spread_regime: best(최상) `spread_low 466.64` / worst(최악) `spread_low 466.64`

### oos
- session_slice: best(최상) `early 279.92, late 132.48, mid 5.17` / worst(최악) `mid 5.17, late 132.48, early 279.92`
- volatility_regime: best(최상) `vol_high 171.07, vol_mid 169.19, vol_low 77.31` / worst(최악) `vol_low 77.31, vol_mid 169.19, vol_high 171.07`
- trend_regime: best(최상) `range_or_weak_trend 231.78, downtrend 185.79` / worst(최악) `downtrend 185.79, range_or_weak_trend 231.78`
- adx_bucket: best(최상) `adx_lt20 231.78, adx_gt25 164.02, adx_20_25 21.77` / worst(최악) `adx_20_25 21.77, adx_gt25 164.02, adx_lt20 231.78`
- spread_regime: best(최상) `spread_low 417.57` / worst(최악) `spread_low 417.57`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
