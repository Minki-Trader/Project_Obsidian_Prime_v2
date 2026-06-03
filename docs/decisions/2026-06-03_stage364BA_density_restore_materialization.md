# run364BA density restore stress-to-candidate materialization(364BA 밀도 복원 압박-후보 물질화)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364BB_train_density_restore_stress_to_candidate_scout_without_db_v1`
- judgment(판정): `materialization_completed_stress_positive_clues_to_candidate_scout_inputs_no_authority`
- source_positive_clue(원천 긍정 단서): `ax03_short_restore_ps450_floor050_stress` PF `1.3019773488`, estimated density(추정 밀도) `3.012012012`
- BB queue rows(BB 대기열 행): `6`
- executable rows(실행 가능 행): `4`
- implementation_required_rows(구현 필요 행): `2`
- candidate estimated density range(후보 추정 밀도 범위): `3.012012012` - `3.1981981982`
- runtime_authority(런타임 권위): `not_claimed`

## BB Queue(BB 대기열)

| queue_rank | queue_id | queue_type | short_probability_threshold | entry_margin_floor | estimated_mt5_density_per_day | implementation_required | expected_effect |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ba01_ax03_stress_to_candidate_floor050_ps450 | candidate(후보) | 0.45 | 0.0005 | 3.012012012 | no | convert strongest PF/density stress pass into candidate review seed(가장 강한 PF/밀도 압박 통과를 후보 검토 씨앗으로 전환) |
| 2 | ba02_between_ax03_ax08_floor025_ps450 | candidate(후보) | 0.45 | 0.00025 | 3.1981981982 | no | search between ax03 density safety and ax08 over-stress buffer(ax03 밀도 안전과 ax08 과압박 완충 사이 탐색) |
| 3 | ba03_short_balance_ps448_floor050 | offensive_candidate(공격 후보) | 0.448 | 0.0005 | 3.0810810811 | no | test slightly lower short threshold while keeping floor050(하한 0.00050을 유지하며 숏 임계값을 더 낮춤) |
| 4 | ba04_candidate_floor075_density_rescue_ps450 | repair_candidate(수리 후보) | 0.45 | 0.00075 | 3.021021021 | no | borrow ax01 PF discipline but add short threshold density rescue(ax01 PF 규율에 숏 임계값 밀도 복원을 더함) |
| 5 | ba05_hour18_19_margin_guard_implementation_seed | implementation_diagnostic(구현 진단) | 0.45 | 0.00025 | 3.1981981982 | yes_runtime_policy_hour18_19_margin_guard(18/19시 마진 가드 런타임 정책 필요) | make skipped ax04 explicit implementation work before package(ax04 건너뜀을 패키지 전 구현 작업으로 명시) |
| 6 | ba06_tail_dd_guard_diagnostic_seed | implementation_diagnostic(구현 진단) | 0.45 | 0.00025 | 3.1981981982 | yes_account_state_guard_not_proxy_only(계정 상태 가드는 프록시만으로 불가) | carry ax06 tail risk as diagnostic not hidden runtime filter(ax06 꼬리 위험을 숨은 런타임 필터가 아니라 진단으로 유지) |

## Guardrails(가드레일)

| queue_id | trade_splitting_ok | top_n_ok | oos_threshold_ok | timestamp_ok | executable_without_new_policy | implementation_required |
| --- | --- | --- | --- | --- | --- | --- |
| ba01_ax03_stress_to_candidate_floor050_ps450 | True | True | True | True | True | no |
| ba02_between_ax03_ax08_floor025_ps450 | True | True | True | True | True | no |
| ba03_short_balance_ps448_floor050 | True | True | True | True | True | no |
| ba04_candidate_floor075_density_rescue_ps450 | True | True | True | True | True | no |
| ba05_hour18_19_margin_guard_implementation_seed | True | True | True | True | False | yes_runtime_policy_hour18_19_margin_guard(18/19시 마진 가드 런타임 정책 필요) |
| ba06_tail_dd_guard_diagnostic_seed | True | True | True | True | False | yes_account_state_guard_not_proxy_only(계정 상태 가드는 프록시만으로 불가) |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| work_packet_schema_lint(작업 묶음 스키마 점검) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/work_packet.json | primary family/skill/gates(주 작업군/스킬/게이트)를 기록한다. |
| input_manifest_gate(입력 목록 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/input_manifest.csv | AZ 입력 path/hash(경로/해시)를 고정한다. |
| experiment_design_audit(실험 설계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/experiment_design_receipt.json | 가설/비교/성공/실패 조건을 닫는다. |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/data_integrity_receipt.json | 시점/라벨/분할 경계를 기록한다. |
| guardrail_matrix_gate(가드레일 행렬 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/stress_to_candidate_guardrail_matrix.csv | 거래 쪼개기/top_n/표본외 임계값 금지를 검증한다. |
| next_queue_gate(다음 대기열 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/run364BB_scout_queue.csv | BB scout(BB 스카우트) 입력 대기열을 생성한다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/artifact_lineage_receipt.json | 입력과 출력 산출물을 연결한다. |
| claim_boundary_gate(주장 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/claim_boundary_receipt.json | 운영 주장을 만들지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Claim Boundary(주장 경계)

`research_development_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): BA는 stress pass(압박 통과)를 BB proxy scout(BB 프록시 스카우트) 입력으로 바꾸고, MT5 package(MT5 패키지)나 runtime authority(런타임 권위)는 주장하지 않는다.
