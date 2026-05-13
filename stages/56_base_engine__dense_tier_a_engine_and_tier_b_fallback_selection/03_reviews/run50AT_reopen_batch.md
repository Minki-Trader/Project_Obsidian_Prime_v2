# run50AT_stage56_extratrees_leaf_granularity_transition_density_source_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AT_stage56_extratrees_leaf_granularity_transition_density_source_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `et20h6_r030_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| et20h6_r015_a | false | 6.551913 | 4.666667 | 1.07 | 1.12 | 226.28 | 277.78 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et20h6_r015_b | true | 6.584699 | 4.748718 | 1.07 | 1.14 | 220.66 | 312.02 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et20h6_r030_a | false | 5.945355 | 4.189744 | 1.13 | 1.11 | 351.16 | 215.59 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et20h6_r030_b | true | 5.983607 | 4.271795 | 1.13 | 1.13 | 346.02 | 249.83 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et20h6_r030_s24l15_a | false | 5.945355 | 4.189744 | 1.13 | 1.11 | 351.16 | 215.59 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et30h6_r015_a | false | 6.125683 | 4.379487 | 1.06 | 1.29 | 157.82 | 604.46 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et30h6_r030_a | false | 5.524590 | 3.902564 | 1.13 | 1.32 | 324.6 | 576.56 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et60h6_r015_a | false | 5.699454 | 4.056410 | 1.06 | 1.27 | 164.77 | 510.11 | `weak_dense_engine_candidate_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| et20h6_r015_a | validation_is | 0.615666 | -0.311276 | 0.648874 | 2.300546 | False |
| et20h6_r015_a | oos | 0.597806 | -0.194747 | 0.660440 | 1.584615 | False |
| et20h6_r015_b | validation_is | 0.617206 | -0.316880 | 0.646473 | 2.327869 | False |
| et20h6_r015_b | oos | 0.596445 | -0.163045 | 0.661987 | 1.605128 | False |
| et20h6_r030_a | validation_is | 0.610043 | -0.177243 | 0.583640 | 2.475410 | False |
| et20h6_r030_a | oos | 0.591648 | -0.236120 | 0.592411 | 1.707692 | False |
| et20h6_r030_b | validation_is | 0.611638 | -0.184000 | 0.581735 | 2.502732 | False |
| et20h6_r030_b | oos | 0.590275 | -0.200084 | 0.596639 | 1.723077 | False |
| et20h6_r030_s24l15_a | validation_is | 0.610043 | -0.177243 | 0.583640 | 2.475410 | False |
| et20h6_r030_s24l15_a | oos | 0.591648 | -0.236120 | 0.592411 | 1.707692 | False |
| et30h6_r015_a | validation_is | 0.588299 | -0.359215 | 0.609277 | 2.393443 | False |
| et30h6_r015_a | oos | 0.624243 | 0.207799 | 0.638173 | 1.584615 | False |
| et30h6_r030_a | validation_is | 0.596116 | -0.178932 | 0.541048 | 2.535519 | False |
| et30h6_r030_a | oos | 0.629239 | 0.257635 | 0.565046 | 1.697436 | False |
| et60h6_r015_a | validation_is | 0.606725 | -0.342023 | 0.597315 | 2.295082 | False |
| et60h6_r015_a | oos | 0.595485 | 0.144893 | 0.614412 | 1.564103 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
