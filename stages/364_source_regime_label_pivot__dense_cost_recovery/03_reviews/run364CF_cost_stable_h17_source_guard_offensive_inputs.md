# run364CF cost-stable h17 source guard offensive inputs(364CF 비용 안정 17시 원천 가드 공격 입력)

## Result(결과)

- status(상태): `completed_stage364CF_cost_stable_h17_source_guard_offensive_inputs_materialized_open_cg_no_authority`
- judgment(판정): `experiment_design_materialized_cost_stable_h17_source_guard_scout_inputs_no_authority`
- decision(결정): `stage364CF_open_run364CG_cost_stable_h17_source_guard_offensive_scout`
- next(다음): `run364CG_train_cost_stable_h17_source_guard_offensive_scout_without_db_v1`
- gate(게이트): `7/7`

## Action(행동)

Action(행동): CE review(CE 리뷰)의 CD02 current-session semantics(CD02 현재 세션 의미), CD02-CD01 zero gross/swap/net delta(총손익/스왑/순수익 차이 0), CD02-CD03 h17 overlay lift(17시 오버레이 우위)를 CG scout(CG 정찰) 입력으로 materialize(구체화)했다.

Effect(효과): 다음 탐색은 stale BX3 swap memory(낡은 BX3 스왑 기억)를 기준으로 삼지 않고, trade splitting(거래 쪼개기) 없이 source quality/cost layer/session guard(원천 품질/비용 층/세션 가드)를 넓게 시험한다.

## Parent Evidence(상위 근거)

| evidence_item | value | metric_1 | metric_1_value | metric_2 | metric_2_value | metric_3 | metric_3_value |
| --- | --- | --- | --- | --- | --- | --- | --- |
| reviewed_best_variant(리뷰된 최선 변형) | cd02_ca01_clone_current_session | net_profit | 997.49 | profit_factor | 1.4 | trade_count | 1008 |
| swap_stability_closed(스왑 안정 닫힘) | cd02_vs_cd01_zero_delta | gross_delta | 0.0 | swap_delta | 0.0 | net_delta | 0.0 |
| h17_overlay_value_preserved(17시 오버레이 가치 보존) | cd02_vs_cd03_positive_overlay_lift | net_lift | 41.09 | left_only_net | 50.53 | right_only_net | 9.44 |
| source_bucket_long_threshold | long_threshold | trade_count | 903 | net_profit | 871.13 | profit_factor_gross | 1.4046 |
| source_bucket_native_short_threshold | native_short_threshold | trade_count | 66 | net_profit | 57.17 | profit_factor_gross | 1.2347 |
| source_bucket_synthetic_short_overlay | synthetic_short_overlay | trade_count | 39 | net_profit | 69.19 | profit_factor_gross | 1.6364 |

## Stability Transfer(안정 의미 인계)

| audit_item | status | observed | effect |
| --- | --- | --- | --- |
| same_session_trade_path(동일 세션 거래 경로) | passed | common=1008, left_only=0, right_only=0 | CF can treat CD02 as current-session semantics(CF가 CD02를 현재 세션 의미로 취급 가능) |
| same_session_cost_delta(동일 세션 비용 차이) | passed | gross=0.0, swap=0.0, net=0.0 | swap table drift is not reused as alpha(스왑표 드리프트를 알파로 재사용하지 않음) |
| functional_set_drift(기능 설정 드리프트) | passed | functional_drift_count=0 | input design does not inherit hidden functional changes(입력 설계가 숨은 기능 변경을 상속하지 않음) |
| required_artifact_identity(필수 산출물 정체성) | passed | required_identity_failures=0 | feature/model/probability source remains tied(피처/모델/확률 원천 연결 유지) |
| report_metric_reconciliation(보고서 지표 대조) | passed | records=3 | headline KPI is tied to parsed report trades(대표 KPI를 파싱 거래와 연결) |

## Offensive Axes(공격 축)

| axis_id | broad_sweep | extreme_sweep | micro_search_gate |
| --- | --- | --- | --- |
| axis01_semantics_anchor(의미 기준축) | preserve CD02 CA01/BX3 current-session semantics(CD02 CA01/BX3 현재 세션 의미 보존) | compare against overlay-off native short control(오버레이 끈 기본 숏 대조와 비교) | CG must keep density >=3/day and no trade splitting(CG는 밀도 일 3회 이상과 거래 쪼개기 금지 유지) |
| axis02_h17_overlay_quality(17시 오버레이 품질축) | loose/mid/strict p_short and margin floors(느슨/중간/엄격 p_short 및 마진 하한) | overlay-only stress and overlay-off control(오버레이 전용 압박과 오버레이 끔 대조) | overlay lift must remain positive after cost stress(비용 압박 후에도 오버레이 우위 양수) |
| axis03_cost_layering(비용 층화축) | gross/net/swap score separation(총손익/순수익/스왑 점수 분리) | swap haircut and gross-only ranking stress(스왑 헤어컷 및 총손익 단독 순위 압박) | candidate cannot depend on one changed swap table(후보가 변한 스왑표 하나에 의존하면 안 됨) |
| axis04_trade_shape_no_split(거래 형태 무분할축) | hold/session/source quality without increasing trade slices(거래 조각 증가 없는 보유/세션/원천 품질) | strict short-balance floor and long hold stress(엄격 숏 균형 하한과 롱 보유 압박) | trade count must not be raised by splitting profit(수익을 나누는 거래수 증가 금지) |

