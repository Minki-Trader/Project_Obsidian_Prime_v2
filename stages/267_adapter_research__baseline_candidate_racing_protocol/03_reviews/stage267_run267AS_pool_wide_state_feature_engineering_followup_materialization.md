# Stage267 Run267AS Pool-wide State Feature Engineering Follow-up Materialization(267단계 267AS 후보군 전체 상태 피처 엔지니어링 후속 물질화)

- action(행동): run267AR(267AR 실행)의 next experiment queue(다음 실험 큐)를 run267AT(267AT 실행)에서 돌릴 수 있는 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.
- effect(효과): headline KPI(대표 핵심 성과 지표)가 좋은 후보를 바로 고르지 않고, Monday(월요일)와 2024-12(2024년 12월) 구멍을 비달력 상태 압박(noncalendar state pressure, 비달력 상태 압박)으로 다시 시험할 수 있다.
- status(상태): `run267AS_pool_wide_state_feature_engineering_followup_materialized_execution_pending`
- judgment(판정): `pool_wide_state_feature_engineering_followup_materialized_execution_pending_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AQ(267AQ 실행)에서는 숫자가 좋아 보여도 월요일과 2024년 12월에서 깊게 깨지는 후보가 많았다.
run267AR(267AR 실행)은 그래서 다음 큐를 만들었고, run267AS(267AS 실행)는 그 큐를 실제 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 입력으로 만들었다.
효과(effect, 효과): 이제 다음 run267AT(267AT 실행)에서 후보가 정말 덜 깨지는지 볼 수 있다. 아직 좋은 후보를 골랐다는 뜻은 아니다.

## Materialization Summary(물질화 요약)

- queue_rows(큐 행): `8`
- ready_queue_rows(준비된 큐 행): `8`
- candidates(후보): `5`
- variants(변형): `8`
- attempts queued(대기 시도): `16`
- model_pressure_audit passed(모델 압박 감사 통과): `8/8`
- candidate_role_pressure_rows(후보 역할 압박 행): `5`
- failure_memory_rows(실패 기억 행): `11`

## Candidate Meaning(후보 의미)

- `s264_aih`: core challenger(핵심 도전자)로 유지하되, range/volatility(범위/변동성) 압박에서 구멍이 줄어야 한다.
- `s264_aia`: OOS anchor(표본외 앵커) 관찰 후보지만, DD(drawdown, 손실폭)와 약한 구간이 편해야 한다.
- `s258_stc`: stress challenger(압박 도전자)라서 강하게 압박하고, 실패하면 가지치기해야 한다.
- `s264_lc`, `s262_lih`: control audit(통제 감사) 전용이다. 좋은 후보 선택 근거가 아니다.

## Boundary(경계)

- MT5 execution(MT5 실행): `not_executed`
- balance/equity curve(잔액/평가금 곡선): `pending_run267AT`
- trade quality(거래 품질): `pending_run267AT`
- candidate selection(후보 선택): `none`
- ONNX(ONNX): `not_reviewed`

## Outputs(산출물)

- pressure_design(압박 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/state_feature_followup_pressure_design.csv`
- materialization_queue(물질화 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/followup_materialization_queue.csv`
- followup_variant_manifest(후속 변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/followup_variant_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/runtime_contract.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/attempt_manifest.csv`
- model_pressure_audit(모델 압박 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/model_pressure_audit.csv`
- candidate_role_pressure(후보 역할 압박): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/candidate_role_pressure_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AS/pool_wide_state_feature_engineering_followup_materialization/failure_memory.csv`

## Next Action(다음 행동)

- next_action(다음 행동): `run267AT_execute_pool_wide_state_feature_engineering_followup_mt5_batch`
- effect(효과): 16개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행한 뒤 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 검토한다.
