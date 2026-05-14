# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et40h3c0_s240l150_r001_a

- run_id(실행 ID): `run50BI_et40h3c0_s240l150_r001_a_logreg_deep_v1`
- variant_id(변형 ID): `et40h3c0_s240l150_r001_a`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1557 | -114.55 | 0.333333 | 13.082214 |
| oos | 1250 | 284.70 | 1.0 | 10.213555 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `mid 64.53, late 52.99, early -232.07` / worst(최악) `early -232.07, late 52.99, mid 64.53`
- volatility_regime: best(최상) `vol_mid 152.91, vol_high -106.02, vol_low -161.44` / worst(최악) `vol_low -161.44, vol_high -106.02, vol_mid 152.91`
- trend_regime: best(최상) `range_or_weak_trend -12.34, downtrend -102.21` / worst(최악) `downtrend -102.21, range_or_weak_trend -12.34`
- adx_bucket: best(최상) `adx_lt20 -12.34, adx_gt25 -14.1, adx_20_25 -88.11` / worst(최악) `adx_20_25 -88.11, adx_gt25 -14.1, adx_lt20 -12.34`
- spread_regime: best(최상) `spread_low -114.55` / worst(최악) `spread_low -114.55`

### oos
- session_slice: best(최상) `early 222.38, mid 74.9, late -12.58` / worst(최악) `late -12.58, mid 74.9, early 222.38`
- volatility_regime: best(최상) `vol_mid 299.11, vol_low 51.57, feature_missing -8.94` / worst(최악) `vol_high -57.04, feature_missing -8.94, vol_low 51.57`
- trend_regime: best(최상) `downtrend 165.29, range_or_weak_trend 128.35, feature_missing -8.94` / worst(최악) `feature_missing -8.94, range_or_weak_trend 128.35, downtrend 165.29`
- adx_bucket: best(최상) `adx_lt20 128.35, adx_20_25 95.29, adx_gt25 70.0` / worst(최악) `feature_missing -8.94, adx_gt25 70.0, adx_20_25 95.29`
- spread_regime: best(최상) `spread_low 293.64, feature_missing -8.94` / worst(최악) `feature_missing -8.94, spread_low 293.64`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
