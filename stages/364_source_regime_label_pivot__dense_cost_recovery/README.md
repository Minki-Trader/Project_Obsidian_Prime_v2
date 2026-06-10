# 364_source_regime_label_pivot__dense_cost_recovery

Current run(현재 실행): `run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1`

Latest completed run(최근 완료 실행): `run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1`

Current truth(현재 진실): run364CN(364CN 실행)이 `cm04_cj09_month08_12_pair_guard`를 MT5 probe input(MT5 탐침 입력) 구체화 대상으로 열었습니다. Proxy KPI(프록시 핵심 성과 지표)는 net `1036.46`, PF `1.4281838362`, density `3.1050955414`, shorts `100`, bad months `0`입니다.

Next action(다음 행동): `run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1`에서 EA/set/model/tester handoff(EA/설정/모델/테스터 인계)를 구체화합니다.

## run364AA_train_density_side_balance_cost_session_stress_scout_without_db_v1

- action(행동): `run364Z` 대기열을 프록시 재생했다.
- effect(효과): 새 stage(단계) 분기 없이 Stage364(364단계)에서 PF/DD 수리를 계속한다.

## run364AB_review_density_side_balance_cost_session_stress_scout_without_db_v1

- action(행동): proxy scout review(프록시 정찰 검토)를 완료했다.
- effect(효과): Stage364(364단계) 분기 없이 run364AC(364AC 실행)로 PF/DD density bridge(PF/DD 밀도 연결)를 계속한다.

## run364AC_materialize_pf_dd_near_miss_density_bridge_without_db_v1

- action(행동): near-miss density bridge queue(근접 실패 밀도 연결 대기열)를 만들었다.
- effect(효과): stage branch(단계 분기) 없이 Stage364(364단계) 안에서 다음 scout(정찰)를 연다.

## run364AD_train_pf_dd_near_miss_density_bridge_scout_without_db_v1

- action(행동): timestamp-safe bridge scout(시점 안전 연결 정찰)를 완료했다.
- effect(효과): Stage364(364단계) 안에서 review(검토)로 이어간다.

## run364AE_review_pf_dd_near_miss_density_bridge_scout_without_db_v1

- action(행동): bridge scout(연결 정찰)를 review(검토)했다.
- effect(효과): Stage364(364단계) 안에서 PF lift density-safe expansion(PF 상승 밀도 안전 확장)으로 이어간다.

## run364AF_materialize_pf_lift_density_safe_expansion_without_db_v1

- action(행동): PF lift density-safe queue(PF 상승 밀도 안전 대기열)를 만들었다.
- effect(효과): Stage364(364단계) 분기 없이 run364AG(364AG 실행)로 이어간다.

## run364AG_train_pf_lift_density_safe_expansion_scout_without_db_v1

- action(행동): PF lift density-safe proxy scout(PF 상승 밀도 안전 프록시 정찰)를 실행했다.
- effect(효과): Stage364(364단계) 안에서 review(검토)로 이어간다.

## run364AH_review_pf_lift_density_safe_expansion_scout_without_db_v1

- action(행동): run364AG(364AG 실행) 프록시 정찰을 검토했다.
- effect(효과): Stage364(364단계) 안에서 run364AI(실행364AI) 수리 입력으로 이어간다.

## run364AI_materialize_session_side_pf_lift_density_repair_inputs_without_db_v1

- action(행동): session/side PF lift density repair inputs(세션/방향 PF 상승 밀도 수리 입력)를 만들었다.
- effect(효과): Stage364(364단계) 안에서 `run364AJ_train_session_side_pf_lift_density_repair_scout_without_db_v1`로 이어간다.

## run364AJ_train_session_side_pf_lift_density_repair_scout_without_db_v1

- action(행동): session/side PF lift density repair proxy scout(세션/방향 PF 상승 밀도 수리 프록시 정찰)를 실행했다.
- effect(효과): Stage364(364단계) 안에서 `run364AK_review_session_side_pf_lift_density_repair_scout_without_db_v1` review(검토)로 이어간다.

## run364AK_review_session_side_pf_lift_density_repair_scout_without_db_v1

- action(행동): run364AJ(364AJ 실행) proxy scout(프록시 정찰)를 검토했다.
- effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 `run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1`로 이어간다.

## run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1

- action(행동): run364AK(364AK 실행) queue(대기열)를 run364AM(364AM 실행) 입력으로 구체화했다.
- effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 공격 탐색을 이어간다.

## run364AM_train_pf_pass_density_restore_offensive_scout_without_db_v1

- action(행동): PF-pass density restore offensive proxy scout(PF 통과 밀도 복원 공격 프록시 정찰)를 실행했다.
- effect(효과): Stage364(364단계) 안에서 `run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1` review(검토)로 이어간다.

## run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1

- action(행동): run364AM(364AM 실행) PF-pass density restore scout(PF 통과 밀도 복원 정찰)를 검토했다.
- effect(효과): Stage364(364단계) 안에서 `run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1` materialization(구체화)로 이어간다.

## run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1

- action(행동): run364AP(364AP 실행) queue(대기열)를 materialize(구체화)했다.
- effect(효과): Stage364(364단계) 안에서 stage(단계) 분기 없이 다음 공격 탐색으로 이어간다.

## run364AP_train_hold6_pf_dd_repair_offensive_scout_without_db_v1

- action(행동): run364AP(364AP 실행) proxy scout(프록시 정찰)를 실행했다.
- effect(효과): Stage364(364단계) 안에서 다음 review(검토)로 이어간다.

## run364AQ_review_hold6_pf_dd_repair_offensive_scout_without_db_v1

- action(행동): run364AQ(364AQ 실행) review(검토)를 닫았다.
- effect(효과): Stage364(364단계) 안에서 다음 materialization(구체화)로 이어간다.

## run364AR Threshold Edge PF Gap Repair Materialization(364AR 임계값 경계 PF 간극 수리 구체화)

Action(행동): AQ queue(대기열) 8행을 AS scout queue(정찰 대기열)로 구체화했다.

Effect(효과): Stage364(364단계) 안에서 stage(단계) 분기 없이 다음 공격 탐색으로 이어간다.

## run364AS Threshold-Edge PF Gap Repair Scout(364AS 임계값 경계 PF 간극 수리 정찰)

Action(행동): AR queue(대기열) 7행을 proxy replay(프록시 재생)했다.

Effect(효과): threshold-edge(임계값 경계) 단서의 PF gap(PF 간극) 수리 가능성을 표면으로 남겼다.

## run364AT Threshold-Edge PF Gap Review(364AT 임계값 경계 PF 간극 검토)

Action(행동): AS strict pass(AS 엄격 통과)를 package/probe(패키지/탐침) 관점으로 검토했다.

Effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 MT5 runtime probe(MT5 런타임 탐침) 준비로 이어간다.

## run364AU Threshold Edge Floor001 Runtime Probe Package(364AU 임계값 경계 하한 0.001 런타임 탐침 패키지)

Action(행동): AS selected proxy(AS 선택 프록시)를 MT5 set/ini(MT5 설정/INI), Common Files(공용 파일), compile receipt(컴파일 영수증)로 package(패키지)했다.

Effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 `run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1` 실행으로 이어간다.

## run364AW Threshold Edge Floor001 MT5 Runtime Probe Review(364AW 임계값 경계 하한 0.001 MT5 런타임 탐침 검토)

Action(행동): AV runtime probe(런타임 탐침)를 성과 귀속(performance attribution, 성과 귀속)으로 검토했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1` density restore(밀도 복원)로 이어간다.

## run364AW Threshold Edge Floor001 MT5 Runtime Probe Review(364AW 임계값 경계 하한 0.001 MT5 런타임 탐침 검토)

Action(행동): AV runtime probe(런타임 탐침)를 성과 귀속(performance attribution, 성과 귀속)으로 검토했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1` density restore(밀도 복원)로 이어간다.

## run364AY Density Restore Cost/Session Proxy Scout(364AY 밀도 복원 비용/세션 프록시 스카우트)

Action(행동): AX queue(대기열)를 proxy replay(프록시 재생)로 실행했다.

Effect(효과): density floor(밀도 하한) 복원 후보를 `run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1` review(검토)로 넘긴다.

## run364AZ Density Restore Scout Review(364AZ 밀도 복원 스카우트 검토)

Action(행동): AY surface(AY 표면)를 package decision(패키지 결정)과 BA queue(BA 대기열)로 검토했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1`로 이어간다.

## run364BA Density Restore Stress-To-Candidate Materialization(364BA 밀도 복원 압박-후보 물질화)

Action(행동): AZ positive clue(AZ 긍정 단서)를 BB queue(BB 대기열)로 물질화했다.

Effect(효과): 다음 proxy scout(프록시 스카우트)를 실행할 수 있게 했다.

## run364BB Density Restore Stress-To-Candidate Proxy Scout(364BB 밀도 복원 압박-후보 프록시 스카우트)

Action(행동): BA queue(BA 대기열)를 proxy replay(프록시 재생)로 실행했다.

Effect(효과): package-reviewable(패키지 검토 가능) 후보 여부를 `run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1` review(검토)로 넘긴다.

## run364BC Density Restore Stress Candidate Review(364BC 밀도 복원 압박 후보 검토)

Action(행동): BB package candidates(BB 패키지 후보)를 검토했다.

Effect(효과): `run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1` runtime probe package(런타임 탐침 패키지)로 이어간다.

## run364BD density restore stress candidate runtime package(밀도 복원 압박 후보 런타임 패키지)

Action(행동): `run364BB_ba02_between_ax03_ax08_floor025_ps450` package(패키지)를 완료했다.

Effect(효과): `run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1` MT5 runtime probe(MT5 런타임 탐침)로 이어간다.

## run364BF Density Restore Stress Candidate MT5 Runtime Probe Review(364BF 밀도 복원 압박 후보 MT5 런타임 탐침 검토)

Action(행동): BE runtime probe(런타임 탐침)를 performance attribution(성과 귀속)으로 검토했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1` forward/regime stress(전진/국면 압박)로 이어간다.

## run364BF Density Restore Stress Candidate MT5 Runtime Probe Review(364BF 밀도 복원 압박 후보 MT5 런타임 탐침 검토)

Action(행동): BE runtime probe(런타임 탐침)를 performance attribution(성과 귀속)으로 검토했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1` forward/regime stress(전진/국면 압박)로 이어간다.

## run364BF Density Restore Stress Candidate MT5 Runtime Probe Review(364BF 밀도 복원 압박 후보 MT5 런타임 탐침 검토)

Action(행동): BE runtime probe(런타임 탐침)를 performance attribution(성과 귀속)으로 검토했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1` forward/regime stress(전진/국면 압박)로 이어간다.

## run364BF Density Restore Stress Candidate MT5 Runtime Probe Review(364BF 밀도 복원 압박 후보 MT5 런타임 탐침 검토)

