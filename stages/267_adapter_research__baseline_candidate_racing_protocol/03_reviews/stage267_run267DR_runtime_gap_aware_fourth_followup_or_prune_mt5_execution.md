# Stage267 Run267DR Runtime Gap Aware Fourth Follow-Up/Prune MT5 Execution(267단계 267DR 런타임 공백 반영 4차 후속/가지치기 MT5 실행)

- status(상태): `run267DR_runtime_gap_aware_fourth_followup_or_prune_mt5_batch_partial`
- attempts(시도): `8/8`
- KPI records(KPI 기록): `5`
- init failures(초기화 실패): `3`
- next_action(다음 행동): `run267DS_review_runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DR(267DR 실행)는 run267DQ(267DQ 실행)가 만든 8개 MT5(MetaTrader 5, 메타트레이더5) 입력을 Strategy Tester(전략 테스터)에 넘겼다.
효과: s258_stc supply continuity(공급 연속성), s258_stc Monday/late DD taper(월요일/후반 손실폭 완화), s264_lc defensive DD zoom control(방어형 손실폭 확대 대조) 입력이 실제 report(보고서)와 KPI(핵심 성과 지표)로 이어지는지 확인한다.
해석: supply continuity(공급 연속성) 3개는 strategy report(전략 보고서)는 생겼지만 EBM table open failure(EBM 테이블 열기 실패)로 init failure(초기화 실패)가 났고, taper/control(완화/대조) 5개만 KPI(핵심 성과 지표)로 이어졌다.

## Boundary(경계)

- 이 실행은 runtime probe(런타임 탐침)이며 runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)를 주장하지 않는다.
- Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계) 입력이다. true Tier B fallback(실제 티어 B 대체) 근거로 해석하지 않는다.
- 다음 run267DS(267DS 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 봐야 한다.

## KPI Preview(KPI 미리보기)

| candidate(후보) | profile(프로필) | tier(티어) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | status(상태) |
|---|---|---|---:|---:|---:|---:|---|
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `Tier A` | 190.76 | 1.29 | 266 | 12.18 | `completed` |
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `Tier A` | -3.69 | 1.0 | 356 | 17.93 | `completed` |
| `s258_stc` | `s258_stc_monday_late_session_dd_taper` | `Tier A` | 33.93 | 1.04 | 259 | 16.39 | `completed` |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `Tier A` | 1522.61 | 1.42 | 473 | 24.39 | `completed` |
| `s264_lc` | `s264_lc_defensive_dd_zoom_control` | `Tier A+B` | 1522.61 | 1.42 | 473 | 24.39 | `completed` |

## Forensics(포렌식)

- forensics rows(포렌식 행): `8`
- tester profile rows(테스터 프로필 행): `8`
- compile status(컴파일 상태): `completed`
- runtime module hashes(런타임 모듈 해시): `7`
- init failure rows(초기화 실패 행): `3`

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DR/runtime_gap_aware_fourth_followup_or_prune_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DR/runtime_gap_aware_fourth_followup_or_prune_mt5_execution/kpi_summary.csv`
- backtest_forensics(백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DR/runtime_gap_aware_fourth_followup_or_prune_mt5_execution/backtest_forensics.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DR/runtime_gap_aware_fourth_followup_or_prune_mt5_execution/runtime_parity_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DR/runtime_gap_aware_fourth_followup_or_prune_mt5_execution/result_judgment.csv`
