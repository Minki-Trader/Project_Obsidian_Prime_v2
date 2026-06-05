# Stage 345 Input Refs(345단계 입력 참조)

- run344N final decision(344N 최종 결정): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344N/final_decision.json`
- run344N attempt package(344N 시도 패키지): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344N/runtime_probe_attempt_package.csv`
- run344N source queue(344N 원천 대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344N/run344O_queue.csv`
- retargeted run345B queue(345B 재지정 대기열): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/02_runs/run345A/run345B_cash_open_long_quality_short_carry_mt5_probe_queue.csv`
- expected tape(예상 테이프): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344N/expected/expected_tape.csv`
- runtime parity contract(런타임 동등성 계약): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344N/runtime_parity_contract.csv`
- tester identity contract(테스터 정체성 계약): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344N/tester_identity_contract.csv`
- packageability matrix(포장 가능성 표): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344N/packageability_matrix.csv`
- source report(원천 보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344N_cash_open_long_quality_short_carry_decomposition_package.md`

Action(행동): Stage345(345단계)는 Stage344(344단계)의 package artifact(패키지 산출물)를 복사하지 않고 참조한다.
Effect(효과): heavy artifact duplication(무거운 산출물 중복)을 줄이고 artifact lineage(산출물 계보)는 유지한다.
