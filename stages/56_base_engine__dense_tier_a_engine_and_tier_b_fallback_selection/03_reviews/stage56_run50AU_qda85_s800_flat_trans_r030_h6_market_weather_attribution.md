# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - qda85_s800_flat_trans_r030_h6

- run_id(실행 ID): `run50AU_qda85_s800_flat_trans_r030_h6_composite_route_density_repair_v1`
- variant_id(변형 ID): `qda85_s800_flat_trans_r030_h6`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1231 | 165.43 | 0.666667 | 28.904151 |
| oos | 859 | 142.01 | 0.571429 | 32.395844 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 161.41, mid 28.19, late -24.17` / worst(최악) `late -24.17, mid 28.19, early 161.41`
- volatility_regime: best(최상) `vol_low 100.59, vol_mid 92.08, vol_high -27.24` / worst(최악) `vol_high -27.24, vol_mid 92.08, vol_low 100.59`
- trend_regime: best(최상) `downtrend 253.72, range_or_weak_trend -88.29` / worst(최악) `range_or_weak_trend -88.29, downtrend 253.72`
- adx_bucket: best(최상) `adx_gt25 203.87, adx_20_25 49.85, adx_lt20 -88.29` / worst(최악) `adx_lt20 -88.29, adx_20_25 49.85, adx_gt25 203.87`
- spread_regime: best(최상) `spread_low 165.43` / worst(최악) `spread_low 165.43`

### oos
- session_slice: best(최상) `early 332.74, mid -65.85, late -124.88` / worst(최악) `late -124.88, mid -65.85, early 332.74`
- volatility_regime: best(최상) `vol_mid 155.12, vol_high 39.6, vol_low -52.71` / worst(최악) `vol_low -52.71, vol_high 39.6, vol_mid 155.12`
- trend_regime: best(최상) `range_or_weak_trend 135.88, downtrend 6.13` / worst(최악) `downtrend 6.13, range_or_weak_trend 135.88`
- adx_bucket: best(최상) `adx_lt20 135.88, adx_20_25 100.58, adx_gt25 -94.45` / worst(최악) `adx_gt25 -94.45, adx_20_25 100.58, adx_lt20 135.88`
- spread_regime: best(최상) `spread_low 142.01` / worst(최악) `spread_low 142.01`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
