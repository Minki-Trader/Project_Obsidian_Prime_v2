# run50AE_stage56_vl_cooldown_density_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AE_stage56_vl_cooldown_density_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `c08b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| c06a | false | 4.710383 | 3.297436 | 0.96 | 1.18 | -121.9 | 333.23 | `quality_failed_actual_routed_mt5` |
| c06b | true | 4.770492 | 3.348718 | 0.95 | 1.14 | -125.69 | 262.13 | `quality_failed_actual_routed_mt5` |
| c08a | false | 4.289617 | 3.133333 | 1.04 | 1.17 | 94.23 | 288.55 | `quality_or_density_inconclusive_actual_routed_mt5` |
| c08b | true | 4.322404 | 3.153846 | 1.05 | 1.19 | 118.68 | 330.59 | `weak_dense_engine_candidate_actual_routed_mt5` |
| c10a | false | 4.005464 | 2.856410 | 0.97 | 1.11 | -65.0 | 162.68 | `quality_failed_actual_routed_mt5` |
| c10b | true | 4.043716 | 2.841026 | 0.97 | 1.18 | -65.78 | 267.6 | `quality_failed_actual_routed_mt5` |
| em6a | false | 3.480874 | 2.507692 | 0.95 | 1.04 | -104.37 | 61.2 | `quality_failed_actual_routed_mt5` |
| em6b | true | 3.508197 | 2.594872 | 0.97 | 0.98 | -78.71 | -34.72 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| c06a | validation_is | 0.628654 | -0.641415 | 0.574246 | 2.005464 | False |
| c06a | oos | 0.581080 | 0.018243 | 0.564541 | 1.435897 | False |
| c06b | validation_is | 0.635067 | -0.643975 | 0.576174 | 2.021858 | False |
| c06b | oos | 0.581641 | -0.098576 | 0.560490 | 1.471795 | False |
| c08a | validation_is | 0.626483 | -0.379962 | 0.528662 | 2.021858 | False |
| c08a | oos | 0.595531 | -0.027741 | 0.536825 | 1.451282 | False |
| c08b | validation_is | 0.625219 | -0.349962 | 0.528445 | 2.038251 | False |
| c08b | oos | 0.598210 | 0.037545 | 0.539837 | 1.451282 | False |
| c10a | validation_is | 0.632595 | -0.588677 | 0.499318 | 2.005464 | False |
| c10a | oos | 0.590337 | -0.207935 | 0.475763 | 1.497436 | False |
| c10b | validation_is | 0.634873 | -0.588892 | 0.493243 | 2.049180 | False |
| c10b | oos | 0.600336 | -0.016968 | 0.467509 | 1.512821 | False |
| em6a | validation_is | 0.630818 | -0.663846 | 0.555730 | 1.546448 | False |
| em6a | oos | 0.577147 | -0.374847 | 0.562372 | 1.097436 | False |
| em6b | validation_is | 0.632098 | -0.622601 | 0.551402 | 1.573770 | False |
| em6b | oos | 0.584084 | -0.568617 | 0.565217 | 1.128205 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `validation_pf`: validation PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
