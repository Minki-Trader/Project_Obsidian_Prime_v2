# Stage267 Run267DT Runtime Gap Aware Fifth Follow-Up/Prune Design(267단계 267DT 런타임 공백 반영 5차 후속/가지치기 설계)

- status(상태): `run267DT_runtime_gap_aware_fifth_followup_or_prune_design_completed`
- parent_run(부모 실행): `run267DS_stage267_runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures_v1`
- feature_blueprints(피처 청사진): `6`
- materialization_queue(물질화 대기열): `6`
- prune_rows(가지치기 행): `4`
- failure_memory(실패 기억): `4`
- next_action(다음 행동): `run267DU_materialize_runtime_gap_aware_fifth_followup_or_prune_queue`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DT(267DT 실행)는 run267DS(267DS 실행)의 결과를 다음 실험 대기열(queue, 대기열)로 바꿨다.
효과: s258_stc(258 STC 후보)는 테이블 인계 실패와 성능 약화를 분리하고, s264_lc(264 LC 후보)는 방어 대조로만 남기며, s264_aih(264 AIH 후보)는 폭발형 공격 실험으로 다시 전면에 올린다.
즉, 수리(repair, 수리)만 하지 않고 공격형(explosive/aggressive, 폭발형/공격형) 탐색도 같이 밀어붙인다.

## Queue(대기열)

| queue_id(대기열 ID) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | intent(의도) |
|---|---|---|---|---|
| `q01_s258_supply_continuity_table_handoff_repair` | `P0_repair` | `s258_stc` | `runtime_handoff_repair(런타임 인계 수리)` | materialize preflight receipts, then narrow MT5 retry(사전 영수증 생성 후 좁은 MT5 재시도). |
| `q02_s258_noncalendar_impulse_reentry_cross_period` | `P0_aggressive` | `s258_stc` | `aggressive_noncalendar_impulse(공격형 비달력 충격)` | materialize aggressive variant pack(공격형 변형 묶음 물질화). |
| `q03_s264_aih_explosive_shock_state_oos_final_month` | `P0_explosive` | `s264_aih` | `explosive_core_challenger_reentry(폭발형 핵심 도전자 재진입)` | materialize explosive challenger attempts(폭발형 도전자 시도 물질화). |
| `q04_s264_lc_defensive_dd_cluster_control` | `P0_control` | `s264_lc` | `defensive_dd_cluster_control(방어 손실폭 군집 대조)` | materialize only if needed as control receipt(필요 시 대조 영수증으로만 물질화). |
| `q05_s264_aia_s262_lih_supply_manifest_diagnostic` | `P1_diagnostic` | `s264_aia;s262_lih` | `pre_runtime_supply_diagnostic(런타임 전 공급 진단)` | do not schedule MT5 until diagnostic passes(진단 통과 전 MT5 배정 금지). |
| `q06_s264_aih_s258_similar_feature_replacement` | `P1_replacement` | `s264_aih;s258_stc` | `similar_feature_replacement(유사 피처 대체)` | materialize after q03/q02 shape is available(q03/q02 형태 확보 후 물질화). |

## Branch Decisions(분기 판단)

| decision(판단) | candidate(후보) | next_use(다음 용도) | stop_condition(중단 조건) |
|---|---|---|---|
| `bd267dt_s258_supply_continuity_repair_once` | `s258_stc` | P0 handoff repair plus narrow MT5 retry(P0 인계 수리와 좁은 MT5 재시도) | 수리 뒤에도 init_failed(초기화 실패)가 반복되면 이 branch(분기)는 닫는다. |
| `bd267dt_s258_taper_not_enough_use_aggressive_noncalendar` | `s258_stc` | P0 aggressive noncalendar reentry(P0 공격형 비달력 재진입) | 거래 수가 얇아지거나 2025H1/H2 품질이 계속 약하면 s258 공격 축을 낮춘다. |
| `bd267dt_s264_aih_reenter_as_explosive_core_challenger` | `s264_aih` | P0 explosive shock-state probe(P0 폭발형 충격 상태 탐침) | OOS 회복이 무너지면 shock-state 방향은 실패 기억으로 닫는다. |
| `bd267dt_s264_lc_keep_control_only` | `s264_lc` | P0 defensive control DD cluster(P0 방어 대조 손실폭 군집) | DD를 줄이려는 수리가 2단계 이상 반복되면 닫는다. |
| `bd267dt_aia_lih_no_blind_retry` | `s264_aia;s262_lih` | P1 supply manifest diagnostic(P1 공급 목록 진단) | 공급 증명이 없으면 이번 루프에서 실행하지 않는다. |

## Failure Memory(실패 기억)

| memory(기억) | affected_scope(영향 범위) | do_not_repeat(반복 금지) |
|---|---|---|
| `fm267dt_ebm_table_open_failed_5003` | s258_stc supply continuity run267dq_01/02/03 | init failure(초기화 실패)를 zero-trade success(무거래 성공)로 해석하지 않는다. |
| `fm267dt_s258_validation_oos_quality_decay` | s258_stc monday late DD taper | 시간대 필터만 더 붙이지 않는다. |
| `fm267dt_s264_lc_dd_cluster` | s264_lc historical_2024 | 수익이 크다는 이유로 선택 후보로 말하지 않는다. |
| `fm267dt_s264_aih_oos_final_month_loss` | s264_aih 2026.04 | OOS 전체 숫자만 보고 약한 마지막 달을 숨기지 않는다. |

## Boundary(경계)

run267DT(267DT 실행)는 design(설계)이다. MT5(MetaTrader 5, 메타트레이더5) 실행 결과, Adapter(어댑터) 패키지, ONNX parity(ONNX 동등성)는 아직 없다.
따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 주장하지 않는다.

## Artifacts(산출물)

- feature_blueprint(피처 청사진): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DT/runtime_gap_aware_fifth_followup_or_prune_design/feature_blueprint.csv`
- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DT/runtime_gap_aware_fifth_followup_or_prune_design/branch_decision_matrix.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DT/runtime_gap_aware_fifth_followup_or_prune_design/materialization_queue.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DT/runtime_gap_aware_fifth_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DT/runtime_gap_aware_fifth_followup_or_prune_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DT/runtime_gap_aware_fifth_followup_or_prune_design/experiment_design_receipt.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DT/runtime_gap_aware_fifth_followup_or_prune_design/review_result.json`
