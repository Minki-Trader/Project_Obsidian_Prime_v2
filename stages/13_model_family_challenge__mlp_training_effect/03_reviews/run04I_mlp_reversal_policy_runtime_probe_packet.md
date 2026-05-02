# run04I_mlp_reversal_policy_runtime_probe_v1 결과 요약(Result Summary, 결과 요약)

- status(상태): `completed`
- judgment(판정): `inconclusive_reversal_policy_runtime_probe_completed`
- source run(원천 실행): `run04F_mlp_direction_asymmetry_runtime_probe_v1`
- boundary(경계): `reversal_policy_runtime_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- OOS net delta(표본외 순수익 차이, close-only minus reverse): `-15.43`

## Policy KPI(정책 핵심 지표)

| policy(정책) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실) | trades(거래 수) | long/short(매수/매도) | reverse(반전) | close opposite(반대 신호 청산) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| immediate_reverse | validation_is | -93.60 | 0.93 | 304.12 | 265 | 216/49 | 29 | 0 |
| close_only | validation_is | -185.56 | 0.87 | 450.69 | 251 | 212/39 | 0 | 21 |
| immediate_reverse | oos | 56.67 | 1.06 | 248.58 | 208 | 159/49 | 25 | 0 |
| close_only | oos | 41.24 | 1.05 | 219.66 | 198 | 153/45 | 0 | 21 |

## Delta(차이)

| split(분할) | metric(지표) | reverse(즉시 반전) | close-only(청산만) | delta(차이) |
|---|---|---:|---:|---:|
| validation_is | net_profit | -93.60 | -185.56 | -91.96 |
| validation_is | profit_factor | 0.93 | 0.87 | -0.06 |
| validation_is | max_drawdown | 304.12 | 450.69 | 146.57 |
| validation_is | trade_count | 265.00 | 251.00 | -14.00 |
| oos | net_profit | 56.67 | 41.24 | -15.43 |
| oos | profit_factor | 1.06 | 1.05 | -0.01 |
| oos | max_drawdown | 248.58 | 219.66 | -28.92 |
| oos | trade_count | 208.00 | 198.00 | -10.00 |

효과(effect, 효과): 같은 MLP(다층 퍼셉트론) 모델과 q90 threshold(q90 임계값)에서 opposite signal policy(반대 신호 정책)만 바꿨으므로, 차이는 정책 민감도 단서로만 읽는다. alpha quality(알파 품질), baseline(기준선), promotion(승격)은 아니다.
