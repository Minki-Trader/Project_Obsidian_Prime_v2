# Stage267 Run267ER Tenth Follow-Up/Prune Design(267단계 267ER 10차 후속/가지치기 설계)

- status(상태): `run267ER_runtime_gap_aware_tenth_followup_or_prune_design_completed`
- source_run(원천 실행): `run267EQ_stage267_runtime_gap_aware_tenth_followup_or_prune_balance_timeslice_trade_quality_review_v1`
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267EQ_runtime_gap_aware_tenth_followup_or_prune_balance_timeslice_trade_quality_review.md`
- candidate_profile_rows(후보-프로필 행): `8`
- init_failure_groups(초기화 실패 묶음): `4`
- negative_slices(음수 구간): `69`
- materialization_queue(물질화 대기열): `5`
- active_queue_rows(활성 대기열 행): `4`
- aggressive_rows(공격형 행): `1`
- next_action(다음 행동): `run267ES_materialize_runtime_gap_aware_tenth_followup_or_prune_queue`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267EQ(267EQ 실행)는 후보를 뽑은 결과가 아니다. 8개 KPI(핵심 성과 지표)를 읽었지만 4개 init/runtime gap(초기화/런타임 공백), 69개 negative slice(음수 구간), 낮은 PF(profit factor, 수익 팩터) 양수 행이 같이 남았다.
따라서 run267ER(267ER 실행)는 다음 실행을 세 갈래로 나눈다. 첫째, 런타임 인계가 막힌 행은 성능 실패가 아니라 handoff triage(인계 진단)로 본다. 둘째, 2026.04 공통 손상은 달력 필터가 아니라 shared adverse-state feature(공유 불리 상태 피처)로 본다. 셋째, 방어 필터만 쌓지 않도록 precheck(사전검사) 뒤 aggressive non-filter experiment(공격형 비필터 실험)를 한 번 보존한다.

## Queue(대기열)

- `q01_runtime_handoff_gap_bounded_triage` `P0` `s258_stc;s264_aih` `active`: 성능 판단 전에 repair(수리) 또는 prune(가지치기) 경계를 정한다.
- `q02_202604_shared_sell_fragility_pivot` `P0` `s264_aih;s264_lc;s262_lih;s264_aia` `active`: 같은 월 필터 반복 대신 시장 상태 피처가 유효한지 판단한다.
- `q03_s262_s264_aia_signature_collapse_audit` `P1` `s262_lih;s264_aia` `active`: 두 후보를 독립 후보로 셀지, 중복 대조로 낮출지 판단한다.
- `q04_validation_positive_low_pf_watch` `P1` `s264_aih;s262_lih;s264_aia` `held`: 양수 숫자만 보고 ONNX(온엑스) 방향으로 건너뛰지 않게 한다.
- `q05_aggressive_experiment_after_handoff_fix` `P2_aggressive` `s258_stc;s264_aih` `conditional_active`: 연구가 방어 필터 누적에 갇히는지 막는다.

## Prune Guard(가지치기 가드)

- `pr01_no_baseline_from_run267EQ` `no_candidate_selection(후보 선택 없음)`: run267EQ는 8개 KPI와 4개 init/runtime gap을 분리했지만 최종 후보 근거가 아니다.
- `pr02_no_same_month_filter_stack` `no_calendar_only_filter_stack(달력 단독 필터 누적 금지)`: 2026.04 손실만 가리는 필터는 구조를 배우지 못한다.
- `pr03_no_duplicate_independent_counting` `duplicate_signature_guard(중복 서명 가드)`: 동일 KPI signature(핵심 성과 지표 서명)를 독립 후보 근거로 세면 과장된다.
- `pr04_no_raw_aggressive_without_precheck` `precheck_before_aggressive(공격 전 사전검사)`: init/runtime gap이 남은 상태에서 공격형 성능을 읽으면 무효다.
- `pr05_no_onnx_from_review` `no_onnx_readiness(온엑스 준비 없음)`: Adapter(어댑터), 안정성, 기간별/구간별 검증, runtime reproduction(런타임 재현), ONNX parity(온엑스 동등성) 근거가 아직 부족하다.

## Boundary(경계)

- 이 설계는 exploratory design(탐색 설계)이다. 후보 선택, 연구 기준 후보 선택, ONNX(온엑스) 준비, Goal Achieve(목표 달성)를 주장하지 않는다.
- run267ES(267ES 실행)는 물질화 단계이며, 새 MT5(MetaTrader 5, 메타트레이더5) 성능 근거는 이후 runtime probe(런타임 탐침)에서만 생긴다.

## Artifacts(산출물)

- feature_engineering_blueprint(피처 엔지니어링 청사진): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/feature_engineering_blueprint.csv`
- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/branch_decision_matrix.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/materialization_queue.csv`
- runtime_handoff_triage_plan(런타임 인계 진단 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/runtime_handoff_triage_plan.csv`
- identity_audit_plan(정체성 감사 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/identity_audit_plan.csv`
- aggressive_reentry_plan(공격형 재진입 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/aggressive_reentry_plan.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/experiment_design_receipt.csv`
- evidence_map(근거 지도): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/evidence_map.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/result_judgment.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/gate_audit.csv`
- run_manifest(실행 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/run_manifest.json`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/lineage.json`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ER/runtime_gap_aware_tenth_followup_or_prune_design/review_result.json`
- report(보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267ER_runtime_gap_aware_tenth_followup_or_prune_design.md`