Action(행동): BE runtime probe(런타임 탐침)를 performance attribution(성과 귀속)으로 검토했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1` forward/regime stress(전진/국면 압박)로 이어간다.

## run364BH Forward Regime Stress Proxy Scout(364BH 전진 국면 압박 프록시 탐색)

Action(행동): 기존 MT5 runtime evidence(런타임 근거)에 미세 margin guard(마진 가드)를 시산했다.

Effect(효과): Stage364(364단계)를 유지하고 `run364BI_review_density_restore_forward_regime_stress_scout_without_db_v1` review(검토)로 이어간다.

## run364BH Forward Regime Stress Proxy Scout(364BH 전진 국면 압박 프록시 탐색)

Action(행동): 기존 MT5 runtime evidence(런타임 근거)에 미세 margin guard(마진 가드)를 시산했다.

Effect(효과): Stage364(364단계)를 유지하고 `run364BI_review_density_restore_forward_regime_stress_scout_without_db_v1` review(검토)로 이어간다.

<!-- run364BI -->
## run364BI forward/regime scout review(전진/국면 탐색 검토)

`proxy_candidate_positive_but_parameter_only_package_ineligible_runtime_guard_support_required_no_authority`. Next(다음): `run364BJ_implement_h19_opposite_margin_runtime_guard_without_db_v1`.

<!-- run364BJ -->
## run364BJ h19 opposite-margin runtime guard(19시 반대마진 런타임 가드)

`mt5_runtime_probe_outputs_available_for_h19_guard_review_required_no_authority`. Next(다음): `run364BK_review_h19_opposite_margin_runtime_probe_without_db_v1`.

## run364BL H19 Stress Short-Balance Materialization(364BL h19 압박 숏 균형 물질화)

Action(행동): BK positive runtime clue(BK 긍정 런타임 단서)를 BM scout(BM 정찰) 입력으로 바꿨다.

Effect(효과): short balance(숏 균형)와 equity DD(평가손익 낙폭)가 닫히기 전까지 운영 주장을 만들지 않는다.

## run364BM H19 Stress Short-Balance Proxy Scout(364BM h19 압박 숏 균형 프록시 정찰)

Action(행동): h17-20 short router(17~20시 숏 라우터)를 fixed6 proxy(고정6봉 프록시)로 정찰했다.

Effect(효과): `bm04_short_router_ps0440_h17_20_overlay_fixed6`가 BN review(BN 검토)로 넘어가며, MT5 재탐침 전까지 운영 주장은 닫는다.

## run364BM H19 Stress Short-Balance Proxy Scout(364BM h19 압박 숏 균형 프록시 정찰)

Action(행동): h17-20 short router(17~20시 숏 라우터)를 fixed6 proxy(고정6봉 프록시)로 정찰했다.

Effect(효과): `bm04_short_router_ps0440_h17_20_overlay_fixed6`가 BN review(BN 검토)로 넘어가며, MT5 재탐침 전까지 운영 주장은 닫는다.

## run364BM H19 Stress Short-Balance Proxy Scout(364BM h19 압박 숏 균형 프록시 정찰)

Action(행동): h17-20 short router(17~20시 숏 라우터)를 fixed6 proxy(고정6봉 프록시)로 정찰했다.

Effect(효과): `bm04_short_router_ps0440_h17_20_overlay_fixed6`가 BN review(BN 검토)로 넘어가며, MT5 재탐침 전까지 운영 주장은 닫는다.

## run364BM H19 Stress Short-Balance Proxy Scout(364BM h19 압박 숏 균형 프록시 정찰)

Action(행동): h17-20 short router(17~20시 숏 라우터)를 fixed6 proxy(고정6봉 프록시)로 정찰했다.

Effect(효과): `bm04_short_router_ps0440_h17_20_overlay_fixed6`가 BN review(BN 검토)로 넘어가며, MT5 재탐침 전까지 운영 주장은 닫는다.

<!-- run364BU -->
## run364BU late-year session gate MT5 precheck(연말 세션 게이트 MT5 사전점검)

`inconclusive_runtime_precheck_calendar_gate_supported_but_exact_mt5_blocked_synthetic_short_source_no_authority`. Next(다음): `run364BV_materialize_synthetic_short_source_runtime_repair_without_db_v1`.

<!-- run364BV -->
## run364BV synthetic short source runtime repair(합성 숏 원천 런타임 수리)

`blocked_runtime_probe_attempted_outputs_or_report_missing_no_authority`. Next(다음): `run364BW_review_synthetic_short_source_runtime_probe_without_db_v1`.

<!-- run364BW -->
- `run364BW_review_synthetic_short_source_runtime_probe_without_db_v1` reviewed BV runtime probe(BV 런타임 탐침 검토): synthetic overlay(합성 덧씌움) weak positive, native short/hour17 clue(기본 숏/17시 단서) opened `run364BX_overlay_hour17_native_short_ablation_runtime_probe_without_db_v1`.

<!-- run364BX -->
## run364BX overlay hour17 native short ablation runtime probe(17시 오버레이 기본 숏 제거 비교 런타임 탐침)

`blocked_runtime_ablation_outputs_or_report_missing_no_authority`. Next(다음): `run364BY_review_overlay_hour17_native_short_ablation_runtime_probe_without_db_v1`.

<!-- run364BY -->
## run364BY BX runtime ablation review(BX 런타임 제거 비교 검토)

`runtime_ablation_review_positive_clue_bx03_december_late_session_guard_no_authority`. Next(다음): `run364BZ_materialize_bx03_december_late_session_guard_inputs_without_db_v1`.

<!-- run364BZ -->
## run364BZ bx03 December late-session guard inputs(BX3 12월 후반 세션 가드 입력)

`materialized_december_h22_calendar_semantics_and_h17_overlay_guard_inputs_no_authority`. Next(다음): `run364CA_execute_bx03_guard_stack_runtime_probe_without_db_v1`.

<!-- run364CA -->
## run364CA bx03 guard stack runtime probe(BX3 가드 묶음 런타임 탐침)

`runtime_probe_completed_best_ca01_bx03_semantics_control_review_required_no_authority`. Next(다음): `run364CB_review_bx03_guard_stack_runtime_probe_without_db_v1`.

<!-- run364CB -->
## run364CB BX3 guard stack runtime probe review(BX3 가드 묶음 런타임 탐침 리뷰)

`runtime_probe_review_usable_with_boundary_ca01_best_positive_vs_bv_but_swap_sensitive_below_bx3_no_authority`. Next(다음): `run364CC_materialize_swap_stable_reprobe_and_source_guard_inputs_without_db_v1`.

<!-- run364CC -->
## run364CC swap-stable reprobe and source guard inputs(스왑 안정 재탐침 및 원천 가드 입력)

`experiment_design_materialized_swap_stable_reprobe_and_source_guard_runtime_handoff_ready_no_authority`. Next(다음): `run364CD_execute_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db_v1`.

<!-- run364CD -->
## run364CD swap-stable source guard MT5 runtime probe(스왑 안정 원천 가드 MT5 런타임 탐침)

`runtime_probe_completed_best_cd01_bx3_clone_current_session_same_session_review_required_no_authority`. Next(다음): `run364CE_review_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db_v1`.

<!-- run364CE -->
## run364CE review swap-stable source guard runtime probe(스왑 안정 원천 가드 런타임 탐침 리뷰)

`runtime_probe_review_usable_with_boundary_same_session_swap_stability_passed_h17_overlay_value_confirmed_no_authority`. Next(다음): `run364CF_materialize_cost_stable_h17_source_guard_offensive_inputs_without_db_v1`.

## run364CG_train_cost_stable_h17_source_guard_offensive_scout_without_db_v1

Action(행동): cost-stable h17 source guard queue(비용 안정 17시 원천 가드 대기열)를 proxy scout(프록시 정찰)로 실행했다.

Effect(효과): `cg09_best_open_hour_overlay_focus`를 CH review(CH 검토)로 넘기고 stage branch(단계 분기)는 만들지 않는다.

<!-- run364CJ__run364CJ_train_h17_focus_month_cost_stress_repair_scout_without_db_v1 -->
## run364CJ h17 focus month cost stress repair scout(17시 집중 월/비용 압박 수리 정찰)

Action(행동): `16` CJ repair candidates(CJ 수리 후보)를 proxy replay(프록시 재생)했다.

Effect(효과): selected proxy repair(선택 프록시 수리) `cj09_cg07_native_short_cost_firewall_short_floor_rescue`를 `run364CK_review_h17_focus_month_cost_stress_repair_scout_without_db_v1` review(검토)로 넘기고 runtime authority(런타임 권위)는 주장하지 않는다.

<!-- run364CK__run364CK_review_h17_focus_month_cost_stress_repair_scout_without_db_v1 -->
## run364CK h17 focus repair review(17시 집중 수리 검토)

Action(행동): CJ selected repair(CJ 선택 수리)를 package gate(패키지 게이트)와 month/source/cost attribution(월/원천/비용 귀속)으로 검토했다.

Effect(효과): package(패키지)는 거절하고 `run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1`로 CL repair input(CL 수리 입력)을 연다.

## run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1

Action(행동): CL bad-month/source-balance queue(CL 손실 월/원천 균형 대기열)를 proxy replay(프록시 재생)했다.

Effect(효과): selected `cm04_cj09_month08_12_pair_guard`를 `run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1` review(검토)로 넘겼고, runtime authority(런타임 권위)는 주장하지 않는다.

<!-- run364CN__run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1 -->
## run364CN h17 bad-month source-balance repair review(17시 손실 월/원천 균형 수리 검토)

Action(행동): `cm04_cj09_month08_12_pair_guard`를 MT5 probe handoff(MT5 탐침 인계) 후보로 검토했습니다.

Effect(효과): 다음 실행 `run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1`에서 runtime input materialization(런타임 입력 구체화)을 진행합니다.

<!-- run364CO__run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1 -->
## run364CO MT5 runtime probe package(MT5 런타임 탐침 패키지)

`cm04_cj09_month08_12_pair_guard` package(패키지) ready(준비). Next(다음): `run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`.

<!-- run364CP__run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1 -->
## run364CP MT5 runtime probe(MT5 런타임 탐침)

`cm04_cj09_month08_12_pair_guard` probe(탐침) attempted(시도됨). Next(다음): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`.

