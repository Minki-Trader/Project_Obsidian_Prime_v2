# Preserved Clue(보존 단서)

F47 preserved clue(보존 단서)는 train-only sequence state risk budget(학습 전용 순서 상태 위험 예산)이 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_candidate(최상 후보): `f47b_0001`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `risk_budget_bad_fast_p72_realized_vol_p82`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 0.8199168093956447
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.1800831906043553
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- train_pf(학습 PF): 1.219246917807805
- forward_min_pf(전진 최소 PF): 0.9977505589480542
- forward_density(전진 거래 밀도): 5.091603053435114 ~ 5.5683060109289615
- forward_max_dd(전진 최대 DD): 8.848376547242854

## Nonwinner Forward Observation(비승자 전진 관찰)

- candidate_id(후보 ID): `f47c_0001`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `repair_risk_budget_squeeze_p80_bad_fast_p80`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 0.9434793246880352
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.05652067531196481
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- forward_min_pf(전진 최소 PF): 1.021888981006332
- forward_density(전진 거래 밀도): 5.656488549618321 ~ 6.628415300546448
- forward_max_dd(전진 최대 DD): 11.448156113453123
- boundary(경계): clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).
