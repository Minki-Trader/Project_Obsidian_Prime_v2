# run364BT late-year short-share stress repair review(364BT 연말 숏비중 압박 수리 검토)

## Current Truth(현재 진실)

- reviewed candidate(검토 후보): `bs02_late_year_parent_session_suppress__moy12__h21__side_long`
- reviewed KPI(검토 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1063.14` / `1.4220035161` / `3.0720720721` / `0.1221896383`
- stress(압박): month_bad_count(월 나쁨 수) `0`, min month net/PF(최저 월 순수익/수익 팩터) `8.44` / `1.0908354181`
- precheck decision(사전검사 결정): `eligible_for_bu_precheck_not_package_authority(BU 사전검사 적격, 패키지 권위 아님)`
- overfit watch(과적합 관찰): `low_sample_month_of_year_session_gate_watch(소표본 월중 세션 게이트 관찰)`

## Action And Effect(행동과 효과)

Action(행동): BS selected proxy(BS 선택 프록시)를 package precheck decision(패키지 사전검사 결정), overfit review(과적합 검토), robustness surface review(강건성 표면 검토), proxy/MT5 diff review(프록시/MT5 차이 검토)로 분리했다.

Effect(효과): BU에서 narrow MT5 Strategy Tester probe(좁은 MT5 전략 테스터 탐침)를 바로 시도할 수 있게 queue(대기열)를 열었고, runtime authority(런타임 권위)는 주장하지 않았다.

## Package Precheck Decision(패키지 사전검사 결정)

| gate_id | gate_status | evidence | interpretation |
| --- | --- | --- | --- |
| headline_kpi_gate | passed_for_precheck(사전검사 통과) | net=1063.14;pf=1.4220035161;density=3.0720720721;short_share=0.1221896383 | selected proxy keeps headline KPI above review floors(선택 프록시가 검토 기준 KPI를 유지) |
| stress_clear_gate | passed_for_precheck(사전검사 통과) | month_bad_count=0;min_month_net=8.44;min_month_pf=1.0908354181 | BS repaired BR month stress in proxy(BS가 BR 월 압박을 프록시에서 수리) |
| low_sample_month_gate | watch_for_precheck(사전검사 관찰) | suppressed_trades=5;month_of_year=12;hours=21 | review accepts only MT5 precheck, not promotion(검토는 MT5 사전검사만 허용하고 승격은 아님) |
| family_concentration_gate | watch_for_precheck(사전검사 관찰) | package_like_rows=37;synthetic_package_like_rows=0 | all stress-clear rows came from parent-session suppression(압박 해소 행은 부모 세션 억제 계열에 몰림) |
| mt5_runtime_gate | pending_for_bu(BU에서 대기) | new_mt5_execution=not_run | proxy cannot replace MT5 Strategy Tester(프록시는 MT5 전략 테스터를 대체하지 않음) |
| decision | eligible_for_bu_precheck_not_package_authority(BU 사전검사 적격, 패키지 권위 아님) | next_run_id=run364BU_prepare_late_year_session_gate_mt5_precheck_without_db_v1 | move to materialized MT5 precheck attempt(물질화된 MT5 사전검사 시도로 이동) |

## Overfit Review(과적합 검토)

| audit_id | status | evidence | effect |
| --- | --- | --- | --- |
| timestamp_safe_boundary(시점 안전 경계) | passed | BS used month_of_year/hour/side/probability/margin, not exact year-month(BS는 정확 연월이 아닌 월중/시간/방향/확률/마진 사용) | look-ahead bias(미래참조 편향) 재발을 막는다. |
| low_sample_repair_watch(소표본 수리 관찰) | watch | suppressed_trade_count=5;suppressed_net=-15.29 | 5개 거래 제거 효과를 운영 승격 근거로 오해하지 않는다. |
| month_of_year_specificity_watch(월중 특이성 관찰) | watch | parent_suppress_months=12;parent_suppress_hours=21 | December(12월) 계절성 수리가 다른 구간에서 깨지는지 MT5/추가 탐색으로 확인한다. |
| no_package_authority_guard(패키지 권위 차단) | passed | new_mt5_execution=not_run; runtime_authority=not_claimed | precheck eligible(사전검사 적격)과 package authority(패키지 권위)를 분리한다. |

## Robustness Surface Review(강건성 표면 검토)

| review_id | value | detail | interpretation |
| --- | --- | --- | --- |
| surface_count_summary(표면 수 요약) | 809 | core_pass_rows=439;package_like_rows=37 | surface is broad enough for review(검토할 만큼 표면이 넓음) |
| selected_intervention_size(선택 개입 크기) | 5 | suppressed_net=-15.29;selected=bs02_late_year_parent_session_suppress__moy12__h21__side_long | small intervention is attractive but sample-risky(작은 개입은 매력적이나 표본 위험이 있음) |
| family_concentration(계열 집중) | 1 | bs02_late_year_parent_session_suppress | precheck should carry parent-session gate explicitly(사전검사는 부모 세션 게이트를 명시해야 함) |
| package_like_rank_01 | 351.568099272 | bs02_late_year_parent_session_suppress__moy12__h21__side_long;net=1063.14;pf=1.4220035161;density=3.0720720721;suppressed=5 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_02 | 351.568099272 | bs02_late_year_parent_session_suppress__moy12__h21__side_both;net=1063.14;pf=1.4220035161;density=3.0720720721;suppressed=5 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_03 | 339.44843126 | bs02_late_year_parent_session_suppress__moy12__h19_21__side_long;net=1069.6;pf=1.4285654756;density=3.0510510511;suppressed=12 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_04 | 339.44843126 | bs02_late_year_parent_session_suppress__moy12__h19_21__side_both;net=1069.6;pf=1.4285654756;density=3.0510510511;suppressed=12 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_05 | 337.747624506 | bs02_late_year_parent_session_suppress__moy12__h19__side_long;net=1054.31;pf=1.4194241877;density=3.0660660661;suppressed=7 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_06 | 337.747624506 | bs02_late_year_parent_session_suppress__moy12__h19__side_both;net=1054.31;pf=1.4194241877;density=3.0660660661;suppressed=7 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_07 | 335.38183584 | bs02_late_year_parent_session_suppress__moy12__h20_21__side_long;net=1057.91;pf=1.4207776639;density=3.0540540541;suppressed=11 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_08 | 335.38183584 | bs02_late_year_parent_session_suppress__moy12__h20_21__side_both;net=1057.91;pf=1.4207776639;density=3.0540540541;suppressed=11 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_09 | 330.530338324 | bs02_late_year_parent_session_suppress__moy12__h18_21__side_long;net=1062.27;pf=1.4260245179;density=3.036036036;suppressed=17 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_10 | 329.825135912 | bs02_late_year_parent_session_suppress__moy12__h19_20_21__side_long;net=1064.37;pf=1.4273414674;density=3.033033033;suppressed=18 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |
| package_like_rank_11 | 329.825135912 | bs02_late_year_parent_session_suppress__moy12__h19_20_21__side_both;net=1064.37;pf=1.4273414674;density=3.033033033;suppressed=18 | neighbor candidate for BU comparison(BU 비교용 이웃 후보) |

## Proxy/MT5 Diff(프록시/MT5 차이)

| comparison_id | mt5_net_profit | proxy_net_profit | net_diff_proxy_minus_mt5 | mt5_profit_factor | proxy_profit_factor | usability |
| --- | --- | --- | --- | --- | --- | --- |
| bs_proxy_vs_bk_mt5_runtime_probe(BS 프록시 대 BK MT5 런타임 탐침) | 959.64 | 1063.14 | 103.5 | 1.3820937835 | 1.4220035161 | usable_for_BU_precheck_handoff_not_runtime_authority(BU 사전검사 인계에는 사용 가능, 런타임 권위 아님) |

## BU Queue(BU 대기열)

| queue_rank | queue_id | action | success_criteria |
| --- | --- | --- | --- |
| 1 | bu01_materialize_session_gate_precheck_request | materialize MT5 precheck request for December h21 long suppression(12월 21시 롱 억제 MT5 사전검사 요청 물질화) | bundle/request records selected rule, hashes, and no-authority boundary(번들/요청이 선택 규칙, 해시, 무권위 경계를 기록) |
| 2 | bu02_attempt_narrow_mt5_strategy_tester_probe | attempt narrow MT5 Strategy Tester probe if runtime tooling supports the gate(런타임 도구가 게이트를 지원하면 좁은 MT5 전략 테스터 탐침 시도) | tester output, trade list, or exact blocker log exists(테스터 출력, 거래 목록, 또는 정확한 차단 로그 존재) |
| 3 | bu03_runtime_gap_or_overfit_repair_branch | if MT5 gap or gate support fails, convert blocker into repair seed(MT5 간극 또는 게이트 지원 실패 시 차단을 수리 씨앗으로 변환) | reject, repair, or package-precheck evidence is explicit(거절/수리/패키지 사전검사 근거가 명시) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_review_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/package_precheck_decision.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/overfit_review.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/proxy_mt5_diff_review.csv | BS review(BS 검토)를 KPI, 과적합, MT5 차이로 분리했다. |
| source_gate_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BS/required_gate_coverage_audit.csv | BS 산출물의 gate(게이트)가 통과된 상태에서만 리뷰했다. |
| kpi_review_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/package_precheck_decision.csv | stress clear(압박 해소)와 precheck eligibility(사전검사 적격)를 확인했다. |
| overfit_watch_recorded | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/overfit_review.csv | low-sample/month-specific risk(소표본/월 특이 위험)를 다음 검증 조건으로 남겼다. |
| proxy_mt5_diff_recorded | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/proxy_mt5_diff_review.csv | proxy(프록시)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않게 했다. |
| next_external_verification_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/run364BU_mt5_precheck_queue.csv | 다음 작업을 MT5 외부 검증 시도로 직접 연결했다. |
| precheck_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/claim_boundary_receipt.json | precheck eligible(사전검사 적격)을 operating promotion(운영 승격)으로 올리지 않았다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/required_gate_coverage_audit.csv | 필수 gate(게이트)와 산출물 연결을 확인했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BT/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단했다. |

## Boundary(경계)

BT is review only(BT는 검토 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
