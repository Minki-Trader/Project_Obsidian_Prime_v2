# frontier45D_stage_closeout_event_utility_model_v1 report(보고서)

## Judgment(판정)
- closeout_class(마감 분류): `negative_memory`
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f45_event_classifier_proxy`
- scout/seed/runtime(탐색/씨앗/런타임): 0/0/0

## Best Observed Row(최상 관찰 행)
- candidate_id(후보 ID): `f45b_0001`
- event_variant(이벤트 변형): `event_mfe65_mae35_loss_contained`
- model_family(모델 계열): `extratrees_cls_d5_leaf240`
- train_profit_factor(학습 PF): 1.1735796387984494
- validation_profit_factor(검증 PF): 0.9025796062128761
- oos_profit_factor(표본외 PF): 0.9507867157484787
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

## Lifecycle(생명주기)
- stage_open(단계 개방): Grok(그록) accepted_stage_open_train_split_only_event_lock
- proxy(프록시): models=12, candidates=36, scout/seed/runtime=0/0/0
- repair(수리): run_capped_event_rarity_threshold_repair / models=25, candidates=84, scout/seed/runtime=0/0/0
- closeout_grok(마감 그록): accepted_closeout_event_classifier_boundary

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
