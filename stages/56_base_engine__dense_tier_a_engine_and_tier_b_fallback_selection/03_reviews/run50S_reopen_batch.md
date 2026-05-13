# run50S_stage56_nonflat_vol_low_block_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50S_stage56_nonflat_vol_low_block_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `nf_vollow_c0_s350l240_b`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf_vollow_c0_s360l250_a | false | 5.535519 | 4.041026 | 1.01 | 1.02 | 45.92 | 51.22 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_c0_s360l250_b | true | 5.715847 | 4.200000 | 1.01 | 1.07 | 16.76 | 187.83 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_c0_s350l240_a | false | 5.557377 | 4.041026 | 1.01 | 1.02 | 47.06 | 51.22 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_c0_s350l240_b | true | 5.748634 | 4.200000 | 1.01 | 1.07 | 24.39 | 187.83 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_c0_s340l230_b | true | 5.748634 | 4.200000 | 1.01 | 1.07 | 24.39 | 187.83 | `quality_or_density_inconclusive_actual_routed_mt5` |
| nf_vollow_c0_s330l220_b | true | 5.754098 | 4.200000 | 1.01 | 1.07 | 21.79 | 187.83 | `quality_or_density_inconclusive_actual_routed_mt5` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nf_vollow_c0_s360l250_a | validation_is | 0.615330 | -0.454669 | 0.708786 | 1.612022 | False |
| nf_vollow_c0_s360l250_a | oos | 0.606705 | -0.435000 | 0.714467 | 1.153846 | False |
| nf_vollow_c0_s360l250_b | validation_is | 0.614889 | -0.483977 | 0.711281 | 1.650273 | False |
| nf_vollow_c0_s360l250_b | oos | 0.619438 | -0.270659 | 0.715507 | 1.194872 | False |
| nf_vollow_c0_s350l240_a | validation_is | 0.615577 | -0.453727 | 0.707965 | 1.622951 | False |
| nf_vollow_c0_s350l240_a | oos | 0.606705 | -0.435000 | 0.714467 | 1.153846 | False |
| nf_vollow_c0_s350l240_b | validation_is | 0.614030 | -0.476816 | 0.711027 | 1.661202 | False |
| nf_vollow_c0_s350l240_b | oos | 0.619438 | -0.270659 | 0.715507 | 1.194872 | False |
| nf_vollow_c0_s340l230_b | validation_is | 0.614030 | -0.476816 | 0.711027 | 1.661202 | False |
| nf_vollow_c0_s340l230_b | oos | 0.619438 | -0.270659 | 0.715507 | 1.194872 | False |
| nf_vollow_c0_s330l220_b | validation_is | 0.614030 | -0.479307 | 0.711301 | 1.661202 | False |
| nf_vollow_c0_s330l220_b | oos | 0.619438 | -0.270659 | 0.715507 | 1.194872 | False |

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
