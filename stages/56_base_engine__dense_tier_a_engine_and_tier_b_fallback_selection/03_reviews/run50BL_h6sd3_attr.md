# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속) - et40h6sd3_s260l170_r001_a

- run_id(실행 ID): `run50BL_et40h6sd3_s260l170_r001_a_logreg_deep_v1`
- variant_id(변형 ID): `et40h6sd3_s260l170_r001_a`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 1097 | 65.68 | 0.444444 | 18.751139 |
| oos | 859 | 503.79 | 0.714286 | 21.641444 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `mid 41.79, early 37.56, late -13.67` / worst(최악) `late -13.67, early 37.56, mid 41.79`
- volatility_regime: best(최상) `vol_high 82.39, vol_low 9.47, vol_mid -26.18` / worst(최악) `vol_mid -26.18, vol_low 9.47, vol_high 82.39`
- trend_regime: best(최상) `range_or_weak_trend 69.54, downtrend -3.86` / worst(최악) `downtrend -3.86, range_or_weak_trend 69.54`
- adx_bucket: best(최상) `adx_lt20 69.54, adx_20_25 33.15, adx_gt25 -37.01` / worst(최악) `adx_gt25 -37.01, adx_20_25 33.15, adx_lt20 69.54`
- spread_regime: best(최상) `spread_low 65.68` / worst(최악) `spread_low 65.68`

### oos
- session_slice: best(최상) `early 288.27, late 210.95, mid 4.57` / worst(최악) `mid 4.57, late 210.95, early 288.27`
- volatility_regime: best(최상) `vol_mid 340.75, vol_high 119.7, vol_low 43.34` / worst(최악) `vol_low 43.34, vol_high 119.7, vol_mid 340.75`
- trend_regime: best(최상) `range_or_weak_trend 310.78, downtrend 193.01` / worst(최악) `downtrend 193.01, range_or_weak_trend 310.78`
- adx_bucket: best(최상) `adx_lt20 310.78, adx_20_25 128.61, adx_gt25 64.4` / worst(최악) `adx_gt25 64.4, adx_20_25 128.61, adx_lt20 310.78`
- spread_regime: best(최상) `spread_low 503.79` / worst(최악) `spread_low 503.79`

## Read(판독)

- action(행동): routed total(라우팅 전체) 거래 목록을 session(세션), ADX(평균 방향 지수), trend/chop(추세/횡보), volatility(변동성), spread(스프레드)로 나눴다.
- effect(효과): Stage56(56단계) 후보의 이익이 어느 시장 상태에서 나왔는지 설명하지만, 이 표만으로 live filter(실거래 필터)를 만들지는 않는다.
