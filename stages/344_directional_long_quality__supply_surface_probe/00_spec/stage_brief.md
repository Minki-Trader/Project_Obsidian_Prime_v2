# Stage 344 Brief(344단계 개요)

## Stage ID(단계 ID)

`344_directional_long_quality__supply_surface_probe`

## Question(질문)

Can a directional long quality surface(방향성 롱 품질 표면) recover long supply(롱 공급) and trade shape(거래 형태) while preserving the run343F profit anchor(343F 수익 앵커)?

## Scope(범위)

- source_stage(원천 단계): `343_quality_margin_runtime__early_long_mix_mt5_probe`
- source_review_run(원천 검토 실행): `run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- branch_run(분기 실행): `run344A_branch_stage343_to_directional_long_supply_quality_surface_without_db_v1`
- superseded_run(대체된 실행): `run343G_design_directional_long_supply_quality_surface_without_db_v1`
- next_run(다음 실행): `run344B_design_directional_long_supply_quality_surface_without_db_v1`

Action(행동): Stage343(343단계)의 next design(다음 설계)을 Stage344(344단계)로 retarget(재지정)한다.
Effect(효과): Stage343(343단계)은 trade shape rescue review(거래 형태 복구 검토)에서 멈추고, long quality source(롱 품질 원천) 탐색은 새 단계에서 좁게 다룬다.

## Source Truth(원천 진실)

- best_attempt(최고 시도): `d01_h04_anchor45`
- net_profit(순수익): `152.79`
- profit_factor(수익 팩터): `3.55`
- drawdown(낙폭): `89.31`
- recovery_factor(회복 계수): `1.71`
- trade_count(거래수): `22`
- long_short(롱/숏): `2/20`
- unresolved_failure(미해결 실패): trade shape rescue failed(거래 형태 복구 실패)

## Evidence Boundary(근거 경계)

This branch(분기)는 state sync(상태 동기화)와 handoff(인계)만 수행한다. No new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음)이다.

## run344C Directional Long Quality Surface Package(344C 방향성 롱 품질 표면 패키지)

- run_id(실행 ID): `run344C_materialize_directional_long_supply_quality_surface_package_without_db_v1`
- attempts(시도): `12`
- next(다음): `run344D_execute_directional_long_supply_quality_surface_mt5_probe_without_db_v1`
- effect(효과): 설계된 long quality surface(롱 품질 표면)를 MT5 runtime probe(MT5 런타임 탐침) 실행 대기열로 바꿨다.

## run344D Directional Long Quality Surface MT5 Probe(344D 방향성 롱 품질 표면 MT5 탐침)

- run_id(실행 ID): `run344D_execute_directional_long_supply_quality_surface_mt5_probe_without_db_v1`
- attempts(시도): `12`
- matched_rows(일치 행): `69924/69924`
- best_attempt(최고 시도): `s07_trend_confirmed_long_only`
- effect(효과): run344C package(344C 패키지)를 실제 MT5(메타트레이더5) 근거로 바꿨다.

## run344E Directional Long Quality Surface Review(344E 방향성 롱 품질 표면 검토)

- run_id(실행 ID): `run344E_review_directional_long_quality_surface_mt5_probe_without_db_v1`
- judgment(판정): `directional_long_quality_surface_positive_mt5_probe_s07_promotion_candidate_not_operating`
- promotion_candidate(승격 후보): `s07_trend_confirmed_long_only`
- effect(효과): Stage(단계) 무게를 줄이고 run344F validation(검증)으로 넘김.

## run344E Directional Long Quality Surface Review(344E 방향성 롱 품질 표면 검토)

- run_id(실행 ID): `run344E_review_directional_long_quality_surface_mt5_probe_without_db_v1`
- judgment(판정): `directional_long_quality_surface_positive_mt5_probe_s07_promotion_candidate_not_operating`
- promotion_candidate(승격 후보): `s07_trend_confirmed_long_only`
- effect(효과): Stage(단계) 무게를 줄이고 run344F validation(검증)으로 넘김.

## run344F s07 Forward/Cost/Stability Validation Design(344F s07 전진/비용/안정성 검증 설계)

- run_id(실행 ID): `run344F_design_s07_trend_confirmed_forward_cost_stability_validation_without_db_v1`
- judgment(판정): `s07_validation_design_ready_for_cost_session_regime_package_no_operating_claim`
- next_run(다음 실행): `run344G_materialize_s07_forward_cost_stability_validation_package_without_db_v1`
- effect(효과): s07 검증을 비용/세션/국면/인계 패키지로 좁힘.

## run344G s07 Validation Package(344G s07 검증 패키지)

- run_id(실행 ID): `run344G_materialize_s07_forward_cost_stability_validation_package_without_db_v1`
- attempts(시도): `3`
- expected_rows(예상 행): `17481`
- next_run(다음 실행): `run344H_execute_s07_forward_cost_stability_validation_mt5_probe_without_db_v1`
- effect(효과): run344H MT5 탐침 실행 패키지를 준비.

## run344G s07 Validation Package(344G s07 검증 패키지)

- run_id(실행 ID): `run344G_materialize_s07_forward_cost_stability_validation_package_without_db_v1`
- attempts(시도): `3`
- expected_rows(예상 행): `17481`
- next_run(다음 실행): `run344H_execute_s07_forward_cost_stability_validation_mt5_probe_without_db_v1`
- effect(효과): run344H MT5 탐침 실행 패키지를 준비.

## run344H s07 Validation MT5 Probe(344H s07 검증 MT5 탐침)

- run_id(실행 ID): `run344H_execute_s07_forward_cost_stability_validation_mt5_probe_without_db_v1`
- attempts(시도): `3`
- matched_rows(일치 행): `17481/17481`
- effect(효과): run344I review(검토)를 열었다.

## run344I s07 Validation Review(344I s07 검증 검토)

- run_id(실행 ID): `run344I_review_s07_forward_cost_stability_validation_mt5_probe_without_db_v1`
- moderate_cost_passed(중간 비용 통과): `True`
- heavy_cost_passed(강한 비용 통과): `False`
- effect(효과): run344J deal-level validation design(거래별 검증 설계)을 열었다.

## run344I s07 Validation Review(344I s07 검증 검토)

- run_id(실행 ID): `run344I_review_s07_forward_cost_stability_validation_mt5_probe_without_db_v1`
- moderate_cost_passed(중간 비용 통과): `True`
- heavy_cost_passed(강한 비용 통과): `False`
- effect(효과): run344J deal-level validation design(거래별 검증 설계)을 열었다.

## run344J Deal-Level Replay Design(344J 거래별 재생 설계)

- run_id(실행 ID): `run344J_design_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- parseable_reports(파싱 가능 보고서): `3/3`
- s07_entry_join_rate(s07 진입 조인율): `1.0`
- effect(효과): run344K materialization(물질화)을 열었다.

