# run50AR_stage56_extratrees_validation_density_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AR_stage56_extratrees_validation_density_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `et40s25_c0_h6_a`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| et40s25_c0_h8_a | false | 6.606557 | 4.861538 | 1.02 | 1.31 | 61.18 | 765.43 | `quality_or_density_inconclusive_actual_routed_mt5` |
| et40s25_c4_h8_a | false | 5.420765 | 3.923077 | 1.01 | 1.28 | 29.91 | 554.97 | `quality_or_density_inconclusive_actual_routed_mt5` |
| et40s25_c0_h6_a | false | 7.404372 | 5.502564 | 1.04 | 1.25 | 147.86 | 655.4 | `quality_or_density_inconclusive_actual_routed_mt5` |
| et40s25_c4_h6_a | false | 5.595628 | 4.117949 | 0.91 | 1.25 | -238.57 | 481.02 | `quality_failed_actual_routed_mt5` |
| et40adxweak_c0_h8_a | false | 4.961749 | 3.492308 | 1.0 | 1.36 | -0.32 | 646.97 | `quality_failed_actual_routed_mt5` |
| et40adxweak_c0_h6_a | false | 5.535519 | 4.025641 | 1.02 | 1.16 | 49.59 | 321.81 | `quality_or_density_inconclusive_actual_routed_mt5` |
| et40s25_c0_h8_b | true | 6.644809 | 4.948718 | 1.03 | 1.31 | 94.67 | 763.47 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| et40s25_c0_h8_a | validation_is | 0.599932 | -0.449396 | 0.682382 | 2.098361 | False |
| et40s25_c0_h8_a | oos | 0.605240 | 0.307416 | 0.721519 | 1.353846 | False |
| et40s25_c4_h8_a | validation_is | 0.599044 | -0.469849 | 0.592742 | 2.207650 | False |
| et40s25_c4_h8_a | oos | 0.613120 | 0.225451 | 0.635294 | 1.430769 | False |
| et40s25_c0_h6_a | validation_is | 0.596523 | -0.390878 | 0.712915 | 2.125683 | False |
| et40s25_c0_h6_a | oos | 0.604692 | 0.110811 | 0.747437 | 1.389744 | False |
| et40s25_c4_h6_a | validation_is | 0.598616 | -0.732979 | 0.617188 | 2.142077 | False |
| et40s25_c4_h6_a | oos | 0.596894 | 0.099029 | 0.652553 | 1.430769 | False |
| et40adxweak_c0_h8_a | validation_is | 0.602248 | -0.500352 | 0.620044 | 1.885246 | False |
| et40adxweak_c0_h8_a | oos | 0.615395 | 0.450029 | 0.643172 | 1.246154 | False |
| et40adxweak_c0_h6_a | validation_is | 0.605179 | -0.451046 | 0.651530 | 1.928962 | False |
| et40adxweak_c0_h6_a | oos | 0.598988 | -0.090051 | 0.682803 | 1.276923 | False |
| et40s25_c0_h8_b | validation_is | 0.599499 | -0.422146 | 0.680921 | 2.120219 | False |
| et40s25_c0_h8_b | oos | 0.602494 | 0.291161 | 0.724352 | 1.364103 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_pf`: validation PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B disabled but no matched enabled comparison in this batch
