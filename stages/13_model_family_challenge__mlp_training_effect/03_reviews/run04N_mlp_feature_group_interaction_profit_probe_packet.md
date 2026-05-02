# run04N_mlp_feature_group_interaction_profit_probe_v1 결과 요약(Result Summary, 결과 요약)

- status(상태): `completed`
- judgment(판정): `inconclusive_feature_group_interaction_profit_completed_with_partial_trade_stopout`
- boundary(경계): `feature_group_interaction_profit_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5/Python parity(MT5/파이썬 동등성): `17` pass(통과), `1` partial trade stopout(부분 거래 손상), total(전체) `18`.

## Core Read(핵심 판독)

- OOS(표본외) probability shape(확률 모양) 최대 변화: `no_volatility_oscillator` / L1 delta(L1 변화) `0.3255`.
- OOS(표본외) net profit(순수익) 최고 변형: `no_trend_structure` / net(순수익) `172.22` / trades(거래 수) `229`.
- OOS(표본외) net profit(순수익) 최저 변형: `no_volatility_range` / net(순수익) `-58.88` / DD(손실) `151.07`.

효과(effect, 효과): 이 결과는 feature group interaction(피처 그룹 상호작용)이 MT5(메타트레이더5) 거래 진단값으로 어떻게 번지는지 보여준다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격)은 만들지 않는다.

## OOS Profit(표본외 수익)

| variant(변형) | net(순수익) | delta(원본 대비) | PF(수익 팩터) | DD(손실) | trades(거래) | win%(승률) | avg hold bars(평균 보유 봉) |
|---|---:|---:|---:|---:|---:|---:|---:|
| no_trend_structure | 172.22 | 115.55 | 1.21 | 150.48 | 229 | 54.15 | 13.917 |
| no_volatility_oscillator | 171.65 | 114.98 | 1.19 | 103.39 | 209 | 54.07 | 30.3541 |
| only_volatility_range | 148.54 | 91.87 | 1.59 | 101.39 | 73 | 60.27 | 29.1644 |
| no_oscillator | 134.13 | 77.46 | 1.15 | 170.26 | 201 | 54.73 | 31.1144 |
| no_volatility_trend | 88.6 | 31.93 | 1.16 | 96.97 | 139 | 54.68 | 9.9856 |
| no_session | 75.74 | 19.07 | 1.09 | 184.19 | 180 | 56.11 | 37.6167 |
| original | 56.67 | 0 | 1.06 | 248.58 | 208 | 51.92 | 22.226 |
| no_volatility_session | 21.55 | -35.12 | 1.03 | 126.28 | 202 | 52.97 | 24.2921 |
| no_volatility_range | -58.88 | -115.55 | 0.93 | 151.07 | 194 | 51.55 | 35.5155 |

## Interaction Residual(상호작용 잔차)

| partner(상대 그룹) | split(분할) | L1 residual(L1 잔차) | net residual(수익 잔차) | interpretation(해석) |
|---|---|---:|---:|---|
| trend_structure | validation_is | -0.141 | 52.46 | non_additive_shape |
| session | validation_is | -0.1305 | -182.62 | non_additive_shape |
| oscillator | validation_is | -0.0782 | 43.64 | non_additive_shape |
| trend_structure | oos | -0.1567 | 31.93 | non_additive_shape |
| session | oos | -0.1187 | 61.36 | non_additive_shape |
| oscillator | oos | -0.0804 | 153.07 | non_additive_shape |
