# run50AO_stage56_lgbm_fwd6_inverse_side_threshold_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AO_stage56_lgbm_fwd6_inverse_side_threshold_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `inv6_s050l043_h3_b060`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| inv6_s048l045_h3_b060 | true | 4.60655737704918 | 3.1487179487179486 | 1.05 | 1.12 | 107.95 | 195.67 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv6_s050l045_h3_b060 | true | 4.273224043715847 | 2.8974358974358974 | 1.08 | 1.11 | 164.1 | 158.45 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv6_s052l045_h3_b060 | true | 4.092896174863388 | 2.5794871794871796 | 1.02 | 1.08 | 36.18 | 103.93 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv6_s048l043_h3_b060 | true | 5.6502732240437155 | 3.887179487179487 | 1.02 | 1.11 | 58.04 | 199.36 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| inv6_s050l043_h3_b060 | true | 5.278688524590164 | 3.6769230769230767 | 1.14 | 1.1 | 318.69 | 179.25 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| inv6_s048l045_h3_b060 | validation_is | 0.607787 | -0.371945 | 0.660735 | 1.562842 | False |
| inv6_s048l045_h3_b060 | oos | 0.630801 | -0.181319 | 0.631922 | 1.158974 | False |
| inv6_s050l045_h3_b060 | validation_is | 0.615653 | -0.290153 | 0.659847 | 1.453552 | False |
| inv6_s050l045_h3_b060 | oos | 0.652341 | -0.219558 | 0.612389 | 1.123077 | False |
| inv6_s052l045_h3_b060 | validation_is | 0.598491 | -0.451696 | 0.642190 | 1.464481 | False |
| inv6_s052l045_h3_b060 | oos | 0.615459 | -0.293380 | 0.626243 | 0.964103 | False |
| inv6_s048l043_h3_b060 | validation_is | 0.626759 | -0.443868 | 0.692456 | 1.737705 | False |
| inv6_s048l043_h3_b060 | oos | 0.631872 | -0.236992 | 0.662269 | 1.312821 | False |
| inv6_s050l043_h3_b060 | validation_is | 0.619253 | -0.170093 | 0.690476 | 1.633880 | False |
| inv6_s050l043_h3_b060 | oos | 0.639853 | -0.250000 | 0.680614 | 1.174359 | False |

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
