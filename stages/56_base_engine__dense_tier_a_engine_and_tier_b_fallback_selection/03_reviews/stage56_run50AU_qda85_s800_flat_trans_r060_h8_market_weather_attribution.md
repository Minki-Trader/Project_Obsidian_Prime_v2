# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - qda85_s800_flat_trans_r060_h8

- run_id(실행 ID): `run50AU_qda85_s800_flat_trans_r060_h8_composite_route_density_repair_v1`
- variant_id(변형 ID): `qda85_s800_flat_trans_r060_h8`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 963 | 277.91 | 0.666667 | 32.634597 |
| oos | 661 | 213.64 | 0.571429 | 36.658094 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `mid 157.59, late 70.32, early 50.0` / worst(최악) `early 50.0, late 70.32, mid 157.59`
- volatility_regime: best(최상) `vol_mid 119.6, vol_high 112.31, vol_low 46.0` / worst(최악) `vol_low 46.0, vol_high 112.31, vol_mid 119.6`
- trend_regime: best(최상) `downtrend 363.87, range_or_weak_trend -85.96` / worst(최악) `range_or_weak_trend -85.96, downtrend 363.87`
- adx_bucket: best(최상) `adx_gt25 273.03, adx_20_25 90.84, adx_lt20 -85.96` / worst(최악) `adx_lt20 -85.96, adx_20_25 90.84, adx_gt25 273.03`
- spread_regime: best(최상) `spread_low 277.91` / worst(최악) `spread_low 277.91`

### oos
- session_slice: best(최상) `early 199.72, late 64.18, mid -50.26` / worst(최악) `mid -50.26, late 64.18, early 199.72`
- volatility_regime: best(최상) `vol_high 104.39, vol_mid 85.35, vol_low 23.9` / worst(최악) `vol_low 23.9, vol_mid 85.35, vol_high 104.39`
- trend_regime: best(최상) `range_or_weak_trend 233.75, downtrend -20.11` / worst(최악) `downtrend -20.11, range_or_weak_trend 233.75`
- adx_bucket: best(최상) `adx_lt20 233.75, adx_gt25 19.92, adx_20_25 -40.03` / worst(최악) `adx_20_25 -40.03, adx_gt25 19.92, adx_lt20 233.75`
- spread_regime: best(최상) `spread_low 213.64` / worst(최악) `spread_low 213.64`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
