# Stage267 Run267AW Pool-wide State Feature Engineering Second Follow-up Materialization(267단계 267AW 후보군 전체 상태 피처 엔지니어링 2차 후속 물질화)

- action(행동): run267AV(267AV 실행)의 next experiment queue(다음 실험 큐)를 run267AX(267AX 실행)에서 돌릴 Tier A(티어 A) MT5(MetaTrader 5, 메타트레이더5) 입력으로 물질화했다.
- effect(효과): Stage58(58단계) 이후 연구 단서를 다시 쓰되, 약한 월/요일 구멍을 달력 직접 필터로 덮지 않고 비달력 상태 압박(noncalendar state pressure, 비달력 상태 압박)으로 한 번 더 검증한다.
- status(상태): `run267AW_pool_wide_state_feature_engineering_second_followup_materialized_execution_pending`
- judgment(판정): `second_followup_materialized_execution_pending_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AU(267AU 실행)에서 숫자가 좋아 보인 후보도 2024-12(2024년 12월)와 Monday(월요일) 구멍이 남았다.
run267AV(267AV 실행)는 그래서 바로 후보를 고르지 않고, 한 번 더 넓은 상태 압박을 설계했다.
run267AW(267AW 실행)는 그 설계를 실제 파일로 만들었다. 아직 성과 판정은 아니고, 다음 MT5 실행 대기 상태다.

## Materialization Summary(물질화 요약)

- queue_rows(큐 행): `8`
- ready_queue_rows(준비 큐 행): `8`
- candidates(후보): `5`
- variants(변형): `8`
- Tier A attempts(티어 A 시도): `8`
- model_pressure_audit passed(모델 압박 감사 통과): `8/8`
- route_gap_rows(라우팅 공백 행): `1`
- failure_memory_rows(실패 기억 행): `7`

## Candidate Meaning(후보 의미)

- `s264_aih`: core challenger(핵심 도전자) 유지 여부를 2차 range/volatility(범위/변동성) 압박으로 본다.
- `s264_aia`: OOS anchor(표본외 앵커)는 Adapter watch(어댑터 관찰)일 뿐이며, 약한 구간이 줄어야 다음으로 간다.
- `s264_lc`, `s262_lih`: control audit(기준 감사) 전용이다. 좋은 후보 선택 근거가 아니다.
- `s258_stc`: stress challenger(압박 도전자)는 엄격한 가지치기/회수 gate(게이트)로만 본다.

## Tier Boundary(티어 경계)

- Tier A separate(Tier A 분리): `materialized`
- Tier B separate(Tier B 분리): `blocked_missing_true_fallback_manifest`
- actual routed total(실제 라우팅 전체): `blocked_missing_true_fallback_manifest`
- effect(효과): 중복 Tier A+B(Tier A+B 합산) 행을 진짜 fallback(대체) 생존성으로 오해하지 않는다.

## Outputs(산출물)

- pressure_design(압박 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/second_followup_pressure_design.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/second_followup_variant_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/runtime_contract.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/attempt_manifest.csv`
- model_pressure_audit(모델 압박 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/model_pressure_audit.csv`
- route_gap_audit(라우팅 공백 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/route_gap_audit.csv`
- tier_record_requirement_audit(티어 기록 필요 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/tier_record_requirement_audit.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/failure_memory.csv`

## Next Action(다음 행동)

- next_action(다음 행동): `run267AX_execute_pool_wide_state_feature_engineering_second_followup_mt5_batch`
- effect(효과): 8개 MT5(MetaTrader 5, 메타트레이더5) Tier A(티어 A) 시도를 실행한 뒤 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 다시 본다.