<!-- run364CQ__run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1 -->
## run364CQ MT5 runtime probe review(MT5 런타임 탐침 검토)

`cm04_cj09_month08_12_pair_guard` review(검토) 완료. Next(다음): `run364CR_materialize_h17_month12_long_equity_drawdown_repair_inputs_without_db_v1`.

<!-- run364CR__run364CR_materialize_h17_month12_long_equity_drawdown_repair_inputs_without_db_v1 -->
## run364CR repair inputs(수리 입력)

Queue(대기열): `8` variants. Next(다음): `run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1`.

<!-- run364CS__run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1 -->
## run364CS proxy scout(364CS 프록시 정찰)

Selected(선택): `cr04_month12_long_hours17_20_floor002`. Next(다음): `run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1`.

<!-- run364CT__run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1 -->
## run364CT review(364CT 검토)

Selected(선택): `cr04_month12_long_hours17_20_floor002`. Next(다음): `run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1`.

<!-- run364CU__run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1 -->
## run364CU runtime package(364CU 런타임 패키지)

`cr04_month12_long_hours17_20_floor002` package(패키지) ready(준비). Next(다음): `run364CV_execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`.

<!-- run364CV__run364CV_execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1 -->
## run364CV MT5 runtime probe(MT5 런타임 탐침)

`cr04_month12_long_hours17_20_floor002` probe(탐침) attempted(시도됨). Next(다음): `run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`.

<!-- run364CW__run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1 -->
## run364CW MT5 runtime probe review(MT5 런타임 탐침 검토)

`cr04_month12_long_hours17_20_floor002` review(검토) 완료. Next(다음): `run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1`.

<!-- run364CX__run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1 -->
## run364CX repair inputs(수리 입력)

Queue(대기열): `12` variants. Next(다음): `run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`.

<!-- run364CY__run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1 -->
## run364CY proxy scout(프록시 정찰)

Selected(선택): `cx05_high_quality_short_boost110_h17_20`. Next(다음): `run364CZ_review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`.

<!-- run364CZ__run364CZ_review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1 -->
## run364CZ review(364CZ 검토)

Selected(선택): `cx05_high_quality_short_boost110_h17_20`. Next(다음): `run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1`.

<!-- run364DA__run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1 -->
## run364DA runtime package(364DA 런타임 패키지)

`cx05_high_quality_short_boost110_h17_20` package(패키지) ready(준비). Next(다음): `run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`.

<!-- run364DB__run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1 -->
## run364DB MT5 runtime probe(MT5 런타임 탐침)

`cx05_high_quality_short_boost110_h17_20` probe(탐침) attempted(시도). Next(다음): `run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`.

<!-- run364DC__run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1 -->
## run364DC review(검토)

DB MT5 review(DB MT5 검토) completed(완료). Next(다음): `run364DD_train_h17_short_source_expansion_runtime_positive_scout_without_db_v1`.

<!-- run364DD__run364DD_train_h17_short_source_expansion_runtime_positive_scout_without_db_v1 -->
## run364DD short-source expansion scout(숏 원천 확장 탐색)

Selected(선택): `dd05_h17_21_short_source_m050_ex_aug`. Next(다음): `run364DE_review_h17_short_source_expansion_runtime_positive_scout_without_db_v1`.

<!-- run364DE__run364DE_review_h17_short_source_expansion_runtime_positive_scout_without_db_v1 -->
## run364DE runtime review(런타임 검토)

Selected(선택): `dd05_h17_21_short_source_m050_ex_aug`. Required repair(필수 보정): `InpSyntheticShortSourceMarginVsFlatMin`. Next(다음): `run364DF_implement_h17_short_source_expansion_runtime_package_without_db_v1`.

<!-- run364DF__run364DF_implement_h17_short_source_expansion_runtime_package_without_db_v1 -->
## run364DF runtime package(런타임 패키지)

Candidate(후보): `dd05_h17_21_short_source_m050_ex_aug`. Next(다음): `run364DG_execute_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`.
<!-- run364DG__run364DG_execute_h17_short_source_expansion_mt5_runtime_probe_without_db_v1 -->
## run364DG MT5 runtime probe(MT5 런타임 탐침)

`dd05_h17_21_short_source_m050_ex_aug` probe(탐침) attempted(시도). Next(다음): `run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`.
<!-- run364DH__run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1 -->
## run364DH review(검토)

DD05 MT5 review(DD05 MT5 검토) completed(완료). Next(다음): `run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1`.
<!-- run364DI__run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1 -->
## run364DI scout(스카우트)

Short-source profit recovery(숏 원천 수익 회복) proxy scout(프록시 스카우트) completed(완료). Next(다음): `run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1`.
<!-- run364DJ__run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1 -->
## run364DJ review(검토)

DI candidate(DI 후보) reviewed(검토됨). Next(다음): `run364DK_implement_h17_short_source_profit_recovery_runtime_package_without_db_v1`.
<!-- run364DK__run364DK_implement_h17_short_source_profit_recovery_runtime_package_without_db_v1 -->
## run364DK runtime package(런타임 패키지)

Candidate(후보): `di02_h17_18_20_21_no19_m050`. Next(다음): `run364DL_execute_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`.
<!-- run364DL__run364DL_execute_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1 -->
## run364DL MT5 runtime probe(MT5 런타임 탐침)

`run364DK_di02_no19_short_source_profit_recovery` probe(탐침) attempted(시도). Next(다음): `run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`.
<!-- run364DM__run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1 -->
## run364DM review(검토)

