# run364AZ density restore scout review(364AZ 밀도 복원 스카우트 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AY_train_threshold_edge_density_restore_cost_session_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1`
- judgment(판정): `no_package_eligible_proxy_stress_pass_positive_clue_open_ba_materialization_no_authority`
- package_decision(패키지 결정): `not_opened_no_package_eligible_rows`
- review_package_eligible_rows(검토 패키지 가능 행): `0`
- selected_positive_clue(선택 긍정 단서): `ax03_short_restore_ps450_floor050_stress` PF `1.3019773488`, estimated MT5 density(추정 MT5 밀도) `3.012012012`
- BA queue rows(BA 대기열 행): `6`
- runtime_authority(런타임 권위): `not_claimed`

## Surface Review(표면 검토)

| queue_rank | queue_id | review_status | combined_profit_factor | estimated_mt5_trade_per_business_day | combined_net_profit | combined_max_drawdown | combined_short_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | ax08_density_overstress_floor000 | positive_clue_stress_not_package(긍정 단서, 압박이라 패키지 아님) | 1.2724135667 | 3.1981981982 | 858.662 | -168.999 | 127 |
| 3 | ax03_short_restore_ps450_floor050_stress | positive_clue_stress_not_package(긍정 단서, 압박이라 패키지 아님) | 1.3019773488 | 3.012012012 | 874.129 | -132.758 | 103 |
| 1 | ax01_density_buffer_floor075_controlled_expand | fail_density_survival(밀도 생존 실패) | 1.3114889692 | 2.9369369369 | 869.181 | -121.708 | 87 |
| 2 | ax02_short_restore_ps452_floor075 | fail_density_survival(밀도 생존 실패) | 1.2938301494 | 2.963963964 | 833.793 | -143.158 | 97 |
| 5 | ax05_sep_dec_stress_label_no_delete | diagnostic_positive_not_package(진단 긍정, 패키지 아님) | 1.2910832467 | 3.024024024 | 850.315 | -150.182 | 118 |
| 7 | ax07_floor001_parent_control | fail_density_survival(밀도 생존 실패) | 1.3105654109 | 2.9159159159 | 862.283 | -133.571 | 87 |

## Positive Clues(긍정 단서)

| clue_id | source_queue_id | profit_factor | estimated_mt5_density | drawdown | use_as |
| --- | --- | --- | --- | --- | --- |
| positive_ax08_density_overstress_floor000 | ax08_density_overstress_floor000 | 1.2724135667 | 3.1981981982 | -168.999 | BA materialization seed(BA 물질화 씨앗) |
| positive_ax03_short_restore_ps450_floor050_stress | ax03_short_restore_ps450_floor050_stress | 1.3019773488 | 3.012012012 | -132.758 | BA materialization seed(BA 물질화 씨앗) |
| positive_ax05_sep_dec_stress_label_no_delete | ax05_sep_dec_stress_label_no_delete | 1.2910832467 | 3.024024024 | -150.182 | BA materialization seed(BA 물질화 씨앗) |

## Failure Memory(실패 기억)

| failure_id | failure_type | evidence | constraint_for_next |
| --- | --- | --- | --- |
| density_survival_ax01_density_buffer_floor075_controlled_expand | estimated_mt5_density_below_floor(추정 MT5 밀도 하한 미달) | estimated_density=2.9369369369;pf=1.3114889692 | BA queue must preserve density buffer above 3/day after AW survival ratio(BA 대기열은 AW 생존비 적용 뒤 3/day 완충을 유지해야 함) |
| density_survival_ax02_short_restore_ps452_floor075 | estimated_mt5_density_below_floor(추정 MT5 밀도 하한 미달) | estimated_density=2.963963964;pf=1.2938301494 | BA queue must preserve density buffer above 3/day after AW survival ratio(BA 대기열은 AW 생존비 적용 뒤 3/day 완충을 유지해야 함) |
| density_survival_ax07_floor001_parent_control | estimated_mt5_density_below_floor(추정 MT5 밀도 하한 미달) | estimated_density=2.9159159159;pf=1.3105654109 | BA queue must preserve density buffer above 3/day after AW survival ratio(BA 대기열은 AW 생존비 적용 뒤 3/day 완충을 유지해야 함) |
| no_package_eligible_rows | package_eligible_zero(패키지 가능 행 0) | AY package_eligible_rows=0 | do not create MT5 package until stress clue is re-materialized as candidate(압박 단서가 후보로 재물질화되기 전 MT5 패키지 금지) |
| implementation_required_rows_visible | proxy_cannot_execute_new_runtime_guards(프록시가 새 런타임 가드를 실행하지 못함) | skipped_implementation_required_rows=2 | runtime/proxy policy implementation must be explicit before package(패키지 전 런타임/프록시 정책 구현 명시 필요) |
| weak_month_side_buckets | sep_dec_and_long_tail_stress_visible(9/12월 및 롱 꼬리 압박 가시화) | 2025-12 long=-83.865; 2025-09 short=-23.864; 2025-07 long=-24.465 | soft stress labels only; no hard month deletion without MT5 evidence(부드러운 압박 라벨만, MT5 근거 없는 월 강제 삭제 금지) |

