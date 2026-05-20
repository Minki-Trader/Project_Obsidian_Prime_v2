# Stage267 Run267W True Internal Ablation Score Table Materialization(267단계 267W 진짜 내부 제거 점수표 물질화)

- action(행동): run267V(267V 실행)의 raw feature surface(원시 피처 표면)에서 24개 feature order(피처 순서)를 만들고 supervised EBM(지도학습 EBM) score table(점수표)을 재학습했다.
- effect(효과): 다음 MT5(MetaTrader 5, 메타트레이더5) 실행은 proxy score extension(대체 점수 확장)이 아니라 실제 내부 feature removal/replacement(피처 제거/대체) 표면을 쓴다.
- status(상태): `run267W_true_internal_ablation_score_tables_materialized_execution_pending`
- judgment(판정): `score_tables_materialized_execution_pending_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267W(267W 실행)는 24개 후보-시험 조합을 모두 새 score table(점수표)로 만들었다. 2024년 결과를 정답으로 쓰지 않았고, label_v1/split_v1(라벨 v1/분할 v1) 학습 표면만 썼다.
효과(effect, 효과)는 다음 MT5(MetaTrader 5, 메타트레이더5) batch(묶음 실행)에서 후보가 진짜로 특정 feature family(피처 계열)를 잃어도 버티는지 볼 수 있게 된 것이다.

## Materialization Summary(물질화 요약)

- candidates(후보): `5`
- variants(변형): `24`
- attempts queued(대기 시도): `48`
- training rows(학습 표면 행): `46650`
- runtime rows per variant(변형별 런타임 행): `11651`
- parity passed(동등성 통과): `24/24`
- surface alignment passed(표면 정렬 통과): `24/24`
- corrected direct compressed rows(직접 압축 행 보정): `3`

## Boundary(경계)

- MT5 execution(MT5 실행): `not_executed`
- trading KPI(거래 핵심 성과 지표): `not_claimed`
- balance/equity curve(잔액/평가금 곡선): `pending_MT5`
- time-slice KPI(시간 구간 핵심 성과 지표): `pending_MT5`
- candidate selection(후보 선정): `none`

## Outputs(산출물)

- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/true_internal_ablation_variant_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/runtime_contract.csv`
- score_table_parity(점수표 동등성): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/score_table_parity_check.csv`
- surface_alignment(표면 정렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/surface_alignment_check.csv`
- schema_correction(스키마 보정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/schema_correction_audit.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/attempts.csv`

## Next Action(다음 행동)

- next_action(다음 행동): `run267X_execute_true_internal_ablation_score_table_mt5_batch`.
- effect(효과): 물질화된 48개 MT5(MetaTrader 5, 메타트레이더5) 시도를 실행해 거래 목록, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)를 확인한다.