DI02 no19 MT5 review(DI02 no19 MT5 검토) completed(완료). Next(다음): `run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1`.
<!-- run364DN__run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1 -->
## run364DN PF/net polish scout(PF/순수익 다듬기 스카우트)

Selected(선택): `dn04_risk_mult125_all_h17_20`. Next(다음): `run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1`.
<!-- run364DO__run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1 -->
## run364DO review(검토)

Parameter-only PF/net polish(파라미터 전용 PF/순수익 다듬기)는 strict package contract(엄격 패키지 계약)를 통과하지 못했습니다. Next(다음): `run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1`.
<!-- run364DP__run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1 -->
## run364DP model/label reseed(모델/라벨 재시드)

Selected(선택): `short_h3_m2__full58(전체_58)__et6_l80_n96(엑스트라트리6_잎80_96)`. Next(다음): `run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1`.
<!-- run364DQ__run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1 -->
## run364DQ review(검토)

DP ONNX seed(DP ONNX 씨앗)는 OOS clue(표본외 단서)지만 package(패키지)는 아닙니다. Next(다음): `run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1`.
<!-- run364DR__run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1 -->
## run364DR density/PF bridge(밀도/PF 브리지)

Selected(선택): `dr03252_h16_21_s0p516397_p0p0_mn0p2_dominant_h8`. Strict candidates(엄격 후보): `0`. Next(다음): `run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1`.
<!-- run364DS__run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1 -->
## run364DS review(검토)

DR bridge(DR 브리지)는 package rejected(패키지 거절)입니다. Next(다음): `run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1`.
<!-- run364DT__run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1 -->
## run364DT regime/behavior reseed(국면/현상 재시드)

Selected(선택): `dir_h6_m3__behavior72(현상_72)__et7_l50_n128(엑스트라트리7_잎50_128)`. Strict candidates(엄격 후보): `0`. Next(다음): `run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1`.
<!-- run364DU__run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1 -->
## run364DU review(검토)

DT regime/behavior reseed(DT 국면/현상 재시드)는 OOS clue(표본외 단서)가 있으나 validation failure(검증 실패) 때문에 package rejected(패키지 거절)입니다. Next(다음): `run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1`.
<!-- run364DV__run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1 -->
## run364DV validation-stability reseed(검증 안정성 재시드)

Selected(선택): `stable_dir_h6_m3__short_stability57(숏_안정성_57)__rf8_l70_n112(랜덤포레스트8_잎70_112)`. Strict candidates(엄격 후보): `0`. Next(다음): `run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1`.
<!-- run364DW__run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1 -->
## run364DW review(검토)

DV는 net/PF(순수익/PF)를 회복했지만 density(밀도)가 낮아 package rejected(패키지 거절)입니다. Next(다음): `run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1`.
<!-- run364DX__run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1 -->
## run364DX density recovery reseed(밀도 회복 재시드)

Selected(선택): `dense_dir_h2_m1p5__stability82(안정성_82)__rf8_l70_n112(랜덤포레스트8_잎70_112)`. Strict candidates(엄격 후보): `0`. Next(다음): `run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1`.
<!-- run364DY__run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1 -->
## run364DY review(검토)

DX는 density(밀도)를 회복했지만 OOS net/PF(표본외 순수익/PF)가 깨져 package rejected(패키지 거절)입니다. Next(다음): `run364DZ_train_h17_density_pf_balance_reseed_without_db_v1`.
<!-- run364DZ__run364DZ_train_h17_density_pf_balance_reseed_without_db_v1 -->
## run364DZ density/PF balance reseed(밀도/PF 균형 재시드)

Selected(선택): `balance_dir_h3_m2__stability82(안정성_82)__et8_l60_n144(엑스트라트리8_잎60_144)`. Strict candidates(엄격 후보): `0`. Next(다음): `run364EA_review_h17_density_pf_balance_reseed_without_db_v1`.
<!-- run364EA__run364EA_review_h17_density_pf_balance_reseed_without_db_v1 -->
## run364EA density/PF balance review(밀도/PF 균형 검토)

Package(패키지): rejected(거절). Next(다음): `run364EB_train_h17_validation_pf_floor_density_recovery_reseed_without_db_v1`.
<!-- run364EB__run364EB_train_h17_validation_pf_floor_density_recovery_reseed_without_db_v1 -->
## run364EB validation PF floor density recovery(검증 PF 바닥 밀도 회복)

Selected(선택): `pf_floor_dir_h2_m2__stability82(안정성_82)__rf8_l60_n128(랜덤포레스트8_잎60_128)`. Strict candidates(엄격 후보): `0`. Next(다음): `run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1`.
<!-- run364EC__run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1 -->
## run364EC validation PF floor review(검증 PF 바닥 검토)

Package(패키지): rejected(거절). Next(다음): `run364ED_train_h17_dual_pf_floor_bridge_reseed_without_db_v1`.
<!-- run364ED__run364ED_train_h17_dual_pf_floor_bridge_reseed_without_db_v1 -->
## run364ED dual PF floor bridge(양쪽 PF 바닥 연결)

Selected(선택): `dual_pf_dir_h2_m1p5__short_stability57(숏_안정성_57)__et7_l55_n192(엑스트라트리7_잎55_192)`. min_pf(최소 PF): `1.0219124076`. Next(다음): `run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1`.
<!-- run364EE__run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1 -->
## run364EE dual PF floor bridge review(양쪽 PF 바닥 연결 검토)

Package(패키지): rejected(거절). Next(다음): `run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1`.
<!-- run364EF__run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1 -->
## run364EF validation source rotation density recovery(검증 원천 회전 밀도 회복)

Selected(선택): `source_rotate_dir_h2_m1p5__source_all82(원천전체_82)__et6_l70_n160(엑스트라트리6_잎70_160)`. min_pf(최소 PF): `1.0474042816`. Next(다음): `run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1`.
<!-- run364EG__run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1 -->
## run364EG validation source rotation review(검증 원천 회전 검토)

Package(패키지): rejected(거절). Next(다음): `run364EH_train_h17_oos_pf108_bridge_density_preserve_without_db_v1`.
<!-- run364EH__run364EH_train_h17_oos_pf108_bridge_density_preserve_without_db_v1 -->
## run364EH OOS PF108 bridge density preserve(표본외 PF108 연결 밀도 보존)

Selected(선택): `oos_pf108_dir_h2_m1p5__source_all82(원천전체_82)__et8_l90_n160(엑스트라트리8_잎90_160)`. min_pf(최소 PF): `1.0646379958`. Next(다음): `run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1`.
<!-- run364EI__run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1 -->
## run364EI OOS PF108 bridge review(표본외 PF108 연결 검토)

