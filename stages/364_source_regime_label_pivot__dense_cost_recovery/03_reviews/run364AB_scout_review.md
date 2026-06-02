# run364AB scout review(364AB 정찰 검토)

## Current truth(현재 진실)

- run_id(실행 ID): `run364AB_review_density_side_balance_cost_session_stress_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AA_train_density_side_balance_cost_session_stress_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AC_materialize_pf_dd_near_miss_density_bridge_without_db_v1`
- judgment(판정): `negative_for_package_positive_near_miss_pf_dd_density_bridge_seed_no_authority`
- package_decision(패키지 결정): `no_package_strict_pass_zero(패키지 없음, 엄격 통과 0)`
- strict_pass_rows(엄격 통과 행): `0`
- near_miss_rows(근접 실패 행): `2`
- best_pf_queue(최고 PF 대기열): `stress_zone_3` / PF `1.2758061959` / density(밀도) `2.984984985` / DD(낙폭) `-142.323`
- runtime_authority(런타임 권위): `not_claimed`

## Top review rows(상위 검토 행)

| queue_id | review_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count |
| --- | --- | --- | --- | --- | --- | --- |
| stress_zone_3 | near_miss_density_bridge_seed(밀도 연결 수리 씨앗) | 840.192 | 1.2758061959 | 2.984984985 | -142.323 | 112.0 |
| short050_hour16_soft_guardrail | reject_density_floor(밀도 하한 탈락) | 794.636 | 1.2706352591 | 2.8738738739 | -172.391 | 6.0 |
| stress_zone_4 | near_miss_density_bridge_seed(밀도 연결 수리 씨앗) | 808.044 | 1.2584924377 | 3.042042042 | -142.323 | 131.0 |
| short055_quality_probe | reject_density_floor(밀도 하한 탈락) | 752.15 | 1.2573454567 | 2.8558558559 | -172.391 | 0.0 |
| short050_quality_probe | reject_density_floor(밀도 하한 탈락) | 749.025 | 1.2519477365 | 2.8828828829 | -172.391 | 8.0 |
| adx38_density_counterfactual | density_only_watch(밀도만 관찰) | 798.689 | 1.2345298327 | 3.1741741742 | -142.197 | 130.0 |
| baseline_replay_control | density_only_watch(밀도만 관찰) | 771.564 | 1.2218406503 | 3.2462462462 | -155.007 | 129.0 |
| hour16_soft_guardrail | density_only_watch(밀도만 관찰) | 744.707 | 1.2194362013 | 3.1741741742 | -192.655 | 106.0 |

## Near miss candidates(근접 실패 후보)

| queue_id | review_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown |
| --- | --- | --- | --- | --- | --- |
| stress_zone_3 | near_miss_density_bridge_seed(밀도 연결 수리 씨앗) | 840.192 | 1.2758061959 | 2.984984985 | -142.323 |
| stress_zone_4 | near_miss_density_bridge_seed(밀도 연결 수리 씨앗) | 808.044 | 1.2584924377 | 3.042042042 | -142.323 |

## Positive clues(긍정 단서)

| clue_id | evidence | kpi_read | effect(효과) |
| --- | --- | --- | --- |
| density_recovered_but_pf_dd_not_repaired(밀도 회복, PF/DD 미수리) | maxhold6_density_control__ps0_45__adx40_0__hold6__none | net=771.423; pf=1.2175571938; density=3.7957957958; dd=-168.999 | maxhold6 density control(최대보유 6 밀도 대조)은 운영 패키지가 아니라 밀도 회복 단서로만 쓴다. |
| stress_zone_3_near_density_floor(3번 압박 구간 밀도 하한 근접) | stress_zone_3__ps0_45__adx40_0__hold8__entry_month2025_03 | best_pf_queue=stress_zone_3; pf=1.2758061959; density=2.984984985; dd=-142.323 | PF/DD(수익 팩터/낙폭)는 좋아졌지만 density(밀도)가 살짝 부족한 조합을 다음 offensive repair(공격 수리) 씨앗으로 쓴다. |
| density_ceiling_requires_quality_filter(밀도 상단은 품질 필터 필요) | maxhold6_density_control__ps0_45__adx40_0__hold6__none | top_density_queue=maxhold6_density_control; density=3.7957957958; pf=1.2175571938; dd=-168.999 | 거래수를 늘리는 행동(action, 행동)은 PF/DD(수익 팩터/낙폭) 압박을 같이 가져오므로 quality bridge(품질 연결)가 필요하다. |

