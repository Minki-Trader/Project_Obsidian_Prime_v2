# frontier47D_stage_closeout_sequence_state_risk_budget_v1 report(보고서)

## Judgment(판정)
- closeout_class(마감 분류): `negative_memory`
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f47_state_risk_budget_proxy`
- scout/seed/runtime(탐색/씨앗/런타임): 0/0/0

## Best Observed Row(최상 관찰 행)
- candidate_id(후보 ID): `f47b_0001`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `logreg_balanced_l2_c0p25__base_extratrees_d3_leaf220__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_extratrees_d3_leaf220`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- risk_budget_variant(위험 예산 변형): `risk_budget_bad_fast_p72_realized_vol_p82`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): 0.8199168093956447
- risk_budget_train_block_rate(위험 예산 학습 차단율): 0.1800831906043553
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- train_profit_factor(학습 PF): 1.219246917807805
- validation_profit_factor(검증 PF): 0.9977505589480542
- oos_profit_factor(표본외 PF): 1.1038671020765347
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

## Lifecycle(생명주기)
- stage_open(단계 개방): Grok(그록) accepted_stage_open_train_split_only_state_risk_budget_lock
- proxy(프록시): models=1, candidates=2, scout/seed/runtime=0/0/0
- repair(수리): run_capped_state_risk_budget_repair / models=1, candidates=4, scout/seed/runtime=0/0/0
- closeout_grok(마감 그록): accepted_closeout_state_risk_budget_boundary

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
