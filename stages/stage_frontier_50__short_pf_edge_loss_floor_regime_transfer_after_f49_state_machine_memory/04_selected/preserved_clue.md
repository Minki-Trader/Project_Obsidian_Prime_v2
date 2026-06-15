# Preserved Clue(보존 단서)

F50 preserved clue(보존 단서)는 train-only loss-floor regime transfer(학습 전용 손실 하한 체제 전이)이 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_candidate(최상 후보): `f50b_0001`
- event_variant(이벤트 변형): `event_loss_floor_transfer_mfe65_mae40_recent_loss`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__loss_floor_transfer_decay_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `loss_floor_transfer_decay_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `hygiene_atr_le2p25_cash_open`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 1.0
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.0
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- train_pf(학습 PF): 1.172556178726751
- forward_min_pf(전진 최소 PF): 0.9700936972765904
- forward_density(전진 거래 밀도): 4.458015267175573 ~ 5.8743169398907105
- forward_max_dd(전진 최대 DD): 8.701818453936315

## Runtime Probe Clue(런타임 탐침 단서)

F50 repair(수리)에서 scout clue(탐색 단서)로 올라온 `f50c_0064`는 MT5 runtime probe(MT5 런타임 탐침)에 넣었다. 효과(effect, 효과)는 proxy(프록시)에서 좋아 보이는 손실 하한 전이 신호가 실제 EA order path(EA 주문 경로)에서 어떻게 변하는지 확인한 것이다.

- candidate_id(후보 ID): `f50c_0064`
- event_variant(이벤트 변형): `event_loss_floor_transfer_mfe65_mae40_recent_loss`
- model_family(모델 계열): `extratrees_cls_d5_leaf240__base_logreg_c0p25__loss_floor_transfer_decay_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `hygiene_squeeze_off_vol5_le2p25`
- proxy_validation(프록시 검증): PF=1.1349674529505298, DD=9.488801530842927, trades(거래)=1282
- proxy_oos(프록시 표본외): PF=1.0578280140948615, DD=15.637907152330031, trades(거래)=912
- MT5_validation_is(MT5 검증 내부): PF=0.81, DD=76.21%, trades(거래)=99, signal_diff(신호 차이)=0
- MT5_oos(MT5 표본외): PF=0.99, DD=31.52%, trades(거래)=71, signal_diff(신호 차이)=0
- preserved_use(보존 용도): loss-floor transfer + MFE/MAE decay memory(손실 하한 전이 + 최대유리/최대불리 감쇠 기억)는 clue only(단서 전용)로 보존한다. MT5 order-path compression(주문 경로 압축)을 모델링하지 않으면 앞으로 보내지 않는다.

## Nonwinner Forward Observation(비승자 전진 관찰)

- candidate_id(후보 ID): `f50c_0011`
- event_variant(이벤트 변형): `event_loss_floor_transfer_mfe65_mae40_recent_loss`
- model_family(모델 계열): `extratrees_cls_d7_leaf320__base_logreg_c0p25__loss_floor_transfer_decay_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_logreg_c0p25`
- context_variant(문맥 변형): `loss_floor_transfer_decay_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `hygiene_atr_le2p25_cash_open`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 1.0
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.0
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- forward_min_pf(전진 최소 PF): 1.02392402650271
- forward_density(전진 거래 밀도): 6.748091603053435 ~ 7.109289617486339
- forward_max_dd(전진 최대 DD): 12.112726661714323
- boundary(경계): clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).
