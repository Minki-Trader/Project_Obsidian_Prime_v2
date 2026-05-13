# run50AP_stage56_lgbm_fwd3_new_source_real_density_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AP_stage56_lgbm_fwd3_new_source_real_density_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `raw3_s045l045_h3_b060`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| raw3_s045l045_h3_b060 | true | 5.136612021857924 | 3.246153846153846 | 1.05 | 1.01 | 125.28 | 17.24 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv3_s045l045_h3_b060 | true | 5.081967213114754 | 3.230769230769231 | 0.93 | 1.06 | -194.7 | 104.69 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv3_s050l043_h3_b060 | true | 4.3497267759562845 | 3.2051282051282053 | 0.81 | 0.85 | -494.22 | -260.5 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv3_s048l040_h2_b060 | true | 8.109289617486338 | 5.410256410256411 | 0.87 | 1.0 | -431.85 | -2.0 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv3_s050l040_h2_b060 | true | 7.551912568306011 | 5.17948717948718 | 0.88 | 0.98 | -362.27 | -44.36 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| raw3_s045l045_h3_b060 | validation_is | 0.625673 | -0.366723 | 0.653191 | 1.781421 | False |
| raw3_s045l045_h3_b060 | oos | 0.617100 | -0.472765 | 0.595577 | 1.312821 | False |
| inv3_s045l045_h3_b060 | validation_is | 0.630935 | -0.709355 | 0.655914 | 1.748634 | False |
| inv3_s045l045_h3_b060 | oos | 0.651278 | -0.333825 | 0.566667 | 1.400000 | False |
| inv3_s050l043_h3_b060 | validation_is | 0.608903 | -1.120879 | 0.680905 | 1.387978 | False |
| inv3_s050l043_h3_b060 | oos | 0.634965 | -0.916800 | 0.652800 | 1.112821 | False |
| inv3_s048l040_h2_b060 | validation_is | 0.584728 | -0.791004 | 0.767520 | 1.885246 | False |
| inv3_s048l040_h2_b060 | oos | 0.604371 | -0.501896 | 0.759242 | 1.302564 | False |
| inv3_s050l040_h2_b060 | validation_is | 0.583537 | -0.762135 | 0.761939 | 1.797814 | False |
| inv3_s050l040_h2_b060 | oos | 0.621157 | -0.543921 | 0.765347 | 1.215385 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `validation_pf`: validation PF >= 1.10
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
