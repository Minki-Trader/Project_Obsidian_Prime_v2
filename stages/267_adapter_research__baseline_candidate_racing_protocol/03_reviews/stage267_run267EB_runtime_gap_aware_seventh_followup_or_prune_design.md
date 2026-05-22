# Stage267 Run267EB Seventh Follow-Up/Prune Design(267단계 267EB 7차 후속/가지치기 설계)

- status(상태): `run267EB_runtime_gap_aware_seventh_followup_or_prune_design_completed`
- source_run(원천 실행): `run267EA_stage267_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review_v1`
- feature_blueprints(피처 청사진): `5`
- branch_decisions(분기 판단): `6`
- materialization_queue(물질화 대기열): `8`
- aggressive_rows(공격형 행): `2`
- prune_rows(가지치기 행): `5`
- failure_memory(실패 기억): `6`
- next_action(다음 행동): `run267EC_materialize_runtime_gap_aware_seventh_followup_or_prune_queue`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267EB(267EB 실행)는 후보를 고른 단계가 아니다. run267EA(267EA 실행)에서 보인 약점을 다음 materialization(물질화) 큐로 바꾼 설계 단계다.
s258_stc는 2023H2 수익만 보고 밀지 않고 2025H1/H2 생존 조건을 먼저 본다. s264_aih는 2026.04 마지막 달 구멍을 한 번만 더 구조적으로 재검토하고, s264_lc는 해석 대조로만 둔다.
또 s262_lih와 s264_aia는 이번 6차 실행 리뷰에 없었기 때문에 후보군 커버리지 차원에서 다시 불러온다. 필터를 더 붙이는 행은 prune guard(가지치기 가드)로 막고, aggressive/explosive(공격/폭발) 실험도 별도 행으로 강행한다.

## Branch Decisions(분기 판단)

| decision(판단) | candidates(후보) | next(다음) |
|---|---|---|
| `bd267eb_s258_period_survival_before_combine` | `s258_stc` | run267EC materializes 2025H1/H2 survival attempts before any combine. |
| `bd267eb_s264_aih_one_rebuild_then_stop` | `s264_aih` | run267EC materializes one counter-shock rebuild and compares with s264_lc control. |
| `bd267eb_s264_lc_interpretation_control_only` | `s264_lc` | Use as paired control(쌍 대조), not candidate selection. |
| `bd267eb_missing_pool_axes_rejoin` | `s262_lih;s264_aia` | run267EC restores at least one coverage row for each missing axis. |
| `bd267eb_force_explosive_not_filter_loop` | `s258_stc;s264_aih` | run267EC includes aggressive/explosive(공격/폭발) rows without hour/month hard bans. |
| `bd267eb_filter_stack_pruned` | `pool` | Keep as guardrail row only. |

## Materialization Queue(물질화 대기열)

| queue(대기열) | priority(우선순위) | candidates(후보) | mode(모드) |
|---|---|---|---|
| `q01_s258_2025h1_period_survival_gate` | `P0_survival_gate(P0 생존 게이트)` | `s258_stc` | `diagnostic_defensive(진단형 방어)` |
| `q02_s258_2025h2_period_survival_gate` | `P0_survival_gate(P0 생존 게이트)` | `s258_stc` | `diagnostic_defensive(진단형 방어)` |
| `q03_s258_explosive_impulse_supply_probe` | `P0_aggressive_explosive(P0 공격형 폭발)` | `s258_stc` | `aggressive_explosive(공격형 폭발)` |
| `q04_s264_aih_validation_anchor_integrity_check` | `P1_validation_integrity(P1 검증 무결성)` | `s264_aih` | `defensive_integrity(방어형 무결성)` |
| `q05_s264_aih_202604_counter_shock_rebuild` | `P0_repair_cap(P0 수리 제한)` | `s264_aih;s264_lc` | `bounded_repair(제한 수리)` |
| `q06_s264_aih_explosive_counter_impulse_probe` | `P1_aggressive_explosive(P1 공격형 폭발)` | `s264_aih` | `aggressive_explosive(공격형 폭발)` |
| `q07_s262_s264_aia_pool_coverage_rejoin` | `P1_pool_coverage(P1 후보군 커버리지)` | `s262_lih;s264_aia` | `coverage_control(커버리지 대조)` |
| `q08_filter_stack_prune_guard_hold` | `P0_prune_guard(P0 가지치기 가드)` | `pool` | `prune_guard(가지치기 가드)` |

## Prune/Failure Boundary(가지치기/실패 경계)

- headline profit selection(대표 수익 선택)은 금지한다.
- one-month rescue selection(한 달 구제 선택)은 금지한다.
- naked calendar/hour filter stack(달력/시간 필터 누적)은 가지치기한다.
- one bounded repair(제한 수리 1회) 뒤에도 깨지면 실패 기억으로 닫는다.

## Boundary(경계)

- 이 설계는 exploratory design(탐색 설계)이며 후보 선택, 연구 기준 후보 선택, ONNX(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
- 다음 run267EC(267EC 실행)는 materialization_queue(물질화 대기열)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿔야 한다.

## Artifacts(산출물)

- feature_blueprint(피처 청사진): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EB/runtime_gap_aware_seventh_followup_or_prune_design/feature_blueprint.csv`
- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EB/runtime_gap_aware_seventh_followup_or_prune_design/branch_decision_matrix.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EB/runtime_gap_aware_seventh_followup_or_prune_design/materialization_queue.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EB/runtime_gap_aware_seventh_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EB/runtime_gap_aware_seventh_followup_or_prune_design/failure_memory.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EB/runtime_gap_aware_seventh_followup_or_prune_design/gate_audit.csv`
- run_manifest(실행 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EB/runtime_gap_aware_seventh_followup_or_prune_design/run_manifest.json`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EB/runtime_gap_aware_seventh_followup_or_prune_design/lineage.json`
