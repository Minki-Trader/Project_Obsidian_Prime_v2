# Stage267 Run267DG Shared Weakness Second Follow-up/Prune Design(267단계 267DG 공유 약점 2차 후속/가지치기 설계)

- status(상태): `run267DG_shared_weakness_breakout_second_followup_or_prune_design_completed`
- source_run(원천 실행): `run267DF_stage267_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review_v1`
- branch_decisions(분기 판단): `5`
- materialization_queue(물질화 대기열): `6`
- prune_rows(가지치기 행): `6`
- failure_memory(실패 기억): `6`
- next_action(다음 행동): `run267DH_materialize_shared_weakness_breakout_second_followup_or_prune_queue`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DF는 후보를 바로 고르라는 결과가 아니었다. s264_aia는 가장 다시 밀어볼 생존 단서지만 세션/월 구멍이 남았고, s262_lih는 방어 대조로 쓸 만하지만 최종 후보는 아니다. s258_stc는 인접 기간 수익이 좋지만 거래 수가 얇다. s264_lc는 수익은 좋아도 DD(drawdown, 손실폭)와 Monday(월요일)가 불편하고, s264_aih는 현재 파괴형 경로를 가지치기한다.

## Branch Decisions(분기 판단)

| candidate(후보) | label(판정) | next_use(다음 사용) | weakest_slice(가장 약한 구간) |
|---|---|---|---|
| `s264_aia` | `survivor_adapter_watch_no_selection(생존 어댑터 관찰, 선택 아님)` | P0 cross-period ablation/replacement survivor gate(P0 확장 기간 제거/대체 생존 게이트) | `session_report:session_07_12_report_time:-128.9` |
| `s262_lih` | `validation_heavy_guardrail_no_selection(검증 중심 가드레일, 선택 아님)` | P0/P1 defensive guardrail crosscheck(방어 가드레일 교차 확인) | `weekday:Monday:-135.08` |
| `s258_stc` | `thin_supply_stress_watch_no_selection(얇은 공급 압박 관찰, 선택 아님)` | P1 impulse supply stress only(P1 충격 공급 압박 전용) | `supply_thin_period:2025H2_trades_167:589.68` |
| `s264_lc` | `profit_with_dd_deescalation_no_selection(수익은 있으나 손실폭 강등, 선택 아님)` | P1 weekday/DD de-escalation audit(P1 요일/손실폭 강등 감사) | `weekday:Monday:-235.05` |
| `s264_aih` | `failed_destructive_prune_failure_memory(파괴형 가지치기 실패 기억)` | prune or rebuild only(가지치기 또는 재구축만) | `month:2024-12:-59.74` |

## Materialization Queue(물질화 대기열)

| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) |
|---|---|---|---|
| `dg_q01_s264_aia_survivor_replacement_ablation_cross_period` | `P0_survivor_adapter_watch(P0 생존 어댑터 관찰)` | `s264_aia` | `s264_aia_cross_period_replacement_ablation` |
| `dg_q02_s262_lih_validation_heavy_control_crosscheck` | `P0_control_guardrail(P0 대조 가드레일)` | `s262_lih` | `s262_lih_validation_guardrail` |
| `dg_q03_s258_stc_thin_supply_impulse_stress` | `P1_aggressive_stress(P1 공격 압박)` | `s258_stc` | `s258_thin_supply_impulse` |
| `dg_q04_s264_lc_weekday_dd_deescalation_control` | `P1_control_deescalation(P1 대조 강등)` | `s264_lc` | `s264_lc_weekday_dd` |
| `dg_q05_s264_aih_prune_or_rebuild_supply_gate` | `P0_destructive_prune(P0 파괴형 가지치기)` | `s264_aih` | `s264_aih_prune_or_rebuild` |
| `dg_q06_runtime_adapter_handoff_gap_for_survivors` | `P2_handoff_guardrail(P2 인계 가드레일)` | `s264_aia;s262_lih;s258_stc` | `adapter_handoff_receipts` |

## Prune Matrix(가지치기 행렬)

| prune(가지치기) | affected(영향 범위) | why(이유) |
|---|---|---|
| `dg_prune_headline_profit_selection` | `all candidates(전체 후보)` | run267DF의 좋은 net/PF(순수익/수익 팩터)만으로는 weak month/session/DD(약한 월/세션/손실폭)를 설명하지 못한다. |
| `dg_prune_s264_aih_current_destructive_path` | `s264_aih` | net=-59.74 PF=0.4933 trades=27로 destructive prune(파괴형 가지치기)가 실패했다. |
| `dg_prune_s264_lc_as_safe_control` | `s264_lc` | DD=24.39 and Monday=-235.05 are too uncomfortable for safe defensive control(안전 방어 대조). |
| `dg_prune_s258_adapter_candidate_before_supply` | `s258_stc` | adjacent-period profits exist, but trade count(거래 수) is still thin. |
| `dg_prune_calendar_only_weak_session_ban` | `weak month/weekday/session repairs(약한 월/요일/세션 수리)` | calendar-only ban(달력만 금지)은 시장 구조를 설명하지 않고 과적합 위험을 키운다. |
| `dg_prune_onnx_before_adapter_runtime_reproduction` | `all survivors(모든 생존 후보)` | Adapter structure(어댑터 구조), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)가 아직 없다. |

## Boundary(경계)

이 설계는 R&D racing(연구개발 경주)의 다음 실행 입력을 만드는 단계다. 선택 후보, 선택 연구 기준 후보, ONNX 준비, 목표 달성은 주장하지 않는다.

## Artifacts(산출물)

- feature_blueprint(피처 청사진): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DG/shared_weakness_breakout_second_followup_or_prune_design/feature_blueprint.csv`
- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DG/shared_weakness_breakout_second_followup_or_prune_design/branch_decision_matrix.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DG/shared_weakness_breakout_second_followup_or_prune_design/materialization_queue.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DG/shared_weakness_breakout_second_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DG/shared_weakness_breakout_second_followup_or_prune_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DG/shared_weakness_breakout_second_followup_or_prune_design/experiment_design_receipt.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DG/shared_weakness_breakout_second_followup_or_prune_design/gate_audit.csv`
