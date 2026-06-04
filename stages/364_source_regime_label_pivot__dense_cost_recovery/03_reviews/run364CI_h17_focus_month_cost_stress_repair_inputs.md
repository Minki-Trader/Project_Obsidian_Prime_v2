# run364CI h17 focus month cost stress repair inputs(364CI 17시 집중 월/비용 압박 수리 입력)

## Current Truth(현재 진실)

- status(상태): `completed_stage364CI_h17_focus_month_cost_stress_repair_inputs_materialized_open_cj_no_authority`
- judgment(판정): `experiment_design_materialized_h17_focus_month_cost_stress_repair_inputs_no_authority`
- next run(다음 실행): `run364CJ_train_h17_focus_month_cost_stress_repair_scout_without_db_v1`
- queue rows(대기열 행): `16`
- reviewed seed(검토 씨앗): `cg09_best_open_hour_overlay_focus`
- reviewed KPI(검토 핵심 성과 지표): net/PF/density/shorts(순수익/수익 팩터/밀도/숏) `1001.5` / `1.3999745705` / `3.2070063694` / `104`
- bad months(나쁜 월): `['2025-08', '2025-12']`
- stress delta(압박 차이): `-1.13`

## Action And Effect(행동과 효과)

Action(행동): CH failure memory(CH 실패 기억)를 cost stress guard(비용 압박 가드), bad month regime guard(나쁜 월 국면 가드), short floor rescue(숏 하한 복원), MT5 precheck boundary(MT5 사전 점검 경계) 네 축으로 materialize(구체화)했다.

Effect(효과): CJ scout(CJ 정찰)가 no-split(무분할), no top_n(no top_n), no exact 2025 date filter(정확한 2025년 날짜 필터 없음) 조건으로 바로 replay(재생)할 수 있다.

## Failure Memory(실패 기억)

| failure_id | failure_type | axis | segment | net_profit | profit_factor | converted_constraint |
| --- | --- | --- | --- | --- | --- | --- |
| bad_month__2025-08 | month_stability_failure(월 안정성 실패) | open_month(진입 월) | 2025-08 | -1.43 | 0.98857093 | month-of-year/quarter guard only, no exact 2025 date memorization(월중/분기 가드만, 정확한 2025년 날짜 암기 금지) |
| bad_month__2025-12 | month_stability_failure(월 안정성 실패) | open_month(진입 월) | 2025-12 | -0.62 | 0.9961409187 | month-of-year/quarter guard only, no exact 2025 date memorization(월중/분기 가드만, 정확한 2025년 날짜 암기 금지) |
| cost_haircut_selected_delta | cost_stress_watch(비용 압박 관찰) | swap_haircut(스왑 헤어컷) | selected_candidate(선택 후보) | 1001.5 | 1.3999745705 | stress_adjusted_net_delta must clear zero before MT5 package(압박 조정 순수익 차이가 0 이상일 때만 MT5 패키지) |
| sparse_synthetic_overlay_positive_but_thin | thin_positive_source(얇은 긍정 원천) | source_bucket(원천 버킷) | synthetic_short_overlay | 73.2 | 1.6990736319 | synthetic overlay clue must keep short_count>=100 and source balance(합성 오버레이 단서는 숏 100개 이상과 원천 균형 필요) |

## Repair Axes(수리 축)

| axis_id | hypothesis | changed_variables | success_criteria | failure_criteria |
| --- | --- | --- | --- | --- |
| ci01_cost_stress_guard | h17 focus can survive if cost stress is guarded(17시 집중은 비용 압박 가드를 붙이면 버틸 수 있다) | cost_stress_policy, native short hour firewall, stress delta floor(비용 압박 정책, 기본 숏 시간 방화벽, 압박 차이 하한) | stress_adjusted_net_delta>=0, PF>=parent, density>=3, short_count>=100 | stress delta remains negative or short floor breaks(압박 차이 음수 유지 또는 숏 하한 붕괴) |
| ci02_bad_month_regime_guard | bad month slices are regime-like and can be constrained without exact-year memorization(나쁜 월 조각은 국면형이며 정확한 연도 암기 없이 제약 가능) | month-of-year class, quarter class, late-year pressure class(월중 클래스, 분기 클래스, 연말 압박 클래스) | bad_month_count decreases without deleting a known exact month(알려진 특정 월 삭제 없이 나쁜 월 수 감소) | net lift disappears or exact-date filter is required(순수익 우위 소멸 또는 정확한 날짜 필터 필요) |
| ci03_short_floor_rescue | higher net CG variants can be rescued by restoring short_count>=100(순수익 높은 CG 변형은 숏 100개 이상 복원으로 회수 가능) | rescue source candidate, native short restore budget, quality floor(회수 원천 후보, 기본 숏 복원 예산, 품질 하한) | net_delta remains positive and short_count>=100(순수익 차이 양수 유지와 숏 100개 이상) | PF lift comes only from shrinking shorts below floor(PF 우위가 숏 하한 미만 축소에서만 나옴) |
| ci04_mt5_precheck_boundary | MT5 precheck should only open after proxy stress/source balance clears(MT5 사전 점검은 프록시 압박/원천 균형 통과 뒤에만 열어야 한다) | package readiness flags only(패키지 준비 플래그만) | CJ emits package candidates only when stress and source balance clear(CJ가 압박과 원천 균형 통과 시에만 패키지 후보 배출) | proxy-only lift is mistaken for runtime claim(프록시 우위를 런타임 주장으로 착각) |

