# run50AG_stage56_s25_quality_oos_density_repair_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AG_stage56_s25_quality_oos_density_repair_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `s24l15a`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s24l15a | false | 5.349727 | 3.646154 | 1.19 | 1.23 | 466.64 | 417.57 | `weak_dense_engine_candidate_actual_routed_mt5` |
| s24l15b | true | 5.404372 | 3.723077 | 1.15 | 1.25 | 381.01 | 453.49 | `weak_dense_engine_candidate_actual_routed_mt5` |
| s22l14a | false | 5.349727 | 3.646154 | 1.19 | 1.23 | 466.64 | 417.57 | `weak_dense_engine_candidate_actual_routed_mt5` |
| s22l14b | true | 5.404372 | 3.723077 | 1.15 | 1.25 | 381.01 | 453.49 | `weak_dense_engine_candidate_actual_routed_mt5` |
| s20l13a | false | 5.349727 | 3.646154 | 1.19 | 1.23 | 466.64 | 417.57 | `weak_dense_engine_candidate_actual_routed_mt5` |
| s20l13b | true | 5.404372 | 3.723077 | 1.15 | 1.25 | 381.01 | 453.49 | `weak_dense_engine_candidate_actual_routed_mt5` |
| s24l15c6a | false | 5.819672 | 3.974359 | 1.02 | 1.14 | 48.1 | 291.49 | `quality_or_density_inconclusive_actual_routed_mt5` |
| s24l15c6b | true | 5.852459 | 4.041026 | 0.99 | 1.16 | -17.35 | 322.45 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| s24l15a | validation_is | 0.602130 | -0.023350 | 0.598570 | 2.147541 | False |
| s24l15a | oos | 0.588858 | 0.087300 | 0.594937 | 1.476923 | False |
| s24l15b | validation_is | 0.602409 | -0.114752 | 0.599596 | 2.163934 | False |
| s24l15b | oos | 0.580031 | 0.124642 | 0.600551 | 1.487179 | False |
| s22l14a | validation_is | 0.602130 | -0.023350 | 0.598570 | 2.147541 | False |
| s22l14a | oos | 0.588858 | 0.087300 | 0.594937 | 1.476923 | False |
| s22l14b | validation_is | 0.602409 | -0.114752 | 0.599596 | 2.163934 | False |
| s22l14b | oos | 0.580031 | 0.124642 | 0.600551 | 1.487179 | False |
| s20l13a | validation_is | 0.602130 | -0.023350 | 0.598570 | 2.147541 | False |
| s20l13a | oos | 0.588858 | 0.087300 | 0.594937 | 1.476923 | False |
| s20l13b | validation_is | 0.602409 | -0.114752 | 0.599596 | 2.163934 | False |
| s20l13b | oos | 0.580031 | 0.124642 | 0.600551 | 1.487179 | False |
| s24l15c6a | validation_is | 0.615433 | -0.454836 | 0.655399 | 2.005464 | False |
| s24l15c6a | oos | 0.584069 | -0.123884 | 0.658065 | 1.358974 | False |
| s24l15c6b | validation_is | 0.612472 | -0.516200 | 0.651727 | 2.038251 | False |
| s24l15c6b | oos | 0.586147 | -0.090799 | 0.656091 | 1.389744 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
