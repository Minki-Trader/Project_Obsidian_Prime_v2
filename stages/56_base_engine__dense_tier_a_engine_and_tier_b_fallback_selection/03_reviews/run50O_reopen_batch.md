# run50O_stage56_hold6_side_adx_density_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50O_stage56_hold6_side_adx_density_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `d320h06_sadx_c0_b045`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| d340h06_sadx_c0_aonly | false | 6.224044 | 4.651282 | 1.07 | 1.0 | 237.11 | 2.49 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d340h06_sadx_c0_b045 | true | 6.349727 | 4.856410 | 1.05 | 1.02 | 148.49 | 52.99 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d320h06_sadx_c0_aonly | false | 6.278689 | 4.671795 | 1.06 | 1.0 | 193.69 | 8.94 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d320h06_sadx_c0_b045 | true | 6.398907 | 4.882051 | 1.04 | 1.02 | 143.47 | 60.5 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d315h06_sadx_c1_aonly | false | 5.715847 | 4.235897 | 1.0 | 1.01 | 15.56 | 23.44 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d315h06_sadx_c1_b045 | true | 5.901639 | 4.435897 | 1.0 | 1.02 | 10.51 | 56.84 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| d340h06_sadx_c0_aonly | validation_is | 0.636656 | -0.291826 | 0.706760 | 1.825137 | False |
| d340h06_sadx_c0_aonly | oos | 0.601788 | -0.497255 | 0.736494 | 1.225641 | False |
| d340h06_sadx_c0_b045 | validation_is | 0.632246 | -0.372212 | 0.709122 | 1.846995 | False |
| d340h06_sadx_c0_b045 | oos | 0.599888 | -0.444044 | 0.741288 | 1.256410 | False |
| d320h06_sadx_c0_aonly | validation_is | 0.638064 | -0.331427 | 0.711053 | 1.814208 | False |
| d320h06_sadx_c0_aonly | oos | 0.605846 | -0.490187 | 0.737651 | 1.225641 | False |
| d320h06_sadx_c0_b045 | validation_is | 0.633625 | -0.377481 | 0.711358 | 1.846995 | False |
| d320h06_sadx_c0_b045 | oos | 0.605966 | -0.436450 | 0.742647 | 1.256410 | False |
| d315h06_sadx_c1_aonly | validation_is | 0.637286 | -0.485124 | 0.682600 | 1.814208 | False |
| d315h06_sadx_c1_aonly | oos | 0.611159 | -0.471622 | 0.698547 | 1.276923 | False |
| d315h06_sadx_c1_b045 | validation_is | 0.630007 | -0.490269 | 0.684259 | 1.863388 | False |
| d315h06_sadx_c1_b045 | oos | 0.622555 | -0.434289 | 0.701734 | 1.323077 | False |

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