## CG Queue(CG 대기열)

| queue_rank | candidate_id | variant_family | queue_status | h17_overlay_policy | cost_stress_policy |
| --- | --- | --- | --- | --- | --- |
| 1 | cg01_current_session_semantics_anchor | semantics_anchor(의미 기준) | ready_for_proxy_scout(프록시 정찰 준비) | keep_h17_overlay_as_is | none |
| 2 | cg02_h17_overlay_loose_margin_floor | h17_overlay_quality(17시 오버레이 품질) | ready_for_proxy_scout(프록시 정찰 준비) | synthetic_overlay_p_short_q25_margin_q25 | none |
| 3 | cg03_h17_overlay_mid_margin_floor | h17_overlay_quality(17시 오버레이 품질) | ready_for_proxy_scout(프록시 정찰 준비) | synthetic_overlay_p_short_q50_margin_q50 | none |
| 4 | cg04_h17_overlay_strict_margin_floor | h17_overlay_quality_extreme(17시 오버레이 품질 극단) | ready_for_proxy_scout(프록시 정찰 준비) | synthetic_overlay_p_short_q75_margin_q75 | none |
| 5 | cg05_overlay_off_native_short_control | negative_control(부정 대조) | ready_for_proxy_scout_control(프록시 정찰 대조 준비) | disable_synthetic_overlay | overlay_off |
| 6 | cg06_overlay_only_extreme_stress | extreme_overlay(극단 오버레이) | ready_for_proxy_scout(프록시 정찰 준비) | synthetic_overlay_only_for_h17_short_bucket | native_short_deprioritized |
| 7 | cg07_native_short_cost_firewall | cost_layering(비용 층화) | ready_for_proxy_scout(프록시 정찰 준비) | keep_synthetic_overlay | native_short_swap_cost_firewall |
| 8 | cg08_bad_overlay_month_guard_scout | regime_guard(국면 가드) | ready_for_proxy_scout(프록시 정찰 준비) | guard_negative_overlay_months=2025-02,2025-04,2025-06,2025-07,2025-08,2026-03 | month_guard_seed_only |
| 9 | cg09_best_open_hour_overlay_focus | session_focus(세션 집중) | ready_for_proxy_scout(프록시 정찰 준비) | focus_best_overlay_open_hour=17 | hour_focus_seed_only |
| 10 | cg10_gross_net_swap_layered_score | cost_layering(비용 층화) | ready_for_proxy_scout(프록시 정찰 준비) | rank_by_gross_net_swap_layered_score | swap_haircut_1x |
| 11 | cg11_short_balance_floor_guard | side_balance(방향 균형) | ready_for_proxy_scout(프록시 정찰 준비) | short_count_floor_100_and_overlay_kept | short_balance_guard |
| 12 | cg12_trade_shape_quality_no_split | trade_shape(거래 형태) | ready_for_proxy_scout(프록시 정찰 준비) | no_count_split_quality_surface | hold_and_source_quality_guard |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| work_packet_schema_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CF/work_packet.json | primary family and required gates are explicit(주 작업군과 필수 게이트 명시) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CF/input_manifest.csv | CE review artifacts are connected(CE 리뷰 산출물 연결) |
| data_integrity_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CF/data_integrity_audit.csv | time axis, duplicate check, leakage boundary are named(시간축/중복/누수 경계 명시) |
| stability_transfer_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CF/stability_transfer_audit.csv | CD02 current-session semantics can be transferred(CD02 현재 세션 의미 인계 가능) |
| offensive_queue_scope_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CF/run364CG_cost_stable_h17_source_guard_scout_queue.csv | broad and extreme scout queue is materialized(넓은/극단 정찰 대기열 구체화) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CF/required_gate_coverage_audit.csv | required gates are linked to closeout(필수 게이트를 종료 기록에 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CF/claim_boundary_receipt.json | no runtime authority or operating promotion claimed(런타임 권위나 운영 승격 주장 없음) |

## Boundary(경계)

CF is materialization only(CF는 구체화 전용). new model training(새 모델 학습), new MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
