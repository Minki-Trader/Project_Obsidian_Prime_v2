# run50BI_stage56_extratrees_raw_density_microcooldown_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50BI_stage56_extratrees_raw_density_microcooldown_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `et40h4c6_s240l150_r001_a`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| et40h3c0_s240l150_r001_a | false | 8.508197 | 6.410256 | 0.97 | 1.12 | -114.55 | 284.7 | `quality_failed_actual_routed_mt5` |
| et40h3c3_s240l150_r001_a | false | 5.846995 | 4.420513 | 0.99 | 1.14 | -25.18 | 225.85 | `quality_failed_actual_routed_mt5` |
| et40h4c3_s240l150_r001_a | false | 5.803279 | 4.333333 | 0.96 | 1.11 | -99.1 | 219.13 | `quality_failed_actual_routed_mt5` |
| et40h4c3_s235l145_r001_a | false | 5.803279 | 4.333333 | 0.96 | 1.11 | -99.1 | 219.13 | `quality_failed_actual_routed_mt5` |
| et40h4c3_s230l140_r001_a | false | 5.803279 | 4.333333 | 0.96 | 1.11 | -99.1 | 219.13 | `quality_failed_actual_routed_mt5` |
| et40h4c3_s240l150_r005_a | false | 5.617486 | 4.123077 | 0.92 | 1.34 | -186.86 | 545.53 | `quality_failed_actual_routed_mt5` |
| et40h4c6_s240l150_r001_a | false | 4.579235 | 3.435897 | 1.06 | 1.27 | 119.63 | 367.74 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et40h4c3_s240l150_r001_b | true | 5.841530 | 4.415385 | 0.96 | 1.14 | -98.55 | 265.08 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| et40h3c0_s240l150_r001_a | validation_is | 0.611801 | -0.573571 | 0.730893 | 2.289617 | False |
| et40h3c0_s240l150_r001_a | oos | 0.609866 | -0.272240 | 0.766400 | 1.497436 | False |
| et40h3c3_s240l150_r001_a | validation_is | 0.615517 | -0.523533 | 0.590654 | 2.393443 | False |
| et40h3c3_s240l150_r001_a | oos | 0.606129 | -0.237993 | 0.654292 | 1.528205 | False |
| et40h4c3_s240l150_r001_a | validation_is | 0.604385 | -0.593315 | 0.596987 | 2.338798 | False |
| et40h4c3_s240l150_r001_a | oos | 0.604351 | -0.240675 | 0.659172 | 1.476923 | False |
| et40h4c3_s235l145_r001_a | validation_is | 0.604385 | -0.593315 | 0.596987 | 2.338798 | False |
| et40h4c3_s235l145_r001_a | oos | 0.604351 | -0.240675 | 0.659172 | 1.476923 | False |
| et40h4c3_s230l140_r001_a | validation_is | 0.604385 | -0.593315 | 0.596987 | 2.338798 | False |
| et40h4c3_s230l140_r001_a | oos | 0.604351 | -0.240675 | 0.659172 | 1.476923 | False |
| et40h4c3_s240l150_r005_a | validation_is | 0.596781 | -0.681770 | 0.571984 | 2.404372 | False |
| et40h4c3_s240l150_r005_a | oos | 0.610452 | 0.178520 | 0.634328 | 1.507692 | False |
| et40h4c6_s240l150_r001_a | validation_is | 0.601633 | -0.357243 | 0.507160 | 2.256831 | False |
| et40h4c6_s240l150_r001_a | oos | 0.596631 | 0.048866 | 0.549254 | 1.548718 | False |
| et40h4c3_s240l150_r001_b | validation_is | 0.604396 | -0.592189 | 0.598690 | 2.344262 | False |
| et40h4c3_s240l150_r001_b | oos | 0.608310 | -0.192125 | 0.659698 | 1.502564 | False |

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
- `tier_b_rule`: Tier B disabled but no matched enabled comparison in this batch
