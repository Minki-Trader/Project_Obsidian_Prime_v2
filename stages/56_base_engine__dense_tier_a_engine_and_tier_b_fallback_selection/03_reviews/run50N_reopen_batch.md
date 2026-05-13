# run50N_stage56_side_adx_filter_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50N_stage56_side_adx_filter_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `c6s330l235_b_sadx`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| c6s350l250_a_sadx | false | 5.693989 | 3.717949 | 1.08 | 1.25 | 236.57 | 514.23 | `weak_dense_engine_candidate_actual_routed_mt5` |
| c6s350l250_b_sadx | true | 6.169399 | 3.994872 | 1.09 | 1.25 | 253.33 | 511.43 | `weak_dense_engine_candidate_actual_routed_mt5` |
| c6s330l235_a_sadx | false | 5.721311 | 3.728205 | 1.08 | 1.27 | 238.73 | 536.95 | `weak_dense_engine_candidate_actual_routed_mt5` |
| c6s330l235_b_sadx | true | 6.196721 | 4.005128 | 1.09 | 1.25 | 256.42 | 508.97 | `weak_dense_engine_candidate_actual_routed_mt5` |
| c6s315l225_a_sadx | false | 5.721311 | 3.728205 | 1.08 | 1.27 | 238.73 | 536.95 | `weak_dense_engine_candidate_actual_routed_mt5` |
| c6s315l225_b_sadx | true | 6.196721 | 4.005128 | 1.09 | 1.25 | 256.42 | 508.97 | `weak_dense_engine_candidate_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| c6s350l250_a_sadx | validation_is | 0.586226 | -0.272965 | 0.659309 | 1.939891 | False |
| c6s350l250_a_sadx | oos | 0.598905 | 0.209283 | 0.660690 | 1.261538 | False |
| c6s350l250_b_sadx | validation_is | 0.613260 | -0.275616 | 0.697077 | 1.868852 | False |
| c6s350l250_b_sadx | oos | 0.618249 | 0.156521 | 0.661104 | 1.353846 | False |
| c6s330l235_a_sadx | validation_is | 0.590467 | -0.271987 | 0.660936 | 1.939891 | False |
| c6s330l235_a_sadx | oos | 0.594966 | 0.238583 | 0.658872 | 1.271795 | False |
| c6s330l235_b_sadx | validation_is | 0.614972 | -0.273880 | 0.696649 | 1.879781 | False |
| c6s330l235_b_sadx | oos | 0.619893 | 0.151690 | 0.661972 | 1.353846 | False |
| c6s315l225_a_sadx | validation_is | 0.590467 | -0.271987 | 0.660936 | 1.939891 | False |
| c6s315l225_a_sadx | oos | 0.594966 | 0.238583 | 0.658872 | 1.271795 | False |
| c6s315l225_b_sadx | validation_is | 0.614972 | -0.273880 | 0.696649 | 1.879781 | False |
| c6s315l225_b_sadx | oos | 0.619893 | 0.151690 | 0.661972 | 1.353846 | False |

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
