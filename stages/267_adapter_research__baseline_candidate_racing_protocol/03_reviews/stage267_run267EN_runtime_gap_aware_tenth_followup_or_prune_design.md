# Stage267 Run267EN Tenth Follow-Up/Prune Design(267단계 267EN 10차 후속/가지치기 설계)

- status(상태): `run267EN_runtime_gap_aware_tenth_followup_or_prune_design_completed`
- source_run(원천 실행): `run267EM_stage267_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review_v1`
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267EM_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review.md`
- next_action(다음 행동): `run267EO_materialize_runtime_gap_aware_tenth_followup_or_prune_queue`
- parsed_candidate_profile_rows(파싱 후보 프로필 행): `8`
- parsed_init_runtime_gap_rows(파싱 초기화/런타임 공백 행): `4`
- source_followup_queue_rows(원천 후속 대기열 행): `5`
- materialization_queue(물질화 대기열): `5`
- aggressive_rows(공격 행): `1`
- prune_rows(가지치기 행): `4`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267EM(267EM 실행)는 숫자 1등을 고르라는 결과가 아니었다. 8개 KPI(핵심 성과 지표) 행 중 양수 행은 PF(수익 팩터)가 낮고, 2026.04 measured slice(측정 구간)는 여러 후보가 같이 음수였다.
따라서 run267EN(267EN 실행)는 같은 필터를 더 붙이지 않고, handoff gap(인계 공백), 2026.04 shared state(공유 상태), duplicate signature(중복 서명), aggressive non-filter experiment(공격형 비필터 실험)를 분리한다.

## Queue(대기열)

- `q01_runtime_handoff_gap_bounded_precheck` `P0` `s258_stc;s264_aih`: handoff gap(인계 공백)이 고칠 수 있는 실행 문제인지 먼저 분류하고, 고칠 수 없으면 가지치기한다.
- `q02_202604_shared_state_feature_pivot` `P0` `s264_aih;s264_lc;s262_lih;s264_aia`: 2026.04 shared state(공유 상태)를 같은 월 필터가 아니라 structural feature engineering(구조적 피처 엔지니어링) 질문으로 바꾼다.
- `q03_s262_s264_aia_signature_identity_audit` `P1` `s262_lih;s264_aia`: duplicate signature(중복 서명)가 실제 동일 표면인지 audit(감사)한 뒤 후보 역할을 다시 나눈다.
- `q04_validation_low_pf_wide_period_watch` `P1` `s264_aih;s262_lih;s264_aia`: positive validation(양수 검증) 행은 watch anchor(관찰 기준점)로만 두고 selected baseline(선택 기준 후보)으로 쓰지 않는다.
- `q05_aggressive_non_filter_reentry_after_precheck` `P2_aggressive` `s258_stc;s264_aih`: precheck(사전검사)가 통과한 뒤에만 aggressive non-filter experiment(공격형 비필터 실험)를 한 번 연다.

## Feature Blueprint(피처 청사진)

- `fb01_runtime_handoff_integrity_precheck` `s258_stc;s264_aih`: 시장 신호가 아니라 파일 인계, 초기화, 출력 공백이 성능 판독을 막는지 먼저 분리한다.
- `fb02_202604_shared_adverse_state` `s264_aih;s264_lc;s262_lih;s264_aia`: 2026.04가 후보별 임계값 문제가 아니라 공유 불리 상태인지 본다.
- `fb03_duplicate_signature_identity_receipt` `s262_lih;s264_aia`: 두 후보가 서로 다른 시장 의미를 잡은 것인지, 같은 표면을 다른 이름으로 본 것인지 확인한다.
- `fb04_aggressive_non_filter_reentry` `s258_stc;s264_aih`: 방어 필터 누적으로만 연구가 굳지 않도록, 인계 수리 뒤 공격형 비필터 실험을 한 번 연다.

## Prune Guard(가지치기 가드)

- `pr01_no_baseline_selection_from_low_pf_validation` `low_pf_validation_selection_pruned`: low PF validation(낮은 수익 팩터 검증)만으로 baseline selection(기준 후보 선택)을 하지 않는다.
- `pr02_no_same_month_filter_stack` `same_month_filter_stack_pruned`: same-month filter stack(같은 월 필터 누적)을 막고 shared-state feature(공유 상태 피처)로 전환한다.
- `pr03_no_duplicate_independent_counting` `duplicate_signature_independence_pruned`: duplicate signature(중복 서명)를 independent evidence(독립 근거)로 두 번 세지 않는다.
- `pr04_no_raw_aggressive_rerun_without_precheck` `raw_aggressive_rerun_pruned`: precheck(사전검사) 없이 raw aggressive rerun(원시 공격형 재실행)을 반복하지 않는다.

## Boundary(경계)

- 이 설계는 exploratory design(탐색 설계)이며 후보 선택, 연구 기준 후보 선택, ONNX(온엑스) 준비, Goal Achieve(목표 달성)를 주장하지 않는다.
- 다음 run267EO(267EO 실행)는 먼저 handoff precheck(인계 사전검사)를 물질화하고, 통과한 경우에만 공격형 비필터 실험을 연다.

## Artifacts(산출물)

- feature_engineering_blueprint(피처 엔지니어링 청사진): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/feature_engineering_blueprint.csv`
- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/branch_decision_matrix.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/materialization_queue.csv`
- runtime_handoff_triage_plan(런타임 인계 진단 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/runtime_handoff_triage_plan.csv`
- identity_audit_plan(정체성 감사 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/identity_audit_plan.csv`
- aggressive_reentry_plan(공격 재진입 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/aggressive_reentry_plan.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/experiment_design_receipt.csv`
- evidence_map(근거 지도): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/evidence_map.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/gate_audit.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EN/runtime_gap_aware_tenth_followup_or_prune_design/lineage.json`
