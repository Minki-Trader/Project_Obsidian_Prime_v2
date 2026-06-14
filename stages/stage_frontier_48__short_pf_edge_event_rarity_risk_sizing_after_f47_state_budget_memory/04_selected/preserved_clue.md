# Preserved Clue(보존 단서)

F48 preserved clue(보존 단서)는 train-only event rarity risk sizing(학습 전용 이벤트 희소성/위험 크기 조절)이 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_candidate(최상 후보): `f48b_0001`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `state_gate_squeeze_off_bad_fast_le1_vol5_le1p5`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 0.8341081477856619
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.1658918522143381
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- train_pf(학습 PF): 1.1887260236137729
- forward_min_pf(전진 최소 PF): 1.0316250802583076
- forward_density(전진 거래 밀도): 4.969465648854962 ~ 5.688524590163935
- forward_max_dd(전진 최대 DD): 9.32068457099996

## Nonwinner Forward Observation(비승자 전진 관찰)

- candidate_id(후보 ID): `f48c_0002`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `repair_state_gate_squeeze_off_vol_atr_le1p75`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 0.8974798140445315
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.10252018595546852
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- forward_min_pf(전진 최소 PF): 1.0426042978096992
- forward_density(전진 거래 밀도): 5.297709923664122 ~ 5.972677595628415
- forward_max_dd(전진 최대 DD): 8.399759205989966
- boundary(경계): clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).
