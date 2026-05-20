# Stage267 Run267S Pool-wide Orthogonal Stability Racing Matrix(267단계 267S 후보군 전체 직교 안정성 경주 행렬)

- status(상태): `run267S_pool_wide_orthogonal_stability_racing_matrix_materialized`
- run_id(실행 ID): `run267S_stage267_pool_wide_orthogonal_stability_racing_matrix_v1`
- parent_run(부모 실행): `run267R_stage267_internal_adapter_stability_followup_or_prune_v1`
- candidate_count(후보 수): `5`
- axis_count(축 수): `3`
- matrix_rows(행렬 행): `15`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267R(267R 실행)은 내부 Adapter(어댑터) 분기를 선택하지 않고 회수 단서로 낮췄다.
Effect(효과): 변형 차이가 같은 KPI shape(핵심 성과 지표 모양)으로 접히고 Monday/session(월요일/세션) 약점이 반복된 분기를 계속 미세 수리하지 않는다.

run267S(267S 실행)는 그 결과를 다섯 Baseline candidates(기준 후보) 전체에 다시 펼쳤다.
Effect(효과): 한 후보나 한 feature(피처)에 붙지 않고, 누가 더 넓은 조건에서 덜 깨지는지 보는 다음 물질화 큐를 만든다.

## Stage58 Question(58단계 질문)

질문은 Stage58(58단계)부터 본격적인 Baseline 후보(기준 후보)를 정하면서 이전 연구를 충분히 이후 stage(단계)에 썼느냐였다.
판정은 `partially_used_but_not_sufficient_for_current_goal(부분 활용, 현재 목표에는 불충분)`이다.
Effect(효과): 이전 연구를 버리지는 않았지만, 압축 feature(피처)와 gate/rank bucket(게이트/순위 구간)에 너무 접힌 부분을 run267S(267S 실행)부터 후보군 전체 축으로 다시 벌린다.

## Candidate Scope(후보 범위)

| candidate(후보) | role(역할) | run267R status(267R 상태) | pool decision(후보군 판정) |
| --- | --- | --- | --- |
| `s264_aih` | core challenger(핵심 도전자) | `run267R_internal_branch_pruned_to_salvage_clue` | `retain_for_run267S_matrix_no_selection` |
| `s264_lc` | defensive control(방어 통제) | `not_in_run267R_internal_branch_restore_to_pool` | `retain_for_run267S_matrix_no_selection` |
| `s262_lih` | validation-heavy(검증 중심) | `not_in_run267R_internal_branch_restore_to_pool` | `retain_for_run267S_matrix_no_selection` |
| `s264_aia` | OOS anchor(표본외 앵커) | `run267R_internal_branch_pruned_to_salvage_clue` | `retain_for_run267S_matrix_no_selection` |
| `s258_stc` | stress challenger(압박 도전자) | `not_in_run267R_internal_branch_restore_to_pool` | `retain_for_run267S_matrix_no_selection` |

## Axes(축)

| axis(축) | priority(우선순위) | effect(효과) |
| --- | --- | --- |
| `run267S_axis01_pool_wide_variant_distinguishability` | `P0` | ablation/replacement(제거/대체) 결과가 같은 KPI shape(핵심 성과 지표 모양)으로 접히는지 후보별로 다시 물질화한다. |
| `run267S_axis02_non_calendar_weak_slice_resilience` | `P0` | weekday/session(요일/세션)을 직접 맞추지 않고 volatility/trend/risk (변동성/추세/위험) 구조 feature(피처)로 약한 구간을 줄이는지 본다. |
| `run267S_axis03_candidate_pool_prune_or_restore` | `P1` | 다섯 후보 유지/탈락/회수 조건을 같은 evidence(근거) 단위로 갱신한다. |

## Boundary(경계)

- judgment(판정): `matrix_materialized_execution_pending_no_candidate_selection(행렬 물질화, 실행 대기, 선택 후보 없음)`.
- next_action(다음 행동): `run267T_build_pool_wide_orthogonal_stability_mt5_attempts`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).

## Artifacts(산출물)

- candidate_scope(후보 범위): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267S/pool_wide_orthogonal_stability_racing_matrix/candidate_scope_update.csv`
- orthogonal_matrix(직교 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267S/pool_wide_orthogonal_stability_racing_matrix/orthogonal_stability_matrix.csv`
- materialization_queue(물질화 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267S/pool_wide_orthogonal_stability_racing_matrix/materialization_queue.csv`
- failure_memory_link(실패 기억 연결): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267S/pool_wide_orthogonal_stability_racing_matrix/failure_memory_link.csv`
- experiment_design_receipt(실험 설계 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267S/pool_wide_orthogonal_stability_racing_matrix/experiment_design_receipt.csv`
- gate_receipt(게이트 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267S/pool_wide_orthogonal_stability_racing_matrix/gate_receipt.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267S/pool_wide_orthogonal_stability_racing_matrix/lineage.json`
- result(결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267S/pool_wide_orthogonal_stability_racing_matrix/result.json`
