# run364AN PF-pass density restore offensive review(364AN PF 통과 밀도 복원 공격 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AM_train_pf_pass_density_restore_offensive_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1`
- judgment(판정): `negative_for_package_positive_for_hold6_density_and_sparse_pf_repair_seed_no_authority`
- package_candidate_rows(패키지 후보 행): `0`
- selected net/PF/trades/density/expectancy/DD/RF(선택 순수익/수익 팩터/거래수/밀도/기대값/낙폭/회복 계수): `858.662` / `1.2724135667` / `1168` / `3.5075075075` / `0.7351558219` / `-168.999` / `5.080870301`
- runtime_authority(런타임 권위): `not_claimed`

## Review Surface(검토 표면)

| queue_id | review_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count |
| --- | --- | --- | --- | --- | --- | --- |
| density_anchor_hold6_pf_probe(밀도 기준 보유6 PF 탐침) | density_safe_pf_dd_fail(밀도 안전, PF/DD 실패) | 858.662 | 1.2724135667 | 3.5075075075 | -168.999 | 127.0 |
| pfpass_core_short_restore_budget_010(PF통과 핵심 숏 0.10 복원) | pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6.0 |
| pfpass_guardrail_no_trade_split(PF통과 거래쪼개기 금지 가드) | pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6.0 |
| pfpass_late_long_density_patch(PF통과 후반 롱 밀도 패치) | pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗) | 810.666 | 1.310783255 | 2.6696696697 | -120.303 | 6.0 |
| pfpass_month_pocket_observation(PF통과 월 포켓 관찰) | pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗) | 799.943 | 1.3066323163 | 2.6726726727 | -120.303 | 8.0 |
| density_anchor_short0455_edge(밀도 기준 숏0.455 경계) | near_density_dd_improved_seed(밀도 근접, 낙폭 개선 씨앗) | 789.589 | 1.2670836468 | 2.9039039039 | -133.361 | 86.0 |
| control_replay_density_anchor(대조 재생 밀도 기준점) | density_safe_pf_fail(밀도 안전, PF 실패) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119.0 |
| dd_seed_density_restore_core_late(낙폭 씨앗 핵심후반 밀도 복원) | reject_or_watch(거절 또는 관찰) | 688.499 | 1.2534558955 | 2.7807807808 | -128.108 | 109.0 |

## Package Gate(패키지 게이트)

| gate_id | status | observed | required | effect |
| --- | --- | --- | --- | --- |
| strict_package_rows(엄격 패키지 행) | failed | 0 | 1 | PF, density, split, side 조건을 동시에 만족하지 못해 package(패키지)를 닫는다. |
| selected_profit_factor_target(선택 PF 목표) | failed | 1.2724135667 | 1.3 | 선택 후보의 PF(수익 팩터)가 목표 아래라 운영 후보가 아니다. |
| selected_density_floor(선택 밀도 하한) | passed | 3.5075075075 | 3.0 | 밀도 회복 단서는 보존한다. |
| selected_drawdown_quality(선택 낙폭 품질) | failed | -168.999 | >= -142.323 reference(기준 이상) | hold6(6봉 보유)는 낙폭을 악화시켜 DD(낙폭) 수리 축이 필요하다. |
| selected_split_profit(선택 분할 수익) | passed | validation=428.254; oos=430.408 | both_positive(둘 다 양수) | 분할 수익은 살아 있어 아이디어 사망이 아니라 수리 단서로 남긴다. |
| external_runtime_evidence(외부 런타임 근거) | out_of_scope_by_claim(주장 범위 밖) | not_run(미실행) | MT5 runtime probe(MT5 런타임 탐침) | 이번 review(검토)를 runtime authority(런타임 권위)로 오해하지 않게 한다. |

## Positive Clues(긍정 단서)

| clue_id | evidence | kpi_read | salvage_value |
| --- | --- | --- | --- |
| hold6_density_net_lift_seed(6봉 보유 밀도/순수익 상승 씨앗) | density_anchor_hold6_pf_probe(밀도 기준 보유6 PF 탐침) | net=858.662; pf=1.2724135667; density=3.5075075075; dd=-168.999 | density and net lift survived; PF/DD repair needed(밀도와 순수익 상승은 생존, PF/DD 수리 필요) |
| sparse_pf_pass_dd_quality_seed(희소 PF 통과/DD 품질 씨앗) | pfpass_core_short_restore_budget_010(PF통과 핵심 숏 0.10 복원) | net=845.554; pf=1.3287468527; density=2.6636636637; dd=-120.303 | PF and DD quality exist, but density bridge failed(PF와 DD 품질은 있으나 밀도 연결 실패) |
| threshold_edge_near_density_dd_seed(임계값 경계 밀도 근접/DD 개선 씨앗) | density_anchor_short0455_edge(밀도 기준 숏0.455 경계) | net=789.589; pf=1.2670836468; density=2.9039039039; dd=-133.361 | short threshold edge improved DD and stayed near 3/day(숏 임계값 경계가 DD를 개선하고 하루 3회에 근접) |

