# run50G_stage56_direction_threshold_tier_b_disablement_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50G_stage56_direction_threshold_tier_b_disablement_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `s390l330h06_b045`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s370l340h06_aonly | false | 6.289617 | 4.702564 | 1.05 | 0.96 | 175.69 | -106.63 | `quality_failed_actual_routed_mt5` |
| s370l340h06_b045 | true | 6.453552 | 4.923077 | 1.05 | 0.99 | 155.89 | -37.16 | `quality_failed_actual_routed_mt5` |
| s380l330h06_aonly | false | 6.065574 | 4.574359 | 1.05 | 1.02 | 176.29 | 49.26 | `quality_or_density_inconclusive_actual_routed_mt5` |
| s380l330h06_b045 | true | 6.224044 | 4.789744 | 1.05 | 1.01 | 173.33 | 42.93 | `quality_or_density_inconclusive_actual_routed_mt5` |
| s390l330h06_aonly | false | 5.852459 | 4.384615 | 1.09 | 1.02 | 287.07 | 58.6 | `quality_or_density_inconclusive_actual_routed_mt5` |
| s390l330h06_b045 | true | 6.005464 | 4.594872 | 1.08 | 1.04 | 274.44 | 109.52 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| s370l340h06_aonly | validation_is | 0.629253 | -0.347359 | 0.712424 | 1.808743 | False |
| s370l340h06_aonly | oos | 0.606888 | -0.616281 | 0.739368 | 1.225641 | False |
| s370l340h06_b045 | validation_is | 0.630254 | -0.368002 | 0.715495 | 1.836066 | False |
| s370l340h06_b045 | oos | 0.610542 | -0.538708 | 0.742708 | 1.266667 | False |
| s380l330h06_aonly | validation_is | 0.628579 | -0.341180 | 0.713514 | 1.737705 | False |
| s380l330h06_aonly | oos | 0.618376 | -0.444776 | 0.738789 | 1.194872 | False |
| s380l330h06_b045 | validation_is | 0.633164 | -0.347823 | 0.716418 | 1.765027 | False |
| s380l330h06_b045 | oos | 0.615246 | -0.454036 | 0.744111 | 1.225641 | False |
| s390l330h06_aonly | validation_is | 0.627604 | -0.231961 | 0.716153 | 1.661202 | False |
| s390l330h06_aonly | oos | 0.621779 | -0.431462 | 0.736842 | 1.153846 | False |
| s390l330h06_b045 | validation_is | 0.632879 | -0.250282 | 0.718835 | 1.688525 | False |
| s390l330h06_b045 | oos | 0.621078 | -0.377768 | 0.742188 | 1.184615 | False |

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
