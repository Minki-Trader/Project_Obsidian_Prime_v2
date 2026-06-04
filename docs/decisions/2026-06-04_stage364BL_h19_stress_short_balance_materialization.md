# run364BL h19 stress short-balance materialization(364BL h19 압박 숏 균형 물질화)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364BL_materialize_h19_runtime_probe_stress_short_balance_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run364BK_review_h19_opposite_margin_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364BM_train_h19_stress_short_balance_proxy_scout_without_db_v1`
- judgment(판정): `materialization_completed_h19_stress_short_balance_scout_inputs_no_authority`
- parent MT5 net/PF/expectancy/trades/density(부모 MT5 순수익/수익 팩터/기대값/거래수/밀도): `959.64` / `1.38` / `0.95` / `1006` / `3.021021021`
- parent long/short/share(부모 롱/숏/비중): `907` / `99` / `0.0984095427`
- equity DD(평가손익 낙폭): `18.24%`
- claim_boundary(주장 경계): `research_development_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Action And Effect(행동과 효과)

Action(행동): BK MT5 runtime probe review(BK MT5 런타임 탐침 검토)를 forward/regime replay(전진/국면 재생), short-source restore(숏 원천 복원), equity DD/cost guardrail(평가손익 낙폭/비용 가드레일) 입력으로 materialize(물질화)했다.

Effect(효과): 긍정적인 net/PF/density(순수익/수익 팩터/밀도)는 보존하지만, short share(숏 비중)와 equity DD(평가손익 낙폭)가 닫히기 전에는 operating promotion(운영 승격)이나 runtime authority(런타임 권위)를 주장하지 않는다.

## Short Math(숏 계산)

- target short share(목표 숏 비중): `0.12`
- additional shorts needed if no long delete(롱 삭제 없을 때 필요한 추가 숏): `25`
- long removals needed if no new short(새 숏 없을 때 필요한 롱 제거): `181`
- density removable trade budget(밀도상 삭제 가능 거래 여유): `7`

## Forward/Regime Preview(전진/국면 미리보기)

| group_type | group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | stress_flags |
| --- | --- | --- | --- | --- | --- |
| quarter | 2025Q2 | 262 | 325.01 | 1.436436638 | stable_positive(안정 양수) |
| quarter | 2025Q4 | 223 | 247.8 | 1.433216783 | december_q4_watch(12월/Q4 감시) |
| quarter | 2026Q1 | 175 | 187.61 | 1.476276307 | stable_positive(안정 양수) |
| quarter | 2025Q1 | 169 | 121.38 | 1.280946209 | stable_positive(안정 양수) |
| quarter | 2025Q3 | 131 | 54.55 | 1.203173303 | stable_positive(안정 양수) |
| quarter | 2026Q2 | 46 | 23.29 | 1.231972112 | stable_positive(안정 양수) |
| month | 2025-12 | 62 | -28.99 | 0.830229562 | net_negative(순수익 음수);pf_thin(PF 얇음);expectancy_thin(기대값 얇음);december_q4_watch(12월/Q4 감시) |

## Short Source Plan(숏 원천 계획)

| axis_id | current_short_share | additional_shorts_needed_if_no_long_delete | long_removals_needed_if_no_new_short | proposed_use | judgment |
| --- | --- | --- | --- | --- | --- |
| short_balance_math(숏 균형 수학) | 0.0984095427 | 25 | 181 |  | new_short_source_required(새 숏 원천 필요) |
| short_quality_source(숏 품질 원천) |  |  |  | lower_short_probability_threshold_without_long_deletion(롱 삭제 없이 숏 확률 임계값 완화) |  |
| short_router_session_regime(숏 라우터 세션/국면) |  |  |  | session/month/regime router with entry-known fields only(진입 시점에 알려진 세션/월/국면 라우터) |  |

## Equity DD Guardrails(평가손익 낙폭 가드레일)

| axis_id | observed_value | threshold | stress_status | proposed_use |
| --- | --- | --- | --- | --- |
| equity_dd_headline(평가손익 낙폭 헤드라인) | 18.24 | 15.0 | stress_required(압박 필요) | runtime_equity_path_must_be_reprobed(런타임 평가손익 경로 재탐침 필요) |
| month_stress_2025-12 | -28.99 | net>=0 and PF>=1(순수익 0 이상 및 PF 1 이상) | month_stress_label(월 압박 라벨) | label_only_soft_guard_no_hard_delete(라벨 전용 소프트 가드, 강제 삭제 없음) |
| hold_bucket_stress_002_7_to_12_m5_calendar | 1.035696011 | PF>=1.1(PF 1.1 이상) | hold_bucket_thin_edge(보유 구간 얇은 우위) | diagnostic_guardrail_no_trade_split(진단 가드레일, 거래 쪼개기 없음) |

## BM Queue(BM 대기열)

| queue_rank | queue_id | idea_type | policy_family | success_criteria |
| --- | --- | --- | --- | --- |
| 1 | bm01_forward_quarter_replay_h19_guard_reference | runtime_verification(런타임 검증) | fixed_h19_guard_forward_like_replay(고정 h19 가드 전진 유사 재생) | no forward-like block net<0 and total density>=3/day(전진 유사 구간 순손실 없음 및 전체 밀도 일 3회 이상) |
| 2 | bm02_december_hour18_19_label_soft_guard | repair_control(수리/대조) | calendar_session_stress_label(달력/세션 압박 라벨) | PF>=1.35 and density>=3/day while equity DD proxy improves(PF 1.35 이상, 밀도 일 3회 이상, 평가손익 낙폭 프록시 개선) |
| 3 | bm03_short_source_router_ps0445_no_long_delete | offensive_exploration(공격 탐색) | short_source_restore(숏 원천 복원) | short share>=0.12 with at least 25 new short-like entries and density>=3/day(숏 비중 목표 및 새 숏 후보, 밀도 일 3회 이상) |
| 4 | bm04_short_router_session_regime_overlay | offensive_exploration(공격 탐색) | session_regime_short_router(세션/국면 숏 라우터) | short PF>=1.15 and combined PF>=1.35 without top_n(숏 PF 1.15 이상, 합산 PF 1.35 이상, top_n 없음) |
| 5 | bm05_equity_dd_hold_7to12_guardrail_diagnostic | repair_control(수리/대조) | equity_dd_hold_shape_diagnostic(평가손익 낙폭 보유형태 진단) | equity DD stress label improves without deleting profitable tail trades(수익성 있는 꼬리 거래 삭제 없이 평가손익 압박 개선) |
| 6 | bm06_runtime_package_gate_if_proxy_survives | runtime_verification(런타임 검증) | package_gate_after_proxy(프록시 이후 패키지 게이트) | proxy candidate preserves MT5 diff usability and has package-ready fixed parameters(프록시 후보가 MT5 차이 활용성과 고정 파라미터 보유) |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BL/run364BM_h19_stress_short_balance_scout_queue.csv | BL queue(BL 대기열), short math(숏 수학), DD stress(낙폭 압박)를 모두 산출했다. |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BL/source_runtime_probe_summary.csv | 부모 MT5 KPI(핵심 성과 지표)를 다음 탐색 입력 기준으로 보존했다. |
| skill_receipt_lint(스킬 영수증 점검) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BL/run_evidence_receipt.json | 실행 근거/실험 설계/데이터/모델/런타임 영수증을 만들었다. |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BL/data_integrity_receipt.json | 시점 안전과 미래 결과 사용 경계를 기록했다. |
| guardrail_matrix_gate(가드레일 행렬 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BL/stress_short_balance_guardrail_matrix.csv | 거래 쪼개기 금지, 밀도 여유, 시점 안전을 점검했다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BL/artifact_lineage_receipt.json | 입력/출력 해시와 소비자 BM을 연결했다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BL/claim_boundary_receipt.json | 운영 승격과 런타임 권위를 모두 닫았다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BL/required_gate_coverage_audit.csv | experiment_execution(실험 실행) 필수 게이트를 closeout(종료 기록)에 연결했다. |

## Boundary(경계)

BL은 materialization only(물질화 전용)이다. 새 model training(모델 학습), 새 MT5 execution(MT5 실행), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 not_claimed(주장 안 함)이다.
