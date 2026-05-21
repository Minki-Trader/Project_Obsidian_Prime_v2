# Stage267 Run267BZ Aggressive Impulse Follow-up/Prune Design(267단계 267BZ 공격형 임펄스 후속/가지치기 설계)

## Summary(요약)

- run_id(실행 ID): `run267BZ_stage267_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design_v1`
- parent_run(상위 실행): `run267BY_stage267_aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review_v1`
- status(상태): `run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design_completed`
- branch_decisions(분기 판단): `4`
- materialization_queue(물질화 대기열): `3`
- prune_rows(가지치기 행): `3`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BY(267BY 실행)의 양수 총합, 손실폭, 후반 세션 약점을 후속 대기열과 가지치기 판단으로 바꿨다.
Effect(효과): 최고 숫자 후보를 바로 고르지 않고, 어떤 후보는 더 압박하고 어떤 수리 방식은 반복하지 않을지 고정했다.

## Candidate Read(후보 판독)

| candidate(후보) | total net(총 순수익) | min PF(최저 수익 팩터) | worst DD%(최악 손실폭 %) | trades(거래 수) | decision(판단) |
| --- | ---: | ---: | ---: | ---: | --- |
| `s258_stc` | 1952.09 | 1.471409 | 15.96 | 571 | P0 stress with DD cap(손실폭 상한 압박) |
| `s264_aih` | 1812.06 | 1.613865 | 13.717068 | 531 | P0 continue(우선 계속) |
| `s264_aia` | 1777.83 | 1.580338 | 15.84 | 535 | control hold(대조 보류) |

## Next Queue(다음 대기열)

| queue(대기열) | priority(우선순위) | candidate(후보) | target(목표) | purpose(목적) |
| --- | --- | --- | --- | --- |
| `run267bz_q01_s264_aih_2025h2_late_session_dd_shape_guard` | `P0` | `s264_aih` | `2025H2` / `close_hour_report=22;session_21_23_report_time` | aggressive_impulse_dd_shape_followup(공격형 임펄스 손실폭 형태 후속) |
| `run267bz_q02_s258_stc_2025h2_stress_dd_cap` | `P0` | `s258_stc` | `2025H2` / `close_hour_report=22;session_21_23_report_time;worst_dd_percent_near_16` | stress_challenger_dd_cap(압박 도전자 손실폭 상한) |
| `run267bz_q03_s264_aih_2023h2_curve_zoom_sanity` | `P1` | `s264_aih` | `2023H2` / `weakest candidate in 2023H2 period summary(2023H2 기간 요약에서 가장 약한 후보)` | curve_zoom_sanity(곡선 확대 정상성) |

## Prune Matrix(가지치기 행렬)

| prune(가지치기) | scope(범위) | reason(이유) | reopen(재개 조건) |
| --- | --- | --- | --- |
| `run267bz_p01_no_headline_positive_selection` | selection_claim(선택 주장) | all three candidates are positive, but Tier B, routed total, Adapter structure, and curve zoom are still missing(세 후보가 모두 양수지만 티어 B, 실제 라우팅 전체, 어댑터 구조, 곡선 확대가 아직 없음) | reopen selection only after materialized follow-up survives MT5 and trade-quality review(물질화 후속이 MT5와 거래 품질 검토를 버틴 뒤에만 선택 재개) |
| `run267bz_p02_no_calendar_only_22h_filter` | repair_method(수리 방식) | 22h is a visible weak bucket, but deleting one clock bucket would hide whether risk shape is real(22시는 보이는 약점이지만 한 시각 삭제는 위험 형태가 실제인지 숨김) | only if multiple periods prove the same clock bucket is structurally invalid(여러 기간에서 같은 시각 구간이 구조적으로 무효임이 증명될 때만 재개) |
| `run267bz_p03_s264_aia_no_standalone_materialization` | s264_aia | OOS anchor has positive net but DD watch remains and it is not the most stable aggressive branch(표본외 앵커는 양수지만 손실폭 관찰이 남고 공격형 분기에서 가장 안정적이지 않음) | reopen only if primary/stress follow-ups fail or control contrast is required(주/압박 후속 실패 또는 대조 필요 때만 재개) |

## Worst Negative Slices(최악 음수 구간)

| candidate(후보) | period(기간) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | DD%(손실폭 %) |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `s258_stc` | `2025H2` | `close_hour_report` | `22` | 5 | -66.79 | 15.596384 |
| `s258_stc` | `2025H2` | `session_report` | `session_21_23_report_time` | 11 | -62.63 | 16.159641 |
| `s264_aih` | `2025H2` | `close_hour_report` | `22` | 4 | -46.54 | 11.651015 |
| `s264_aia` | `2025H2` | `close_hour_report` | `22` | 4 | -45.77 | 11.500994 |
| `s264_aih` | `2025H2` | `session_report` | `session_21_23_report_time` | 10 | -43.34 | 12.39977 |
| `s264_aia` | `2025H2` | `session_report` | `session_21_23_report_time` | 10 | -42.63 | 12.263572 |
| `s264_aia` | `2025H1` | `close_hour_report` | `21` | 19 | -14.07 | 7.236712 |
| `s264_aih` | `2025H1` | `close_hour_report` | `21` | 19 | -14.06 | 7.236712 |

## Boundary(경계)

- run267BZ(267BZ 실행)는 design-only(설계 전용) 증거다.
- selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 없다.
- 다음은 run267CA(267CA 실행) 물질화이며, 그 뒤 MT5(MetaTrader 5, 메타트레이더5) 실행과 거래 품질 검토가 필요하다.
- 같은 약점만 계속 깎는 수리 루프는 금지하며, 한 번 더 실행 후 살릴지 버릴지 판단한다.

## Artifacts(산출물)

- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BZ/aggressive_impulse_dd_shape_cross_period_followup_or_prune_design/branch_decision_matrix.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BZ/aggressive_impulse_dd_shape_cross_period_followup_or_prune_design/materialization_queue.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BZ/aggressive_impulse_dd_shape_cross_period_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BZ/aggressive_impulse_dd_shape_cross_period_followup_or_prune_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BZ/aggressive_impulse_dd_shape_cross_period_followup_or_prune_design/experiment_design_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BZ/aggressive_impulse_dd_shape_cross_period_followup_or_prune_design/result_judgment.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BZ/aggressive_impulse_dd_shape_cross_period_followup_or_prune_design/lineage.json`
- next_action(다음 행동): `run267CA_materialize_aggressive_impulse_dd_shape_followup_queue`
