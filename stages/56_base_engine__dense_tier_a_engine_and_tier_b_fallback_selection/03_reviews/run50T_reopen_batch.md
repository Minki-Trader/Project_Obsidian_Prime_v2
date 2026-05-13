# run50T_stage56_nonflat_vol_low_hold_compression_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50T_stage56_nonflat_vol_low_hold_compression_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf_vollow_h06_s350l240_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf_vollow_h08_s350l240_a | false | 6.158470 | 4.538462 | 1.01 | 1.05 | 38.23 | 142.43 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_h08_s350l240_b | true | 6.327869 | 4.712821 | 1.0 | 1.06 | -16.9 | 155.0 | `quality_failed_actual_routed_mt5` |
| nf_vollow_h08_s340l230_b | true | 6.327869 | 4.712821 | 1.0 | 1.06 | -16.9 | 155.0 | `quality_failed_actual_routed_mt5` |
| nf_vollow_h06_s350l240_a | false | 7.054645 | 5.241026 | 1.02 | 1.03 | 84.06 | 87.01 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_h06_s350l240_b | true | 7.311475 | 5.471795 | 1.03 | 1.05 | 116.61 | 146.5 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_h06_s340l230_b | true | 7.311475 | 5.471795 | 1.03 | 1.05 | 116.61 | 146.5 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nf_vollow_h08_s350l240_a | validation_is | 0.616986 | -0.466078 | 0.739130 | 1.606557 | False |
| nf_vollow_h08_s350l240_a | oos | 0.579034 | -0.339062 | 0.736723 | 1.194872 | False |
| nf_vollow_h08_s350l240_b | validation_is | 0.626931 | -0.514594 | 0.740069 | 1.644809 | False |
| nf_vollow_h08_s350l240_b | oos | 0.581375 | -0.331338 | 0.739935 | 1.225641 | False |
| nf_vollow_h08_s340l230_b | validation_is | 0.626931 | -0.514594 | 0.740069 | 1.644809 | False |
| nf_vollow_h08_s340l230_b | oos | 0.581375 | -0.331338 | 0.739935 | 1.225641 | False |
| nf_vollow_h06_s350l240_a | validation_is | 0.620467 | -0.434888 | 0.769171 | 1.628415 | False |
| nf_vollow_h06_s350l240_a | oos | 0.591056 | -0.414863 | 0.772016 | 1.194872 | False |
| nf_vollow_h06_s350l240_b | validation_is | 0.624435 | -0.412848 | 0.769806 | 1.683060 | False |
| nf_vollow_h06_s350l240_b | oos | 0.599617 | -0.362699 | 0.778819 | 1.210256 | False |
| nf_vollow_h06_s340l230_b | validation_is | 0.624435 | -0.412848 | 0.769806 | 1.683060 | False |
| nf_vollow_h06_s340l230_b | oos | 0.599617 | -0.362699 | 0.778819 | 1.210256 | False |

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
