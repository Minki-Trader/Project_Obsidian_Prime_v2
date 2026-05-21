# Stage267 Run267BT Pool-Wide Directional/Impulse Follow-Up MT5 Execution(267단계 267BT 후보군 전체 방향/임펄스 후속 MT5 실행)

## Summary(요약)

- run_id(실행 ID): `run267BT_stage267_pool_wide_directional_impulse_followup_mt5_execution_v1`
- source_run(원천 실행): `run267BS_stage267_pool_wide_directional_impulse_followup_materialization_v1`
- status(상태): `run267BT_pool_wide_directional_impulse_followup_mt5_batch_completed`
- attempts_executed(실행 시도): `10`
- kpi_records(KPI 기록): `10`
- blocked_or_gap_attempts(차단 또는 공백 시도): `0`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BS(267BS 실행)의 방향 비대칭(directional asymmetry, 방향 비대칭)과 공격형 임펄스 대체(aggressive impulse replacement, 공격형 임펄스 대체) 10개 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5) Strategy Tester(전략 테스터)로 실행했다.
Effect(효과): 다섯 baseline candidates(기준 후보)가 새 feature engineering(피처 엔지니어링) 압박을 받을 때 실제 tester output(테스터 출력), runtime output(런타임 출력), KPI(핵심 성과 지표)까지 이어지는지 확인한다.

## KPI Snapshot(KPI 요약)

| candidate(후보) | profile(프로필) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | max_DD%(최대 손실폭 %) |
| --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `directional_asymmetry` | -26.15 | 0.99 | 353 | 49.73 |
| `s264_lc` | `directional_asymmetry` | -48.21 | 0.98 | 350 | 50.89 |
| `s262_lih` | `directional_asymmetry` | -69.77 | 0.97 | 352 | 53.29 |
| `s264_aia` | `directional_asymmetry` | -34.51 | 0.98 | 354 | 49.98 |
| `s258_stc` | `directional_asymmetry` | -22.07 | 0.99 | 378 | 51.57 |
| `s264_aih` | `aggressive_impulse_replacement` | 93.46 | 1.05 | 353 | 36.1 |
| `s264_lc` | `aggressive_impulse_replacement` | 71.38 | 1.04 | 350 | 36.59 |
| `s262_lih` | `aggressive_impulse_replacement` | 51.42 | 1.03 | 352 | 39.01 |
| `s264_aia` | `aggressive_impulse_replacement` | 92.91 | 1.05 | 354 | 35.76 |
| `s258_stc` | `aggressive_impulse_replacement` | 105.26 | 1.05 | 378 | 40.04 |

## Blocked / Gap Attempts(차단/공백 시도)

| attempt(시도) | candidate(후보) | profile(프로필) | tester(테스터) | runtime(런타임) | report(보고서) | note(메모) |
| --- | --- | --- | --- | --- | --- | --- |
| `none` |  |  |  |  |  |  |

## Boundary(경계)

- 이 실행은 R&D racing(연구개발 경주) 실행이며 candidate selection(후보 선택)이 아니다.
- balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 검토 전에는 좋은 후보라고 말하지 않는다.
- ONNX parity(ONNX 동등성)나 ONNX conversion(ONNX 변환)은 시작하지 않는다.
- Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 생기기 전까지 blocked(차단)이다.

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BT/pool_wide_directional_impulse_followup_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BT/pool_wide_directional_impulse_followup_mt5_execution/kpi_summary.csv`
- forensics(포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BT/pool_wide_directional_impulse_followup_mt5_execution/backtest_forensics.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BT/pool_wide_directional_impulse_followup_mt5_execution/runtime_parity_receipt.csv`
- next_action(다음 행동): `run267BU_review_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality`
