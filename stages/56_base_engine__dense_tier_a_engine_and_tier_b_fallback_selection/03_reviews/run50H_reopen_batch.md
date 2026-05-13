# run50H_stage56_long_density_short_filter_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50H_stage56_long_density_short_filter_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `s410l315h06_b045`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s390l320h06_aonly | false | 5.852459 | 4.384615 | 1.09 | 1.02 | 287.07 | 58.6 | `quality_or_density_inconclusive_actual_routed_mt5` |
| s390l320h06_b045 | true | 6.005464 | 4.594872 | 1.08 | 1.04 | 274.44 | 109.52 | `quality_or_density_inconclusive_actual_routed_mt5` |
| s400l320h06_aonly | false | 5.715847 | 4.230769 | 1.09 | 1.0 | 297.21 | -0.04 | `quality_failed_actual_routed_mt5` |
| s400l320h06_b045 | true | 5.874317 | 4.420513 | 1.09 | 1.03 | 292.46 | 81.62 | `quality_or_density_inconclusive_actual_routed_mt5` |
| s410l315h06_aonly | false | 5.491803 | 4.071795 | 1.08 | 1.01 | 242.77 | 36.26 | `quality_or_density_inconclusive_actual_routed_mt5` |
| s410l315h06_b045 | true | 5.644809 | 4.276923 | 1.08 | 1.06 | 240.62 | 145.24 | `weak_dense_engine_candidate_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| s390l320h06_aonly | validation_is | 0.627604 | -0.231961 | 0.716153 | 1.661202 | False |
| s390l320h06_aonly | oos | 0.621779 | -0.431462 | 0.736842 | 1.153846 | False |
| s390l320h06_b045 | validation_is | 0.632879 | -0.250282 | 0.718835 | 1.688525 | False |
| s390l320h06_b045 | oos | 0.621078 | -0.377768 | 0.742188 | 1.184615 | False |
| s400l320h06_aonly | validation_is | 0.634675 | -0.215860 | 0.715105 | 1.628415 | False |
| s400l320h06_aonly | oos | 0.625477 | -0.500048 | 0.735758 | 1.117949 | False |
| s400l320h06_b045 | validation_is | 0.642516 | -0.227944 | 0.720000 | 1.644809 | False |
| s400l320h06_b045 | oos | 0.622426 | -0.405313 | 0.738979 | 1.153846 | False |
| s410l315h06_aonly | validation_is | 0.635247 | -0.258438 | 0.715423 | 1.562842 | False |
| s410l315h06_aonly | oos | 0.636377 | -0.454332 | 0.739295 | 1.061538 | False |
| s410l315h06_b045 | validation_is | 0.642225 | -0.267067 | 0.719264 | 1.584699 | False |
| s410l315h06_b045 | oos | 0.628700 | -0.325851 | 0.738609 | 1.117949 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `validation_pf`: validation PF >= 1.10
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
