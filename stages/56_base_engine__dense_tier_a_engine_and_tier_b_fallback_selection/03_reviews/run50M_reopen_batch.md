# run50M_stage56_cooldown_threshold_interpolation_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50M_stage56_cooldown_threshold_interpolation_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf150_c8_h10_s340l240_b045`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf150_c6_h10_s350l250_aonly | false | 6.404372 | 4.184615 | 1.01 | 1.2 | 35.34 | 452.98 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf150_c6_h10_s350l250_b045 | true | 6.907104 | 4.430769 | 1.01 | 1.28 | 26.31 | 590.3 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf150_c8_h10_s340l240_aonly | false | 5.945355 | 3.820513 | 1.0 | 1.21 | -3.09 | 404.48 | `quality_failed_actual_routed_mt5` |
| nf150_c8_h10_s340l240_b045 | true | 6.415301 | 4.066667 | 1.03 | 1.11 | 91.64 | 233.06 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nf150_c6_h10_s350l250_aonly | validation_is | 0.585990 | -0.469846 | 0.686860 | 2.005464 | False |
| nf150_c6_h10_s350l250_aonly | oos | 0.595907 | 0.055123 | 0.685049 | 1.317949 | False |
| nf150_c6_h10_s350l250_b045 | validation_is | 0.603088 | -0.479185 | 0.710443 | 2.000000 | False |
| nf150_c6_h10_s350l250_b045 | oos | 0.604276 | 0.183218 | 0.685185 | 1.394872 | False |
| nf150_c8_h10_s340l240_aonly | validation_is | 0.586307 | -0.502840 | 0.647978 | 2.092896 | False |
| nf150_c8_h10_s340l240_aonly | oos | 0.600952 | 0.042926 | 0.644295 | 1.358974 | False |
| nf150_c8_h10_s340l240_b045 | validation_is | 0.598745 | -0.421942 | 0.682283 | 2.038251 | False |
| nf150_c8_h10_s340l240_b045 | oos | 0.588035 | -0.206103 | 0.683480 | 1.287179 | False |

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
