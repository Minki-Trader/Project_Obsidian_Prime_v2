# run50R_stage56_nonflat_adx_band_block_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50R_stage56_nonflat_adx_band_block_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf_adxblk_c0_s380l270_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf_adxblk_c1_s390l280_a | false | 6.377049 | 4.425641 | 0.94 | 1.02 | -223.82 | 69.69 | `quality_failed_actual_routed_mt5` |
| nf_adxblk_c1_s390l280_b | true | 7.038251 | 4.753846 | 0.98 | 1.06 | -67.37 | 156.55 | `quality_failed_actual_routed_mt5` |
| nf_adxblk_c1_s380l270_a | false | 6.579235 | 4.517949 | 0.95 | 1.04 | -193.2 | 120.79 | `quality_failed_actual_routed_mt5` |
| nf_adxblk_c1_s380l270_b | true | 7.180328 | 4.851282 | 0.98 | 1.05 | -64.24 | 151.62 | `quality_failed_actual_routed_mt5` |
| nf_adxblk_c0_s390l280_b | true | 7.480874 | 5.071795 | 0.99 | 1.0 | -22.26 | 15.41 | `quality_failed_actual_routed_mt5` |
| nf_adxblk_c0_s380l270_b | true | 7.655738 | 5.164103 | 1.0 | 1.02 | 1.24 | 67.89 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nf_adxblk_c1_s390l280_a | validation_is | 0.595918 | -0.691791 | 0.724079 | 1.759563 | False |
| nf_adxblk_c1_s390l280_a | oos | 0.602114 | -0.419247 | 0.723059 | 1.225641 | False |
| nf_adxblk_c1_s390l280_b | validation_is | 0.617584 | -0.552306 | 0.732143 | 1.885246 | False |
| nf_adxblk_c1_s390l280_b | oos | 0.594971 | -0.331122 | 0.730313 | 1.282051 | False |
| nf_adxblk_c1_s380l270_a | validation_is | 0.598922 | -0.660465 | 0.730897 | 1.770492 | False |
| nf_adxblk_c1_s380l270_a | oos | 0.595075 | -0.362894 | 0.724177 | 1.246154 | False |
| nf_adxblk_c1_s380l270_b | validation_is | 0.610561 | -0.548889 | 0.735160 | 1.901639 | False |
| nf_adxblk_c1_s380l270_b | oos | 0.588314 | -0.339725 | 0.733615 | 1.292308 | False |
| nf_adxblk_c0_s390l280_b | validation_is | 0.614892 | -0.516260 | 0.758218 | 1.808743 | False |
| nf_adxblk_c0_s390l280_b | oos | 0.611841 | -0.484419 | 0.753286 | 1.251282 | False |
| nf_adxblk_c0_s380l270_b | validation_is | 0.609011 | -0.499115 | 0.759458 | 1.841530 | False |
| nf_adxblk_c0_s380l270_b | oos | 0.606297 | -0.432582 | 0.756703 | 1.256410 | False |

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
