# run50AC_stage56_cooldown12_regime_firewall_v1(Stage56 재개 최적화 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50AC_stage56_cooldown12_regime_firewall_v1`
- mt5_attempted(MT5 시도): `True`
- selected_research_baseline(선택 연구 기준선): `none`
- judgment(판정): `in_progress_no_selected_research_baseline`
- best_variant(최선 변형): `none`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.
Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.

## Variant Results(변형 결과)

| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| nfac_c12_h08_s260l170_lvol_a | false |  |  | None | None | None | None | `blocked_or_unverified_no_actual_mt5_closed_trade_basis` |
| nfac_c12_h08_s260l170_lvol_b | true |  |  | None | None | None | None | `blocked_or_unverified_no_actual_mt5_closed_trade_basis` |
| nfac_c12_h08_s240l150_lvol_a | false |  |  | None | None | None | None | `blocked_or_unverified_no_actual_mt5_closed_trade_basis` |
| nfac_c12_h08_s240l150_lvol_b | true |  |  | None | None | None | None | `blocked_or_unverified_no_actual_mt5_closed_trade_basis` |
| nfac_c12_h08_s260l170_ladx2025_a | false |  |  | None | None | None | None | `blocked_or_unverified_no_actual_mt5_closed_trade_basis` |
| nfac_c12_h08_s260l170_ladx2025_b | true |  |  | None | None | None | None | `blocked_or_unverified_no_actual_mt5_closed_trade_basis` |
| nfac_c12_h08_s260l170_ldown_a | false |  |  | None | None | None | None | `blocked_or_unverified_no_actual_mt5_closed_trade_basis` |
| nfac_c12_h08_s260l170_ldown_b | true |  |  | None | None | None | None | `blocked_or_unverified_no_actual_mt5_closed_trade_basis` |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |
|---|---|---:|---:|---:|---:|---:|
| nfac_c12_h08_s260l170_lvol_a | validation_is |  |  |  |  |  |
| nfac_c12_h08_s260l170_lvol_a | oos |  |  |  |  |  |
| nfac_c12_h08_s260l170_lvol_b | validation_is |  |  |  |  |  |
| nfac_c12_h08_s260l170_lvol_b | oos |  |  |  |  |  |
| nfac_c12_h08_s240l150_lvol_a | validation_is |  |  |  |  |  |
| nfac_c12_h08_s240l150_lvol_a | oos |  |  |  |  |  |
| nfac_c12_h08_s240l150_lvol_b | validation_is |  |  |  |  |  |
| nfac_c12_h08_s240l150_lvol_b | oos |  |  |  |  |  |
| nfac_c12_h08_s260l170_ladx2025_a | validation_is |  |  |  |  |  |
| nfac_c12_h08_s260l170_ladx2025_a | oos |  |  |  |  |  |
| nfac_c12_h08_s260l170_ladx2025_b | validation_is |  |  |  |  |  |
| nfac_c12_h08_s260l170_ladx2025_b | oos |  |  |  |  |  |
| nfac_c12_h08_s260l170_ldown_a | validation_is |  |  |  |  |  |
| nfac_c12_h08_s260l170_ldown_a | oos |  |  |  |  |  |
| nfac_c12_h08_s260l170_ldown_b | validation_is |  |  |  |  |  |
| nfac_c12_h08_s260l170_ldown_b | oos |  |  |  |  |  |

## Read(판독)

- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`
