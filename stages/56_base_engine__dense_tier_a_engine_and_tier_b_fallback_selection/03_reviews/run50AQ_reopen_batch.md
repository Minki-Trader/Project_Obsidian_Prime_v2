# run50AQ_stage56_extratrees_model_axis_density_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AQ_stage56_extratrees_model_axis_density_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `et40s25b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| et20s25a | false | 4.852459 | 3.646154 | 0.98 | 1.13 | -60.48 | 237.74 | `quality_failed_actual_routed_mt5` |
| et20s25b | true | 4.923497 | 3.682051 | 0.98 | 1.12 | -42.29 | 224.69 | `quality_failed_actual_routed_mt5` |
| et40s25a | false | 4.540984 | 3.276923 | 1.0 | 1.29 | -6.12 | 473.93 | `quality_failed_actual_routed_mt5` |
| et40s25b | true | 4.568306 | 3.389744 | 1.0 | 1.34 | 0.05 | 540.59 | `quality_or_density_inconclusive_actual_routed_mt5` |
| et20s30a | false | 4.852459 | 3.646154 | 0.98 | 1.13 | -60.48 | 237.74 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| et20s25a | validation_is | 0.598463 | -0.568108 | 0.538288 | 2.240437 | False |
| et20s25a | oos | 0.586190 | -0.165626 | 0.590717 | 1.492308 | False |
| et20s25b | validation_is | 0.599714 | -0.546937 | 0.534961 | 2.289617 | False |
| et20s25b | oos | 0.585521 | -0.187061 | 0.586351 | 1.523077 | False |
| et40s25a | validation_is | 0.592287 | -0.507365 | 0.530686 | 2.131148 | False |
| et40s25a | oos | 0.608452 | 0.241674 | 0.564945 | 1.425641 | False |
| et40s25b | validation_is | 0.588039 | -0.499940 | 0.527512 | 2.158470 | False |
| et40s25b | oos | 0.604362 | 0.317837 | 0.571861 | 1.451282 | False |
| et20s30a | validation_is | 0.598463 | -0.568108 | 0.538288 | 2.240437 | False |
| et20s30a | oos | 0.586190 | -0.165626 | 0.590717 | 1.492308 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `validation_pf`: validation PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
