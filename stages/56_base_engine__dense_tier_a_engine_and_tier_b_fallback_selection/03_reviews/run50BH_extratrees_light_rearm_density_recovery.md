# run50BH_stage56_extratrees_light_rearm_density_recovery_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50BH_stage56_extratrees_light_rearm_density_recovery_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `et40h6_r001_a`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| et40h6_r001_a | false | 6.846995 | 5.102564 | 1.1 | 1.26 | 313.49 | 613.58 | `strong_selected_research_baseline_candidate_actual_routed_mt5` |
| et40h6_r005_a | false | 6.677596 | 4.902564 | 1.1 | 1.43 | 314.45 | 911.32 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et40h6_r010_a | false | 6.344262 | 4.620513 | 1.18 | 1.38 | 505.33 | 743.61 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et30h6_r001_a | false | 7.142077 | 5.200000 | 1.04 | 1.35 | 140.74 | 818.43 | `quality_or_density_inconclusive_actual_routed_mt5` |
| et30h6_r005_a | false | 6.901639 | 5.035897 | 1.0 | 1.4 | -13.81 | 886.15 | `quality_failed_actual_routed_mt5` |
| et30h6_r005_b | true | 6.939891 | 5.128205 | 1.0 | 1.4 | 13.11 | 890.13 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| et40h6_r001_a | validation_is | 0.597153 | -0.249808 | 0.683958 | 2.163934 | False |
| et40h6_r001_a | oos | 0.622472 | 0.116663 | 0.718593 | 1.435897 | False |
| et40h6_r005_a | validation_is | 0.599127 | -0.242676 | 0.672668 | 2.185792 | False |
| et40h6_r005_a | oos | 0.624715 | 0.453264 | 0.703975 | 1.451282 | False |
| et40h6_r010_a | validation_is | 0.598202 | -0.064746 | 0.650301 | 2.218579 | False |
| et40h6_r010_a | oos | 0.606429 | 0.325316 | 0.675916 | 1.497436 | False |
| et30h6_r001_a | validation_is | 0.609525 | -0.392318 | 0.687070 | 2.234973 | False |
| et30h6_r001_a | oos | 0.632943 | 0.307130 | 0.724852 | 1.430769 | False |
| et30h6_r005_a | validation_is | 0.598487 | -0.510934 | 0.673793 | 2.251366 | False |
| et30h6_r005_a | oos | 0.635997 | 0.402393 | 0.712831 | 1.446154 | False |
| et30h6_r005_b | validation_is | 0.598681 | -0.489677 | 0.672441 | 2.273224 | False |
| et30h6_r005_b | oos | 0.635023 | 0.390130 | 0.714000 | 1.466667 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B disabled but no matched enabled comparison in this batch
