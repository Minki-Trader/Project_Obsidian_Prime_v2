# run50V_stage56_nonflat_vol_low_hold6_tierb_gate_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50V_stage56_nonflat_vol_low_hold6_tierb_gate_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nfv_h6_s37l24_bcm`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfv_h6_s37l24_bcm | true | 7.054645 | 5.297436 | 1.04 | 1.04 | 153.96 | 107.69 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nfv_h6_s39l23_bcm | true | 6.934426 | 5.200000 | 1.06 | 1.03 | 203.4 | 79.77 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nfv_h6_s39l23_bmx | true | 6.934426 | 5.200000 | 1.06 | 1.03 | 199.26 | 79.77 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nfv_h6_s39l23_bma | true | 7.103825 | 5.287179 | 1.05 | 1.03 | 171.17 | 96.88 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfv_h6_s37l24_bcm | validation_is | 0.618878 | -0.380744 | 0.769171 | 1.628415 | False |
| nfv_h6_s37l24_bcm | oos | 0.589626 | -0.395750 | 0.769603 | 1.220513 | False |
| nfv_h6_s39l23_bcm | validation_is | 0.621242 | -0.339716 | 0.768322 | 1.606557 | False |
| nfv_h6_s39l23_bcm | oos | 0.597230 | -0.421331 | 0.768245 | 1.205128 | False |
| nfv_h6_s39l23_bmx | validation_is | 0.621242 | -0.342979 | 0.768322 | 1.606557 | False |
| nfv_h6_s39l23_bmx | oos | 0.597230 | -0.421331 | 0.768245 | 1.205128 | False |
| nfv_h6_s39l23_bma | validation_is | 0.619587 | -0.368331 | 0.773077 | 1.612022 | False |
| nfv_h6_s39l23_bma | oos | 0.607952 | -0.406033 | 0.778855 | 1.169231 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_pf`: validation PF >= 1.10
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
