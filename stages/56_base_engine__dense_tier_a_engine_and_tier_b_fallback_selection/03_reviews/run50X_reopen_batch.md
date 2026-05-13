# run50X_stage56_nonflat_adx_soft_firewall_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50X_stage56_nonflat_adx_soft_firewall_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nfx_s33l20_c3_s2030`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfx_s35l22_c2_s2030 | true | 7.683060 | 5.400000 | 1.16 | 1.08 | 505.06 | 205.86 | `selected_research_baseline_candidate_actual_routed_mt5` |
| nfx_s33l20_c3_s2030 | true | 7.196721 | 5.056410 | 1.15 | 1.1 | 451.99 | 251.32 | `strong_selected_research_baseline_candidate_actual_routed_mt5` |
| nfx_s35l22_c2_s2030l40 | true | 7.038251 | 5.025641 | 1.12 | 1.08 | 367.11 | 211.76 | `selected_research_baseline_candidate_actual_routed_mt5` |
| nfx_s33l20_c3_s2030l40 | true | 6.513661 | 4.641026 | 1.12 | 1.14 | 329.45 | 318.73 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfx_s35l22_c2_s2030l30p | true | 6.010929 | 4.082051 | 1.13 | 1.06 | 357.49 | 147.9 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfx_s33l20_c3_s2030l30p | true | 5.437158 | 3.810256 | 1.19 | 1.08 | 444.73 | 171.66 | `weak_dense_engine_candidate_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfx_s35l22_c2_s2030 | validation_is | 0.617503 | -0.140782 | 0.786629 | 1.639344 | False |
| nfx_s35l22_c2_s2030 | oos | 0.597282 | -0.304501 | 0.769231 | 1.246154 | False |
| nfx_s33l20_c3_s2030 | validation_is | 0.614284 | -0.156803 | 0.750949 | 1.792350 | False |
| nfx_s33l20_c3_s2030 | oos | 0.605995 | -0.245112 | 0.748479 | 1.271795 | False |
| nfx_s35l22_c2_s2030l40 | validation_is | 0.633893 | -0.214977 | 0.750000 | 1.759563 | False |
| nfx_s35l22_c2_s2030l40 | oos | 0.601210 | -0.283918 | 0.734694 | 1.333333 | False |
| nfx_s33l20_c3_s2030l40 | validation_is | 0.623251 | -0.223616 | 0.710570 | 1.885246 | False |
| nfx_s33l20_c3_s2030l40 | oos | 0.602726 | -0.147812 | 0.712707 | 1.333333 | False |
| nfx_s35l22_c2_s2030l30p | validation_is | 0.625663 | -0.175009 | 0.683636 | 1.901639 | False |
| nfx_s35l22_c2_s2030l30p | oos | 0.621122 | -0.314196 | 0.641960 | 1.461538 | False |
| nfx_s33l20_c3_s2030l30p | validation_is | 0.626560 | -0.053035 | 0.621106 | 2.060109 | False |
| nfx_s33l20_c3_s2030l30p | oos | 0.625468 | -0.268964 | 0.611036 | 1.482051 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
