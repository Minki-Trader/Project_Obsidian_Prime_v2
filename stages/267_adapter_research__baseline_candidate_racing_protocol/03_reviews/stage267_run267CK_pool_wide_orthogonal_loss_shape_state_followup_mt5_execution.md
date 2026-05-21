# Stage267 Run267CK Follow-up MT5 Execution(267단계 267CK 후속 MT5 실행)

- status(상태): `run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_batch_completed`
- attempts(시도): `4/4`
- KPI records(KPI 기록): `4`
- next_action(다음 행동): `run267CL_review_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## What Changed(무엇이 바뀌었나)

- action(행동): run267CJ(267CJ 실행)의 4개 MT5(MetaTrader 5, 메타트레이더5) 입력을 tester profile(테스터 프로필)로 다시 만들고 Strategy Tester(전략 테스터)에 넘겼다.
- effect(효과): `s264_lc`와 `s264_aia`의 follow-up state pressure(후속 상태 압박)가 실제 runtime output(런타임 출력)과 KPI(핵심 성과 지표)로 이어지는지 확인한다.

## Boundary(경계)

- 이 실행은 runtime probe(런타임 탐침)이며 runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)는 주장하지 않는다.
- Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계) 입력이다. true Tier B fallback(실제 티어 B 대체) 증거로 해석하지 않는다.
- 다음 run267CL(267CL 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 봐야 한다.

## KPI Preview(KPI 미리보기)

| candidate(후보) | profile(프로필) | tier(티어) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | status(상태) |
|---|---|---|---:|---:|---:|---:|---|
| `s264_lc` | `controlled_impulse_dd_state_throttle` | `Tier A` | 1207.3 | 1.51 | 354 | 17.62 | `completed` |
| `s264_lc` | `controlled_impulse_dd_state_throttle` | `Tier A+B` | 1207.3 | 1.51 | 354 | 17.62 | `completed` |
| `s264_aia` | `oos_anchor_impulse_pressure` | `Tier A` | 1119.33 | 1.55 | 320 | 16.03 | `completed` |
| `s264_aia` | `oos_anchor_impulse_pressure` | `Tier A+B` | 1119.33 | 1.55 | 320 | 16.03 | `completed` |

## Forensics(포렌식)

- forensics rows(포렌식 행): `4`
- tester profile rows(테스터 프로필 행): `4`
- compile status(컴파일 상태): `completed`
- runtime module hashes(런타임 모듈 해시): `7`

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CK/pool_wide_orthogonal_loss_shape_state_followup_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CK/pool_wide_orthogonal_loss_shape_state_followup_mt5_execution/kpi_summary.csv`
- backtest_forensics(백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CK/pool_wide_orthogonal_loss_shape_state_followup_mt5_execution/backtest_forensics.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CK/pool_wide_orthogonal_loss_shape_state_followup_mt5_execution/runtime_parity_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CK/pool_wide_orthogonal_loss_shape_state_followup_mt5_execution/result_judgment.csv`
