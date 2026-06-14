# Preserved Clue(보존 단서)

F46 preserved clue(보존 단서)는 train-only lagged short event sequence context(학습 전용 지연 숏 이벤트 순서 문맥)가 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_candidate(최상 후보): `f46b_0001`
- event_variant(이벤트 변형): `event_mfe75_mae50_ratio70`
- model_family(모델 계열): `extratrees_cls_d5_leaf240__base_logreg_c0p25__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_logreg_c0p25`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- train_pf(학습 PF): 1.3545715224788049
- forward_min_pf(전진 최소 PF): 0.8051129263743074
- forward_density(전진 거래 밀도): 7.382513661202186 ~ 8.885496183206106
- forward_max_dd(전진 최대 DD): 24.590590885523888

## Nonwinner Forward Observation(비승자 전진 관찰)

- candidate_id(후보 ID): `f46b_0004`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- forward_min_pf(전진 최소 PF): 1.0050123327867062
- forward_density(전진 거래 밀도): 6.282442748091603 ~ 7.021857923497268
- forward_max_dd(전진 최대 DD): 11.699764717548211
- boundary(경계): clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).
