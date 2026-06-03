# run364BC density restore stress candidate review(364BC 밀도 복원 압박 후보 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364BB_train_density_restore_stress_to_candidate_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1`
- judgment(판정): `package_review_candidate_exists_open_runtime_probe_package_no_authority`
- package_decision(패키지 결정): `open_runtime_probe_package_queue_no_authority`
- review_package_candidate_rows(검토 패키지 후보 행): `3`
- selected(선택): `ba02_between_ax03_ax08_floor025_ps450` / `run364BB_ba02_between_ax03_ax08_floor025_ps450`
- selected net/PF/density/DD/trades(선택 순수익/수익 팩터/밀도/낙폭/거래수): `919.75` / `1.3178004168` / `3.045045045` / `-127.733` / `1112`
- runtime_authority(런타임 권위): `not_claimed`

## Surface Review(표면 검토)

| queue_rank | queue_id | review_status | combined_profit_factor | estimated_mt5_trade_per_business_day | combined_net_profit | combined_max_drawdown | combined_short_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | ba02_between_ax03_ax08_floor025_ps450 | package_review_candidate(패키지 검토 후보) | 1.3178004168 | 3.045045045 | 919.75 | -127.733 | 103 |
| 1 | ba01_ax03_stress_to_candidate_floor050_ps450 | package_review_candidate(패키지 검토 후보) | 1.3019773488 | 3.012012012 | 874.129 | -132.758 | 103 |
| 3 | ba03_short_balance_ps448_floor050 | package_review_candidate(패키지 검토 후보) | 1.2947886727 | 3.033033033 | 857.741 | -144.033 | 111 |
| 4 | ba04_candidate_floor075_density_rescue_ps450 | fail_density_survival(밀도 생존 실패) | 1.3051213139 | 2.981981982 | 869.182 | -129.758 | 103 |

## Package Candidates(패키지 후보)

| candidate_rank | package_role | queue_id | combined_profit_factor | estimated_mt5_trade_per_business_day | combined_net_profit | combined_max_drawdown | runtime_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | selected_primary(선택 주 후보) | ba02_between_ax03_ax08_floor025_ps450 | 1.3178004168 | 3.045045045 | 919.75 | -127.733 | open_bd_package(364BD 패키지 열기) |
| 2 | retained_alternative(보존 대안) | ba01_ax03_stress_to_candidate_floor050_ps450 | 1.3019773488 | 3.012012012 | 874.129 | -132.758 | record_as_alternative(대안으로 기록) |
| 3 | retained_alternative(보존 대안) | ba03_short_balance_ps448_floor050 | 1.2947886727 | 3.033033033 | 857.741 | -144.033 | record_as_alternative(대안으로 기록) |

## Failure Memory(실패 기억)

| failure_id | failure_type | evidence | constraint_for_next |
| --- | --- | --- | --- |
| fail_density_survival__ba04_candidate_floor075_density_rescue_ps450 | fail_density_survival(밀도 생존 실패) | pf=1.3051213139;density=2.981981982;dd=-129.758 | do not package this row without repair(수리 없이 이 행을 패키지하지 않음) |
| implementation_required_rows_visible | proxy_cannot_execute_new_runtime_guards(프록시가 새 런타임 가드를 실행하지 못함) | skipped_implementation_required_rows=2 | runtime/proxy policy implementation must be explicit before package(패키지 전 런타임/프록시 정책 구현 명시 필요) |

## Next Queue(다음 대기열)

| package_queue_id | package_role | source_queue_id | short_probability_threshold | entry_margin_floor | expected_profit_factor | expected_estimated_mt5_density | runtime_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bd_package_ba02_between_ax03_ax08_floor025_ps450 | selected_primary(선택 주 후보) | ba02_between_ax03_ax08_floor025_ps450 | 0.45 | 0.00025 | 1.3178004168 | 3.045045045 | runtime_probe_package_input_only_no_authority(런타임 탐침 패키지 입력만, 권위 없음) |
| bd_package_ba01_ax03_stress_to_candidate_floor050_ps450 | retained_alternative(보존 대안) | ba01_ax03_stress_to_candidate_floor050_ps450 | 0.45 | 0.0005 | 1.3019773488 | 3.012012012 | runtime_probe_package_input_only_no_authority(런타임 탐침 패키지 입력만, 권위 없음) |
| bd_package_ba03_short_balance_ps448_floor050 | retained_alternative(보존 대안) | ba03_short_balance_ps448_floor050 | 0.448 | 0.0005 | 1.2947886727 | 3.033033033 | runtime_probe_package_input_only_no_authority(런타임 탐침 패키지 입력만, 권위 없음) |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BC/bb_surface_review.csv | BB 표면의 net/PF/density/DD/trade count(순수익/수익 팩터/밀도/낙폭/거래수)를 검토했다. |
| row_grain_audit(행 단위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BC/bb_surface_review.csv | 후보 variant(변형) 한 행 단위로 판정했다. |
| source_authority_audit(원천 권위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/final_decision.json | BB final decision(BB 최종 결정)을 부모 원천으로 고정했다. |
| package_decision_gate(패키지 결정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BC/package_decision.csv | 패키지 가능 행 3개를 확인하고 BD 패키지 대기열을 열었다. |
| selected_primary_gate(선택 주 후보 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/selected_proxy_candidate.json | BB selection_score(BB 선택 점수)가 고른 주 후보를 그대로 인계했다. |
| next_queue_gate(다음 대기열 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BC/run364BD_runtime_probe_package_queue.csv | BD runtime probe package queue(BD 런타임 탐침 패키지 대기열)를 만들었다. |
| external_claim_boundary_gate(외부 주장 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BC/claim_boundary_receipt.json | MT5 실행 전이라 runtime authority(런타임 권위)를 주장하지 않았다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BC/required_gate_coverage_audit.csv | work packet(작업 묶음)의 필수 게이트를 closeout(종료 기록)에 연결했다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BC/claim_boundary_receipt.json | operating promotion(운영 승격), live readiness(실거래 준비), goal achieve(목표 달성)를 주장하지 않았다. |

## Claim Boundary(주장 경계)

`research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): BB proxy(프록시)에서 패키지 가능 후보를 확인했으므로 BD runtime probe package(BD 런타임 탐침 패키지)를 열지만, MT5 실행 근거가 아직 없어 운영 승격은 주장하지 않는다.
