# run50P_stage56_nonflat_side_adx_density_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50P_stage56_nonflat_side_adx_density_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf_h10c2_s390l280_b_sadx`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf_h10c0_s420l360_a_sadx | false | 6.524590 | 4.702564 | 1.0 | 0.95 | -12.22 | -168.44 | `quality_failed_actual_routed_mt5` |
| nf_h10c0_s420l360_b_sadx | true | 7.284153 | 5.061538 | 1.04 | 1.0 | 173.46 | -10.97 | `quality_failed_actual_routed_mt5` |
| nf_h10c0_s400l300_a_sadx | false | 7.000000 | 4.912821 | 1.01 | 0.95 | 51.31 | -179.24 | `quality_failed_actual_routed_mt5` |
| nf_h10c0_s400l300_b_sadx | true | 7.786885 | 5.307692 | 1.04 | 0.98 | 150.62 | -80.51 | `quality_failed_actual_routed_mt5` |
| nf_h10c2_s390l280_a_sadx | false | 6.295082 | 4.420513 | 1.01 | 1.03 | 54.49 | 71.67 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_h10c2_s390l280_b_sadx | true | 7.136612 | 4.758974 | 1.03 | 1.05 | 116.66 | 140.04 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nf_h10c0_s420l360_a_sadx | validation_is | 0.630481 | -0.510235 | 0.780570 | 1.431694 | False |
| nf_h10c0_s420l360_a_sadx | oos | 0.615714 | -0.683686 | 0.782988 | 1.020513 | False |
| nf_h10c0_s420l360_b_sadx | validation_is | 0.608929 | -0.369872 | 0.797449 | 1.475410 | False |
| nf_h10c0_s420l360_b_sadx | oos | 0.627230 | -0.511114 | 0.781155 | 1.107692 | False |
| nf_h10c0_s400l300_a_sadx | validation_is | 0.616495 | -0.459945 | 0.779859 | 1.540984 | False |
| nf_h10c0_s400l300_a_sadx | oos | 0.608610 | -0.687098 | 0.776618 | 1.097436 | False |
| nf_h10c0_s400l300_b_sadx | validation_is | 0.617684 | -0.394302 | 0.795789 | 1.590164 | False |
| nf_h10c0_s400l300_b_sadx | oos | 0.624231 | -0.577787 | 0.783575 | 1.148718 | False |
| nf_h10c2_s390l280_a_sadx | validation_is | 0.607355 | -0.452700 | 0.745660 | 1.601093 | False |
| nf_h10c2_s390l280_a_sadx | oos | 0.593248 | -0.416856 | 0.725058 | 1.215385 | False |
| nf_h10c2_s390l280_b_sadx | validation_is | 0.615519 | -0.410674 | 0.763400 | 1.688525 | False |
| nf_h10c2_s390l280_b_sadx | oos | 0.614114 | -0.349095 | 0.724138 | 1.312821 | False |

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
