# run50J_stage56_hold_extension_direction_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50J_stage56_hold_extension_direction_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `h10_s400l295_aonly`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| h10_s390l300_aonly | false | 4.497268 | 3.210256 | 1.11 | 1.04 | 327.11 | 107.53 | `quality_or_density_inconclusive_actual_routed_mt5` |
| h10_s390l300_b045 | true | 4.666667 | 3.400000 | 1.09 | 1.03 | 273.55 | 68.94 | `quality_or_density_inconclusive_actual_routed_mt5` |
| h10_s400l295_aonly | false | 4.360656 | 3.071795 | 1.14 | 1.07 | 397.72 | 157.34 | `weak_dense_engine_candidate_actual_routed_mt5` |
| h10_s400l295_b045 | true | 4.519126 | 3.266667 | 1.15 | 1.01 | 418.26 | 27.75 | `quality_or_density_inconclusive_actual_routed_mt5` |
| h10_s410l290_aonly | false | 4.174863 | 2.943590 | 1.09 | 1.03 | 267.4 | 68.19 | `density_failed_actual_routed_mt5` |
| h10_s410l290_b045 | true | 4.327869 | 3.123077 | 1.1 | 1.01 | 282.43 | 27.66 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| h10_s390l300_aonly | validation_is | 0.635531 | -0.102539 | 0.640340 | 1.617486 | False |
| h10_s390l300_aonly | oos | 0.624112 | -0.328227 | 0.637380 | 1.164103 | False |
| h10_s390l300_b045 | validation_is | 0.624950 | -0.179684 | 0.645199 | 1.655738 | False |
| h10_s390l300_b045 | oos | 0.620503 | -0.396018 | 0.653092 | 1.179487 | False |
| h10_s400l295_aonly | validation_is | 0.638763 | -0.001604 | 0.639098 | 1.573770 | False |
| h10_s400l295_aonly | oos | 0.626980 | -0.237329 | 0.636060 | 1.117949 | False |
| h10_s400l295_b045 | validation_is | 0.632809 | 0.005756 | 0.644498 | 1.606557 | False |
| h10_s400l295_b045 | oos | 0.620676 | -0.456436 | 0.651491 | 1.138462 | False |
| h10_s410l290_aonly | validation_is | 0.641014 | -0.150000 | 0.633508 | 1.530055 | False |
| h10_s410l290_aonly | oos | 0.620253 | -0.381202 | 0.637631 | 1.066667 | False |
| h10_s410l290_b045 | validation_is | 0.635297 | -0.143396 | 0.638889 | 1.562842 | False |
| h10_s410l290_b045 | oos | 0.618882 | -0.454581 | 0.658456 | 1.066667 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
