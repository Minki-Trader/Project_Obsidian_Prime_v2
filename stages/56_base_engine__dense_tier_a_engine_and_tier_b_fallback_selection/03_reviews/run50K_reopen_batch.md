# run50K_stage56_model_axis_density_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50K_stage56_model_axis_density_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf150_h10_s420l360_b045`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf150_h10_s420l360_aonly | false | 6.907104 | 4.958974 | 1.01 | 0.97 | 20.68 | -81.84 | `quality_failed_actual_routed_mt5` |
| nf150_h10_s420l360_b045 | true | 7.704918 | 5.323077 | 1.03 | 0.98 | 120.56 | -53.42 | `quality_failed_actual_routed_mt5` |
| nf150_h10_s400l300_aonly | false | 7.459016 | 5.205128 | 1.02 | 0.96 | 86.49 | -145.52 | `quality_failed_actual_routed_mt5` |
| recent24_h10_s400l300_aonly | false | 5.453552 | 4.287179 | 0.92 | 0.87 | -260.41 | -384.93 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nf150_h10_s420l360_aonly | validation_is | 0.615857 | -0.483639 | 0.781646 | 1.508197 | False |
| nf150_h10_s420l360_aonly | oos | 0.616694 | -0.584633 | 0.786970 | 1.056410 | False |
| nf150_h10_s420l360_b045 | validation_is | 0.595702 | -0.414496 | 0.797163 | 1.562842 | False |
| nf150_h10_s420l360_b045 | oos | 0.619826 | -0.551464 | 0.786127 | 1.138462 | False |
| nf150_h10_s400l300_aonly | validation_is | 0.606165 | -0.436637 | 0.779487 | 1.644809 | False |
| nf150_h10_s400l300_aonly | oos | 0.607933 | -0.643369 | 0.785222 | 1.117949 | False |
| recent24_h10_s400l300_aonly | validation_is | 0.628829 | -0.760932 | 0.669339 | 1.803279 | False |
| recent24_h10_s400l300_aonly | oos | 0.622675 | -0.960443 | 0.710526 | 1.241026 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_net_positive`: OOS net > 0
- `validation_pf`: validation PF >= 1.10
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
