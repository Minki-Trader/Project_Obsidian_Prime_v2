# run50AV_stage56_cooldown12_new_source_density_survival_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AV_stage56_cooldown12_new_source_density_survival_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf200c12_h4_s240l150_a`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| et40c12_h4_s220l140_a | false | 3.464481 | 2.600000 | 0.93 | 1.37 | -113.5 | 353.84 | `quality_failed_actual_routed_mt5` |
| et40c12_h4_s200l120_a | false | 3.464481 | 2.600000 | 0.93 | 1.37 | -113.5 | 353.84 | `quality_failed_actual_routed_mt5` |
| et30c12_h4_s220l140_a | false | 3.655738 | 2.553846 | 0.88 | 1.28 | -179.23 | 274.45 | `quality_failed_actual_routed_mt5` |
| et20c12_h4_s240l150_a | false | 3.590164 | 2.738462 | 0.95 | 0.99 | -82.27 | -14.4 | `quality_failed_actual_routed_mt5` |
| nf200c12_h4_s240l150_a | false | 4.295082 | 3.041026 | 1.29 | 1.01 | 435.08 | 7.66 | `quality_or_density_inconclusive_actual_routed_mt5` |
| et40c12_h4_s220l140_b | true | 3.480874 | 2.671795 | 0.99 | 1.18 | -9.26 | 184.8 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| et40c12_h4_s220l140_a | validation_is | 0.610498 | -0.679022 | 0.148265 | 2.950820 | False |
| et40c12_h4_s220l140_a | oos | 0.608833 | 0.197909 | 0.187377 | 2.112821 | False |
| et40c12_h4_s200l120_a | validation_is | 0.610498 | -0.679022 | 0.148265 | 2.950820 | False |
| et40c12_h4_s200l120_a | oos | 0.608833 | 0.197909 | 0.187377 | 2.112821 | False |
| et30c12_h4_s220l140_a | validation_is | 0.579434 | -0.767907 | 0.185351 | 2.978142 | False |
| et30c12_h4_s220l140_a | oos | 0.596177 | 0.051104 | 0.184739 | 2.082051 | False |
| et20c12_h4_s240l150_a | validation_is | 0.618508 | -0.625221 | 0.153729 | 3.038251 | False |
| et20c12_h4_s240l150_a | oos | 0.597969 | -0.526966 | 0.209738 | 2.164103 | False |
| nf200c12_h4_s240l150_a | validation_is | 0.613343 | 0.053537 | 0.148855 | 3.655738 | False |
| nf200c12_h4_s240l150_a | oos | 0.615093 | -0.487083 | 0.133221 | 2.635897 | False |
| et40c12_h4_s220l140_b | validation_is | 0.626123 | -0.514537 | 0.142857 | 2.983607 | False |
| et40c12_h4_s220l140_b | oos | 0.596430 | -0.145298 | 0.178503 | 2.194872 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B disabled but no matched enabled comparison in this batch
