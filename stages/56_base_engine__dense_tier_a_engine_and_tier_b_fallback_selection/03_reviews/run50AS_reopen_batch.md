# run50AS_stage56_extratrees_rearm_real_density_guard_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AS_stage56_extratrees_rearm_real_density_guard_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `et40h6_r030_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| et40h6_tr_a | false | 5.338798 | 3.615385 | 1.08 | 1.44 | 196.93 | 663.37 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et40h6_r015_a | false | 5.978142 | 4.271795 | 1.12 | 1.34 | 317.78 | 632.5 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et40h6_r030_a | false | 5.535519 | 3.800000 | 1.14 | 1.39 | 357.69 | 633.65 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et40h6_r050_a | false | 5.382514 | 3.641026 | 1.09 | 1.43 | 216.76 | 650.43 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et40h6_r030_s24l15_a | false | 5.535519 | 3.800000 | 1.14 | 1.39 | 357.69 | 633.65 | `weak_dense_engine_candidate_actual_routed_mt5` |
| et40h8_r030_a | false | 5.398907 | 3.641026 | 1.04 | 1.34 | 109.06 | 592.96 | `quality_or_density_inconclusive_actual_routed_mt5` |
| et40h6_r030_b | true | 5.584699 | 3.892308 | 1.16 | 1.39 | 385.93 | 639.18 | `weak_dense_engine_candidate_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| et40h6_tr_a | validation_is | 0.598507 | -0.298434 | 0.548618 | 2.409836 | False |
| et40h6_tr_a | oos | 0.618090 | 0.440950 | 0.520567 | 1.733333 | False |
| et40h6_r015_a | validation_is | 0.600701 | -0.209525 | 0.615174 | 2.300546 | False |
| et40h6_r015_a | oos | 0.606260 | 0.259304 | 0.620648 | 1.620513 | False |
| et40h6_r030_a | validation_is | 0.600148 | -0.146900 | 0.573544 | 2.360656 | False |
| et40h6_r030_a | oos | 0.615901 | 0.355128 | 0.546559 | 1.723077 | False |
| et40h6_r050_a | validation_is | 0.599015 | -0.279939 | 0.553299 | 2.404372 | False |
| et40h6_r050_a | oos | 0.617139 | 0.416099 | 0.522535 | 1.738462 | False |
| et40h6_r030_s24l15_a | validation_is | 0.600148 | -0.146900 | 0.573544 | 2.360656 | False |
| et40h6_r030_s24l15_a | oos | 0.615901 | 0.355128 | 0.546559 | 1.723077 | False |
| et40h8_r030_a | validation_is | 0.603753 | -0.389615 | 0.563765 | 2.355191 | False |
| et40h8_r030_a | oos | 0.588181 | 0.335155 | 0.542254 | 1.666667 | False |
| et40h6_r030_b | validation_is | 0.600498 | -0.122378 | 0.573386 | 2.382514 | False |
| et40h6_r030_b | oos | 0.615861 | 0.342134 | 0.552042 | 1.743590 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
