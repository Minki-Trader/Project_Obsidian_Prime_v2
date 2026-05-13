# run50AN_stage56_lgbm_fwd6_inverse_signal_probe_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AN_stage56_lgbm_fwd6_inverse_signal_probe_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `inv6_s045l045_h3_b060`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| inv6_s040l040_h3_b060 | true | 9.327868852459016 | 6.887179487179488 | 0.89 | 0.94 | -465.22 | -185.52 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv6_s042l040_h3_b060 | true | 8.721311475409836 | 6.4051282051282055 | 0.98 | 0.97 | -75.85 | -89.44 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv6_s045l045_h3_b060 | true | 5.371584699453552 | 3.6256410256410256 | 1.11 | 1.05 | 265.28 | 84.42 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv6_s048l045_h4_b060 | true | 4.163934426229508 | 2.8153846153846156 | 1.11 | 1.17 | 223.57 | 258.0 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| inv6_s040l040_h3_b060 | validation_is | 0.624182 | -0.772537 | 0.760984 | 2.229508 | False |
| inv6_s040l040_h3_b060 | oos | 0.610422 | -0.638138 | 0.761727 | 1.641026 | False |
| inv6_s042l040_h3_b060 | validation_is | 0.612737 | -0.547525 | 0.739348 | 2.273224 | False |
| inv6_s042l040_h3_b060 | oos | 0.603185 | -0.571609 | 0.757406 | 1.553846 | False |
| inv6_s045l045_h3_b060 | validation_is | 0.622104 | -0.230132 | 0.654120 | 1.857923 | False |
| inv6_s045l045_h3_b060 | oos | 0.596407 | -0.380594 | 0.652051 | 1.261538 | False |
| inv6_s048l045_h4_b060 | validation_is | 0.596348 | -0.206601 | 0.608924 | 1.628415 | False |
| inv6_s048l045_h4_b060 | oos | 0.631508 | -0.030055 | 0.599271 | 1.128205 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
