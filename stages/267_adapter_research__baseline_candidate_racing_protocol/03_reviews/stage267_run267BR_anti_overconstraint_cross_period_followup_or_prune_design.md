# Stage267 run267BR Anti-overconstraint Cross-period Follow-up/Prune Design(과제약 제거 확장 기간 후속/가지치기 설계)

## Summary(요약)

- run_id(실행 ID): `run267BR_stage267_anti_overconstraint_cross_period_followup_or_prune_design_v1`
- parent_run(상위 실행): `run267BQ_stage267_anti_overconstraint_cross_period_balance_timeslice_trade_quality_v1`
- status(상태): `run267BR_anti_overconstraint_cross_period_followup_or_prune_design_completed`
- branch_decisions(분기 판단): `4`
- followup_queue_rows(후속 대기열 행): `3`
- failure_memory_rows(실패 기억 행): `2`
- negative_register_status(부정 결과 등록 상태): `registered`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BQ(267BQ 실행)의 확장 기간 리뷰를 후보 선택이 아니라 follow-up/prune design(후속/가지치기 설계)로 바꿨다.
Effect(효과): anti_overconstraint_prune(과제약 제거)을 독립 후보로 고르지 않고, 방향 비대칭과 공격형 임펄스 대체 실험으로 넘긴다.

## Cross-period Evidence(확장 기간 근거)

| period(기간) | trades(거래) | net(순수익) | PF(수익 팩터) | closed DD%(폐쇄 손실폭 %) | late net(후반 순수익) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `2023H2` | 221 | 998.53 | 1.920915 | 13.794638 | 563.95 | `watch_more_pressure_no_selection(추가 압박 관찰, 선택 아님)` |
| `2025H1` | 372 | 113.39 | 1.077543 | 22.118133 | -102.01 | `fragile_watch_or_prune(취약 관찰 또는 가지치기)` |
| `2025H2` | 219 | 55.79 | 1.049843 | 28.148763 | -74.79 | `fragile_watch_or_prune(취약 관찰 또는 가지치기)` |

## Key Branch Decisions(핵심 분기 판단)

| decision(판단) | label(라벨) | next_use(다음 사용) |
| --- | --- | --- |
| `br_d01_standalone_anti_overconstraint_prune` | `downgrade_to_salvage_clue_no_selection(회수 단서로 하향, 선택 아님)` | Preserve the 2023H2 momentum clue, but do not treat this variant as a research baseline candidate. |
| `br_d02_sell_side_fragility` | `asymmetric_surface_probe_needed(비대칭 표면 탐침 필요)` | Design side-specific margin/rank reweighting across the full baseline pool. |
| `br_d03_time_slice_fragility` | `no_calendar_blacklist_repair(달력 블랙리스트 수리 금지)` | Use time slices as diagnostics for non-calendar state features, not as hard filters. |
| `br_d04_aggressive_impulse_branch` | `open_aggressive_pool_wide_branch(공격형 후보군 전체 분기 개방)` | Materialize run267BS as a pool-wide directional asymmetry and impulse replacement queue. |

## Next Queue(다음 대기열)

| queue(대기열) | priority(우선순위) | workstream(작업 흐름) | purpose(목적) |
| --- | --- | --- | --- |
| `run267bs_q01_pool_wide_directional_asymmetry` | `P0` | `pool_wide_directional_asymmetry` | Confirm whether sell-side fragility is structural or only a s264_aih filter accident. |
| `run267bs_q02_aggressive_impulse_replacement` | `P0` | `aggressive_impulse_replacement` | Force an aggressive branch that can produce a genuinely strong candidate instead of only reducing weak trades. |
| `run267bs_q03_late_segment_risk_shape` | `P1` | `late_segment_risk_shape_adapter` | Decide whether an Adapter branch should alter risk/ATR or hold-shape handoff before ONNX is even considered. |

## Worst Negative Slices(최악 음수 구간)

| period(기간) | axis(축) | bucket(구간) | trades(거래) | net(순수익) | PF(수익 팩터) |
| --- | --- | --- | ---: | ---: | ---: |
| `2025H1` | `direction` | `sell` | 119 | -267.91 | 0.678229 |
| `2025H1` | `close_hour_report` | `16` | 64 | -185.24 | 0.626841 |
| `2025H1` | `weekday` | `Wednesday` | 71 | -127.18 | 0.60343 |
| `2025H1` | `chron_segment` | `chron_late` | 124 | -102.01 | 0.834176 |
| `2025H1` | `month` | `2025-05` | 39 | -76.7 | 0.690389 |
| `2025H2` | `chron_segment` | `chron_late` | 73 | -74.79 | 0.799668 |
| `2025H2` | `month` | `2025-12` | 41 | -69.07 | 0.720138 |
| `2025H2` | `weekday` | `Monday` | 28 | -63.28 | 0.653526 |

## Boundary(경계)

- 이 실행은 design-only(설계 전용) 작업이다.
- anti_overconstraint_prune(과제약 제거)은 standalone selection(독립 선택)에서 하향한다.
- 다음은 run267BS(267BS 실행) materialization(물질화)이며, MT5(MetaTrader 5, 메타트레이더5) 성과 주장은 아직 없다.
- selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX conversion(ONNX 변환), Goal Achieve(목표 달성)는 주장하지 않는다.

## Artifacts(산출물)

- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BR/anti_overconstraint_cross_period_followup_or_prune_design/branch_decision_matrix.csv`
- followup_queue(후속 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BR/anti_overconstraint_cross_period_followup_or_prune_design/followup_queue.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BR/anti_overconstraint_cross_period_followup_or_prune_design/failure_memory.csv`
- performance_attribution(성과 귀속): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BR/anti_overconstraint_cross_period_followup_or_prune_design/performance_attribution.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BR/anti_overconstraint_cross_period_followup_or_prune_design/experiment_design_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BR/anti_overconstraint_cross_period_followup_or_prune_design/result_judgment.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BR/anti_overconstraint_cross_period_followup_or_prune_design/gate_audit.csv`
- next_action(다음 행동): `run267BS_materialize_pool_wide_directional_impulse_followup_queue`
