# Stage267 Run267CM Follow-Up/Prune Design(267단계 267CM 후속/가지치기 설계)

- action(행동): run267CL(267CL 실행)의 follow-up review(후속 검토)를 branch decision(분기 판단), materialization queue(물질화 대기열), prune matrix(가지치기 행렬)로 바꿨다.
- effect(효과): 수익이 있는 두 후보를 성급히 고르지 않고, 같은 축 수리 루프를 끊고, 후보군 전체 상태 피처와 공격형 분기로 다음 실험을 연다.
- status(상태): `run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_completed`
- feature_blueprints(피처 청사진): `3`
- branch_decisions(분기 판단): `5`
- materialization_queue_rows(물질화 대기열 행): `4`
- prune_rows(가지치기 행): `4`
- failure_memory_rows(실패 기억 행): `4`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run267CN_materialize_pool_wide_shared_weakness_breakout_queue`

## Easy Read(쉬운 해석)

run267CL(267CL 실행)은 `s264_lc`와 `s264_aia`가 수익은 낼 수 있지만 Monday(월요일), 2024-12(2024년 12월), session_07_12(7-12 세션)에서 깊게 파인다는 것을 보여줬다. 그래서 이번 run267CM(267CM 실행)은 두 후보를 고르지 않는다.

핵심 판단은 두 가지다. 첫째, `s264_lc`와 `s264_aia`의 같은 축 repair(수리)는 여기서 끊고 control(대조)로만 남긴다. 둘째, 후보군 전체의 shared weakness(공유 약점)를 state interaction feature(상태 상호작용 피처)로 다시 열고, `s264_aih`는 aggressive shock-release reentry(공격형 충격 해소 재진입)로 강행한다.

## Branch Decisions(분기 판단)

| candidate(후보) | role(역할) | source profile(원천 프로필) | net(순수익) | DD%(손실폭) | decision(판단) | next use(다음 용도) |
| --- | --- | --- | ---: | ---: | --- | --- |
| `s264_aih` | core_challenger(핵심 도전자) | `not_in_run267CL_followup_scope(run267CL 후속 범위 밖)` |  |  | reopen_aggressive_challenger_blast(공격형 도전자 재개) | aggressive_shock_release_reentry_branch(공격형 충격 해소 재진입 분기) |
| `s264_lc` | defensive_control(방어 대조) | `controlled_impulse_dd_state_throttle` | 1207.3 | 17.62 | hold_control_prune_same_axis_repair(대조 보류, 같은 축 수리 가지치기) | defensive_control_for_shared_weakness_breakout(공유 약점 돌파 방어 대조) |
| `s262_lih` | validation_heavy(검증 중심) | `not_in_run267CL_followup_scope(run267CL 후속 범위 밖)` |  |  | retain_validation_heavy_control(검증 중심 대조 유지) | validation_damage_detector_for_new_features(새 피처 검증 손상 감지기) |
| `s264_aia` | oos_anchor(표본외 앵커) | `oos_anchor_impulse_pressure` | 1119.33 | 16.03 | retain_oos_anchor_watch_no_selection(표본외 앵커 관찰 유지, 선택 아님) | oos_anchor_control_for_shared_weakness_breakout(공유 약점 돌파 표본외 앵커 대조) |
| `s258_stc` | stress_challenger(압박 도전자) | `not_in_run267CL_followup_scope(run267CL 후속 범위 밖)` |  |  | stress_comparator_only_no_deep_repair(압박 비교 전용, 깊은 수리 없음) | stress_comparator_receipt(압박 비교 영수증) |

## Materialization Queue(물질화 대기열)

| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | success(성공 기준) |
| --- | --- | --- | --- | --- |
| `run267cn_q01_shared_monday_december_state_interaction` | `P0` | `s264_aih;s264_lc;s262_lih;s264_aia;s258_stc` | shared_weakness_state_breakout(공유 약점 상태 돌파) | Monday and 2024-12 improve by at least 30% while trade count stays useful(월요일과 2024-12가 30% 이상 완화되고 거래 수가 유지). |
| `run267cn_q02_s264_aih_aggressive_shock_release_reentry` | `P0` | `s264_aih` | aggressive_explosive_reentry(공격형 폭발 재진입) | net > 1200, PF >= 1.45, DD < 22%, trades > 300, Monday > -180(순수익 1200 초과, PF 1.45 이상, 손실폭 22% 미만, 거래 300 초과, 월요일 -180 초과). |
| `run267cn_q03_anchor_control_holdout_trace` | `P1` | `s264_lc;s264_aia` | anchor_control_holdout(앵커/대조 보류 추적) | new branches beat controls on weak-slice and curve metrics(새 분기가 약점 구간과 곡선 지표에서 대조를 이김). |
| `run267cn_q04_validation_and_stress_guardrails` | `P2` | `s262_lih;s258_stc` | guardrail_receipts(가드레일 영수증) | new feature queue names validation/stress failure conditions(새 피처 대기열이 검증/압박 실패 조건을 이름 붙임). |

## Prune Matrix(가지치기 행렬)

| prune(가지치기) | label(라벨) | affected(대상) | reopen(재개 조건) |
| --- | --- | --- | --- |
| `run267cm_p01_no_same_axis_third_repair` | no_same_axis_third_repair(같은 축 3차 수리 금지) | s264_lc controlled impulse DD state throttle; s264_aia OOS anchor impulse pressure | new state-interaction feature, not threshold polish(임계값 미세조정이 아닌 새 상태 상호작용 피처). |
| `run267cm_p02_no_literal_calendar_filter` | no_literal_calendar_filter(달력 직접 필터 금지) | Monday, 2024-12, session_07_12_report_time | calendar used only as attribution label, not permission rule(달력은 귀속 라벨로만 사용). |
| `run267cm_p03_no_headline_profit_selection` | no_headline_profit_selection(대표 수익 선택 금지) | run267CL profitable rows | balance/equity curve and time-slice review survive next pressure(다음 압박에서 잔액/평가금 곡선과 시간구간 검토가 버팀). |
| `run267cm_p04_no_onnx_adapter_claim` | no_onnx_or_adapter_claim(ONNX/어댑터 주장 금지) | run267CM design outputs | after R&D racing survivor, Adapter package, runtime reproduction, and ONNX parity evidence(연구개발 생존자, 어댑터 패키지, 런타임 재현, ONNX 동등성 근거 이후). |

## Failure Memory(실패 기억)

| memory(기억) | pattern(패턴) | affected(대상) | do not repeat(반복 금지) |
| --- | --- | --- | --- |
| `run267cm_m01_monday_cluster` | shared_monday_loss_cluster(공유 월요일 손실 군집) | s264_lc;s264_aia | do not add Monday-off filter(월요일 제외 필터 추가 금지) |
| `run267cm_m02_december_hole` | 2024_12_drawdown_hole(2024년 12월 손실 구멍) | s264_lc;s264_aia | do not tune a December-only threshold(12월 전용 임계값 튜닝 금지) |
| `run267cm_m03_session_07_12_sparse_loss` | sparse_session_loss(희소 세션 손실) | s264_lc;s264_aia | do not overfit sparse session count(희소 세션 수에 과적합 금지) |
| `run267cm_m04_tier_fallback_boundary` | duplicate_boundary_not_true_fallback(중복 경계, 진짜 대체 아님) | run267CL evidence boundary | do not call duplicate-boundary rows actual routed totals(중복 경계 행을 실제 라우팅 전체로 부르지 않음) |

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design`.
- judgment_label(판정 라벨): `exploratory_design_only(탐색 설계 전용)`.
- evidence_available(사용 가능 근거): run267CL(267CL 실행) review_result(검토 결과), candidate profile review(후보 프로필 검토), negative slice summary(음수 구간 요약).
- evidence_missing(누락 근거): run267CN(267CN 실행) materialization(물질화), MT5(MetaTrader 5, 메타트레이더5) execution(실행), 새 trade list(거래 목록), Adapter(어댑터), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.py`
- source_review_result(원천 검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/review_result.json`
- feature_blueprint(피처 청사진): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/feature_blueprint.csv`
- branch_decisions(분기 판단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/branch_decisions.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/materialization_queue.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/experiment_design_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/result_judgment.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/gate_audit.csv`
- run_manifest(실행 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/run_manifest.json`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/lineage.json`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CM/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/review_result.json`
