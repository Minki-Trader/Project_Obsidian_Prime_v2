# run271C Fresh Edge Scoring/Handoff Inputs(271C 새 거래 우위 점수/인계 입력)

- run_id(실행 ID): `run271C_materialize_fresh_edge_scoring_handoff_inputs_v1`
- status(상태): `completed_fresh_edge_scoring_handoff_input_materialization_no_candidate_selection`
- judgment(판정): `exploratory_scoring_handoff_inputs_materialized_no_candidate_selection`
- dataset_rows(데이터셋 행): `46650`
- feature_count(피처 수): `58`
- feature_order_hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- package_rows(패키지 행): `4`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run271D_execute_fresh_edge_scoring_probe`

## Meaning(의미)

run271C(271C 실행)는 run271B(271B 실행)의 blueprint(청사진)를 scoring input spec(점수 입력 규격)과 handoff skeleton(인계 골격)으로 바꿨다.
효과(effect, 효과): 다음 run271D(271D 실행)는 feature order(피처 순서), score columns(점수 열), decision/risk hash(판단/위험 해시)를 잃지 않고 실제 score table(점수표)을 만들 수 있다.

## Packages(패키지)

- `cp271A_damage_first_loss_asymmetry_surface`: score columns(점수 열) `8`, handoff skeleton(인계 골격) `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/02_runs/run271C/handoff/cp271A_damage_first_loss_asymmetry_surface.json`
- `cp271B_time_risk_phase_router_surface`: score columns(점수 열) `8`, handoff skeleton(인계 골격) `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/02_runs/run271C/handoff/cp271B_time_risk_phase_router_surface.json`
- `cp271C_recovery_tail_payoff_rebalance_surface`: score columns(점수 열) `8`, handoff skeleton(인계 골격) `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/02_runs/run271C/handoff/cp271C_recovery_tail_payoff_rebalance_surface.json`
- `cp271D_stage270_reference_control_boundary`: score columns(점수 열) `6`, handoff skeleton(인계 골격) `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/02_runs/run271C/handoff/cp271D_stage270_reference_control_boundary.json`

## Gate Coverage(게이트 커버리지)

- feature_order_parity(피처 순서 동등성): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- data_integrity_boundary(데이터 무결성 경계): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/02_runs/run271C/data_integrity_receipt.json`
- model_validation_boundary(모델 검증 경계): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/02_runs/run271C/model_validation_receipt.json`
- artifact_lineage_audit(산출물 계보 감사): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/02_runs/run271C/artifact_lineage_receipt.json`
- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