## CJ Queue(CJ 대기열)

| queue_rank | candidate_id | axis_id | seed_candidate_id | cost_stress_policy | month_guard_policy | short_floor_policy |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | cj01_h17_focus_stress_delta_floor | ci01_cost_stress_guard | cg09_best_open_hour_overlay_focus | stress_delta_floor_ge_0 | none | preserve_short_floor_100 |
| 2 | cj02_h17_focus_native_hour_cost_firewall_soft | ci01_cost_stress_guard | cg09_best_open_hour_overlay_focus | native_short_hour17_20_soft_firewall | none | restore_native_short_if_below_100 |
| 3 | cj03_h17_focus_swap_negative_native_trim | ci01_cost_stress_guard | cg09_best_open_hour_overlay_focus | trim_negative_swap_native_only | none | short_floor_hard_guard |
| 4 | cj04_h17_focus_cost_anchor_control | ci01_cost_stress_guard | cg09_best_open_hour_overlay_focus | no_extra_cost_filter_control | none | preserve_short_floor_100 |
| 5 | cj05_month_of_year_08_overlay_soft_guard | ci02_bad_month_regime_guard | cg09_best_open_hour_overlay_focus | stress_delta_floor_ge_0 | month_of_year=08(월중=08) | preserve_short_floor_100 |
| 6 | cj06_quarter_q3_pressure_overlay_soft_guard | ci02_bad_month_regime_guard | cg09_best_open_hour_overlay_focus | stress_delta_floor_ge_0 | quarter=Q3(분기=Q3) | preserve_short_floor_100 |
| 7 | cj07_month_of_year_12_overlay_soft_guard | ci02_bad_month_regime_guard | cg09_best_open_hour_overlay_focus | stress_delta_floor_ge_0 | month_of_year=12(월중=12) | preserve_short_floor_100 |
| 8 | cj08_quarter_q4_pressure_overlay_soft_guard | ci02_bad_month_regime_guard | cg09_best_open_hour_overlay_focus | stress_delta_floor_ge_0 | quarter=Q4(분기=Q4) | preserve_short_floor_100 |
| 9 | cj09_cg07_native_short_cost_firewall_short_floor_rescue | ci03_short_floor_rescue | cg07_native_short_cost_firewall | inherit_source_cost_policy_with_stress_floor | none | restore_native_short_until_floor_100 |
| 10 | cj10_cg12_trade_shape_quality_no_split_short_floor_rescue | ci03_short_floor_rescue | cg12_trade_shape_quality_no_split | inherit_source_cost_policy_with_stress_floor | none | restore_native_short_until_floor_100 |
| 11 | cj11_cg08_bad_overlay_month_guard_scout_short_floor_rescue | ci03_short_floor_rescue | cg08_bad_overlay_month_guard_scout | inherit_source_cost_policy_with_stress_floor | none | restore_native_short_until_floor_100 |
| 12 | cj12_cg05_overlay_off_native_short_control_short_floor_rescue | ci03_short_floor_rescue | cg05_overlay_off_native_short_control | inherit_source_cost_policy_with_stress_floor | none | restore_native_short_until_floor_100 |
| 13 | cj13_combined_h17_month_cost_guard | ci04_mt5_precheck_boundary | cg09_best_open_hour_overlay_focus | stress_delta_floor_ge_0_and_native_cost_soft | month_of_year_or_quarter_soft_guard | preserve_short_floor_100 |
| 14 | cj14_package_precheck_gate_only | ci04_mt5_precheck_boundary | cg09_best_open_hour_overlay_focus | package_precheck_only | package_precheck_only | package_precheck_only |
| 15 | cj15_no_split_topn_forbidden_guardrail | ci04_mt5_precheck_boundary | cg09_best_open_hour_overlay_focus | guardrail_only | guardrail_only | guardrail_only |
| 16 | cj16_parent_cd02_anchor_replay | ci04_mt5_precheck_boundary | cd02_ca01_clone_current_session | parent_cost_anchor | none | parent_short_floor |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CI/run364CJ_h17_focus_month_cost_stress_repair_scout_queue.csv | CJ scout queue(CJ 정찰 대기열)가 충분히 materialized(구체화)됐다. |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CI/input_manifest.csv | CH/CG input artifacts(CH/CG 입력 산출물)가 연결됐다. |
| experiment_design_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CI/experiment_design_receipt.json | hypothesis/comparison/criteria(가설/비교/기준)가 기록됐다. |
| data_integrity_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CI/data_integrity_audit.csv | timestamp-safe/no-split/no-topn(시점 안전/무분할/no-topn)을 점검했다. |
| repair_axis_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CI/h17_focus_repair_axis_map.csv | CH의 네 CI 축이 모두 구체화됐다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CI/required_gate_coverage_audit.csv | 필수 gate(게이트)가 closeout(종료 기록)에 연결됐다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CI/claim_boundary_receipt.json | 운영 주장(operating claim, 운영 주장)을 하지 않았다. |

## Boundary(경계)

CI is materialization only(CI는 구체화 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
