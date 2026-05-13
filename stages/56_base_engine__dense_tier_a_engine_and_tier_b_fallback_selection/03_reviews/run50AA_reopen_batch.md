# run50AA_stage56_same_move_cost_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AA_stage56_same_move_cost_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nfaa_s23l13_c6_l30_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfaa_s25l14_c6_l30_a | false | 4.431694 | 2.979487 | 1.11 | 1.2 | 250.43 | 305.18 | `density_failed_actual_routed_mt5` |
| nfaa_s23l13_c6_l30_a | false | 4.431694 | 2.979487 | 1.11 | 1.2 | 250.43 | 305.18 | `density_failed_actual_routed_mt5` |
| nfaa_s23l13_c6_l30_b | true | 4.464481 | 3.020513 | 1.14 | 1.21 | 288.34 | 308.82 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfaa_s21l12_c6_l30_a | false | 4.431694 | 2.979487 | 1.11 | 1.2 | 250.43 | 305.18 | `density_failed_actual_routed_mt5` |
| nfaa_s23l13_c5_l30_a | false | 4.743169 | 3.148718 | 1.04 | 1.14 | 99.11 | 227.77 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nfaa_s23l13_c6_l35_a | false | 4.983607 | 3.405128 | 1.13 | 1.08 | 305.19 | 134.0 | `weak_dense_engine_candidate_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfaa_s25l14_c6_l30_a | validation_is | 0.648103 | -0.191208 | 0.532676 | 2.071038 | False |
| nfaa_s25l14_c6_l30_a | oos | 0.604636 | 0.025267 | 0.509466 | 1.461538 | False |
| nfaa_s23l13_c6_l30_a | validation_is | 0.648103 | -0.191208 | 0.532676 | 2.071038 | False |
| nfaa_s23l13_c6_l30_a | oos | 0.604636 | 0.025267 | 0.509466 | 1.461538 | False |
| nfaa_s23l13_c6_l30_b | validation_is | 0.645337 | -0.147075 | 0.525092 | 2.120219 | False |
| nfaa_s23l13_c6_l30_b | oos | 0.607286 | 0.024312 | 0.504244 | 1.497436 | False |
| nfaa_s21l12_c6_l30_a | validation_is | 0.648103 | -0.191208 | 0.532676 | 2.071038 | False |
| nfaa_s21l12_c6_l30_a | oos | 0.604636 | 0.025267 | 0.509466 | 1.461538 | False |
| nfaa_s23l13_c5_l30_a | validation_is | 0.631936 | -0.385818 | 0.556452 | 2.103825 | False |
| nfaa_s23l13_c5_l30_a | oos | 0.613585 | -0.129039 | 0.550489 | 1.415385 | False |
| nfaa_s23l13_c6_l35_a | validation_is | 0.636161 | -0.165362 | 0.581140 | 2.087432 | False |
| nfaa_s23l13_c6_l35_a | oos | 0.605593 | -0.298193 | 0.572289 | 1.456410 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
