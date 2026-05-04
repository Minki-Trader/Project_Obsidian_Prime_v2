# Stage19 RUN13H EBM Feature/Hold/Routing Attribution(19단계 실행13H EBM 피처/보유/라우팅 귀속)

- judgment(판정): `inconclusive_ebm_feature_hold6_routing_attribution_completed`
- source runs(원천 실행): `run13B, run13F, run13G`
- focus run(중심 실행): `run13F_ebm_q90_hold6_probe_v1`
- boundary(경계): `ebm_feature_hold6_routing_attribution_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

## Hold6/Q90 Read(6봉/Q90 판독)

- hold6 OOS net(6봉 표본밖 순손익): `39.65` / PF(수익 팩터): `1.04`
- hold6 validation net(6봉 검증 순손익): `-188.66` / PF(수익 팩터): `0.85`
- hold6 OOS rank(6봉 표본밖 순위): `1`
- hold6 validation rank(6봉 검증 순위): `3`

효과(effect, 효과): hold6/q90(6봉/q90)은 OOS(표본밖)에서 가장 나았지만 validation(검증)이 음수라서 edge(거래 우위)로 올리지 않는다.

## Feature Contribution(피처 기여도)

| tier/split/side(티어/분할/방향) | signals(신호) | top features(상위 피처) | top10 share(상위10 비중) |
|---|---:|---|---:|
| Tier A/oos/long | `480` | `['atr_14', 'ema9_ema20_diff', 'ema50_ema200_diff', 'hl_zscore_50', 'atr_50']` | `0.6126501207919282` |
| Tier A/oos/short | `264` | `['ema9_ema20_diff', 'atr_14', 'close_ema50_ratio', 'atr_14_over_atr_50', 'historical_vol_20']` | `0.5899138828670545` |
| Tier B/oos/long | `25` | `['ema50_ema200_diff', 'atr_14', 'ema20_ema50_diff', 'atr_50', 'sma50_sma200_ratio']` | `0.6454384271125397` |
| Tier B/oos/short | `8` | `['ema9_ema20_diff', 'atr_14_over_atr_50', 'ema20_ema50_diff', 'is_first_30m_after_open', 'ema50_ema200_diff']` | `0.6024565387113885` |

## Tier A/B Routing(티어 A/B 라우팅)

- Tier B fallback-only OOS net(Tier B 대체 단독 표본밖 순손익): `70.92`
- Tier B fallback routed share(Tier B 대체 라우팅 비중): `0.12283136710617627`
- routed component profit(라우팅 구성요소 수익): `not separable(분리 불가)`

효과(effect, 효과): Tier B(티어 B)는 단독 tester run(테스터 실행)에서는 양수 단서를 보였지만 routed total(라우팅 전체)의 합성 가산값으로 해석하지 않는다.

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
