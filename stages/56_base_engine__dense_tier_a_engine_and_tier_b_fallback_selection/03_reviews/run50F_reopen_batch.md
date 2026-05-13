# run50F_stage56_cooldown_b_tight_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50F_stage56_cooldown_b_tight_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `d330h06_b045_c1`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| d330h06_b042_c1 | true | 6.393443 | 4.758974 | 1.01 | 1.03 | 33.33 | 86.1 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d320h06_b042_c1 | true | 6.393443 | 4.758974 | 1.01 | 1.03 | 33.33 | 86.1 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d330h06_b045_c1 | true | 6.333333 | 4.728205 | 1.02 | 1.04 | 53.4 | 114.76 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d320h06_b045_c1 | true | 6.333333 | 4.728205 | 1.02 | 1.04 | 53.4 | 114.76 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d315h06_b045_c2 | true | 5.863388 | 4.317949 | 1.06 | 1.02 | 164.1 | 42.81 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d305h06_b045_c2 | true | 5.863388 | 4.317949 | 1.06 | 1.02 | 164.1 | 42.81 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| d330h06_b042_c1 | validation_is | 0.618432 | -0.471513 | 0.693162 | 1.961749 | False |
| d330h06_b042_c1 | oos | 0.622368 | -0.407220 | 0.713362 | 1.364103 | False |
| d320h06_b042_c1 | validation_is | 0.618432 | -0.471513 | 0.693162 | 1.961749 | False |
| d320h06_b042_c1 | oos | 0.622368 | -0.407220 | 0.713362 | 1.364103 | False |
| d330h06_b045_c1 | validation_is | 0.619816 | -0.453926 | 0.696290 | 1.923497 | False |
| d330h06_b045_c1 | oos | 0.624341 | -0.375531 | 0.713666 | 1.353846 | False |
| d320h06_b045_c1 | validation_is | 0.619816 | -0.453926 | 0.696290 | 1.923497 | False |
| d320h06_b045_c1 | oos | 0.624341 | -0.375531 | 0.713666 | 1.353846 | False |
| d315h06_b045_c2 | validation_is | 0.628996 | -0.347064 | 0.667288 | 1.950820 | False |
| d315h06_b045_c2 | oos | 0.607006 | -0.449157 | 0.685273 | 1.358974 | False |
| d305h06_b045_c2 | validation_is | 0.628996 | -0.347064 | 0.667288 | 1.950820 | False |
| d305h06_b045_c2 | oos | 0.607006 | -0.449157 | 0.685273 | 1.358974 | False |

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
