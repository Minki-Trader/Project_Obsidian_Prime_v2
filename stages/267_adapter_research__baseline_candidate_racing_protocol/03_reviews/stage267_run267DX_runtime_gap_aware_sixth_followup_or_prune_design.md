# Stage267 Run267DX Runtime Gap Aware Sixth Follow-Up/Prune Design(267단계 267DX 런타임 공백 반영 6차 후속/가지치기 설계)

- status(상태): `run267DX_runtime_gap_aware_sixth_followup_or_prune_design_completed`
- source_run(원천 실행): `run267DW_stage267_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures_v1`
- queue_rows(대기열 행): `6`
- aggressive_or_explosive_rows(공격/폭발 행): `3`
- prune_rows(가지치기 행): `3`
- failure_memory_rows(실패 기억 행): `4`
- next_action(다음 행동): `run267DY_materialize_runtime_gap_aware_sixth_followup_or_prune_queue`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DX(267DX 실행)는 run267DW(267DW 실행)의 review(검토)를 다음 materialization queue(물질화 대기열)로 바꾼 설계다.
효과: s258_stc(258 STC 후보)는 수익은 살아 있지만 DD(drawdown, 손실폭)와 약한 시간/월 구간이 불편해서 구조적 반증으로만 계속 본다.
효과: s264_aih(264 AIH 후보)는 validation anchor(검증 앵커) init failure(초기화 실패)와 2026.04 음수가 겹쳐, 한 번만 수리하고 실패하면 가지치기한다.
효과: s264_lc(264 LC 후보)는 같은 달 control(대조)로만 남기고 도전자 수리는 하지 않는다.

baseline(기준 후보)을 정하는 데 오래 걸리는 이유는 여기서 baseline(기준 후보)이 운영 기준선이 아니기 때문이다. 지금은 R&D racing(연구개발 경주)용 후보군이므로, 숫자 몇 개보다 balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), 약한 월/요일/시간, Adapter(어댑터) 확장 가능성을 같이 본다.

## Queue(대기열)

| queue_id(대기열 ID) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | instruction(지시) |
|---|---|---|---|---|
| `q01_s258_stc_structural_dd_shape_split` | `P0` | `s258_stc` | structural_dd_shape_split(구조적 손실폭 형태 분리) | materialize structural variants(구조 변형 물질화); avoid hour-only exclusion(시간만 제외 금지) |
| `q02_s258_stc_adverse_slice_falsification` | `P0` | `s258_stc` | adverse_slice_falsification(불리 구간 반증) | materialize falsification variants(반증 변형 물질화) with structural state features(구조 상태 피처) |
| `q03_s264_aih_validation_anchor_one_repair` | `P0` | `s264_aih` | validation_anchor_one_repair(검증 앵커 1회 수리) | one repair only(1회 수리만); then prune if failure persists(실패 지속 시 가지치기) |
| `q04_s264_aih_counter_shock_final_month_probe` | `P0` | `s264_aih` | counter_shock_final_month_probe(반대 충격 마지막 달 탐침) | materialize as falsification probe(반증 탐침으로 물질화), not selection(선택 아님) |
| `q05_s264_lc_same_month_control_hold` | `P1` | `s264_lc` | same_month_control_hold(같은 월 대조 보류) | hold unless paired control is needed(쌍 대조 필요 시에만 보류 해제) |
| `q06_prune_micro_filter_stack` | `P0_guardrail` | `s258_stc;s264_aih;s264_lc` | anti_micro_filter_stack(미세 필터 누적 방지) | do not materialize standalone(단독 물질화 금지) |

## Branch Decisions(분기 판단)

