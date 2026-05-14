# run50BL_stage56_same_direction_cooldown_real_density_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50BL_stage56_same_direction_cooldown_real_density_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `et40h6sd3_s260l170_r001_a`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| et40h3sd2_s240l150_r001_a | false | 7.081967 | 5.307692 | 0.92 | 1.07 | -226.7 | 146.42 | `quality_failed_actual_routed_mt5` |
| et40h3sd3_s240l150_r001_a | false | 6.633880 | 4.953846 | 0.97 | 1.08 | -74.06 | 149.01 | `quality_failed_actual_routed_mt5` |
| et40h3sd4_s240l150_r001_a | false | 6.289617 | 4.625641 | 0.89 | 1.1 | -279.01 | 181.38 | `quality_failed_actual_routed_mt5` |
| et40h3sd3_s250l160_r001_a | false | 6.633880 | 4.953846 | 0.97 | 1.08 | -74.06 | 149.01 | `quality_failed_actual_routed_mt5` |
| et40h4sd3_s250l160_r001_a | false | 6.333333 | 4.707692 | 1.0 | 1.21 | -3.73 | 412.04 | `quality_failed_actual_routed_mt5` |
| et40h6sd3_s260l170_r001_a | false | 5.994536 | 4.405128 | 1.02 | 1.24 | 65.68 | 503.79 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| et40h3sd2_s240l150_r001_a | validation_is | 0.612617 | -0.674923 | 0.672068 | 2.322404 | False |
| et40h3sd2_s240l150_r001_a | oos | 0.627348 | -0.358531 | 0.707246 | 1.553846 | False |
| et40h3sd3_s240l150_r001_a | validation_is | 0.618915 | -0.561005 | 0.643328 | 2.366120 | False |
| et40h3sd3_s240l150_r001_a | oos | 0.612449 | -0.345745 | 0.685300 | 1.558974 | False |
| et40h3sd4_s240l150_r001_a | validation_is | 0.611338 | -0.742407 | 0.613380 | 2.431694 | False |
| et40h3sd4_s240l150_r001_a | oos | 0.610130 | -0.298914 | 0.656319 | 1.589744 | False |
| et40h3sd3_s250l160_r001_a | validation_is | 0.618915 | -0.561005 | 0.643328 | 2.366120 | False |
| et40h3sd3_s250l160_r001_a | oos | 0.612449 | -0.345745 | 0.685300 | 1.558974 | False |
| et40h4sd3_s250l160_r001_a | validation_is | 0.608930 | -0.503218 | 0.625539 | 2.371585 | False |
| et40h4sd3_s250l160_r001_a | oos | 0.607062 | -0.051155 | 0.673203 | 1.538462 | False |
| et40h6sd3_s260l170_r001_a | validation_is | 0.597859 | -0.440128 | 0.630811 | 2.213115 | False |
| et40h6sd3_s260l170_r001_a | oos | 0.603358 | 0.086484 | 0.667055 | 1.466667 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `validation_pf`: validation PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B disabled but no matched enabled comparison in this batch
