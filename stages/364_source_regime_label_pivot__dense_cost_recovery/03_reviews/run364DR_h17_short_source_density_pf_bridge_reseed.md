# run364DR H17 Short-Source Density/PF Bridge Reseed(숏 원천 밀도/PF 브리지 재시드)

Created(생성): 2026-06-06T09:54:16Z

## Summary(요약)

Action(행동): DP selected model score(DP 선택 모델 점수)를 runtime telemetry(런타임 기록)의 p_short/session filter(숏 확률/세션 필터)와 결합해 density/PF bridge(밀도/PF 브리지)를 탐색했습니다.

Effect(효과): 낮은 밀도 OOS clue(표본외 단서)를 package(패키지)로 과장하지 않고, 검증/표본외 동시 통과 여부를 durable evidence(지속 근거)로 남겼습니다.

## Selected(선택)

- selected_variant_id(선택 변형 ID): `dr03378_h16_21_s0p516397_p0p0_mn0p2_not_august_h8`
- validation net/PF/density(검증 순수익/PF/밀도): `157.466` / `1.1648525481` / `1.2732240437`
- OOS net/PF/density(표본외 순수익/PF/밀도): `223.165` / `1.3264464563` / `1.4198473282`
- strict_candidate_count(엄격 후보 수): `0`
- density_both_count(양쪽 밀도 통과 수): `4411`
- density_and_net_count(양쪽 밀도+순수익 통과 수): `0`

## Judgment(판정)

`inconclusive_density_pf_bridge_reseed_no_cross_split_candidate_no_package_no_authority`

Claim boundary(주장 경계): `research_development_proxy_scout_only_density_pf_bridge_no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Runtime package(런타임 패키지), MT5 execution(MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1`에서 DR bridge(브리지)를 review(검토)하고 package(패키지) 차단 또는 다음 offensive seed(공격 씨앗)를 결정합니다.

## Gates(게이트)

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/dr_density_pf_bridge_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/data_integrity_audit.csv
- model_score_join_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/data_integrity_audit.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/dr_density_pf_bridge_surface.csv
- density_pf_contract_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/dr_bridge_component_audit.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/selected_dr_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/claim_boundary_receipt.json
