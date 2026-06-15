# frontier49D_stage_closeout_forward_floor_state_machine_v1 report(보고서)

## Judgment(판정)
- closeout_class(마감 분류): `negative_memory`
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f49_forward_floor_state_machine_proxy`
- scout/seed/runtime(탐색/씨앗/런타임): 0/0/0

## Eligibility Rule(적격 규칙)
- weak_positive_pf(약한 양수 PF) below scout threshold(탐색 임계값 미만)는 near-miss alpha(근접 알파)가 아니라 negative_memory(부정 기억)로 남긴다.
- scout floor(탐색 하한): forward_min_pf(전진 최소 PF) >= 1.05, density(밀도) 4.0..12.0/day, forward_max_dd(전진 최대 DD) <= 18.0.
- closest_nonwinner_check(가장 가까운 비승자 확인): `f49c_0008` forward_min_pf=0.9120028238834444, forward_max_dd=14.124019229609253, runtime_candidate=False.

## Best Observed Row(최상 관찰 행)
- candidate_id(후보 ID): `f49c_0001`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `repair_floor_state_good_recent24_squeeze_off`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 0.8225214198286414
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.17747858017135865
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- train_profit_factor(학습 PF): 1.1714729901965568
- validation_profit_factor(검증 PF): 0.9979294087239854
- oos_profit_factor(표본외 PF): 0.8929082126961188
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

## Lifecycle(생명주기)
- stage_open(단계 개방): Grok(그록) accepted_stage_open_train_split_only_forward_floor_state_machine_lock
- proxy(프록시): models=1, candidates=0, scout/seed/runtime=0/0/0
- repair(수리): run_capped_nonpercentile_state_gate_repair / models=3, candidates=8, scout/seed/runtime=0/0/0
- closeout_grok(마감 그록): accepted_closeout_boundary_ok

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
