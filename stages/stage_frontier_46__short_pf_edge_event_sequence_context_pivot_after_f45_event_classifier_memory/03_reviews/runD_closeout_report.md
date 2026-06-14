# frontier46D_stage_closeout_event_sequence_context_v1 report(보고서)

## Judgment(판정)
- closeout_class(마감 분류): `negative_memory`
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f46_sequence_context_proxy`
- scout/seed/runtime(탐색/씨앗/런타임): 0/0/0

## Best Observed Row(최상 관찰 행)
- candidate_id(후보 ID): `f46b_0001`
- event_variant(이벤트 변형): `event_mfe75_mae50_ratio70`
- model_family(모델 계열): `extratrees_cls_d5_leaf240__base_logreg_c0p25__lagged_score_outcome_q86_w12_36`
- base_scorer_family(기본 채점기 계열): `base_logreg_c0p25`
- context_variant(문맥 변형): `lagged_score_outcome_q86_w12_36`
- past_outcome_embargo_bars(과거 결과 유예 봉 수): 13
- train_profit_factor(학습 PF): 1.3545715224788049
- validation_profit_factor(검증 PF): 0.8051129263743074
- oos_profit_factor(표본외 PF): 0.9343910059690459
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

## Lifecycle(생명주기)
- stage_open(단계 개방): Grok(그록) accepted_stage_open_train_split_only_event_lock
- proxy(프록시): models=96, candidates=36, scout/seed/runtime=0/0/0
- repair(수리): run_capped_event_rarity_threshold_repair / models=300, candidates=84, scout/seed/runtime=0/0/0
- closeout_grok(마감 그록): accepted_closeout_sequence_context_boundary

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
