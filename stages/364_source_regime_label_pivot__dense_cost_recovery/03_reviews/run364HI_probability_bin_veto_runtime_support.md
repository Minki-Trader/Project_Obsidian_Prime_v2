# run364HI Probability-Bin Veto Runtime Support(확률 구간 차단 런타임 지원)

Created(생성): 2026-06-08T12:07:18Z

Action(행동): `ProbabilityBinVeto.mqh` reusable module(재사용 모듈)을 추가하고 `ObsidianPrimeV2_RuntimeProbeEA.mq5`에 input(입력값), configure(설정), apply(적용) 호출을 연결했습니다.

Effect(효과): HH의 `open_hour|pflat_bin|sl_gap_bin` probability-bin veto(확률 구간 차단)를 MT5 EA(메타트레이더5 전문가 자문)가 재현할 수 있게 됐습니다.

- judgment(판정): `runtime_support_implemented_compile_passed_no_package_no_authority`
- MetaEditor compile(메타에디터 컴파일): `completed`
- compile log(컴파일 로그): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime_v2/stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/mt5/mt5_compile.log`
- runtime package(런타임 패키지): `not_opened`
- new MT5 tester execution(새 MT5 테스터 실행): `not_run(실행 안 함)`
- next_run_id(다음 실행 ID): `run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/runtime_implementation_manifest.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/input_manifest.csv
- runtime_module_integration_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/runtime_implementation_manifest.csv
- probability_veto_contract_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/probability_bin_veto_parameter_contract.json
- module_hash_identity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/runtime_module_hashes.csv
- metaeditor_compile_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/mt5/mt5_compile.log
- runtime_parity_boundary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/runtime_parity_receipt.json
- next_action_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/hi_hj_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
