# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et40s25_c0_h6_a

- run_id(실행 ID): `run50AR_et40s25_c0_h6_a_logreg_deep_v1`
- variant_id(변형 ID): `et40s25_c0_h6_a`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1355 | 147.86 | 0.333333 | 21.200738 |
| oos | 1073 | 655.40 | 0.857143 | 23.314073 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 105.26, late 55.2, mid -12.6` / worst(최악) `mid -12.6, late 55.2, early 105.26`
- volatility_regime: best(최상) `vol_high 105.74, vol_low 36.05, vol_mid 6.07` / worst(최악) `vol_mid 6.07, vol_low 36.05, vol_high 105.74`
- trend_regime: best(최상) `range_or_weak_trend 82.79, downtrend 65.07` / worst(최악) `downtrend 65.07, range_or_weak_trend 82.79`
- adx_bucket: best(최상) `adx_gt25 133.77, adx_lt20 82.79, adx_20_25 -68.7` / worst(최악) `adx_20_25 -68.7, adx_lt20 82.79, adx_gt25 133.77`
- spread_regime: best(최상) `spread_low 147.86` / worst(최악) `spread_low 147.86`

### oos
- session_slice: best(최상) `early 365.9, late 293.9, mid -4.4` / worst(최악) `mid -4.4, late 293.9, early 365.9`
- volatility_regime: best(최상) `vol_mid 359.85, vol_low 163.19, vol_high 132.36` / worst(최악) `vol_high 132.36, vol_low 163.19, vol_mid 359.85`
- trend_regime: best(최상) `downtrend 367.28, range_or_weak_trend 288.12` / worst(최악) `range_or_weak_trend 288.12, downtrend 367.28`
- adx_bucket: best(최상) `adx_lt20 288.12, adx_gt25 194.76, adx_20_25 172.52` / worst(최악) `adx_20_25 172.52, adx_gt25 194.76, adx_lt20 288.12`
- spread_regime: best(최상) `spread_low 655.4` / worst(최악) `spread_low 655.4`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
