# Stage267 run267BI Tester Profile No-BOM Handoff Repair(테스터 프로필 BOM 제거 인계 수리)

## Summary(요약)

- run_id(실행 ID): `run267BI_stage267_tester_profile_nobom_handoff_repair_v1`
- parent_run(상위 실행): `run267BG_stage267_adjacent_period_replacement_fresh_report_mt5_execution_v1`
- status(상태): `run267BI_tester_profile_nobom_handoff_repair_completed`
- external_profile_has_bom(외부 프로필 BOM 있음): `False`
- runtime_status(런타임 상태): `completed`
- report_status(보고서 상태): `completed`
- kpi_records(KPI 기록): `1`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BG(267BG 실행)에서 막힌 q02(큐 02)를 UTF-8 no BOM(UTF-8 BOM 없음) Tester profile(테스터 프로필)로 다시 실행했다.
Effect(효과): tester start(테스터 시작) 전 handoff(인계) 차단이 profile encoding(프로필 인코딩) 문제였는지 좁히고, 다음 aggressive tranche(공격형 묶음)가 같은 문제로 막히지 않게 한다.

## Boundary(경계)

- 이 실행은 handoff repair(인계 수리) 근거이며 candidate selection(후보 선택)이 아니다.
- true fallback(실제 대체)과 actual routed total(실제 라우팅 전체)은 route manifest(라우트 목록)가 생기기 전까지 차단 상태다.
- ONNX parity(ONNX 동등성)는 아직 시작하지 않는다.

## Artifacts(산출물)

- execution result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BI/tester_profile_nobom_handoff_repair/execution_result.json`
- profile encoding receipt(프로필 인코딩 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BI/tester_profile_nobom_handoff_repair/profile_encoding_receipt.csv`
- KPI records(KPI 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BI/tester_profile_nobom_handoff_repair/kpi_records.json`
- forensics(포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BI/tester_profile_nobom_handoff_repair/backtest_forensics.csv`
- next_action(다음 행동): `run267BJ_materialize_first_aggressive_pressure_tranche_with_nobom_profiles`

## KPI Snapshot(KPI 요약)

| net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | max_DD%(최대 손실폭 %) |
| ---: | ---: | ---: | ---: |
| 104.75 | 1.16 | 212 | 19.25 |
