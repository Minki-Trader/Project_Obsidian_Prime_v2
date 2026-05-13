# run50I_stage56_early_mid_session_direction_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50I_stage56_early_mid_session_direction_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `em_s390l300h06_aonly`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| em_s390l300h06_aonly | false | 4.502732 | 3.512821 | 1.01 | 1.22 | 21.61 | 471.91 | `quality_or_density_inconclusive_actual_routed_mt5` |
| em_s390l300h06_b045 | true | 4.644809 | 3.666667 | 1.0 | 1.19 | -0.82 | 409.19 | `quality_failed_actual_routed_mt5` |
| em_s400l290h06_aonly | false | 4.420765 | 3.425641 | 0.96 | 1.19 | -116.24 | 414.89 | `quality_failed_actual_routed_mt5` |
| em_s400l290h06_b045 | true | 4.562842 | 3.574359 | 0.96 | 1.18 | -108.89 | 393.25 | `quality_failed_actual_routed_mt5` |
| em_s410l285h06_aonly | false | 4.267760 | 3.312821 | 0.99 | 1.19 | -24.36 | 399.79 | `quality_failed_actual_routed_mt5` |
| em_s410l285h06_b045 | true | 4.404372 | 3.466667 | 1.0 | 1.17 | -5.64 | 360.54 | `quality_failed_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| em_s390l300h06_aonly | validation_is | 0.638745 | -0.473774 | 0.717233 | 1.273224 | False |
| em_s390l300h06_aonly | oos | 0.607596 | 0.188920 | 0.740146 | 0.912821 | False |
| em_s390l300h06_b045 | validation_is | 0.640823 | -0.500965 | 0.710588 | 1.344262 | False |
| em_s390l300h06_b045 | oos | 0.602693 | 0.072294 | 0.734266 | 0.974359 | False |
| em_s400l290h06_aonly | validation_is | 0.643264 | -0.643684 | 0.723115 | 1.224044 | False |
| em_s400l290h06_aonly | oos | 0.607634 | 0.121093 | 0.738024 | 0.897436 | False |
| em_s400l290h06_b045 | validation_is | 0.645256 | -0.630407 | 0.719760 | 1.278689 | False |
| em_s400l290h06_b045 | oos | 0.600698 | 0.064204 | 0.737446 | 0.938462 | False |
| em_s410l285h06_aonly | validation_is | 0.645439 | -0.531191 | 0.723431 | 1.180328 | False |
| em_s410l285h06_aonly | oos | 0.618516 | 0.118870 | 0.735294 | 0.876923 | False |
| em_s410l285h06_b045 | validation_is | 0.645928 | -0.506998 | 0.719603 | 1.234973 | False |
| em_s410l285h06_b045 | oos | 0.610363 | 0.033343 | 0.735207 | 0.917949 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `validation_pf`: validation PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
