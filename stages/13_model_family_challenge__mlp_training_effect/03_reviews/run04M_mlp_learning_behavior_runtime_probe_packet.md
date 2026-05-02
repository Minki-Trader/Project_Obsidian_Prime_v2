# run04M_mlp_learning_behavior_runtime_probe_v1 결과 요약(Result Summary, 결과 요약)

- status(상태): `completed`
- judgment(판정): `inconclusive_mlp_learning_behavior_runtime_shape_confirmed`
- boundary(경계): `mlp_learning_behavior_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

## Core Read(핵심 판독)

- feature group ablation(피처 그룹 제거) OOS(표본외) 최대 변화: `ablate_volatility_range` / L1 delta(L1 변화) `0.2776` / decision flip(결정 뒤집힘) `0.1001`.
- scaling/noise sensitivity(스케일/노이즈 민감도) OOS(표본외) 최대 변화: `noise_sigma010` / L1 delta(L1 변화) `0.0753` / decision flip(결정 뒤집힘) `0.0270`.
- calibration shape(보정 모양) OOS(표본외): confidence(확신도) `0.495`, accuracy(정확도) `0.452`, ECE(기대 보정 오차) `0.043`.
- MT5/Python parity(MT5/파이썬 동등성): `12` / `12` probability shape(확률 모양) rows pass(통과).

효과(effect, 효과): 이 결과는 MLP(다층 퍼셉트론) learning behavior(학습 행동)를 설명한다. trade edge(거래 우위), alpha quality(알파 품질), baseline(기준선)은 만들지 않는다.