Package(패키지): rejected(거절). Next(다음): `run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1`.
<!-- run364EJ__run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1 -->
## run364EJ density floor OOS PF salvage(밀도 바닥 표본외 PF 회수)

Selected(선택): `density_salvage_dir_h2_m1__source_all82__et7_l70_n192`. min_pf(최소 PF): `1.0183147066`. Next(다음): `run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1`.
<!-- run364EK__run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1 -->
## run364EK density floor OOS PF salvage review(밀도 바닥 표본외 PF 회수 검토)

Package(패키지): rejected(거절). Next(다음): `run364EL_train_h17_oos108_validation_floor_bridge_without_db_v1`.
<!-- run364EL__run364EL_train_h17_oos108_validation_floor_bridge_without_db_v1 -->
## run364EL OOS108 validation floor bridge(표본외108 검증 바닥 연결)

Selected(선택): `oos108_valfloor_dir_h2_m1__source_all82__rf8_l70_n160`. min_pf(최소 PF): `1.1329169764`. Next(다음): `run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1`.
<!-- run364EM__run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1 -->
## run364EM OOS108 validation floor bridge review(표본외108 검증 바닥 연결 검토)

Package(패키지): eligible for runtime probe(런타임 탐침 가능). Next(다음): `run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1`.
<!-- run364EN__run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1 -->
## run364EN runtime package(런타임 패키지)

Candidate(후보): `oos108_valfloor_dir_h2_m1__source_all82__rf8_l70_n160`. Next(다음): `run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`.
<!-- run364EO__run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1 -->
## run364EO MT5 runtime probe(MT5 런타임 탐침)

`oos108_valfloor_dir_h2_m1__source_all82__rf8_l70_n160` probe(탐침) attempted(시도됨). Next(다음): `run364EP_review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`.
<!-- run364EP__run364EP_review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1 -->
## run364EP review(검토)

OOS108 MT5 review(OOS108 MT5 검토) completed(완료). Next(다음): `run364EQ_train_h17_oos108_scope_aligned_cost_side_repair_scout_without_db_v1`.
## run364EQ

