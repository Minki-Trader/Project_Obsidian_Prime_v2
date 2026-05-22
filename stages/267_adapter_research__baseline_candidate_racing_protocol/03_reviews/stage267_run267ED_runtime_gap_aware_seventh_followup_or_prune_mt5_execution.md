# Stage267 Run267ED Runtime Gap Aware Seventh Follow-Up/Prune MT5 Execution(267단계 267ED 런타임 공백 반영 7차 후속/가지치기 MT5 실행)

- status(상태): `run267ED_runtime_gap_aware_seventh_followup_or_prune_mt5_batch_partial`
- attempts(시도): `14/14`
- KPI records(KPI 기록): `9`
- init failures(초기화 실패): `5`
- next_action(다음 행동): `run267EE_review_runtime_gap_aware_seventh_followup_or_prune_balance_timeslice_trade_quality_with_init_failures`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267ED(267ED 실행)는 run267EC(267EC 실행)가 만든 14개 MT5(MetaTrader 5, 메타트레이더5) 입력을 Strategy Tester(전략 테스터)에 넘겼다.
효과: s258_stc structural DD shape split(구조적 손실폭 형태 분리), s258_stc adverse state falsification(불리 구간 상태 반증), s264_aih validation anchor repair(검증 앵커 수리), s264_aih final-month counter shock(마지막 달 역충격), s264_lc same-month control(같은 달 대조)이 실제 report(보고서)와 KPI(핵심 성과 지표)로 이어지는지 확인한다.
해석: completed KPI(완료 KPI)는 `9`개이고 init failure(초기화 실패)는 `5`개다. 실패 행은 다음 review(검토)에서 수리 또는 가지치기 대상으로 따로 본다.

## Boundary(경계)

- 이 실행은 runtime probe(런타임 탐침)이며 runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)를 주장하지 않는다.
- Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계) 입력이다. true Tier B fallback(실제 티어 B 대체) 근거로 해석하지 않는다.
- 다음 run267EE(267EE 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 봐야 한다.

## KPI Preview(KPI 미리보기)

| candidate(후보) | profile(프로필) | tier(티어) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | status(상태) |
|---|---|---|---:|---:|---:|---:|---|
| `s258_stc` | `s258_stc_2025h1_period_survival_gate` | `Tier A` | 301.88 | 1.18 | 357 | 14.65 | `completed` |
| `s258_stc` | `s258_stc_2025h2_period_survival_gate` | `Tier A` | 164.54 | 1.13 | 257 | 20.51 | `completed` |
| `s264_aih` | `s264_aih_validation_anchor_integrity` | `Tier A` | 518.62 | 1.22 | 467 | 11.71 | `completed` |
| `s264_aih` | `s264_aih_202604_counter_shock_rebuild` | `Tier A` | -30.46 | 0.43 | 17 | 8.58 | `completed` |
| `s264_lc` | `s264_lc_202604_counter_shock_control` | `Tier A` | -39.29 | 0.4 | 17 | 10.36 | `completed` |
| `s262_lih` | `s262_lih_validation_coverage_rejoin` | `Tier A` | 574.21 | 1.21 | 458 | 13.39 | `completed` |
| `s262_lih` | `s262_lih_202604_coverage_rejoin` | `Tier A` | -39.29 | 0.4 | 17 | 10.36 | `completed` |
| `s264_aia` | `s264_aia_validation_coverage_rejoin` | `Tier A` | 574.21 | 1.21 | 458 | 13.39 | `completed` |
| `s264_aia` | `s264_aia_202604_coverage_rejoin` | `Tier A` | -39.29 | 0.4 | 17 | 10.36 | `completed` |

## Forensics(포렌식)

- forensics rows(포렌식 행): `14`
- tester profile rows(테스터 프로필 행): `14`
- compile status(컴파일 상태): `completed`
- runtime module hashes(런타임 모듈 해시): `7`
- init failure rows(초기화 실패 행): `5`

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ED/runtime_gap_aware_seventh_followup_or_prune_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ED/runtime_gap_aware_seventh_followup_or_prune_mt5_execution/kpi_summary.csv`
- backtest_forensics(백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ED/runtime_gap_aware_seventh_followup_or_prune_mt5_execution/backtest_forensics.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ED/runtime_gap_aware_seventh_followup_or_prune_mt5_execution/runtime_parity_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267ED/runtime_gap_aware_seventh_followup_or_prune_mt5_execution/result_judgment.csv`
