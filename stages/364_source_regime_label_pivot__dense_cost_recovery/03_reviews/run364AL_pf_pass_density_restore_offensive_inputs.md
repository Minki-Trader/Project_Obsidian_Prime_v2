# run364AL PF-pass density restore offensive inputs(364AL PF 통과 밀도 복원 공격 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AK_review_session_side_pf_lift_density_repair_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AM_train_pf_pass_density_restore_offensive_scout_without_db_v1`
- judgment(판정): `pf_pass_density_restore_offensive_inputs_ready_no_operating_claim`
- queue_rows(대기열 행): `12`
- control/candidate/observation(대조/후보/관찰): `2` / `9` / `1`
- top_n_rows(top_n 행): `0`
- trade_splitting_rows(거래 쪼개기 행): `0`
- runtime_authority(런타임 권위): `not_claimed`

## Density Profile(밀도 프로필)

| profile_id | source | profit_factor | density | drawdown | effect(효과) |
| --- | --- | --- | --- | --- | --- |
| selected_density_anchor(선택 밀도 기준) | selected_control_full_session_선택_대조_전체_세션__ps0_45__floor0_0__hold8 | 1.2739357721 | 3.006006006 | -142.323 | density(밀도)는 유지되지만 PF(수익 팩터)가 목표 아래라 공격 수리 기준으로 쓴다. |
| pf_pass_density_fail_seed(PF 통과 밀도 실패 씨앗) | pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8; pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8; pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8; pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8; pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8; pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8; pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8 | 1.3287468527; 1.3287468527; 1.3287468527; 1.3287468527; 1.3287468527; 1.3287468527; 1.3287468527 | 2.6636636637; 2.6636636637; 2.6636636637; 2.6636636637; 2.6636636637; 2.6636636637; 2.6636636637 | -120.303; -120.303; -120.303; -120.303; -120.303; -120.303; -120.303 | PF(수익 팩터) 통과 씨앗을 density restore(밀도 복원) 대상으로 고정한다. |
| control_and_observation_rows(대조 및 관찰 행) | control_replay_density_anchor(대조 재생 밀도 기준점); density_anchor_pf_floor_012(밀도 기준 PF 하한 0.12); density_anchor_hold6_pf_probe(밀도 기준 보유6 PF 탐침); density_anchor_short0455_edge(밀도 기준 숏0.455 경계) |  |  |  | control(대조)과 observation(관찰)을 후보와 섞어 승격하지 않게 한다. |

## Materialized Queue(구체화 대기열)

| queue_rank | queue_id | queue_type | seed_profit_factor | seed_trade_per_business_day | density_restore_budget | materialized_policy |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | control_replay_density_anchor(대조 재생 밀도 기준점) | control(대조) | 1.2739357721 | 3.006006006 | 0.0 | control_replay_density_anchor(대조 재생 밀도 기준) |
| 2 | pfpass_core_short_restore_budget_010(PF통과 핵심 숏 0.10 복원) | candidate(후보) | 1.3287468527 | 2.6636636637 | 0.1 | pf_pass_core_short_density_restore_budget_010(PF 통과 핵심 숏 밀도 복원 0.10) |
| 3 | pfpass_core_short_restore_budget_020(PF통과 핵심 숏 0.20 복원) | candidate(후보) | 1.3287468527 | 2.6636636637 | 0.2 | pf_pass_core_short_density_restore_budget_020(PF 통과 핵심 숏 밀도 복원 0.20) |
| 4 | pfpass_late_long_density_patch(PF통과 후반 롱 밀도 패치) | candidate(후보) | 1.3287468527 | 2.6636636637 | 0.16 | pf_pass_late_long_density_patch(PF 통과 후반 롱 밀도 패치) |
| 5 | pfpass_non_drag_session_restore(PF통과 비끌림 세션 복원) | candidate(후보) | 1.3287468527 | 2.6636636637 | 0.24 | pf_pass_non_drag_session_restore(PF 통과 비끌림 세션 복원) |
| 6 | density_anchor_pf_floor_012(밀도 기준 PF 하한 0.12) | candidate(후보) | 1.2739357721 | 3.006006006 | 0.04 | density_anchor_margin_floor_012(밀도 기준 마진 하한 0.12) |
| 7 | density_anchor_hold6_pf_probe(밀도 기준 보유6 PF 탐침) | candidate(후보) | 1.2739357721 | 3.006006006 | 0.0 | density_anchor_hold6_pf_probe(밀도 기준 보유 6 PF 탐침) |
| 8 | dd_seed_density_restore_core_late(낙폭 씨앗 핵심후반 밀도 복원) | candidate(후보) | 1.2958707973 | 2.6576576577 | 0.29 | dd_seed_core_late_density_restore(낙폭 씨앗 핵심/후반 밀도 복원) |
| 9 | pfpass_validation_balance_patch(PF통과 검증 균형 패치) | candidate(후보) | 1.3287468527 | 2.6636636637 | 0.18 | pf_pass_validation_balance_patch(PF 통과 검증 균형 패치) |
| 10 | pfpass_month_pocket_observation(PF통과 월 포켓 관찰) | observation(관찰) | 1.3287468527 | 2.6636636637 | 0.0 | month_pocket_observation_no_filter(월 포켓 관찰, 필터 아님) |
| 11 | density_anchor_short0455_edge(밀도 기준 숏0.455 경계) | candidate(후보) | 1.2739357721 | 3.006006006 | 0.0 | density_anchor_short0455_edge(밀도 기준 숏 0.455 경계) |
| 12 | pfpass_guardrail_no_trade_split(PF통과 거래쪼개기 금지 가드) | control(대조) | 1.3287468527 | 2.6636636637 | 0.0 | pf_pass_guardrail_no_trade_split(PF 통과 거래 쪼개기 금지 가드) |

## Guardrails(가드레일)

- top_n(상위 N개): `forbidden(금지)`
- trade_splitting(거래 쪼개기): `not_used(없음)`
- OOS threshold selection(표본외 임계값 선택): `forbidden(금지)`

## Gate Audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/final_decision.json | run364AL materialization(구체화)을 완료했다. |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/input_manifest.csv | run364AK 산출물과 queue(대기열)를 확인했다. |
| queue_materialization_gate(대기열 구체화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/run364AM_scout_queue.csv | run364AM scout queue(정찰 대기열)를 만들었다. |
| density_requirement_gate(밀도 요구 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/density_restore_profile.csv | density floor(밀도 하한) 3/day 기준을 명시했다. |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/run364AM_scout_queue.csv | top_n 금지를 모든 행에 기록했다. |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/run364AM_scout_queue.csv | 거래 쪼개기 없음 상태를 모든 행에 기록했다. |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/data_integrity_receipt.json | timestamp-safe(시점 안전) 경계를 기록했다. |
| experiment_design_gate(실험 설계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/experiment_design_receipt.json | 다음 scout(정찰)의 가설과 실패 조건을 기록했다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/artifact_lineage_receipt.json | 입력/출력 hash(해시)를 연결했다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/claim_boundary_receipt.json | 운영 승격을 주장하지 않았다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AL/required_gate_coverage_audit.csv | 필수 gate(게이트)를 종료 기록에 연결했다. |

## Claim Boundary(주장 경계)

`research_development_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): run364AL은 next scout(다음 정찰) 입력만 만들며 package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
