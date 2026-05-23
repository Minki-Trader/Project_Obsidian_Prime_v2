# run271D Fresh Edge Scoring Probe(271D 새 거래 우위 점수 탐침)

- run_id(실행 ID): `run271D_execute_fresh_edge_scoring_probe_v1`
- status(상태): `completed_fresh_edge_scoring_probe_no_candidate_selection`
- judgment(판정): `exploratory_score_table_materialized_no_candidate_selection`
- scoreboard(점수판): `structural_scout(구조 스카우트)`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run271E_screen_fresh_edge_score_surfaces`

## Meaning(의미)

run271D(271D 실행)는 run271C(271C 실행)의 scoring input specs(점수 입력 규격)를 Tier A/Tier B/Tier A+B(티어 A/티어 B/티어 A+B) score table(점수표)로 물질화했다.
효과(effect, 효과): fresh edge package(새 거래 우위 패키지)를 아직 선택하지 않고, run271E(271E 실행)에서 선별할 구조 점수 근거를 만든다.

## Packages(패키지)

- `cp271A_damage_first_loss_asymmetry_surface`
- `cp271B_time_risk_phase_router_surface`
- `cp271C_recovery_tail_payoff_rebalance_surface`
- `cp271D_stage270_reference_control_boundary`

## Tier Records(티어 기록)

- `Tier A separate`: rows(행) `46650`, status(상태) `materialized_full_context_score_inputs`
- `Tier B separate`: rows(행) `46650`, status(상태) `materialized_partial_context_score_inputs`
- `Tier A+B combined`: rows(행) `93300`, status(상태) `materialized_combined_score_input_view_no_routed_pnl`

## Signal Read Preview(신호 판독 미리보기)

- `cp271A_damage_first_loss_asymmetry_surface` / `Tier A separate` / `oos`: decisions(판단) `2514`, alignment(정렬률) `0.49379109`
- `cp271A_damage_first_loss_asymmetry_surface` / `Tier A separate` / `validation`: decisions(판단) `2919`, alignment(정렬률) `0.48922156`
- `cp271B_time_risk_phase_router_surface` / `Tier A separate` / `oos`: decisions(판단) `3590`, alignment(정렬률) `0.49480642`
- `cp271B_time_risk_phase_router_surface` / `Tier A separate` / `validation`: decisions(판단) `4201`, alignment(정렬률) `0.51776266`
- `cp271C_recovery_tail_payoff_rebalance_surface` / `Tier A separate` / `oos`: decisions(판단) `4517`, alignment(정렬률) `0.49727005`
- `cp271C_recovery_tail_payoff_rebalance_surface` / `Tier A separate` / `validation`: decisions(판단) `5482`, alignment(정렬률) `0.49410609`
- `cp271D_stage270_reference_control_boundary` / `Tier A separate` / `oos`: decisions(판단) `0`, alignment(정렬률) ``
- `cp271D_stage270_reference_control_boundary` / `Tier A separate` / `validation`: decisions(판단) `0`, alignment(정렬률) ``

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): score table(점수표), handoff JSON(인계 JSON), tier receipt(티어 영수증), signal read summary(신호 판독 요약)를 생성했다.
- kpi_contract_audit(KPI 계약 감사): scoreboard(점수판)는 `structural_scout(구조 스카우트)`이고 trading KPI(거래 핵심 성과 지표)는 주장하지 않는다.
- skill_receipt_lint(스킬 영수증 점검): data integrity(데이터 무결성), model validation(모델 검증), artifact lineage(산출물 계보), result judgment(결과 판정) receipt(영수증)를 남겼다.
- required_gate_coverage_audit(필수 게이트 커버리지 감사): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)을 모두 기록했다.
- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
