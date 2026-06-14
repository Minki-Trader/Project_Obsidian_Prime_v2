# Frontier30B Gate Audit(전선30B 게이트 감사)

- stage_open_lock_gate(단계 개방 잠금 게이트): `stages/stage_frontier_30__train_density_preserving_selector_before_loss_veto_or_exit_shape_pivot_onnx_scout/02_runs/frontier30A_stage_open_train_density_preserving_selector_or_exit_shape_pivot_hypothesis_design_v1/density_preserving_preselector_lock.json` read(읽음)
- source_surface_gate(원천 표면 게이트): `stages/stage_frontier_28__train_only_stability_gap_penalty_for_pf_dd_balance_onnx_scout/02_runs/frontier28B_train_only_stability_gap_penalty_proxy_scout_v1/stability_gap_candidate_summary.csv` rows(행) `234`
- veto_surface_gate(차단 표면 게이트): `stages/stage_frontier_29__train_only_loss_concentration_veto_for_pf_dd_balance_onnx_scout/02_runs/frontier29B_train_only_loss_concentration_veto_proxy_scout_v1/loss_veto_candidate_summary.csv` used as reference(참조로 사용)
- train_only_selection_gate(학습 전용 선택 게이트): preselector score(사전 선택기 점수)는 train inputs(학습 입력)만 사용
- leakage_guard(누수 방어): validation/OOS(검증/표본외)는 read-only diagnostics(읽기 전용 진단)
- tier_pair_gate(티어 쌍 게이트): Tier B(티어 B)는 missing_required(필수 누락), Tier A+B(티어 A+B)는 out_of_scope_by_claim(주장 범위 밖)
- runtime_probe_gate(런타임 탐침 게이트): `runtime_probe_out_of_scope_by_claim_scout_only_no_handoff`
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
