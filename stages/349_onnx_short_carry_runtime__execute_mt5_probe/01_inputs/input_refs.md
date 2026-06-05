# Stage 349 Input Refs(349단계 입력 참조)

- run348C final decision(348C 최종 결정): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/final_decision.json`
- run348C attempt package(348C 시도 패키지): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/runtime_probe_attempt_package.csv`
- run348D source queue(348D 원천 대기열): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/run348D_queue.csv`
- retargeted run349B queue(349B 재지정 대기열): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349A/run349B_onnx_short_carry_mt5_probe_queue.csv`
- expected tape(예상 테이프): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/expected/expected_tape.csv`
- runtime parity contract(런타임 동등성 계약): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/runtime_parity_contract.csv`
- tester identity contract(테스터 정체성 계약): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/tester_identity_contract.csv`
- runtime mapping audit(런타임 매핑 감사): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/runtime_mapping_audit.csv`
- proxy MT5 comparison contract(프록시 MT5 비교 계약): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/proxy_mt5_comparison_contract.csv`
- source report(원천 보고서): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/03_reviews/run348C_onnx_deployable_short_carry_probe_package.md`

Action(행동): Stage349(349단계)는 Stage348(348단계)의 package artifact(패키지 산출물)를 복사하지 않고 참조한다.
Effect(효과): lineage(계보)는 유지하면서 stage payload(단계 적재량)를 줄인다.
