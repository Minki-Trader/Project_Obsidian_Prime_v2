# run50Q_stage56_nonflat_side_adx_cooldown_interp_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50Q_stage56_nonflat_side_adx_cooldown_interp_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf_h10c1_s390l280_b_sadx`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf_h10c1_s410l330_a_sadx | false | 6.306011 | 4.517949 | 0.98 | 0.97 | -66.12 | -78.09 | `quality_failed_actual_routed_mt5` |
| nf_h10c1_s410l330_b_sadx | true | 7.071038 | 4.912821 | 0.96 | 0.98 | -154.04 | -74.27 | `quality_failed_actual_routed_mt5` |
| nf_h10c1_s400l300_a_sadx | false | 6.502732 | 4.610256 | 0.99 | 1.0 | -47.86 | -8.62 | `quality_failed_actual_routed_mt5` |
| nf_h10c1_s400l300_b_sadx | true | 7.300546 | 5.005128 | 0.98 | 1.01 | -94.74 | 15.63 | `quality_failed_actual_routed_mt5` |
| nf_h10c1_s390l280_a_sadx | false | 6.743169 | 4.723077 | 0.99 | 1.0 | -50.68 | -4.22 | `quality_failed_actual_routed_mt5` |
| nf_h10c1_s390l280_b_sadx | true | 7.530055 | 5.102564 | 1.0 | 1.03 | -8.43 | 99.37 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nf_h10c1_s410l330_a_sadx | validation_is | 0.615564 | -0.557296 | 0.770364 | 1.448087 | False |
| nf_h10c1_s410l330_a_sadx | oos | 0.605629 | -0.588638 | 0.757094 | 1.097436 | False |
| nf_h10c1_s410l330_b_sadx | validation_is | 0.619469 | -0.619042 | 0.769706 | 1.628415 | False |
| nf_h10c1_s410l330_b_sadx | oos | 0.611296 | -0.577526 | 0.760960 | 1.174359 | False |
| nf_h10c1_s400l300_a_sadx | validation_is | 0.620203 | -0.540218 | 0.763025 | 1.540984 | False |
| nf_h10c1_s400l300_a_sadx | oos | 0.603579 | -0.509588 | 0.753059 | 1.138462 | False |
| nf_h10c1_s400l300_b_sadx | validation_is | 0.621058 | -0.570913 | 0.767216 | 1.699454 | False |
| nf_h10c1_s400l300_b_sadx | oos | 0.604977 | -0.483986 | 0.763320 | 1.184615 | False |
| nf_h10c1_s390l280_a_sadx | validation_is | 0.617883 | -0.541070 | 0.769044 | 1.557377 | False |
| nf_h10c1_s390l280_a_sadx | oos | 0.601185 | -0.504582 | 0.755700 | 1.153846 | False |
| nf_h10c1_s390l280_b_sadx | validation_is | 0.624613 | -0.506118 | 0.769231 | 1.737705 | False |
| nf_h10c1_s390l280_b_sadx | oos | 0.607672 | -0.400131 | 0.767839 | 1.184615 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_net_positive`: validation net > 0
- `validation_pf`: validation PF >= 1.10
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B enabled but fallback-only OOS is negative
