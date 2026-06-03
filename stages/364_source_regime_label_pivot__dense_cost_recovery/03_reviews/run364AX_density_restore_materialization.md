# run364AX threshold edge density restore cost/session materialization(364AX 임계값 경계 밀도 복원 비용/세션 물질화)

## Current Truth(현재 진실)

- action(행동): run364AW(364AW 실행)의 MT5 runtime probe review(MT5 런타임 탐침 검토)를 run364AY(364AY 실행) scout queue(스카우트 대기열)로 materialize(물질화)했다.
- effect(효과): Stage364(364단계)를 새 Stage(단계)로 분기하지 않고, density restore(밀도 복원), short-side restore(숏 방향 복원), cost/session stress(비용/세션 압박)를 다음 실행 가능한 입력으로 묶었다.
- parent MT5 net/PF/trades(부모 MT5 순수익/수익 팩터/거래수): `878.55` / `1.36` / `971`
- parent density(부모 밀도): `2.9159159159` per business day(영업일당), floor(하한) `3.0`
- observed survival ratio(관측 생존 비율): `0.9117370892`
- claim_boundary(주장 경계): `research_development_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Queue(대기열)

| rank | queue_id | type | short_th | floor | proxy_density | est_mt5_density | impl |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ax01_density_buffer_floor075_controlled_expand | candidate(후보) | 0.455 | 0.00075 | 3.35 | 3.0540540541 | no |
| 2 | ax02_short_restore_ps452_floor075 | candidate(후보) | 0.452 | 0.00075 | 3.4 | 3.0990990991 | no |
| 3 | ax03_short_restore_ps450_floor050_stress | stress_candidate(압박 후보) | 0.45 | 0.0005 | 3.5 | 3.1921921922 | no |
| 4 | ax04_hour18_19_margin_guard_floor050 | candidate(후보) | 0.452 | 0.0005 | 3.38 | 3.0840840841 | yes_runtime_policy_if_not_in_replay(재생에 없으면 런타임 정책 구현 필요) |
| 5 | ax05_sep_dec_stress_label_no_delete | diagnostic_candidate(진단 후보) | 0.452 | 0.00075 | 3.35 | 3.0540540541 | no |
| 6 | ax06_hold_tail_dd_guard_diagnostic | guardrail(가드레일) | 0.452 | 0.00075 | 3.35 | 3.0540540541 | yes_account_state_guard_not_proxy_only(계좌 상태 가드는 프록시만으로 불가) |
| 7 | ax07_floor001_parent_control | control(대조군) | 0.455 | 0.001 | 3.1981981982 | 2.9159159159 | no |
| 8 | ax08_density_overstress_floor000 | stress_candidate(압박 후보) | 0.45 | 0.0 | 3.7 | 3.3723723724 | no |

## Guardrails(가드레일)

| guardrail | status | evidence | effect |
| --- | --- | --- | --- |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | queue has no split trades(대기열에 거래 쪼개기 없음) | 사용자 금지조건을 직접 닫는다. |
| top_n_absence_gate(top_n 부재 게이트) | passed | top_n forbidden for every row(모든 행 top_n 금지) | 랭킹으로 거래수를 인위 조절하지 않는다. |
| oos_threshold_lock_gate(OOS 임계값 잠금 게이트) | passed | OOS threshold selection forbidden(OOS 임계값 선택 금지) | 검증 표본으로 threshold(임계값)를 고르지 않는다. |
| timestamp_boundary_gate(시점 경계 게이트) | passed | entry-time known closed-bar only(진입 시점 닫힌 봉만 사용) | look-ahead bias(미래참조 편향)를 차단한다. |
| proxy_density_buffer_gate(프록시 밀도 완충 게이트) | passed | min_candidate_estimated_mt5_density=3.0540540541 | MT5 밀도 하한 생존 가능성을 후보 선별 앞에 둔다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| work_packet_schema_lint(작업 묶음 스키마 점검) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/work_packet.json | primary_family/skill/gates(주 작업군/스킬/게이트)를 기록한다. |
| input_manifest_gate(입력 목록 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/input_manifest.csv | AW 입력 근거의 path/hash(경로/해시)를 고정한다. |
| experiment_design_audit(실험 설계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/experiment_design_receipt.json | hypothesis/comparison/control(가설/비교/통제)을 닫는다. |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/data_integrity_receipt.json | 시점/라벨/분할 경계를 기록한다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/artifact_lineage_receipt.json | 입력과 출력 산출물을 연결한다. |
| policy_guardrail_matrix_gate(정책 가드레일 행렬 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/density_restore_guardrail_matrix.csv | trade splitting/top_n/timestamp(거래 쪼개기/top_n/시점)을 한 번에 검증한다. |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/run364AY_scout_queue.csv | AY scout(스카우트) 입력 queue(대기열)를 생성한다. |
| claim_boundary_gate(주장 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/claim_boundary_receipt.json | 운영 승격/런타임 권위/목표 달성을 주장하지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/required_gate_coverage_audit.csv | closeout(종료 기록)에 필수 게이트를 연결한다. |

## Judgment(판정)

Action(행동): AX는 새 model training(모델 학습), MT5 execution(MT5 실행), forward pass(전진 통과)를 하지 않았다.

Effect(효과): 이 결과는 materialization only(물질화 전용)이고, runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.

## Next Action(다음 행동)

`run364AY_train_threshold_edge_density_restore_cost_session_scout_without_db_v1`에서 이 queue(대기열)를 proxy scout(프록시 스카우트)로 실행한다. trade splitting(거래 쪼개기), top_n(top_n), OOS threshold selection(OOS 임계값 선택)은 계속 금지한다.