## run344K Deal-Level Materialization(344K 거래별 물질화)

- run_id(실행 ID): `run344K_materialize_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- trade_rows(거래 행): `71`
- s07_net(s07 순손익): `186.67`
- effect(효과): run344L review(검토)를 열었다.

## run344L s07 Deal-Level Review(344L s07 거래별 검토)

- run_id(실행 ID): `run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- s07_net(s07 순수익): `186.67`
- moderate_cost_passed(중간 비용 통과): `True`
- cash_open_net_share(현금장 초반 순수익 비중): `0.652542`
- effect(효과): run344M cash-open/short-carry decomposition(현금장 초반/숏 기여 분해)을 열었다.

## run344L s07 Deal-Level Review(344L s07 거래별 검토)

- run_id(실행 ID): `run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- s07_net(s07 순수익): `186.67`
- moderate_cost_passed(중간 비용 통과): `True`
- cash_open_net_share(현금장 초반 순수익 비중): `0.652542`
- effect(효과): run344M cash-open/short-carry decomposition(현금장 초반/숏 기여 분해)을 열었다.

## run344M Cash-Open Decomposition Design(344M 현금장 초반 분해 설계)

- run_id(실행 ID): `run344M_design_cash_open_long_quality_short_carry_decomposition_probe_without_db_v1`
- variant_rows(변형 행): `8`
- next_run(다음 실행): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- effect(효과): 현금장 초반 롱/숏 분해를 런타임 패키지 큐로 넘겼다.

## run344N Cash-Open Runtime Package(344N 현금장 런타임 패키지)

- run_id(실행 ID): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- attempts(시도): `6`
- expected_rows(예상 행): `34962`
- effect(효과): run344O MT5 탐침을 열었다.

## run345A Stage Branch Handoff(345A 단계 분기 인계)

- run_id(실행 ID): `run345A_branch_stage344_to_cash_open_long_quality_short_carry_runtime_probe_without_db_v1`
- next_stage(다음 단계): `345_cash_open_decomposition__long_quality_short_carry_runtime_probe`
- next_run(다음 실행): `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- effect(효과): Stage344(344단계)는 run344N package(패키지)에서 멈추고, cash-open MT5 runtime probe(현금장 MT5 런타임 탐침)는 Stage345(345단계)로 넘긴다.