- report(보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364EQ_oos108_cost_side_scout.md`
- judgment(판정): `negative_current_surface_cost_side_strict_pass_zero_positive_reseed_seed_existing_surface_insufficient_no_authority`
- next(다음): `run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1`
## run364EQ

- report(보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364EQ_oos108_cost_side_scout.md`
- judgment(판정): `negative_current_surface_cost_side_strict_pass_zero_positive_reseed_seed_existing_surface_insufficient_no_authority`
- next(다음): `run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1`
<!-- run364ER__run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1 -->
## run364ER cost/side model-label-feature reseed(비용/방향 모델-라벨-피처 재시드)

Selected(선택): `costside_dir_h2_m3__costside_all72__et8_l45_n160`. Strict candidates(엄격 후보): `0`. Next(다음): `run364ES_review_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1`.
<!-- run364ES__run364ES_review_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1 -->
## run364ES cost/side reseed review(비용/방향 재시드 검토)

Package(패키지): rejected(거절). Next(다음): `run364ET_train_h17_oos108_density_cost_short_balance_reseed_without_db_v1`.
<!-- run364ET__run364ET_train_h17_oos108_density_cost_short_balance_reseed_without_db_v1 -->
## run364ET density/cost/short balance reseed(밀도/비용/숏 균형 재시드)

Selected(선택): `densecost_sym_h2_m2p5__et_all72__rf9_l45_n144`. Strict candidates(엄격 후보): `0`. Next(다음): `run364EU_review_h17_oos108_density_cost_short_balance_reseed_without_db_v1`.
<!-- run364EU__run364EU_review_h17_oos108_density_cost_short_balance_reseed_without_db_v1 -->
## run364EU density/cost/short balance review(밀도/비용/숏 균형 검토)

Package(패키지): rejected(거절). Next(다음): `run364EV_train_h17_oos108_cost09_density_edge_recovery_without_db_v1`.
<!-- run364EV__run364EV_train_h17_oos108_cost09_density_edge_recovery_without_db_v1 -->
## run364EV cost09/density edge recovery(비용0.9/밀도 엣지 회복)

Next(다음): `run364EW_review_h17_oos108_cost09_density_edge_recovery_without_db_v1`.
<!-- run364EW__run364EW_review_h17_oos108_cost09_density_edge_recovery_without_db_v1 -->
## run364EW cost09/density edge review(비용0.9/밀도 엣지 검토)

Package(패키지): rejected(거절). Next(다음): `run364EX_train_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1`.
<!-- run364EX__run364EX_train_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1 -->
## run364EX OOS preserve cost09/short rebalance(표본외 보존 비용0.9/숏 재균형)

Next(다음): `run364EY_review_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1`.
<!-- run364EY__run364EY_review_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1 -->
## run364EY OOS preserve cost09/short review(표본외 보존 비용0.9/숏 검토)

Package(패키지): rejected(거절). Next(다음): `run364EZ_train_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1`.
<!-- run364EZ__run364EZ_train_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1 -->
## run364EZ OOS PF125 cost09 gap repair(표본외 PF 1.25 비용0.9 간격 수리)

Next(다음): `run364FA_review_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1`.
<!-- run364FA__run364FA_review_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1 -->
## run364FA OOS PF125 cost09 gap review(표본외 PF 1.25 비용0.9 간격 검토)

Package(패키지): rejected(거절). Next(다음): `run364FB_train_h17_oos108_pf125_density_bridge_repair_without_db_v1`.
<!-- run364FB__run364FB_train_h17_oos108_pf125_density_bridge_repair_without_db_v1 -->
## run364FB PF125 density bridge repair(PF125 밀도 연결 수리)

Next(다음): `run364FC_review_h17_oos108_pf125_density_bridge_repair_without_db_v1`.
<!-- run364FC__run364FC_review_h17_oos108_pf125_density_bridge_repair_without_db_v1 -->
## run364FC PF125 density bridge review(PF125 밀도 연결 검토)

Package(패키지): rejected(거절). Next(다음): `run364FD_train_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1`.
<!-- run364FD__run364FD_train_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1 -->
## run364FD PF125 short/cost09 balance repair(PF125 숏/비용0.9 균형 수리)

Next(다음): `run364FE_review_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1`.
<!-- run364FE__run364FE_review_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1 -->
## run364FE PF125 short/cost09 balance review(PF125 숏/비용0.9 균형 검토)

Package(패키지): rejected(거절). Next(다음): `run364FF_train_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1`.
<!-- run364FF__run364FF_train_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1 -->
## run364FF PF125 density rejoin cost09 short guard(PF125 밀도 재결합 비용0.9 숏 가드)

Next(다음): `run364FG_review_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1`.
<!-- run364FG__run364FG_review_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1 -->
## run364FG PF125 density rejoin review(PF125 밀도 재결합 검토)

Package(패키지): rejected(거절). Next(다음): `run364FH_train_h17_oos108_pf125_validation_density_profit_repair_without_db_v1`.
<!-- run364FH__run364FH_train_h17_oos108_pf125_validation_density_profit_repair_without_db_v1 -->
## run364FH validation density profit repair(검증 밀도 수익 수리)

Next(다음): `run364FI_review_h17_oos108_pf125_validation_density_profit_repair_without_db_v1`.
<!-- run364FI__run364FI_review_h17_oos108_pf125_validation_density_profit_repair_without_db_v1 -->
## run364FI validation density profit review(검증 밀도 수익 검토)

Package(패키지): rejected(거절). Next(다음): `run364FJ_train_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1`.
<!-- run364FJ__run364FJ_train_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1 -->
## run364FJ OOS density preserve repair(표본외 밀도 보존 수리)

Next(다음): `run364FK_review_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1`.
<!-- run364FK__run364FK_review_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1 -->
## run364FK OOS density preserve review(표본외 밀도 보존 검토)

Package(패키지): rejected(거절). Next(다음): `run364FL_train_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1`.
<!-- run364FL__run364FL_train_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1 -->
## run364FL dual density OOS cost bridge(양쪽 밀도 표본외 비용 연결)

Next(다음): `run364FM_review_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1`.
<!-- run364FM__run364FM_review_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1 -->
## run364FM dual density OOS cost bridge review(양쪽 밀도 표본외 비용 연결 검토)

Package(패키지): rejected(거절). Next(다음): `run364FN_train_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1`.
<!-- run364FN__run364FN_train_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1 -->
## run364FN density cost decoupled bridge(밀도 비용 분리 연결)

Next(다음): `run364FO_review_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1`.
<!-- run364FO__run364FO_review_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1 -->
## run364FO density cost decoupled bridge review(밀도 비용 분리 연결 검토)

Package(패키지): rejected(거절). Next(다음): `run364FP_train_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1`.
<!-- run364FP__run364FP_train_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1 -->
## run364FP positive density floor reseed(양수 밀도 바닥 재시드)

Next(다음): `run364FQ_review_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1`.
<!-- run364FQ__run364FQ_review_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1 -->
## run364FQ positive density floor reseed review(양수 밀도 바닥 재시드 검토)

Package(패키지): rejected(거절). Next(다음): `run364FR_train_h17_oos108_pf125_density3_regime_split_repair_without_db_v1`.
<!-- run364FR__run364FR_train_h17_oos108_pf125_density3_regime_split_repair_without_db_v1 -->
## run364FR density3 regime split repair(밀도3 국면 분할 수리)

Next(다음): `run364FS_review_h17_oos108_pf125_density3_regime_split_repair_without_db_v1`.
<!-- run364FS__run364FS_review_h17_oos108_pf125_density3_regime_split_repair_without_db_v1 -->
## run364FS density3 regime split repair review(밀도3 국면 분할 수리 검토)

Package(패키지): rejected(거절). Next(다음): `run364FT_train_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1`.
<!-- run364FT__run364FT_train_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1 -->
## run364FT regime profit density reexpand(국면 수익 밀도 재확장)

Next(다음): `run364FU_review_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1`.
<!-- run364FU__run364FU_review_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1 -->
## run364FU regime profit density reexpand review(국면 수익 밀도 재확장 검토)

Next(다음): `run364FV_train_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1`.
<!-- run364FV__run364FV_train_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1 -->
## run364FV density3 OOS profit bridge(밀도3 표본외 수익 연결)

Next(다음): `run364FW_review_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1`.
<!-- run364FW__run364FW_review_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1 -->
## run364FW density3 OOS profit bridge review(밀도3 표본외 수익 연결 검토)

Next(다음): `run364FX_train_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1`.
<!-- run364FX__run364FX_train_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1 -->
## run364FX profit density dual anchor rejoin(수익 밀도 이중 앵커 재결합)

Next(다음): `run364FY_review_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1`.
<!-- run364FY__run364FY_review_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1 -->
## run364FY profit density dual anchor rejoin review(수익 밀도 이중 앵커 재결합 검토)

Next(다음): `run364FZ_train_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1`.
<!-- run364FZ__run364FZ_train_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1 -->
## run364FZ density profit conflict reblend(밀도 수익 충돌 재혼합)

Next(다음): `run364GA_review_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1`.
<!-- run364GA__run364GA_review_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1 -->
## run364GA density profit conflict reblend review(밀도 수익 충돌 재혼합 검토)

Next(다음): `run364GB_train_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1`.
<!-- run364GB__run364GB_train_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1 -->
## run364GB session side loss veto rescue(세션 방향 손실 차단 회수)

Next(다음): `run364GC_review_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1`.
<!-- run364GC__run364GC_review_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1 -->
## run364GC session side loss veto rescue review(세션 방향 손실 차단 회수 검토)

Next(다음): `run364GD_train_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1`.
<!-- run364GD__run364GD_train_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1 -->
## run364GD profit preserving density recovery(수익 보존 밀도 회복)

Next(다음): `run364GE_review_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1`.
<!-- run364GE__run364GE_review_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1 -->
## run364GE profit preserving density recovery review(수익 보존 밀도 회복 검토)

Next(다음): `run364GF_train_h17_oos108_pf125_profit_floor_density_lift_without_db_v1`.
<!-- run364GF__run364GF_train_h17_oos108_pf125_profit_floor_density_lift_without_db_v1 -->
## run364GF profit-floor density lift(수익 바닥 밀도 상승)

Next(다음): `run364GG_review_h17_oos108_pf125_profit_floor_density_lift_without_db_v1`.
<!-- run364GG__run364GG_review_h17_oos108_pf125_profit_floor_density_lift_without_db_v1 -->
## run364GG profit-floor density lift review(수익 바닥 밀도 상승 검토)

Next(다음): `run364GH_train_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1`.
<!-- run364GH__run364GH_train_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1 -->
## run364GH density3 profit-floor repair(밀도3 수익 바닥 수리)

Next(다음): `run364GI_review_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1`.
<!-- run364GI__run364GI_review_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1 -->
## run364GI density3 profit-floor repair review(밀도3 수익 바닥 수리 검토)

Next(다음): `run364GJ_train_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1`.
<!-- run364GK__run364GK_review_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1 -->
## run364GK density-cost floor rejoin review(밀도-비용 바닥 재결합 검토)

Next(다음): `run364GL_train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1`.
<!-- run364GJ__run364GJ_train_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1 -->
## run364GJ density-cost floor rejoin(밀도-비용 바닥 재결합)

Next(다음): `run364GK_review_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1`.
<!-- run364GL__run364GL_train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1 -->
## run364GL cost-repaired density reexpand(비용 수리 후 밀도 재확장)

Next(다음): `run364GM_review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1`.
<!-- run364GM__run364GM_review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1 -->
## run364GM cost-repaired density reexpand review(비용 수리 후 밀도 재확장 검토)

Next(다음): `run364GN_train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1`.
<!-- run364GN__run364GN_train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1 -->
## run364GN density-cost dual-anchor router(밀도-비용 이중 앵커 라우터)

Next(다음): `run364GO_review_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1`.
<!-- run364GO__run364GO_review_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1 -->
## run364GO density-cost dual-anchor router review(밀도-비용 이중 앵커 라우터 검토)

Next(다음): `run364GP_train_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1`.
<!-- run364GP__run364GP_train_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1 -->
## run364GP density-floor PF-capped router(밀도 바닥 PF 캡 라우터)

Next(다음): `run364GQ_review_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1`.
<!-- run364GQ__run364GQ_review_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1 -->
## run364GQ density-floor PF-capped router review(밀도 바닥 PF 캡 라우터 검토)

Next(다음): `run364GR_train_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1`.
<!-- run364GR__run364GR_train_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1 -->
## run364GR cost-near density floor router(비용 근접 밀도 바닥 라우터)

Next(다음): `run364GS_review_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1`.
<!-- run364GS__run364GS_review_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1 -->
## run364GS cost-near density floor router review(비용 근접 밀도 바닥 라우터 검토)

Next(다음): `run364GT_train_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1`.
<!-- run364GT__run364GT_train_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1 -->
## run364GT cost-near density lift router(비용 근접 밀도 상승 라우터)

Next(다음): `run364GU_review_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1`.
<!-- run364GU__run364GU_review_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1 -->
## run364GU cost-near density lift router review(비용 근접 밀도 상승 라우터 검토)

Next(다음): `run364GV_train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1`.
<!-- run364GV__run364GV_train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1 -->
## run364GV OOS cost0.6 density preserve router(표본외 비용0.6 밀도 보존 라우터)

Next(다음): `run364GW_review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1`.
<!-- run364GW__run364GW_review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1 -->
## run364GW OOS cost0.6 density preserve router review(표본외 비용0.6 밀도 보존 라우터 검토)

Next(다음): `run364GX_train_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1`.
<!-- run364GX__run364GX_train_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1 -->
## run364GX density recover cost0.6 hold router(밀도 회복 비용0.6 유지 라우터)

Next(다음): `run364GY_review_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1`.
<!-- run364GY__run364GY_review_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1 -->
## run364GY density recover cost0.6 hold router review(밀도 회복 비용0.6 유지 라우터 검토)

Next(다음): `run364GZ_train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1`.
<!-- run364GZ__run364GZ_train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1 -->
## run364GZ cost-density joint frontier router(비용-밀도 공동 경계 라우터)

Next(다음): `run364HA_review_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1`.
<!-- run364HA__run364HA_review_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1 -->
## run364HA cost-density joint frontier router review(비용-밀도 공동 경계 라우터 검토)

Next(다음): `run364HB_train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1`.
<!-- run364HB__run364HB_train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1 -->
## run364HB OOS profit-density rebalance cost floor router(표본외 수익-밀도 재균형 비용 바닥 라우터)

Next(다음): `run364HC_review_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1`.
<!-- run364HC__run364HC_review_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1 -->
## run364HC OOS profit-density rebalance review(표본외 수익-밀도 재균형 검토)

Next(다음): `run364HD_train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1`.
<!-- run364HD__run364HD_train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1 -->
## run364HD dual-surface density-profit switch router(이중 표면 밀도-수익 전환 라우터)

Next(다음): `run364HE_review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1`.
<!-- run364HE__run364HE_review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1 -->
## run364HE dual-surface router review(이중 표면 라우터 검토)

Next(다음): `run364HF_train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1`.
<!-- run364HF__run364HF_train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1 -->
## run364HF near-miss profit/PF lift switch router(근접 실패 수익/PF 리프트 전환 라우터)

Next(다음): `run364HG_review_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1`.
<!-- run364HG__run364HG_review_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1 -->
## run364HG near-miss profit/PF lift review(근접 실패 수익/PF 리프트 검토)

Next(다음): `run364HH_materialize_h17_oos108_pf125_near_miss_profit_pf_lift_runtime_capability_inputs_without_db_v1`.
<!-- run364HH__run364HH_materialize_h17_oos108_pf125_near_miss_profit_pf_lift_runtime_capability_inputs_without_db_v1 -->
## run364HH runtime capability input materialization(런타임 기능 입력 물질화)

Next(다음): `run364HI_implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db_v1`.
<!-- run364HI__run364HI_implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db_v1 -->
## run364HI probability-bin veto runtime support(확률 구간 차단 런타임 지원)

Next(다음): `run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1`.
<!-- run364HJ__run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1 -->
## run364HJ runtime package(런타임 패키지)

Candidate(후보): `gz_cost_h2_m0p32__gz_joint_frontier_blend__rf9_l20_n176` + `hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`. Next(다음): `run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`.
<!-- run364HK__run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->
## run364HK MT5 runtime probe(MT5 런타임 탐침)

Probability-bin veto(확률 구간 거부) probe(탐침) attempted(시도). Next(다음): `run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`.
<!-- run364HL__run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->
## run364HL review(검토)

Probability-bin veto MT5 review(확률 구간 거부 MT5 검토) completed(완료). Next(다음): `run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1`.
<!-- run364HM__run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1 -->
## run364HM density/side/cost repair scout(밀도/방향/비용 수리 탐색)

Next(다음): `run364HN_review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1`.
<!-- run364HN__run364HN_review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1 -->
## run364HN package review(패키지 검토)

Selected model(선택 모델): `fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160`. Next(다음): `run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1`.
<!-- run364HO__run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1 -->
## run364HO runtime package(런타임 패키지)

Candidate(후보): `fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160`. Next(다음): `run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1`.
<!-- run364HP__run364HP_execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->
## run364HP MT5 runtime probe(MT5 런타임 탐침)

Single-source probability-bin veto(단일 원천 확률 구간 거부) probe(탐침) attempted(시도). Next(다음): `run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1`.
<!-- run364HQ__run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1 -->
## run364HQ review(검토)

Single-source probability-bin veto MT5 review(단일 원천 확률 구간 거부 MT5 검토) completed(완료). Next(다음): `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`.
<!-- run364HR__run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1 -->
## run364HR scout(탐색)

Trade-quality density repair(거래 품질 밀도 수리) proxy replay(프록시 재생) completed(완료). Next(다음): `run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`.
