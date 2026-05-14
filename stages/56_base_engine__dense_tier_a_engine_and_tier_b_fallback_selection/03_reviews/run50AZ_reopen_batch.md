# run50AZ_stage56_cooldown12_broad_model_source_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AZ_stage56_cooldown12_broad_model_source_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf250c12_h4_s160l090_a`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| et10c12_h4_s160l090_a | false | 4.071038 | 3.092308 | 0.78 | 1.11 | -395.56 | 135.34 | `quality_failed_actual_routed_mt5` |
| et10c12_h4_s160l090_b | true | 4.163934 | 3.184615 | 0.8 | 1.11 | -379.85 | 133.66 | `quality_failed_actual_routed_mt5` |
| nf250c12_h4_s160l090_a | false | 4.513661 | 3.035897 | 1.03 | 0.91 | 45.74 | -118.83 | `quality_failed_actual_routed_mt5` |
| r24balc12_h4_s140l080_a | false | 3.901639 | 2.958974 | 0.77 | 0.85 | -405.47 | -223.22 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| et10c12_h4_s160l090_a | validation_is | 0.600934 | -1.030953 | 0.210738 | 3.213115 | False |
| et10c12_h4_s160l090_a | oos | 0.591983 | -0.275556 | 0.230514 | 2.379487 | False |
| et10c12_h4_s160l090_b | validation_is | 0.605638 | -0.998491 | 0.216535 | 3.262295 | False |
| et10c12_h4_s160l090_b | oos | 0.595894 | -0.284767 | 0.235105 | 2.435897 | False |
| nf250c12_h4_s160l090_a | validation_is | 0.595652 | -0.444625 | 0.179177 | 3.704918 | False |
| nf250c12_h4_s160l090_a | oos | 0.603662 | -0.700726 | 0.118243 | 2.676923 | False |
| r24balc12_h4_s140l080_a | validation_is | 0.624638 | -1.067885 | 0.217087 | 3.054645 | False |
| r24balc12_h4_s140l080_a | oos | 0.595075 | -0.886863 | 0.244367 | 2.235897 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `oos_net_positive`: OOS net > 0
- `validation_pf`: validation PF >= 1.10
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B disabled but no matched enabled comparison in this batch
