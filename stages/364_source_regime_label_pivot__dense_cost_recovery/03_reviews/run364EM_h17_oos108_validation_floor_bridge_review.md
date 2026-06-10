# run364EM H17 OOS108 Validation Floor Bridge Review(표본외108 검증 바닥 연결 검토)

Created(생성): 2026-06-06T15:11:22Z

Action(행동): EL OOS108 validation floor bridge(EL 표본외108 검증 바닥 연결) 후보를 package eligibility(패키지 가능성), cost stress(비용 압박), month stability(月 안정성), side balance(방향 균형) 관점에서 검토했습니다.

Effect(효과): 강한 proxy(프록시) 후보를 runtime authority(런타임 권위)로 올리지 않고, EN runtime package(EN 런타임 패키지) 입력으로만 넘깁니다.

Findings(발견):

- selected model(선택 모델): `oos108_valfloor_dir_h2_m1__source_all82__rf8_l70_n160`
- validation net/PF/density(검증 순수익/PF/밀도): `202.78` / `1.1329169764` / `3.9344262295`
- OOS net/PF/density(표본외 순수익/PF/밀도): `201.155` / `1.1960498616` / `3.9618320611`
- bridge_count(연결 후보 수): `322`
- pf108_count(PF108 후보 수): `84`
- ONNX smoke pass(ONNX 스모크 통과): `24`
- long/short count(롱/숏 거래수): `128` / `391`
- month negatives(월 음수): validation(검증) `4`, OOS(표본외) `2`
- cost stress warning(비용 압박 주의): `True`

Package decision(패키지 결정): `eligible_for_runtime_probe_package(런타임 탐침 패키지 가능)`

Judgment(판정): `positive_proxy_oos108_validation_floor_bridge_package_eligible_review_cost_stress_caution_no_authority`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1`

Gates(게이트):

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/input_manifest.csv
- review_summary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/em_oos108_validation_floor_bridge_review_summary.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/package_decision.csv
- cost_stress_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/cost_stress_review.csv
- month_stability_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/month_stability_review.csv
- side_balance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/side_balance_review.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/run364EN_runtime_package_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/claim_boundary_receipt.json
