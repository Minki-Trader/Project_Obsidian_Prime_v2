# run50W_stage56_nonflat_regime_firewall_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50W_stage56_nonflat_regime_firewall_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nfw_s33l20_c3_sadx`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfw_s37l24_c0_sadx | true | 9.972678 | 7.010256 | 1.03 | 0.97 | 125.01 | -118.07 | `quality_failed_actual_routed_mt5` |
| nfw_s37l24_c1_sadx | true | 9.038251 | 6.241026 | 1.04 | 1.06 | 177.38 | 185.04 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nfw_s35l22_c2_sadx | true | 8.185792 | 5.830769 | 1.18 | 1.05 | 600.73 | 139.96 | `selected_research_baseline_candidate_actual_routed_mt5` |
| nfw_s33l20_c3_sadx | true | 7.754098 | 5.384615 | 1.13 | 1.06 | 397.59 | 149.56 | `selected_research_baseline_candidate_actual_routed_mt5` |
| nfw_s37l24_c0_sadxlgt | true | 6.655738 | 4.430769 | 0.99 | 1.11 | -40.76 | 269.72 | `quality_failed_actual_routed_mt5` |
| nfw_s35l22_c1_sadxlgt | true | 6.120219 | 4.066667 | 1.02 | 1.07 | 47.4 | 174.23 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfw_s37l24_c0_sadx | validation_is | 0.620046 | -0.431501 | 0.832329 | 1.672131 | False |
| nfw_s37l24_c0_sadx | oos | 0.581565 | -0.586372 | 0.828822 | 1.200000 | False |
| nfw_s37l24_c1_sadx | validation_is | 0.616111 | -0.392757 | 0.804111 | 1.770492 | False |
| nfw_s37l24_c1_sadx | oos | 0.608262 | -0.347954 | 0.808546 | 1.194872 | False |
| nfw_s35l22_c2_sadx | validation_is | 0.622372 | -0.098979 | 0.779706 | 1.803279 | False |
| nfw_s35l22_c2_sadx | oos | 0.594122 | -0.376904 | 0.780123 | 1.282051 | False |
| nfw_s33l20_c3_sadx | validation_is | 0.624112 | -0.219810 | 0.753347 | 1.912568 | False |
| nfw_s33l20_c3_sadx | oos | 0.596677 | -0.357562 | 0.760000 | 1.292308 | False |
| nfw_s37l24_c0_sadxlgt | validation_is | 0.612588 | -0.533465 | 0.687192 | 2.081967 | False |
| nfw_s37l24_c0_sadxlgt | oos | 0.596143 | -0.187824 | 0.687500 | 1.384615 | False |
| nfw_s35l22_c1_sadxlgt | validation_is | 0.621609 | -0.457679 | 0.646429 | 2.163934 | False |
| nfw_s35l22_c1_sadxlgt | oos | 0.610599 | -0.280290 | 0.650694 | 1.420513 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
