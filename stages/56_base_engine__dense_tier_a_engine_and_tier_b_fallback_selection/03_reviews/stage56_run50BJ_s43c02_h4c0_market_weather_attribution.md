# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - s43c02_h4c0

- run_id(실행 ID): `run50BJ_stage56_independent_event_source_cooldown_sweep_v1_s43c02_h4c0`
- variant_id(변형 ID): `s43c02_h4c0`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1353 | 363.02 | 0.555556 | 24.971914 |
| oos | 1092 | 156.49 | 0.571429 | 24.412137 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `late 306.44, mid 109.22, early -52.64` / worst(최악) `early -52.64, mid 109.22, late 306.44`
- volatility_regime: best(최상) `vol_high 211.07, vol_low 111.25, vol_mid 38.5` / worst(최악) `feature_missing 2.2, vol_mid 38.5, vol_low 111.25`
- trend_regime: best(최상) `downtrend 232.17, range_or_weak_trend 128.65, feature_missing 2.2` / worst(최악) `feature_missing 2.2, range_or_weak_trend 128.65, downtrend 232.17`
- adx_bucket: best(최상) `adx_20_25 144.78, adx_lt20 128.65, adx_gt25 87.39` / worst(최악) `feature_missing 2.2, adx_gt25 87.39, adx_lt20 128.65`
- spread_regime: best(최상) `spread_low 363.02` / worst(최악) `spread_low 363.02`

### oos
- session_slice: best(최상) `early 206.9, mid 77.46, late -127.87` / worst(최악) `late -127.87, mid 77.46, early 206.9`
- volatility_regime: best(최상) `vol_mid 230.03, vol_high 102.47, feature_missing 11.95` / worst(최악) `vol_low -187.96, feature_missing 11.95, vol_high 102.47`
- trend_regime: best(최상) `range_or_weak_trend 98.26, downtrend 46.28, feature_missing 11.95` / worst(최악) `feature_missing 11.95, downtrend 46.28, range_or_weak_trend 98.26`
- adx_bucket: best(최상) `adx_lt20 98.26, adx_gt25 32.43, adx_20_25 13.85` / worst(최악) `feature_missing 11.95, adx_20_25 13.85, adx_gt25 32.43`
- spread_regime: best(최상) `spread_low 156.49` / worst(최악) `spread_low 156.49`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
