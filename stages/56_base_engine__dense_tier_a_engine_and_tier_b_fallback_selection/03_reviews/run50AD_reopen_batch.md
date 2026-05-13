# run50AD_stage56_c12_rf_path_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AD_stage56_c12_rf_path_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `lv26b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| lv26a | false | 3.803279 | 2.482051 | 1.01 | 1.31 | 21.07 | 414.56 | `density_failed_actual_routed_mt5` |
| lv26b | true | 3.836066 | 2.533333 | 1.01 | 1.23 | 23.4 | 312.41 | `density_failed_actual_routed_mt5` |
| lv24a | false | 3.803279 | 2.482051 | 1.01 | 1.31 | 21.07 | 414.56 | `density_failed_actual_routed_mt5` |
| lv24b | true | 3.836066 | 2.533333 | 1.01 | 1.23 | 23.4 | 312.41 | `density_failed_actual_routed_mt5` |
| ax26a | false | 1.743169 | 3.010256 | 0.59 | 1.03 | -491.75 | 45.12 | `quality_failed_actual_routed_mt5` |
| ax26b | true | 4.562842 | 3.112821 | 1.0 | 1.01 | -5.53 | 20.83 | `quality_failed_actual_routed_mt5` |
| dn26a | false | 1.355191 | 0.984615 | 0.71 | 1.12 | -347.29 | 86.68 | `quality_failed_actual_routed_mt5` |
| dn26b | true | 1.382514 | 1.020513 | 0.7 | 1.08 | -359.59 | 64.82 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| lv26a | validation_is | 0.626404 | -0.469727 | 0.303161 | 2.650273 | False |
| lv26a | oos | 0.619432 | 0.356529 | 0.245868 | 1.871795 | False |
| lv26b | validation_is | 0.626898 | -0.466667 | 0.304843 | 2.666667 | False |
| lv26b | oos | 0.613230 | 0.132409 | 0.242915 | 1.917949 | False |
| lv24a | validation_is | 0.626404 | -0.469727 | 0.303161 | 2.650273 | False |
| lv24a | oos | 0.619432 | 0.356529 | 0.245868 | 1.871795 | False |
| lv24b | validation_is | 0.626898 | -0.466667 | 0.304843 | 2.666667 | False |
| lv24b | oos | 0.613230 | 0.132409 | 0.242915 | 1.917949 | False |
| ax26a | validation_is | 0.596472 | -2.041536 | 0.388715 | 1.065574 | False |
| ax26a | oos | 0.553419 | -0.423135 | 0.270869 | 2.194872 | False |
| ax26b | validation_is | 0.594068 | -0.506623 | 0.314970 | 3.125683 | False |
| ax26b | oos | 0.547101 | -0.465684 | 0.266886 | 2.282051 | False |
| dn26a | validation_is | 0.596459 | -1.900363 | 0.000000 | 1.355191 | False |
| dn26a | oos | 0.569786 | -0.048542 | 0.000000 | 0.984615 | False |
| dn26b | validation_is | 0.610041 | -1.921304 | 0.000000 | 1.382514 | False |
| dn26b | oos | 0.574089 | -0.174271 | 0.000000 | 1.020513 | False |

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
