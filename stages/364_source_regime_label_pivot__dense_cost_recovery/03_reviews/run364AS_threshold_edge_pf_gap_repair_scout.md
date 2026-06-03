# run364AS threshold-edge PF gap repair scout(364AS 임계값 경계 PF 간극 수리 정찰)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AS_train_threshold_edge_pf_gap_repair_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AR_materialize_threshold_edge_pf_gap_repair_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run364AT_review_threshold_edge_pf_gap_repair_scout_without_db_v1`
- judgment(판정): `proxy_scout_completed_threshold_edge_pf_gap_repair_ranked_review_required_no_authority`
- scout_rows(정찰 행): `7`
- skipped_new_policy_rows(새 정책 건너뜀 행): `1`
- strict_pass_rows(엄격 통과 행): `1`
- selected_net/PF/density/DD(선택 순수익/PF/밀도/낙폭): `862.283` / `1.3105654109` / `3.1981981982` / `-133.571`
- runtime_authority(런타임 권위): `not_claimed`

## Surface(표면)

| queue_rank | queue_id | candidate_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침) | pass_proxy_pf_density_restore(PF/밀도 복원 프록시 통과) | 862.283 | 1.3105654109 | 3.1981981982 | -133.571 | 87 | 917.263304614 |
| 1 | threshold_edge_hold6_control(임계값 경계 6봉 대조) | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 840.779 | 1.2804442925 | 3.3843843844 | -147.924 | 87 | 849.817790125 |
| 7 | pf_pass_density_bridge_hold6_probe(PF 통과 밀도 연결 6봉 탐침) | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 765.45 | 1.2781248762 | 3.1861861862 | -157.864 | 7 | 752.98116953 |
| 2 | late_long_hold6_control(후반 롱 6봉 대조) | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 706.218 | 1.2520021924 | 3.0690690691 | -147.473 | 127 | 707.10767506 |
| 3 | threshold_edge_hold5_probe(임계값 경계 5봉 탐침) | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 588.663 | 1.1840210198 | 3.7717717718 | -169.6 | 91 | 628.999635846 |
| 6 | threshold_edge_late_long_blend_probe(임계값 경계 후반 롱 혼합 탐침) | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 606.277 | 1.2177465697 | 3.1411411411 | -143.346 | 96 | 580.245770305 |
| 4 | threshold_edge_hold4_probe(임계값 경계 4봉 탐침) | fail_split_profit(분할 수익 실패) | 361.57 | 1.1131824339 | 4.2672672673 | -213.135 | 97 | -173.719526069 |

## Threshold-Edge Comparison(임계값 경계 비교)

| metric_id | reference_value | selected_value | delta_selected_minus_reference |
| --- | --- | --- | --- |
| combined_net_profit | 840.779 | 862.283 | 21.504 |
| combined_profit_factor | 1.2804442925 | 1.3105654109 | 0.0301211184 |
| combined_trade_count | 1127.0 | 1065 | -62.0 |
| combined_trade_per_business_day | 3.3843843844 | 3.1981981982 | -0.1861861862 |
| combined_expectancy | 0.746032 | 0.8096553991 | 0.0636233991 |
| combined_max_drawdown | -147.924 | -133.571 | 14.353 |
| combined_recovery_factor | 5.683856 | 6.4556153656 | 0.7717593656 |
| combined_long_count | 1040.0 | 978 | -62.0 |
| combined_short_count | 87.0 | 87 | 0.0 |
| combined_long_short_balance |  | 0.0889570552 | 0.0889570552 |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| parent_materialization_gate(부모 구체화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AR/final_decision.json | AR materialization(구체화) 완료 확인 |
| queue_replay_gate(대기열 재생 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AS/threshold_edge_pf_gap_repair_proxy_scout_surface.csv | 실행 가능 queue(대기열) 행을 재생함 |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AS/queue_replay_audit.csv | top_n 사용 없음 |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AS/queue_replay_audit.csv | 거래 쪼개기 없음 |
| oos_threshold_lock_gate(표본외 임계값 잠금 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AR/run364AS_scout_queue.csv | 표본외 임계값 선택 금지 유지 |
| timestamp_boundary_gate(시점 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AR/run364AS_scout_queue.csv | 진입 시점에 알려진 값만 사용 |
| split_report_gate(분할 보고 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AS/threshold_edge_pf_gap_repair_proxy_scout_surface.csv | validation/OOS(검증/표본외) KPI를 분리 기록 |
| tier_ledger_gate(티어 장부 게이트) | passed | docs/registers/alpha_run_ledger.csv | Tier A/B/합산 장부 행을 기록 |
| claim_boundary_gate(주장 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AS/claim_boundary_receipt.json | 운영 주장 없음 |
| artifact_lineage_gate(산출물 계보 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AS/artifact_lineage_receipt.json | 입력/출력 해시를 기록 |

## Claim Boundary(주장 경계)

`research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): run364AS(364AS 실행)는 proxy scout(프록시 정찰)이며, package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.
