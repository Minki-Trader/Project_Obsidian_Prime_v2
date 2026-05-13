# run50Z_stage56_partial_buy_adx_reintro_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50Z_stage56_partial_buy_adx_reintro_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nfz_s31l18_c3_s2030_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfz_s31l18_c3_s2030_a | false | 7.142077 | 4.969231 | 1.15 | 1.08 | 457.87 | 201.81 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfz_s31l18_c3_s2030_b | true | 7.196721 | 5.056410 | 1.15 | 1.1 | 451.99 | 251.32 | `strong_selected_research_baseline_candidate_actual_routed_mt5` |
| nfz_s30l17_c3_l25_a | false | 4.857923 | 3.276923 | 1.15 | 1.12 | 351.33 | 214.53 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfz_s29l16_c3_l30_a | false | 5.420765 | 3.748718 | 1.16 | 1.08 | 381.44 | 166.44 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfz_s28l15_c3_l35_a | false | 6.213115 | 4.179487 | 1.06 | 1.16 | 157.12 | 333.12 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfz_s27l15_c6_l30_a | false | 4.431694 | 2.979487 | 1.11 | 1.2 | 250.43 | 305.18 | `density_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfz_s31l18_c3_s2030_a | validation_is | 0.616404 | -0.149679 | 0.751339 | 1.775956 | False |
| nfz_s31l18_c3_s2030_a | oos | 0.609801 | -0.291734 | 0.750258 | 1.241026 | False |
| nfz_s31l18_c3_s2030_b | validation_is | 0.614284 | -0.156803 | 0.750949 | 1.792350 | False |
| nfz_s31l18_c3_s2030_b | oos | 0.605995 | -0.245112 | 0.748479 | 1.271795 | False |
| nfz_s30l17_c3_l25_a | validation_is | 0.631400 | -0.104803 | 0.566929 | 2.103825 | False |
| nfz_s30l17_c3_l25_a | oos | 0.612328 | -0.164272 | 0.564945 | 1.425641 | False |
| nfz_s29l16_c3_l30_a | validation_is | 0.626093 | -0.115484 | 0.621976 | 2.049180 | False |
| nfz_s29l16_c3_l30_a | oos | 0.629732 | -0.272312 | 0.615595 | 1.441026 | False |
| nfz_s28l15_c3_l35_a | validation_is | 0.623209 | -0.361812 | 0.676341 | 2.010929 | False |
| nfz_s28l15_c3_l35_a | oos | 0.606878 | -0.091264 | 0.669939 | 1.379487 | False |
| nfz_s27l15_c6_l30_a | validation_is | 0.648103 | -0.191208 | 0.532676 | 2.071038 | False |
| nfz_s27l15_c6_l30_a | oos | 0.604636 | 0.025267 | 0.509466 | 1.461538 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
