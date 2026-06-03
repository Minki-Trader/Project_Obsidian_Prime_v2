# run364AO hold6 PF/DD repair inputs(364AO 6봉 PF/DD 수리 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AP_train_hold6_pf_dd_repair_offensive_scout_without_db_v1`
- judgment(판정): `hold6_pf_dd_repair_inputs_ready_with_loss_guard_as_diagnostic_no_authority`
- AP queue rows(AP 대기열 행): `8`
- control/candidate/guardrail(대조/후보/가드레일): `2` / `5` / `1`
- implementation_required_rows(구현 필요 행): `1`
- top_n_rows(top_n 행): `0`
- trade_splitting_rows(거래 쪼개기 행): `0`
- runtime_authority(런타임 권위): `not_claimed`

## Queue(대기열)

| queue_rank | queue_id | queue_type | seed_profit_factor | seed_trade_per_business_day | seed_max_drawdown | entry_margin_floor | max_hold_m5 | target_repair | implementation_required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | hold6_density_anchor_control(6봉 밀도 기준 대조) | control(대조) | 1.2724135667 | 3.5075075075 | -168.999 | 0.0 | 6 | preserve density>=3 while measuring PF/DD(PF/DD 측정 중 밀도 3 이상 보존) | no |
| 2 | sparse_pf_pass_anchor_control(희소 PF 통과 대조) | control(대조) | 1.3287468527 | 2.6636636637 | -120.303 | 0.0 | 8 | preserve PF>=1.30 while measuring density gap(PF 1.30 이상 보존 중 밀도 간극 측정) | no |
| 3 | threshold_edge_hold6_density_repair(임계값 경계 6봉 밀도 수리) | candidate(후보) | 1.2670836468 | 2.9039039039 | -133.361 | 0.0 | 6 | recover density while keeping DD improvement(낙폭 개선을 유지하며 밀도 회복) | no |
| 4 | late_long_hold6_pf_patch(후반 롱 6봉 PF 패치) | candidate(후보) | 1.3287468527 | 2.6636636637 | -120.303 | 0.0 | 6 | add density without PF collapse(PF 붕괴 없이 밀도 추가) | no |
| 5 | soft_margin_floor_0_003(소프트 마진 하한 0.003) | candidate(후보) | 1.2724135667 | 3.5075075075 | -168.999 | 0.003 | 6 | raise PF and reduce DD without overfilter(PF 상승과 낙폭 축소, 과필터 방지) | no |
| 6 | soft_margin_floor_0_006(소프트 마진 하한 0.006) | candidate(후보) | 1.2724135667 | 3.5075075075 | -168.999 | 0.006 | 6 | raise PF and reduce DD without overfilter(PF 상승과 낙폭 축소, 과필터 방지) | no |
| 7 | loss_cluster_session_guard(손실 클러스터 세션 가드) | candidate(후보) | 1.2724135667 | 3.5075075075 | -168.999 | 0.0 | 6 | repair DD without top_n or month-only overfit(top_n 또는 월 단독 과적합 없이 낙폭 수리) | yes |
| 8 | pf_pass_density_bridge_no_split_guard(PF 통과 밀도 연결 무분할 가드) | guardrail(가드레일) | 1.3287468527 | 2.6636636637 | -120.303 | 0.0 | 8 | keep next scout honest(다음 정찰을 정직하게 유지) | no |

## DD Guardrail(낙폭 가드)

| guardrail_rank | observed_scope | segment_net_profit | segment_profit_factor | allowed_use | forbidden |
| --- | --- | --- | --- | --- | --- |
| 1 | 2025-12 long | -83.865 | 0.602128245 | diagnostic_only_no_month_hard_filter(진단 전용, 월 고정 필터 금지) | top_n, trade_splitting, hard month-only filtering(top_n, 거래 쪼개기, 월 단독 고정 필터) |
| 2 | 2025-07 long | -24.465 | 0.7269927354 | diagnostic_only_no_month_hard_filter(진단 전용, 월 고정 필터 금지) | top_n, trade_splitting, hard month-only filtering(top_n, 거래 쪼개기, 월 단독 고정 필터) |
| 3 | 2025-10 long | -15.476 | 0.9217751719 | diagnostic_only_no_month_hard_filter(진단 전용, 월 고정 필터 금지) | top_n, trade_splitting, hard month-only filtering(top_n, 거래 쪼개기, 월 단독 고정 필터) |
| 4 | 2025-08 long | -5.53 | 0.9558169078 | diagnostic_only_no_month_hard_filter(진단 전용, 월 고정 필터 금지) | top_n, trade_splitting, hard month-only filtering(top_n, 거래 쪼개기, 월 단독 고정 필터) |
| 5 | 2026-04 long | -2.325 | 0.980325788 | diagnostic_only_no_month_hard_filter(진단 전용, 월 고정 필터 금지) | top_n, trade_splitting, hard month-only filtering(top_n, 거래 쪼개기, 월 단독 고정 필터) |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/final_decision.json | run364AO materialization(364AO 구체화)을 완료했다. |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/input_manifest.csv | run364AN review(364AN 검토)와 대기열을 확인했다. |
| queue_materialization_gate(대기열 구체화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/run364AP_scout_queue.csv | run364AP scout queue(364AP 정찰 대기열)를 만들었다. |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/run364AP_scout_queue.csv | 모든 row(행)에 top_n forbidden(금지)을 기록했다. |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/run364AP_scout_queue.csv | 모든 row(행)에 거래 쪼개기 없음 상태를 기록했다. |
| timestamp_boundary_gate(시점 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/data_integrity_receipt.json | 진입 시점에 알려진 값만 사용하도록 경계를 기록했다. |
| dd_guardrail_gate(낙폭 가드 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/dd_guardrail_design.csv | 손실 클러스터를 진단 전용으로 묶었다. |
| experiment_design_gate(실험 설계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/experiment_design_receipt.json | 가설, 성공/실패 조건, 금지를 기록했다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/artifact_lineage_receipt.json | 입력/출력 hash(해시)를 연결했다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/claim_boundary_receipt.json | 운영 승격과 런타임 권위를 주장하지 않았다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AO/required_gate_coverage_audit.csv | 필수 gate(게이트)를 종료 기록에 연결했다. |

## Claim Boundary(주장 경계)

`research_development_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): run364AO(364AO 실행)는 run364AP(364AP 실행) 입력만 만들며, package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.
