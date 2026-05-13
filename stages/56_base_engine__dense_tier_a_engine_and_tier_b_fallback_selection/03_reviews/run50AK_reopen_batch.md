# run50AK_stage56_entry_transition_gate_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AK_stage56_entry_transition_gate_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nfak_s33l20_tr_s2030`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfak_s33l20_tr_s2030 | true | 4.530055 | 3.030769 | 1.21 | 1.27 | 378.23 | 369.49 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfak_s30l18_tr_s2030 | true | 4.530055 | 3.030769 | 1.21 | 1.27 | 378.23 | 369.49 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfak_s28l16_tr_s2030 | true | 4.530055 | 3.030769 | 1.21 | 1.27 | 378.23 | 369.49 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nfak_s30l18_tr_s2030l40 | true | 4.469945 | 3.020513 | 1.16 | 1.23 | 297.9 | 323.6 | `weak_dense_engine_candidate_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfak_s33l20_tr_s2030 | validation_is | 0.605948 | -0.043752 | 0.464415 | 2.426230 | False |
| nfak_s33l20_tr_s2030 | oos | 0.590549 | 0.125195 | 0.429780 | 1.728205 | False |
| nfak_s30l18_tr_s2030 | validation_is | 0.605948 | -0.043752 | 0.464415 | 2.426230 | False |
| nfak_s30l18_tr_s2030 | oos | 0.590549 | 0.125195 | 0.429780 | 1.728205 | False |
| nfak_s28l16_tr_s2030 | validation_is | 0.605948 | -0.043752 | 0.464415 | 2.426230 | False |
| nfak_s28l16_tr_s2030 | oos | 0.590549 | 0.125195 | 0.429780 | 1.728205 | False |
| nfak_s30l18_tr_s2030l40 | validation_is | 0.610090 | -0.135819 | 0.453545 | 2.442623 | False |
| nfak_s30l18_tr_s2030l40 | oos | 0.600711 | 0.049406 | 0.410866 | 1.779487 | False |

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
