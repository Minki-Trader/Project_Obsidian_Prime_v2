# run50AM_stage56_lgbm_fwd6_density_branch_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AM_stage56_lgbm_fwd6_density_branch_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `lgbm6_s048l045_h6_b060`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| lgbm6_s048l045_h4_b060 | true | 2.2185792349726774 | 2.8205128205128207 | 0.69 | 0.77 | -496.02 | -448.65 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| lgbm6_s045l045_h4_b060 | true | 2.5737704918032787 | 3.348717948717949 | 0.7 | 0.81 | -496.35 | -412.52 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| lgbm6_s050l045_h4_b060 | true | 2.442622950819672 | 2.5743589743589745 | 0.73 | 0.83 | -495.84 | -288.19 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |
| lgbm6_s048l045_h6_b060 | true | 3.387978142076503 | 2.3794871794871795 | 0.83 | 0.79 | -411.56 | -394.85 | `inconclusive_stage56_lgbm_fwd6_density_branch_mt5_runtime_probe_completed` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| lgbm6_s048l045_h4_b060 | validation_is | 0.641810 | -1.721724 | 0.689655 | 0.688525 | False |
| lgbm6_s048l045_h4_b060 | oos | 0.618021 | -1.315727 | 0.589091 | 1.158974 | False |
| lgbm6_s045l045_h4_b060 | validation_is | 0.611140 | -1.553822 | 0.700637 | 0.770492 | False |
| lgbm6_s045l045_h4_b060 | oos | 0.606861 | -1.131730 | 0.617152 | 1.282051 | False |
| lgbm6_s050l045_h4_b060 | validation_is | 0.604442 | -1.609262 | 0.680089 | 0.781421 | False |
| lgbm6_s050l045_h4_b060 | oos | 0.589624 | -1.074084 | 0.571713 | 1.102564 | False |
| lgbm6_s048l045_h6_b060 | validation_is | 0.631646 | -1.163806 | 0.548387 | 1.530055 | False |
| lgbm6_s048l045_h6_b060 | oos | 0.637338 | -1.350970 | 0.495690 | 1.200000 | False |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## Best Variant Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `validation_net_positive`: validation net > 0
- `oos_net_positive`: OOS net > 0
- `validation_pf`: validation PF >= 1.10
- `oos_pf`: OOS PF >= 1.10
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
