# Stage267 Run267AC Noncalendar State Guard Score Table Materialization(267단계 267AC 비달력 상태 방어 점수표 물질화)

- action(행동): run267AB(267AB 실행)의 guard queue(방어 큐)를 run267W(267W 실행)의 true internal score table(진짜 내부 점수표)에 soft guard score(부드러운 방어 점수)로 붙였다.
- effect(효과): calendar literal filter(달력 직접 필터)를 쓰지 않고, 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 약한 상태가 덜 깨지는지 확인할 수 있다.
- status(상태): `run267AC_noncalendar_state_guard_score_tables_materialized_execution_pending`
- judgment(판정): `state_guard_score_tables_materialized_execution_pending_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AB(267AB 실행)는 약한 거래가 자주 모이는 market state(시장 상태)를 찾았다. run267AC(267AC 실행)는 그 상태를 바로 잘라내지 않고, 모델 점수표(score table, 점수표)에 작은 flat-bias(무거래 쪽 가중)로 붙였다.
Effect(효과): 거래 수가 무너지는지, 손실이 다른 구간으로 옮겨가는지, 실제로 약한 구간이 나아지는지는 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 봐야 한다.

## Materialization Summary(물질화 요약)

- candidates(후보): `5`
- variants(변형): `7`
- attempts queued(대기 시도): `14`
- neutral parity passed(중립 동등성 통과): `7/7`
- surface alignment passed(표면 정렬 통과): `7/7`
- context missing rows(문맥 누락 행): `0`

## Boundary(경계)

- MT5 execution(MT5 실행): `not_executed`
- trading KPI(거래 핵심 성과 지표): `not_claimed`
- balance/equity curve(잔액/평가금 곡선): `pending_MT5`
- candidate selection(후보 선택): `none`
- ONNX(ONNX): `not_reviewed`

## Outputs(산출물)

- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/noncalendar_state_guard_variant_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/runtime_contract.csv`
- guard_diagnostics(방어 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/guard_state_diagnostics.csv`
- neutral_parity(중립 동등성): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/neutral_guard_score_parity_check.csv`
- surface_alignment(표면 정렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/surface_alignment_check.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AC/noncalendar_state_guard_score_table_materialization/attempts.csv`

## Next Action(다음 행동)

- next_action(다음 행동): `run267AD_execute_noncalendar_state_guard_score_table_mt5_batch`.
- effect(효과): 14개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행해서 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)를 확인한다.
