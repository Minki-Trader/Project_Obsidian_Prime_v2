# run364ED H17 Dual PF Floor Bridge Reseed(양쪽 PF 바닥 연결 재시드)

Created(생성): 2026-06-06T13:16:28Z

## Summary(요약)

Action(행동): EC failure memory(EC 실패 기억)를 받아 validation/OOS min_pf(검증/표본외 최소 PF)를 직접 보상하는 label/filter/model sweep(라벨/필터/모델 탐색)을 실행했습니다.

Effect(효과): EB의 density_net(밀도+순수익) 단서를 PF 한쪽 회복이 아니라 dual PF floor(양쪽 PF 바닥) 회복 후보로 다시 판정할 수 있게 했습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `dual_pf_dir_h2_m1p5__short_stability57(숏_안정성_57)__et7_l55_n192(엑스트라트리7_잎55_192)`
- selected_filter(선택 필터): `none`
- selection_pool(선택 풀): `density_net`
- validation net/PF/density(검증 순수익/PF/밀도): `35.216` / `1.0219124076` / `3.9071038251`
- OOS net/PF/density(표본외 순수익/PF/밀도): `93.285` / `1.0982297894` / `3.3435114504`
- selected_min_profit_factor(선택 최소 수익 팩터): `1.0219124076`
- density_net_count(밀도+순수익 후보 수): `6`
- pf110_count(PF 1.10 양쪽 통과 수): `0`
- scout115_count(PF 1.15 스카우트 수): `0`
- strict_candidate_count(엄격 후보 수): `0`

## Judgment(판정)

`inconclusive_dual_pf_floor_bridge_reseed_no_pf_bridge_candidate_no_package_no_authority`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1`에서 ED 결과를 review(검토)합니다.

## Gates(게이트)

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/ed_dual_pf_floor_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/ed_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/ed_dual_pf_floor_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/run364EE_dual_pf_floor_bridge_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/selected_ed_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ED/claim_boundary_receipt.json
