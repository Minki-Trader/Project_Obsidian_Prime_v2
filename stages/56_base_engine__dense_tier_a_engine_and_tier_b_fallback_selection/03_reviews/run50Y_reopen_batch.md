# run50Y_stage56_buy_side_firewall_tierb_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50Y_stage56_buy_side_firewall_tierb_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nfy_s31l18_c3_adx_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfy_s33l20_c3_adx_a | false | 3.857923 | 2.574359 | 1.07 | 1.33 | 129.45 | 420.75 | `density_failed_actual_routed_mt5` |
| nfy_s31l18_c3_adx_b | true | 3.868852 | 2.625641 | 1.09 | 1.29 | 166.36 | 378.86 | `density_failed_actual_routed_mt5` |
| nfy_s29l16_c6_adx_b | true | 3.196721 | 2.194872 | 1.02 | 1.21 | 29.3 | 230.9 | `density_failed_actual_routed_mt5` |
| nfy_s33l20_c3_lvol_a | false | 6.125683 | 4.323077 | 0.99 | 1.04 | -27.78 | 102.2 | `quality_failed_actual_routed_mt5` |
| nfy_s33l20_c3_lvol_b | true | 6.180328 | 4.410256 | 0.97 | 1.05 | -79.97 | 118.66 | `quality_failed_actual_routed_mt5` |
| nfy_s31l18_c6_lvol_b | true | 4.967213 | 3.620513 | 0.97 | 1.18 | -67.82 | 317.34 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfy_s33l20_c3_adx_a | validation_is | 0.605062 | -0.316643 | 0.487252 | 1.978142 | False |
| nfy_s33l20_c3_adx_a | oos | 0.631381 | 0.338147 | 0.470120 | 1.364103 | False |
| nfy_s31l18_c3_adx_b | validation_is | 0.604484 | -0.265028 | 0.487288 | 1.983607 | False |
| nfy_s31l18_c3_adx_b | oos | 0.628193 | 0.239961 | 0.474609 | 1.379487 | False |
| nfy_s29l16_c6_adx_b | validation_is | 0.628694 | -0.449915 | 0.393162 | 1.939891 | False |
| nfy_s29l16_c6_adx_b | oos | 0.629406 | 0.039486 | 0.397196 | 1.323077 | False |
| nfy_s33l20_c3_lvol_a | validation_is | 0.621825 | -0.524781 | 0.669045 | 2.027322 | False |
| nfy_s33l20_c3_lvol_a | oos | 0.594588 | -0.378766 | 0.657177 | 1.482051 | False |
| nfy_s33l20_c3_lvol_b | validation_is | 0.620175 | -0.570707 | 0.667551 | 2.054645 | False |
| nfy_s33l20_c3_lvol_b | oos | 0.594078 | -0.362023 | 0.660465 | 1.497436 | False |
| nfy_s31l18_c6_lvol_b | validation_is | 0.629906 | -0.574609 | 0.574257 | 2.114754 | False |
| nfy_s31l18_c6_lvol_b | oos | 0.594022 | -0.050510 | 0.569405 | 1.558974 | False |

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
