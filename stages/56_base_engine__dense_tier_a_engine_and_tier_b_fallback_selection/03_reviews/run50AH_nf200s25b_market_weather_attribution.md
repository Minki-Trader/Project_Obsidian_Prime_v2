# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - nf200s25b

- run_id(실행 ID): `run50AH_nf200s25b_logreg_deep_v1`
- variant_id(변형 ID): `nf200s25b`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1009 | 459.98 | 0.777778 | 40.109333 |
| oos | 739 | 428.88 | 0.857143 | 41.240898 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 240.08, late 212.96, mid 6.94` / worst(최악) `mid 6.94, late 212.96, early 240.08`
- volatility_regime: best(최상) `vol_high 328.43, vol_low 81.79, vol_mid 39.36` / worst(최악) `feature_missing 10.4, vol_mid 39.36, vol_low 81.79`
- trend_regime: best(최상) `downtrend 352.57, range_or_weak_trend 97.01, feature_missing 10.4` / worst(최악) `feature_missing 10.4, range_or_weak_trend 97.01, downtrend 352.57`
- adx_bucket: best(최상) `adx_20_25 223.85, adx_gt25 128.72, adx_lt20 97.01` / worst(최악) `feature_missing 10.4, adx_lt20 97.01, adx_gt25 128.72`
- spread_regime: best(최상) `spread_low 459.98` / worst(최악) `spread_low 459.98`

### oos
- session_slice: best(최상) `early 283.03, late 108.05, mid 37.8` / worst(최악) `mid 37.8, late 108.05, early 283.03`
- volatility_regime: best(최상) `vol_high 183.33, vol_mid 169.51, vol_low 62.4` / worst(최악) `feature_missing 13.64, vol_low 62.4, vol_mid 169.51`
- trend_regime: best(최상) `range_or_weak_trend 237.65, downtrend 177.59, feature_missing 13.64` / worst(최악) `feature_missing 13.64, downtrend 177.59, range_or_weak_trend 237.65`
- adx_bucket: best(최상) `adx_lt20 237.65, adx_gt25 137.35, adx_20_25 40.24` / worst(최악) `feature_missing 13.64, adx_20_25 40.24, adx_gt25 137.35`
- spread_regime: best(최상) `spread_low 428.88` / worst(최악) `spread_low 428.88`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
