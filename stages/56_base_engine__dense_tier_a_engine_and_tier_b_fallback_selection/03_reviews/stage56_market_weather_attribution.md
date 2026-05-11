# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속)

- run_id(실행 ID): `run50C_d38h10_logreg_dense_v1`
- variant_id(변형 ID): `d38h10`
- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Split Summary(분할 요약)

| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |
|---|---:|---:|---:|---:|
| validation | 817 | 190.38 | 0.666667 | 33.056304 |
| oos | 672 | 302.10 | 0.571429 | 29.392857 |

## Key Attribution(핵심 귀속)

### validation
- session_slice: best(최상) `early 297.34, mid 73.61, late -180.57` / worst(최악) `late -180.57, mid 73.61, early 297.34`
- volatility_regime: best(최상) `vol_mid 160.58, vol_low 87.9, vol_high -4.33` / worst(최악) `feature_missing -53.77, vol_high -4.33, vol_low 87.9`
- trend_regime: best(최상) `downtrend 290.77, range_or_weak_trend -46.62, feature_missing -53.77` / worst(최악) `feature_missing -53.77, range_or_weak_trend -46.62, downtrend 290.77`
- adx_bucket: best(최상) `adx_gt25 458.79, adx_lt20 -46.62, feature_missing -53.77` / worst(최악) `adx_20_25 -168.02, feature_missing -53.77, adx_lt20 -46.62`
- spread_regime: best(최상) `spread_low 190.38` / worst(최악) `spread_low 190.38`

### oos
- session_slice: best(최상) `early 259.5, mid 47.33, late -4.73` / worst(최악) `late -4.73, mid 47.33, early 259.5`
- volatility_regime: best(최상) `vol_high 121.93, feature_missing 88.1, vol_low 71.0` / worst(최악) `vol_mid 21.07, vol_low 71.0, feature_missing 88.1`
- trend_regime: best(최상) `range_or_weak_trend 203.77, feature_missing 88.1, downtrend 10.23` / worst(최악) `downtrend 10.23, feature_missing 88.1, range_or_weak_trend 203.77`
- adx_bucket: best(최상) `adx_lt20 203.77, feature_missing 88.1, adx_20_25 58.51` / worst(최악) `adx_gt25 -48.28, adx_20_25 58.51, feature_missing 88.1`
- spread_regime: best(최상) `spread_low 302.1` / worst(최악) `spread_low 302.1`

## Read(판독)

- 이 귀속은 hard filter(강제 필터)가 아니라 explanation table(설명 표)이다.
- 효과(effect, 효과): d38h10 후보가 어느 시장 상태에서 손익을 만들거나 잃는지 설명하지만, Stage56(56단계) 안에서 새 운영 필터를 만들지는 않는다.
