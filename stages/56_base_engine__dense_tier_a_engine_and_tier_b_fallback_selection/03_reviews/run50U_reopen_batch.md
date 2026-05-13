# run50U_stage56_nonflat_vol_low_hold6_short_filter_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50U_stage56_nonflat_vol_low_hold6_short_filter_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf_vollow_h06_s370l240_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf_vollow_h06_s370l240_a | false | 7.010929 | 5.225641 | 1.03 | 1.03 | 125.65 | 92.04 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_h06_s370l240_b | true | 7.278689 | 5.456410 | 1.04 | 1.05 | 155.07 | 151.12 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_h06_s390l230_a | false | 6.890710 | 5.128205 | 1.05 | 1.02 | 175.09 | 64.12 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_h06_s390l230_b | true | 7.147541 | 5.358974 | 1.06 | 1.04 | 199.48 | 105.84 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_h06_s410l220_b | true | 6.961749 | 5.256410 | 1.06 | 1.02 | 196.11 | 68.67 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_h06_s390l230_bcoremixed | true |  |  | None | None | None | None | `blocked_or_unverified_no_actual_mt5_closed_trade_basis` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nf_vollow_h06_s370l240_a | validation_is | 0.618058 | -0.402065 | 0.770850 | 1.606557 | False |
| nf_vollow_h06_s370l240_a | oos | 0.591123 | -0.409676 | 0.772326 | 1.189744 | False |
| nf_vollow_h06_s370l240_b | validation_is | 0.621925 | -0.383581 | 0.771021 | 1.666667 | False |
| nf_vollow_h06_s370l240_b | oos | 0.599682 | -0.357970 | 0.779135 | 1.205128 | False |
| nf_vollow_h06_s390l230_a | validation_is | 0.620425 | -0.361150 | 0.770024 | 1.584699 | False |
| nf_vollow_h06_s390l230_a | oos | 0.598873 | -0.435880 | 0.771000 | 1.174359 | False |
| nf_vollow_h06_s390l230_b | validation_is | 0.620387 | -0.347492 | 0.771407 | 1.633880 | False |
| nf_vollow_h06_s390l230_b | oos | 0.606799 | -0.398718 | 0.776077 | 1.200000 | False |
| nf_vollow_h06_s410l220_b | validation_is | 0.614134 | -0.346068 | 0.773155 | 1.579235 | False |
| nf_vollow_h06_s410l220_b | oos | 0.608156 | -0.433005 | 0.776585 | 1.174359 | False |
| nf_vollow_h06_s390l230_bcoremixed | validation_is |  |  |  |  |  |
| nf_vollow_h06_s390l230_bcoremixed | oos |  |  |  |  |  |

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
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
