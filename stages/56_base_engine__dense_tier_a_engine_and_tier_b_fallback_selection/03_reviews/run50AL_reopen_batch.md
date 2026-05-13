# run50AL_stage56_entry_confidence_rearm_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AL_stage56_entry_confidence_rearm_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nfal_s33l20_r060`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfal_s33l20_r020 | true | 7.202186 | 4.789744 | 1.13 | 1.09 | 423.32 | 213.37 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfal_s33l20_r040 | true | 5.530055 | 3.651282 | 1.16 | 1.18 | 373.47 | 310.99 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfal_s33l20_r060 | true | 4.857923 | 3.292308 | 1.19 | 1.25 | 383.21 | 390.95 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfal_s33l20_r040l40 | true | 5.300546 | 3.574359 | 1.15 | 1.19 | 347.36 | 324.45 | `weak_dense_engine_candidate_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfal_s33l20_r020 | validation_is | 0.610455 | -0.178816 | 0.707132 | 2.109290 | False |
| nfal_s33l20_r020 | oos | 0.597298 | -0.271552 | 0.663812 | 1.610256 | False |
| nfal_s33l20_r040 | validation_is | 0.611627 | -0.130958 | 0.522727 | 2.639344 | False |
| nfal_s33l20_r040 | oos | 0.590385 | -0.063216 | 0.495787 | 1.841026 | False |
| nfal_s33l20_r060 | validation_is | 0.600843 | -0.068943 | 0.475816 | 2.546448 | False |
| nfal_s33l20_r060 | oos | 0.601398 | 0.108956 | 0.456386 | 1.789744 | False |
| nfal_s33l20_r040l40 | validation_is | 0.615695 | -0.141897 | 0.518557 | 2.551913 | False |
| nfal_s33l20_r040l40 | oos | 0.600974 | -0.034505 | 0.489240 | 1.825641 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
