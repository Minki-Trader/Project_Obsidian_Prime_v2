# Run50E Density Reentry Tier B Disablement(50E 밀도 재진입 Tier B 비활성화)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50E_stage56_density_reentry_tier_b_disablement_v1`
- mt5_attempted(MT5 시도): `False`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `d390h10_aonly`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| d390h10_aonly | false | 3.775956 | 2.794872 | 1.19 | 1.09 | 488.03 | 204.48 | `density_failed_actual_routed_mt5` |
| d380h08_aonly | false | 4.612022 | 3.564103 | 1.0 | 0.96 | -6.17 | -103.69 | `quality_failed_actual_routed_mt5` |
| d370h08_aonly | false | 5.021858 | 3.800000 | 1.01 | 0.96 | 33.25 | -115.46 | `quality_failed_actual_routed_mt5` |
| d360h07_aonly | false | 5.622951 | 4.256410 | 1.03 | 0.99 | 97.71 | -35.61 | `quality_failed_actual_routed_mt5` |
| d350h06_aonly | false | 6.448087 | 4.841026 | 1.08 | 1.0 | 280.64 | 10.53 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d340h06_aonly | false | 6.633880 | 4.958974 | 1.08 | 1.02 | 288.77 | 44.91 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d335h06_aonly | false | 6.693989 | 4.979487 | 1.07 | 1.02 | 232.86 | 50.56 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d350h06_ab_b040 | true | 6.732240 | 5.148718 | 1.06 | 1.03 | 199.14 | 95.6 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d340h06_ab_b040 | true | 6.934426 | 5.282051 | 1.06 | 1.03 | 202.83 | 99.77 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| d390h10_aonly | validation_is | 0.643659 | 0.206266 | 0.597685 | 1.519126 | False |
| d390h10_aonly | oos | 0.636333 | -0.124807 | 0.585321 | 1.158974 | False |
| d380h08_aonly | validation_is | 0.627696 | -0.507310 | 0.649289 | 1.617486 | False |
| d380h08_aonly | oos | 0.600498 | -0.649194 | 0.651799 | 1.241026 | False |
| d370h08_aonly | validation_is | 0.618185 | -0.463819 | 0.652884 | 1.743169 | False |
| d370h08_aonly | oos | 0.598368 | -0.655816 | 0.669366 | 1.256410 | False |
| d360h07_aonly | validation_is | 0.629893 | -0.405044 | 0.683188 | 1.781421 | False |
| d360h07_aonly | oos | 0.606327 | -0.542904 | 0.708434 | 1.241026 | False |
| d350h06_aonly | validation_is | 0.628425 | -0.262169 | 0.716949 | 1.825137 | False |
| d350h06_aonly | oos | 0.603294 | -0.488845 | 0.743644 | 1.241026 | False |
| d340h06_aonly | validation_is | 0.625955 | -0.262133 | 0.716639 | 1.879781 | False |
| d340h06_aonly | oos | 0.605397 | -0.453557 | 0.747673 | 1.251282 | False |
| d335h06_aonly | validation_is | 0.624866 | -0.309910 | 0.717551 | 1.890710 | False |
| d335h06_aonly | oos | 0.610713 | -0.447930 | 0.748713 | 1.251282 | False |
| d350h06_ab_b040 | validation_is | 0.622321 | -0.338360 | 0.719156 | 1.890710 | False |
| d350h06_ab_b040 | oos | 0.607095 | -0.404781 | 0.747012 | 1.302564 | False |
| d340h06_ab_b040 | validation_is | 0.619176 | -0.340165 | 0.721040 | 1.934426 | False |
| d340h06_ab_b040 | oos | 0.607552 | -0.403136 | 0.752427 | 1.307692 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
- `tier_b_rule`: Tier B disabled but no matched enabled comparison in this batch
