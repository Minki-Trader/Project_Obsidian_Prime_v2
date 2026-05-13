# run50L_stage56_lifecycle_cooldown_model_axis_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50L_stage56_lifecycle_cooldown_model_axis_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf150_c6_h10_s370l270_b045`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf150_c6_h10_s370l270_aonly | false | 6.185792 | 4.056410 | 1.02 | 1.14 | 75.91 | 326.85 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf150_c6_h10_s370l270_b045 | true | 6.693989 | 4.292308 | 1.04 | 1.19 | 125.87 | 413.78 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf150_c12_h10_s330l240_aonly | false | 5.043716 | 3.215385 | 0.96 | 0.99 | -110.0 | -19.91 | `quality_failed_actual_routed_mt5` |
| nf150_c12_h10_s330l240_b045 | true | 5.459016 | 3.502564 | 0.96 | 1.1 | -88.1 | 186.39 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nf150_c6_h10_s370l270_aonly | validation_is | 0.585763 | -0.432942 | 0.679329 | 1.983607 | False |
| nf150_c6_h10_s370l270_aonly | oos | 0.593149 | -0.086789 | 0.682680 | 1.287179 | False |
| nf150_c6_h10_s370l270_b045 | validation_is | 0.601982 | -0.397249 | 0.706939 | 1.961749 | False |
| nf150_c6_h10_s370l270_b045 | oos | 0.601528 | -0.005639 | 0.682198 | 1.364103 | False |
| nf150_c12_h10_s330l240_aonly | validation_is | 0.575080 | -0.619177 | 0.414951 | 2.950820 | False |
| nf150_c12_h10_s330l240_aonly | oos | 0.597488 | -0.531754 | 0.352472 | 2.082051 | False |
| nf150_c12_h10_s330l240_b045 | validation_is | 0.599176 | -0.588188 | 0.375375 | 3.409836 | False |
| nf150_c12_h10_s330l240_b045 | oos | 0.614695 | -0.227101 | 0.339678 | 2.312821 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `validation_pf`: validation PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