| decision(판단) | candidate(후보) | next_use(다음 용도) | stop_condition(중단 조건) |
|---|---|---|---|
| `bd267dx_s258_keep_only_as_structural_stress_challenger` | `s258_stc` | q01/q02에서 구조적 DD와 약한 구간 반증으로만 사용한다. | 단순 제외형 필터로만 좋아지면 stress-only(압박 전용) 보류로 낮춘다. |
| `bd267dx_s264_aih_one_repair_then_prune` | `s264_aih` | q03 repair gate(수리 게이트)와 q04 counter shock(반대 충격)으로만 사용한다. | init failure 또는 final-month negative(마지막 달 음수)가 반복되면 해당 branch(분기)를 종료한다. |
| `bd267dx_s264_lc_control_only` | `s264_lc` | q03/q04가 실행될 때 시장 공통 약점 판별용으로만 쓴다. | 독립 도전자 repair(수리)로 확장하지 않는다. |
| `bd267dx_filter_stack_pruned` | `pool_guardrail` | run267DY materialization audit(물질화 감사)에 적용한다. | filter-only(필터 전용) 변형은 실행하지 않는다. |

## Prune Matrix(가지치기 행렬)

| prune_id(가지치기 ID) | affected(대상) | why(이유) | do_not_repeat(반복 금지) |
|---|---|---|---|
| `pr267dx_hour_weekday_month_only_filters` | `s258_stc` | 단순 제외는 balance/equity curve(잔액/평가금 곡선) 체질 개선을 증명하지 못한다. | hour-only, weekday-only, month-only 제외 실험 반복 금지 |
| `pr267dx_s264_aih_deep_repair_loop_cap` | `s264_aih` | 한 후보의 table handoff(테이블 인계) 수리를 3 stage(단계) 이상 끌면 목표의 repair cap(수리 제한)을 어긴다. | init failure 반복 branch(분기)를 계속 끌지 않는다. |
| `pr267dx_s264_lc_challenger_expansion` | `s264_lc` | final month(마지막 달) net -39.29와 PF 0.403975라 새 도전자 축으로 확장할 근거가 없다. | 독립 repair(수리) 분기로 열지 않는다. |

## Failure Memory(실패 기억)

| memory(기억) | affected_scope(대상 범위) | do_not_repeat(반복 금지) |
|---|---|---|
| `fm267dx_s258_profit_with_dd_fragility` | s258_stc 2025H1/2025H2 | 수익만 보고 선택하지 않는다. |
| `fm267dx_s258_adverse_slice_concentration` | hour16;Monday;2025-12 | 특정 bucket(구간)만 제거하는 미세 조정 반복 금지 |
| `fm267dx_s264_aih_anchor_and_final_month_break` | s264_aih validation anchor and 2026.04 | 깊은 repair loop(수리 루프) 반복 금지 |
| `fm267dx_s264_lc_control_negative` | s264_lc 2026.04 | 도전자처럼 수리하지 않는다. |

## Gate Audit(게이트 감사)

| gate(게이트) | status(상태) | effect(효과) |
|---|---|---|
| `gate267dx_input_evidence` | `pass` | design starts from run267DW evidence(267DW 근거에서 시작) |
| `gate267dx_aggressive_branch` | `pass` | avoids too-defensive-only loop(방어만 도는 루프 방지) |
| `gate267dx_repair_cap` | `pass` | prevents dragging one repair branch(한 수리 분기 장기화 방지) |
| `gate267dx_anti_filter_stack` | `pass` | weak slices become structural tests(약한 구간을 구조 시험으로 전환) |
| `gate267dx_materialization_ready` | `pass` | run267DY can create variants/attempts(변형/시도 생성 가능) |
| `gate267dx_claim_guard` | `pass` | keeps this as R&D racing design(연구개발 경주 설계) only |

## Boundary(경계)

run267DX(267DX 실행)는 design(설계)이다. 새 MT5(MetaTrader 5, 메타트레이더5) 결과, Adapter(어댑터) 패키지, ONNX parity(ONNX 동등성) 근거는 아직 없다.
따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 주장하지 않는다.

## Artifacts(산출물)

- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DX/runtime_gap_aware_sixth_followup_or_prune_design/materialization_queue.csv`
- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DX/runtime_gap_aware_sixth_followup_or_prune_design/branch_decision_matrix.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DX/runtime_gap_aware_sixth_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DX/runtime_gap_aware_sixth_followup_or_prune_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DX/runtime_gap_aware_sixth_followup_or_prune_design/experiment_design_receipt.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DX/runtime_gap_aware_sixth_followup_or_prune_design/gate_audit.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DX/runtime_gap_aware_sixth_followup_or_prune_design/review_result.json`