## Failure memory(실패 기억)

| failure_id | evidence | kpi_read | constraint_for_next(다음 제약) |
| --- | --- | --- | --- |
| strict_pass_zero(엄격 통과 0) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/cost_session_guardrail_proxy_scout_surface.csv | strict_pass_rows=0 | no MT5 package until PF/DD/density/short balance pass together(PF/DD/밀도/숏 균형 동시 통과 전 MT5 패키지 금지) |
| maxhold6_worse_than_baseline_pf_dd(최대보유 6 기준 대비 PF/DD 악화) | maxhold6_density_control__ps0_45__adx40_0__hold6__none | pf_delta=-0.0042834565; dd_delta=-13.992; net_delta=-0.141 | do not promote density-only selection(밀도만 좋은 선택 승격 금지) |
| account_dd_soft_stop_overkills_density(계좌 낙폭 소프트스톱 밀도 과도 감소) | prevdd_2pct_soft_stop / prevdd_5pct_soft_stop | trade_count collapsed to 5 or 40(거래수 5 또는 40으로 붕괴) | avoid hard account-state stops as primary repair(계좌 상태 하드 중단을 주 수리로 쓰지 않음) |

## Next queue(다음 대기열)

| queue_id | seed_variant_id | hypothesis(가설) | required_control(필수 대조) |
| --- | --- | --- | --- |
| density_bridge_from_stress_zone_3(3번 압박 구간 밀도 연결) | stress_zone_3__ps0_45__adx40_0__hold8__entry_month2025_03 | restore only timestamp-safe low-risk trades around the 2025-03 block to lift density above 3/day while preserving PF/DD(2025-03 차단 주변 저위험 거래만 복원해 밀도 3 이상과 PF/DD 보존을 동시에 노린다) | no trade splitting(거래 쪼개기 금지); compare against baseline_replay_control and stress_zone_3(기준 재생과 3번 압박 구간 비교) |
| stress_zone_4_pf_lift(4번 압박 구간 PF 상승) | stress_zone_4__ps0_45__adx40_0__hold8__entry_month2025_03_sidelong | use month-long block plus selective short quality threshold to lift PF toward 1.30 without losing density(월별 롱 차단과 선택적 숏 품질 임계값으로 밀도 손실 없이 PF 1.30에 접근한다) | long/short balance audit(롱/숏 균형 감사); density floor >=3/day(밀도 일 3회 이상) |
| adx38_stress_blend(ADX38 압박 혼합) | adx38_density_counterfactual | blend ADX38 density recovery with stress-zone DD cuts using timestamp-safe entry filters(ADX38 밀도 회복과 압박 구간 낙폭 절감을 시점 안전 진입 필터로 섞는다) | baseline_replay_control, adx38 only, stress block only(기준 재생, ADX38 단독, 압박 차단 단독) |

## Gate audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AB/final_decision.json | run364AB review(364AB 검토) 범위를 닫는다. |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AB/input_manifest.csv | run364AA 산출물과 gate(게이트)를 확인한다. |
| proxy_scout_review_gate(프록시 정찰 검토 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AB/surface_review.csv | 16개 surface row(표면 행)를 판정한다. |
| strict_pass_boundary_gate(엄격 통과 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AB/strict_pass_audit.csv | strict pass 0(엄격 통과 0)을 패키지 금지로 연결한다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AB/performance_attribution_receipt.json | PF/DD/density(수익 팩터/낙폭/밀도) 차이를 귀속한다. |
| next_queue_gate(다음 대기열 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AB/run364AC_repair_queue.csv | run364AC repair queue(수리 대기열)를 만든다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AB/artifact_lineage_receipt.json | 입력/출력 경로와 hash(해시)를 연결한다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AB/claim_boundary_receipt.json | runtime authority(런타임 권위)를 주장하지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AB/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Claim boundary(주장 경계)

`research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 review(검토)는 package(패키지), MT5 runtime probe(MT5 런타임 탐침), operating promotion(운영 승격)을 열지 않고, Stage364(364단계) 안에서 다음 offensive repair(공격 수리) 재료만 남긴다.
