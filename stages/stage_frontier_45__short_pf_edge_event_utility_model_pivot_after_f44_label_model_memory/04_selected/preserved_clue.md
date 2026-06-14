# Preserved Clue(보존 단서)

F45 preserved clue(보존 단서)는 train-only short event-utility classifier(학습 전용 숏 이벤트 효용 분류기)가 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_candidate(최상 후보): `f45b_0001`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `extratrees_cls_d5_leaf240`
- train_pf(학습 PF): 1.1735796387984494
- forward_min_pf(전진 최소 PF): 0.9025796062128761
- forward_density(전진 거래 밀도): 4.748633879781421 ~ 5.549618320610687
- forward_max_dd(전진 최대 DD): 12.388082979253179

## Nonwinner Forward Observation(비승자 전진 관찰)

- candidate_id(후보 ID): `f45c_0077`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `logreg_balanced_l2_c0p25`
- forward_min_pf(전진 최소 PF): 1.00304534015195
- forward_density(전진 거래 밀도): 6.163934426229508 ~ 8.67175572519084
- forward_max_dd(전진 최대 DD): 10.696364875743402
- boundary(경계): clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).