## Next Queue(다음 대기열)

| queue_rank | queue_id | axis_id | short_probability_threshold | entry_margin_floor | implementation_required | expected_effect |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ba01_ax03_stress_to_candidate_floor050_ps450 | stress_to_candidate(압박 후보를 후보로 전환) | 0.45 | 0.0005 | no | convert strongest PF/density stress pass into candidate review seed(가장 강한 PF/밀도 압박 통과를 후보 검토 씨앗으로 전환) |
| 2 | ba02_between_ax03_ax08_floor025_ps450 | density_buffer_midpoint(밀도 완충 중간점) | 0.45 | 0.00025 | no | search between ax03 density safety and ax08 over-stress buffer(ax03 밀도 안전과 ax08 과압박 완충 사이 탐색) |
| 3 | ba03_short_balance_ps448_floor050 | short_balance_offense(숏 균형 공격) | 0.448 | 0.0005 | no | test slightly lower short threshold while keeping floor050(하한 0.00050을 유지하며 숏 임계값을 더 낮춤) |
| 4 | ba04_candidate_floor075_density_rescue_ps450 | candidate_density_rescue(후보 밀도 구조) | 0.45 | 0.00075 | no | borrow ax01 PF discipline but add short threshold density rescue(ax01 PF 규율에 숏 임계값 밀도 복원을 더함) |
| 5 | ba05_hour18_19_margin_guard_implementation_seed | runtime_policy_implementation_seed(런타임 정책 구현 씨앗) | 0.45 | 0.00025 | yes_runtime_policy_hour18_19_margin_guard(18/19시 마진 가드 런타임 정책 필요) | make skipped ax04 explicit implementation work before package(ax04 건너뜀을 패키지 전 구현 작업으로 명시) |
| 6 | ba06_tail_dd_guard_diagnostic_seed | equity_tail_diagnostic_seed(수익곡선 꼬리 진단 씨앗) | 0.45 | 0.00025 | yes_account_state_guard_not_proxy_only(계정 상태 가드는 프록시만으로 불가) | carry ax06 tail risk as diagnostic not hidden runtime filter(ax06 꼬리 위험을 숨은 런타임 필터가 아니라 진단으로 유지) |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AZ/ay_surface_review.csv | AY surface(AY 표면)의 net/PF/density/DD(순수익/수익 팩터/밀도/낙폭)를 검토한다. |
| row_grain_audit(행 단위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AZ/ay_surface_review.csv | AY scout row(스카우트 행) 단위로 판정을 남긴다. |
| source_authority_audit(원천 권위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AY/final_decision.json | AY final decision(최종 결정)을 부모 원천으로 고정한다. |
| package_decision_gate(패키지 결정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AZ/package_decision.csv | package_eligible_rows=0이면 MT5 package(MT5 패키지)를 열지 않는다. |
| positive_clue_gate(긍정 단서 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AZ/positive_clues.csv | 압박 통과 단서를 BA materialization(BA 물질화) 씨앗으로 분리한다. |
| failure_memory_gate(실패 기억 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AZ/failure_memory.csv | 밀도 하한 실패와 구현 필요 행을 다음 제약으로 남긴다. |
| next_queue_gate(다음 대기열 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AZ/run364BA_materialization_queue.csv | BA materialization queue(BA 물질화 대기열)를 만든다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AZ/required_gate_coverage_audit.csv | work packet(작업 묶음)의 필수 게이트를 closeout(종료 기록)에 연결한다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AZ/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), goal achieve(목표 달성)를 주장하지 않는다. |

## Claim Boundary(주장 경계)

`research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): AZ는 AY stress pass(AY 압박 통과)를 MT5 package(MT5 패키지)가 아니라 BA materialization(BA 물질화) 입력으로 바꿔 Stage364(364단계)를 계속 밀고 간다.