## Failure Memory(실패 기억)

| failure_id | failed_boundary | why_failed | do_not_repeat |
| --- | --- | --- | --- |
| strict_package_zero(엄격 패키지 0) | PF>=1.30 and density>=3/day and split profit(PF 1.30 이상, 하루 3회 이상, 분할 수익) | PF-pass rows lost density; density-safe rows stayed below PF target(PF 통과 행은 밀도 상실, 밀도 안전 행은 PF 목표 미달) | do not call hold6 net lift a package without PF/DD repair(hold6 순수익 상승을 PF/DD 수리 없이 패키지로 부르지 않음) |
| hold6_pf_dd_degradation(hold6 PF/DD 악화) | quality trade shape(품질 거래 형태) | PF=1.2724135667 and DD=-168.999 worsened against reference(PF와 DD가 기준 대비 악화) | do not increase density by simply shortening hold without loss-cluster guard(손실 클러스터 가드 없이 보유만 줄여 밀도만 올리지 않음) |
| margin_floor_overfilter(마진 하한 과필터) | density restore(밀도 복원) | floor 0.12 and 0.02 removed too many signals(0.12와 0.02 하한이 신호를 과도하게 제거) | do not jump to large entry_margin_floor values(큰 마진 하한으로 바로 뛰지 않음) |

## Next Queue(다음 대기열)

| queue_rank | queue_id | queue_type | materialization_question | expected_effect |
| --- | --- | --- | --- | --- |
| 1 | hold6_density_anchor_control | control | replay selected hold6 density anchor(선택 hold6 밀도 기준 재생) | hold density>=3 while repairing PF/DD(PF/DD 수리 중 밀도 3 이상 유지) |
| 2 | sparse_pf_pass_anchor_control | control | replay sparse PF-pass anchor(희소 PF 통과 기준 재생) | preserve PF>=1.30 while adding density bridge(PF 1.30 이상 보존 후 밀도 연결) |
| 3 | threshold_edge_hold6_density_repair | candidate | combine short 0.455 edge with hold6(숏 0.455 경계와 hold6 결합) | recover density while keeping DD improvement(DD 개선을 유지하며 밀도 회복) |
| 4 | late_long_hold6_pf_patch | candidate | combine late-long PF patch with hold6(후반 롱 PF 패치와 hold6 결합) | test whether hold6 adds density without PF collapse(hold6가 PF 붕괴 없이 밀도 추가하는지 시험) |
| 5 | soft_margin_floor_micro_sweep | candidate | try floor 0.003/0.006 only(하한 0.003/0.006만 시험) | avoid previous overfilter while removing worst low-margin trades(이전 과필터를 피하며 최악 저마진 거래 제거) |
| 6 | loss_cluster_session_guard | candidate | review selected tape loss clusters by session/month(선택 테이프 손실 클러스터를 세션/월별 검토) | repair DD without top_n or trade splitting(top_n/거래 쪼개기 없이 DD 수리) |
| 7 | pf_pass_density_bridge_no_split_guard | guardrail | no top_n no trade splitting row grain guard(top_n 없음, 거래 쪼개기 없음 행 단위 가드) | keep next scout honest(다음 정찰을 정직하게 유지) |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AN/surface_review.csv | net/PF/expectancy/DD/RF/trades/density를 검토 |
| row_grain_audit(행 단위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AN/package_gate_audit.csv | top_n(상위 N개)과 거래 쪼개기 없이 행 단위 판정 |
| source_authority_audit(원천 권위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AN/input_manifest.csv | 부모 run364AM(364AM 실행) 산출물만 원천으로 사용 |
| package_gate_audit(패키지 게이트 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AN/package_gate_audit.csv | strict package(엄격 패키지) 없음 확인 |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AN/performance_attribution_receipt.json | hold6와 PF-pass 실패 원인 분리 |
| result_judgment_gate(결과 판정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AN/result_judgment_receipt.json | negative_for_package(패키지 부정)와 positive_seed(긍정 씨앗) 경계 기록 |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AN/artifact_lineage_receipt.json | 입력/출력 해시 연결 |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AN/claim_boundary_receipt.json | 런타임 권위 주장 없음 |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AN/required_gate_coverage_audit.csv | 필수 게이트를 종료 기록에 연결 |

## Claim Boundary(주장 경계)

`research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): package(패키지)는 닫고, hold6 density(6봉 보유 밀도)와 sparse PF(희소 수익 팩터) 단서를 다음 materialization(구체화)으로 넘긴다.
