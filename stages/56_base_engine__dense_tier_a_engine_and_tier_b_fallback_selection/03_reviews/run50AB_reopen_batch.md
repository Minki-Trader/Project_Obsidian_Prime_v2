# run50AB_stage56_cooldown12_density_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AB_stage56_cooldown12_density_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nfab_c12_h08_s300l210_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfab_c12_h10_s300l210_a | false | 5.043716 | 3.215385 | 0.96 | 0.99 | -110.0 | -19.91 | `quality_failed_actual_routed_mt5` |
| nfab_c12_h10_s300l210_b | true | 5.103825 | 3.317949 | 0.92 | 1.05 | -197.76 | 87.86 | `quality_failed_actual_routed_mt5` |
| nfab_c12_h08_s300l210_a | false | 1.863388 | 3.374359 | 0.59 | 1.03 | -496.16 | 50.74 | `quality_failed_actual_routed_mt5` |
| nfab_c12_h08_s300l210_b | true | 5.054645 | 3.430769 | 1.03 | 1.08 | 71.06 | 139.42 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nfab_c12_h06_s300l210_a | false | 4.699454 | 3.225641 | 1.07 | 0.99 | 136.22 | -12.03 | `quality_failed_actual_routed_mt5` |
| nfab_c12_h06_s300l210_b | true | 4.803279 | 3.282051 | 1.04 | 0.93 | 85.14 | -111.75 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfab_c12_h10_s300l210_a | validation_is | 0.575080 | -0.619177 | 0.414951 | 2.950820 | False |
| nfab_c12_h10_s300l210_a | oos | 0.597488 | -0.531754 | 0.352472 | 2.082051 | False |
| nfab_c12_h10_s300l210_b | validation_is | 0.572683 | -0.711734 | 0.413276 | 2.994536 | False |
| nfab_c12_h10_s300l210_b | oos | 0.595936 | -0.364204 | 0.355487 | 2.138462 | False |
| nfab_c12_h08_s300l210_a | validation_is | 0.596969 | -1.955015 | 0.395894 | 1.125683 | False |
| nfab_c12_h08_s300l210_a | oos | 0.585196 | -0.422888 | 0.332827 | 2.251282 | False |
| nfab_c12_h08_s300l210_b | validation_is | 0.583870 | -0.423178 | 0.364324 | 3.213115 | False |
| nfab_c12_h08_s300l210_b | oos | 0.581873 | -0.291599 | 0.325859 | 2.312821 | False |
| nfab_c12_h06_s300l210_a | validation_is | 0.587527 | -0.341605 | 0.263953 | 3.459016 | False |
| nfab_c12_h06_s300l210_a | oos | 0.574203 | -0.519126 | 0.235294 | 2.466667 | False |
| nfab_c12_h06_s300l210_b | validation_is | 0.590645 | -0.403140 | 0.271900 | 3.497268 | False |
| nfab_c12_h06_s300l210_b | oos | 0.576848 | -0.674609 | 0.232813 | 2.517949 | False |

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
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
