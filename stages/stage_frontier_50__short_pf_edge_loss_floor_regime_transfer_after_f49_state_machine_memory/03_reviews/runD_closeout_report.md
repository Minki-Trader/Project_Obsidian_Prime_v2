# frontier50D_stage_closeout_loss_floor_regime_transfer_v1 report(보고서)

## Judgment(판정)
- closeout_class(마감 분류): `preserved_clue_negative_memory`
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_observation_no_authority`
- scout/seed/runtime(탐색/씨앗/런타임): 3/0/0

## Eligibility Rule(적격 규칙)
- weak_positive_pf(약한 양수 PF) below scout threshold(탐색 임계값 미만)는 near-miss alpha(근접 알파)가 아니라 negative_memory(부정 기억)로 남긴다.
- scout floor(탐색 하한): forward_min_pf(전진 최소 PF) >= 1.05, density(밀도) 4.0..12.0/day, forward_max_dd(전진 최대 DD) <= 18.0.
- closest_nonwinner_check(가장 가까운 비승자 확인): `f50c_0011` forward_min_pf=1.02392402650271, forward_max_dd=12.112726661714323, runtime_candidate=False.

## Best Observed Row(최상 관찰 행)
- candidate_id(후보 ID): `f50b_0001`
- event_variant(이벤트 변형): `event_loss_floor_transfer_mfe65_mae40_recent_loss`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__loss_floor_transfer_decay_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `loss_floor_transfer_decay_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `hygiene_atr_le2p25_cash_open`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 1.0
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.0
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- train_profit_factor(학습 PF): 1.172556178726751
- validation_profit_factor(검증 PF): 0.9891676797926019
- oos_profit_factor(표본외 PF): 0.9700936972765904
- forward_min_pf(전진 최소 PF): 0.9700936972765904
- forward_density(전진 거래 밀도): 4.458015267175573 ~ 5.8743169398907105
- forward_max_dd(전진 최대 DD): 8.701818453936315

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

## Lifecycle(생명주기)
- stage_open(단계 개방): Grok(그록) accepted_stage_open_train_split_only_loss_floor_regime_transfer_lock
- proxy(프록시): models=1, candidates=4, scout/seed/runtime=0/0/0
- repair(수리): run_capped_loss_floor_transfer_input_surface_repair / models=48, candidates=90, scout/seed/runtime=3/0/0
- mt5_runtime_probe(런타임 탐침): `frontier50Z_runtime_probe_backfill_v1` completed(완료), observation only(관찰 전용), candidate(후보)=`f50c_0064`
- closeout_grok(마감 그록): accepted(수용), boundary_ok(경계 적합)=yes(예), local_verification(로컬 검증)=True

## MT5 Runtime Probe Observation(MT5 런타임 탐침 관찰)
- validation_is(검증 내부): proxy PF/DD/trades(프록시 수익 팩터/손실폭/거래)=1.1349674529505298/9.488801530842927/1282 -> MT5 PF/DD/trades(MT5 수익 팩터/손실폭/거래)=0.81/76.21/99, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0.
- oos(표본외): proxy PF/DD/trades(프록시 수익 팩터/손실폭/거래)=1.0578280140948615/15.637907152330031/912 -> MT5 PF/DD/trades(MT5 수익 팩터/손실폭/거래)=0.99/31.52/71, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0.
- interpretation(해석): signal handoff parity(신호 인계 동등성)는 맞았지만, Python first-hit proxy(파이썬 첫 터치 프록시)가 MT5 single-position/order path(MT5 단일 포지션/주문 경로)의 DD/trade-count compression(손실폭/거래수 압축)을 과소평가했다.
- next_stage_clue(다음 단계 단서): F51 전에는 explicit order-path layer(명시적 주문 경로 층) 또는 narrow order-path simulator(좁은 주문 경로 시뮬레이터)를 proxy(프록시)에 넣어 DD/trade compression(손실폭/거래 압축)을 먼저 보정한다.

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
