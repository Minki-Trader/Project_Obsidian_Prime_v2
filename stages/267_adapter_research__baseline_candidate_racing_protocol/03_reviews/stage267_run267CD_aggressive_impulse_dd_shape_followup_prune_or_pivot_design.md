# Stage267 Run267CD Aggressive Impulse DD-shape Follow-up Prune or Pivot Design(267단계 267CD 공격형 임펄스 손실폭 형태 후속 가지치기 또는 방향전환 설계)

## Summary(요약)

- run_id(실행 ID): `run267CD_stage267_aggressive_impulse_dd_shape_followup_prune_or_pivot_design_v1`
- parent_run(상위 실행): `run267CC_stage267_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review_v1`
- status(상태): `run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design_completed`
- branch_decisions(분기 판단): `5`
- pivot_queue_rows(방향전환 대기열 행): `4`
- prune_rows(가지치기 행): `4`
- failure_memory_rows(실패 기억 행): `7`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267CC(267CC 실행)의 양수 후속 결과를 다시 읽고, 같은 DD-shape(손실폭 형태) repair loop(수리 루프)를 닫을지 판단했다.
Effect(효과): s264_aih는 상대적으로 나은 관찰 후보로만 유지하고, s258_stc는 stress comparator(압박 비교군)로 낮추며, 다음은 후보군 전체의 orthogonal loss-shape/state pivot(직교 손실형태/상태 방향전환)으로 넘긴다.

## Why This Took Time(왜 오래 걸렸나)

- baseline(기준 후보)은 운영 기준선이 아니라 R&D racing(연구개발 경주) 출발 후보군이다.
- 숫자 1등을 고르는 일이 아니라, 기간/구간/피처/대체/곡선/거래품질에서 덜 깨지는지를 확인해야 한다.
- 이번 분기는 양수였지만 worst DD(최악 손실폭)가 `15%` 이상이라 선택으로 닫으면 과장이다.
- 그래서 결과를 버리지 않고 failure memory(실패 기억)와 다음 pivot queue(방향전환 대기열)로 바꿨다.

## Candidate Read(후보 판독)

| candidate(후보) | net(순익) | PF(수익 팩터) | trades(거래 수) | worst DD%(최악 손실폭) | read(판독) |
| --- | ---: | ---: | ---: | ---: | --- |
| `s264_aih` | 415.11 | 1.65 | 151 | 15.52 | `single_period_followup_dd_watch_no_selection(단일 기간 후속 관찰, 선택 아님)` |
| `s258_stc` | 394.51 | 1.62 | 149 | 16.08 | `single_period_followup_dd_watch_no_selection(단일 기간 후속 관찰, 선택 아님)` |

## Branch Decisions(분기 판단)

| decision(판단) | label(라벨) | next_use(다음 사용) |
| --- | --- | --- |
| `run267cd_d01_close_current_ddshape_repair_loop` | `close_branch_no_selection(분기 종료, 선택 아님)` | pivot to pool-wide orthogonal loss-shape/state design(후보군 전체 직교 손실형태/상태 설계로 전환) |
| `run267cd_d02_keep_s264_aih_as_relative_watch_only` | `watch_relative_best_not_selected(상대 최선 관찰, 선택 아님)` | carry as core challenger reference in the next pivot, not as a chosen baseline(다음 전환의 핵심 도전자 참조로 유지, 선택 기준 아님) |
| `run267cd_d03_prune_s258_stc_deep_repair_from_this_branch` | `stress_comparator_only_prune_deep_repair(압박 비교군만 유지, 깊은 수리 중단)` | keep as stress comparator and reopen only if a broader loss-shape feature rescues DD(압박 비교군으로만 유지하고 넓은 손실형태 피처가 DD를 살릴 때만 재개) |
| `run267cd_d04_reanchor_full_candidate_pool` | `reanchor_controls_and_anchor(대조군과 앵커 재고정)` | next queue must include all five roles or explicitly justify exclusion(다음 큐는 다섯 역할을 포함하거나 제외 이유를 명시) |
| `run267cd_d05_pivot_to_orthogonal_loss_shape_state` | `pivot_not_calendar_filter(달력 필터가 아닌 방향 전환)` | design adverse-excursion, giveback, volatility-state, and session-state features across the pool(후보군 전체에 불리한 이동, 수익 반납, 변동성 상태, 세션 상태 피처 설계) |

## Pivot Queue(방향전환 대기열)

| queue(대기열) | priority(우선순위) | candidate(후보) | purpose(목적) |
| --- | --- | --- | --- |
| `run267ce_q01_pool_wide_loss_shape_state_feature_engineering` | `P0` | `s264_aih;s264_lc;s262_lih;s264_aia;s258_stc` | decide whether the next branch should be feature engineering, Adapter tracing, or candidate pruning(다음 분기가 피처 엔지니어링, 어댑터 추적, 후보 가지치기 중 무엇인지 결정) |
| `run267ce_q02_reanchor_defensive_controls_and_oos_anchor` | `P0` | `s264_lc;s262_lih;s264_aia` | prevent s264_aih or s258_stc from becoming a silent baseline by absence of controls(대조군 부재로 s264_aih 또는 s258_stc가 조용히 기준처럼 굳는 것을 막음) |
| `run267ce_q03_s264_aih_relative_best_adapter_trace_watch` | `P1` | `s264_aih` | decide whether Adapter development is worth a bounded branch later(나중에 제한된 어댑터 개발 분기 가치가 있는지 판단) |
| `run267ce_q04_s258_stc_stress_reopen_rule` | `P1` | `s258_stc` | keep failure memory alive without wasting another repair loop(실패 기억은 살리고 또 다른 수리 루프 낭비 방지) |

## Prune Boundary(가지치기 경계)

| prune(가지치기) | label(라벨) | reopen(재개 조건) |
| --- | --- | --- |
| `run267cd_p01_no_candidate_selection_from_positive_2025h2` | `no_headline_selection(대표 숫자 선택 금지)` | multi-period, pool-wide, curve-shape evidence improves without DD relocation(다기간 후보군 전체 곡선 근거가 DD 이동 없이 개선) |
| `run267cd_p02_no_calendar_only_slice_repair` | `no_calendar_only_filter(달력 단독 필터 금지)` | only as diagnostic after non-calendar state feature fails(비달력 상태 피처가 실패한 뒤 진단으로만 재개) |
| `run267cd_p03_no_third_pass_same_ddshape_loop` | `stop_same_branch_loop(같은 분기 루프 중단)` | new cross-candidate feature meaning, not another threshold or slice tweak(또 다른 임계값/구간 조정이 아니라 후보 공통 피처 의미) |
| `run267cd_p04_no_onnx_or_adapter_claim` | `no_onnx_adapter_claim(ONNX/어댑터 주장 금지)` | goal gates later satisfied by strong candidate package(나중에 강한 후보 패키지가 목표 게이트 충족) |

## Judgment(판정)

- current branch(현재 분기): `close_branch_no_selection(분기 종료, 선택 아님)`
- s264_aih: `watch_relative_best_not_selected(상대 최선 관찰, 선택 아님)`
- s258_stc: `stress_comparator_only(압박 비교군만)`
- next_action(다음 행동): `run267CE_design_pool_wide_orthogonal_loss_shape_state_pivot_queue`
- ONNX conversion(ONNX 변환), runtime reproduction(런타임 재현), Adapter materialization(어댑터 물질화)은 아직 진행하지 않는다.

## Artifacts(산출물)

- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/branch_decision_matrix.csv`
- pivot_queue(방향전환 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/pivot_queue.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/experiment_design_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/result_judgment.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/lineage.json`
