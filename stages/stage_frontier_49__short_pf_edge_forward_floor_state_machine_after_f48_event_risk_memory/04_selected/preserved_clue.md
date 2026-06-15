# Preserved Clue(보존 단서)

F49 preserved clue(보존 단서)는 train-only forward floor state machine(학습 전용 전진 하한 상태기계)이 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_candidate(최상 후보): `f49c_0001`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `repair_floor_state_good_recent24_squeeze_off`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 0.8225214198286414
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.17747858017135865
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- train_pf(학습 PF): 1.1714729901965568
- forward_min_pf(전진 최소 PF): 0.8929082126961188
- forward_density(전진 거래 밀도): 4.267175572519084 ~ 5.1256830601092895
- forward_max_dd(전진 최대 DD): 11.05877842171833

## Nonwinner Forward Observation(비승자 전진 관찰)

- candidate_id(후보 ID): `f49c_0008`
- event_variant(이벤트 변형): `event_mfe70_mae45_horizon_pos`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `repair_floor_state_good_recent24_squeeze_off`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 0.8164014687882497
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.1835985312117503
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- forward_min_pf(전진 최소 PF): 0.9120028238834444
- forward_density(전진 거래 밀도): 4.900763358778626 ~ 5.5683060109289615
- forward_max_dd(전진 최대 DD): 14.124019229609253
- boundary(경계): clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).
