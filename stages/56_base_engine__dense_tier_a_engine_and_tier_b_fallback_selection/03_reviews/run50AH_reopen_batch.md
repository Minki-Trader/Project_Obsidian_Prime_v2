# run50AH_stage56_s25_model_axis_oos_density_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AH_stage56_s25_model_axis_oos_density_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf200s25b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| c025s25a | false | 5.377049 | 3.553846 | 1.18 | 1.16 | 449.96 | 294.18 | `weak_dense_engine_candidate_actual_routed_mt5` |
| c025s25b | true | 5.431694 | 3.605128 | 1.14 | 1.24 | 364.33 | 427.07 | `weak_dense_engine_candidate_actual_routed_mt5` |
| c100s25a | false | 5.349727 | 3.625641 | 1.16 | 1.26 | 398.56 | 468.44 | `weak_dense_engine_candidate_actual_routed_mt5` |
| c100s25b | true | 5.393443 | 3.697436 | 1.13 | 1.31 | 334.28 | 545.59 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nf200s25a | false | 5.437158 | 3.733333 | 1.23 | 1.17 | 550.2 | 310.59 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nf200s25b | true | 5.513661 | 3.789744 | 1.18 | 1.24 | 459.98 | 428.88 | `weak_dense_engine_candidate_actual_routed_mt5` |
| r23s25a | false | 3.814208 | 2.820513 | 1.06 | 0.98 | 122.86 | -29.41 | `quality_failed_actual_routed_mt5` |
| r23s25b | true | 3.841530 | 2.958974 | 1.05 | 0.99 | 108.69 | -22.21 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| c025s25a | validation_is | 0.601619 | -0.042724 | 0.595528 | 2.174863 | False |
| c025s25a | oos | 0.582234 | -0.075498 | 0.590188 | 1.456410 | False |
| c025s25b | validation_is | 0.601900 | -0.133471 | 0.596579 | 2.191257 | False |
| c025s25b | oos | 0.581566 | 0.107496 | 0.588905 | 1.482051 | False |
| c100s25a | validation_is | 0.605445 | -0.092891 | 0.594484 | 2.169399 | False |
| c100s25a | oos | 0.587306 | 0.162574 | 0.592645 | 1.476923 | False |
| c100s25b | validation_is | 0.607057 | -0.161317 | 0.594732 | 2.185792 | False |
| c100s25b | oos | 0.580989 | 0.256713 | 0.599168 | 1.482051 | False |
| nf200s25a | validation_is | 0.606140 | 0.052965 | 0.595980 | 2.196721 | False |
| nf200s25a | oos | 0.587402 | -0.073365 | 0.609890 | 1.456410 | False |
| nf200s25b | validation_is | 0.606710 | -0.044123 | 0.598612 | 2.213115 | False |
| nf200s25b | oos | 0.581881 | 0.080352 | 0.608931 | 1.482051 | False |
| r23s25a | validation_is | 0.641396 | -0.323983 | 0.508596 | 1.874317 | False |
| r23s25a | oos | 0.585318 | -0.553473 | 0.505455 | 1.394872 | False |
| r23s25b | validation_is | 0.643724 | -0.345391 | 0.504979 | 1.901639 | False |
| r23s25b | oos | 0.591250 | -0.538492 | 0.519931 | 1.420513 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
