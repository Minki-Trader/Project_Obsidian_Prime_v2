# run364CC swap-stable reprobe and source guard inputs(364CC 스왑 안정 재탐침 및 원천 가드 입력)

## Result(결과)

Action(행동): CB review(CB 리뷰)의 trade path(거래 경로), gross/net/swap(총손익/순수익/스왑), set hash(설정 해시)를 읽어 CD MT5 runtime probe(CD MT5 런타임 탐침) 입력으로 materialize(구체화)했다.

Effect(효과): CA01과 BX3의 신호 경로가 같은지, 아니면 swap table(스왑 표)만 흔들렸는지 다음 실행에서 한 묶음으로 확인할 수 있게 됐다.

- status(상태): `completed_stage364CC_swap_stable_reprobe_and_source_guard_inputs_materialized_open_cd_no_authority`
- judgment(판정): `experiment_design_materialized_swap_stable_reprobe_and_source_guard_runtime_handoff_ready_no_authority`
- next(다음): `run364CD_execute_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db_v1`
- ready candidates(준비 후보): `3`
- gate(게이트): `7/7`

## Runtime Queue(런타임 대기열)

| candidate_id | runtime_priority | source_variant_id | synthetic_enabled | calendar_start_hour | calendar_end_hour | expected_net_anchor |
| --- | --- | --- | --- | --- | --- | --- |
| cd01_bx3_clone_current_session | 1 | bx03_hour17_overlay_plus_weak_late_session_firewall | True | 21 | 23 | 1008.18 |
| cd02_ca01_clone_current_session | 2 | ca01_bx03_semantics_control | True | 21 | 23 | 997.49 |
| cd03_native_short_same_calendar_current_session | 3 | ca06_native_short_same_calendar_control | False | 21 | 23 | 956.4 |

## Same-Session Pairs(동일 세션 쌍)

| pair_id | left_candidate_id | right_candidate_id | prior_swap_delta | success_condition |
| --- | --- | --- | --- | --- |
| cd01_vs_cd02_swap_stability_control | cd02_ca01_clone_current_session | cd01_bx3_clone_current_session | -10.69 | same trade path and abs(swap/net delta) <= 1.00(동일 거래 경로 및 스왑/순수익 차이 절댓값 1.00 이하) |
| cd02_vs_cd03_source_overlay_value | cd02_ca01_clone_current_session | cd03_native_short_same_calendar_current_session | 0.0 | h17 synthetic overlay keeps positive net lift against native short control(17시 합성 오버레이가 기본 숏 대조 대비 순수익 우위 유지) |

## Swap-Neutral Surface(스왑 중립 표면)

| variant_id | net_profit | gross_profit | swap | swap_neutral_score | net_rank_role |
| --- | --- | --- | --- | --- | --- |
| bx03_hour17_overlay_plus_weak_late_session_firewall | 1008.18 | 1002.63 | 5.55 | 1002.63 | use_only_after_same_session_cost_check(동일 세션 비용 확인 뒤 사용) |
| ca01_bx03_semantics_control | 997.49 | 1002.63 | -5.14 | 1002.63 | use_only_after_same_session_cost_check(동일 세션 비용 확인 뒤 사용) |
| ca02_december_h22_only_long_block_isolation | 989.62 | 994.88 | -5.26 | 994.88 | use_only_after_same_session_cost_check(동일 세션 비용 확인 뒤 사용) |
| ca03_december_h21_h23_long_block_stress | 997.49 | 1002.63 | -5.14 | 1002.63 | use_only_after_same_session_cost_check(동일 세션 비용 확인 뒤 사용) |
| ca06_native_short_same_calendar_control | 956.4 | 961.54 | -5.14 | 961.54 | use_only_after_same_session_cost_check(동일 세션 비용 확인 뒤 사용) |

## Source Guard(원천 가드)

| guard_id | guard_type | status | evidence |
| --- | --- | --- | --- |
| preserve_h17_synthetic_overlay_seed | source_guard_seed(원천 가드 씨앗) | materialized_for_reprobe(재탐침용 구체화) | CA01 vs CA06 net delta 41.09 |
| keep_h21_h22_december_long_block | calendar_constraint(달력 제약) | kept_as_failure_memory(실패 기억으로 유지) | h22-only isolation added 4 trades and net -7.87 |
| separate_gross_net_swap_layers | score_guard(점수 가드) | materialized_for_review(리뷰용 구체화) | CA01 vs BX3 gross delta 0.0 and swap delta -10.69 |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| work_packet_schema_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CC/work_packet.json | primary family and required gates are explicit(주 작업군과 필수 게이트 명시) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CC/input_manifest.csv | CB evidence and source sets are connected(CB 근거와 원천 설정 연결) |
| same_session_reprobe_design_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CC/same_session_reprobe_pair_matrix.csv | swap drift can be isolated in one MT5 batch(스왑 드리프트를 한 MT5 묶음에서 분리 가능) |
| source_guard_design_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CC/source_guard_candidate_matrix.csv | offensive h17 source clue is preserved(공격적 17시 원천 단서 유지) |
| runtime_handoff_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CC/run364CD_runtime_attempt_queue.csv | CD has exactly three default runtime attempts(CD 기본 런타임 시도 3개 고정) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CC/required_gate_coverage_audit.csv | receipts and gates are linked(영수증과 게이트 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CC/claim_boundary_receipt.json | no runtime authority or operating promotion is claimed(런타임 권위나 운영 승격 주장 없음) |

## Boundary(경계)

CC는 input materialization(입력 구체화)만 주장한다. 새 MT5 execution(MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
