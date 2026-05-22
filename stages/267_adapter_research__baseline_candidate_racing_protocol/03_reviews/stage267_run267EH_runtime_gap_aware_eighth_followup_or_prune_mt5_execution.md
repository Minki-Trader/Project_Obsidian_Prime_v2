# Stage267 Run267EH Runtime Gap Aware Eighth Follow-Up/Prune MT5 Execution(267단계 267EH 런타임 공백 반영 8차 후속/가지치기 MT5 실행)

- status(상태): `run267EH_runtime_gap_aware_eighth_followup_or_prune_mt5_batch_partial`
- attempts(시도): `15/15`
- KPI records(KPI 기록): `9`
- init failures(초기화 실패): `6`
- next_action(다음 행동): `run267EI_review_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267EH(267EH 실행)는 run267EG(267EG 실행)가 만든 15개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 Strategy Tester(전략 테스터)에 넣어 본 단계다.
효과는 s258_stc 생존성, s264_aih 제한 수리, 2026.04 공유 매도 취약성, s262/s264_aia feature order(피처 순서), 공격형 handoff(인계)가 실제 tester output(테스터 출력)으로 이어지는지 확인하는 것이다.
해석은 아직 다음 review(검토) 단계가 필요하다. 이번 실행의 KPI records(KPI 기록)는 `9`개이고 init failure(초기화 실패)는 `6`개다.

## Boundary(경계)

- 이 실행은 runtime probe(런타임 탐침)이며 runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)를 주장하지 않는다.
- Tier A+B(Tier A+B 합산)는 duplicate boundary(중복 경계) 입력이다. true Tier B fallback(실제 Tier B 대체) 근거로 해석하지 않는다.
- 다음 run267EI(267EI 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 봐야 한다.

## KPI Preview(KPI 미리보기)

| candidate(후보) | profile(프로필) | tier(티어) | net_profit(순손익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | status(상태) |
|---|---|---|---:|---:|---:|---:|---|
| `s264_aih` | `s264_aih_validation_integrity_recheck` | `Tier A` | 442.89 | 1.21 | 467 | 15.74 | `completed` |
| `s264_aih` | `s264_aih_202604_bounded_repair` | `Tier A` | -27.89 | 0.43 | 17 | 7.85 | `completed` |
| `s264_lc` | `s264_lc_202604_paired_control` | `Tier A` | -39.29 | 0.4 | 17 | 10.36 | `completed` |
| `s264_aih` | `s264_aih_202604_shared_sell_pressure` | `Tier A` | -28.77 | 0.44 | 17 | 8.26 | `completed` |
| `s264_lc` | `s264_lc_202604_shared_sell_pressure` | `Tier A` | -30.22 | 0.43 | 17 | 8.51 | `completed` |
| `s262_lih` | `s262_lih_202604_shared_sell_pressure` | `Tier A` | -30.1 | 0.42 | 17 | 8.19 | `completed` |
| `s264_aia` | `s264_aia_202604_shared_sell_pressure` | `Tier A` | -28.77 | 0.44 | 17 | 8.26 | `completed` |
| `s262_lih` | `s262_lih_validation_identity_audit` | `Tier A` | 574.21 | 1.21 | 458 | 13.39 | `completed` |
| `s264_aia` | `s264_aia_validation_identity_audit` | `Tier A` | 574.21 | 1.21 | 458 | 13.39 | `completed` |

## Forensics(포렌식)

- forensics rows(포렌식 행): `15`
- tester profile rows(테스터 프로필 행): `15`
- compile status(컴파일 상태): `completed`
- runtime module hashes(런타임 모듈 해시): `7`
- init failure rows(초기화 실패 행): `6`

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EH/runtime_gap_aware_eighth_followup_or_prune_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EH/runtime_gap_aware_eighth_followup_or_prune_mt5_execution/kpi_summary.csv`
- backtest_forensics(백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EH/runtime_gap_aware_eighth_followup_or_prune_mt5_execution/backtest_forensics.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EH/runtime_gap_aware_eighth_followup_or_prune_mt5_execution/runtime_parity_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EH/runtime_gap_aware_eighth_followup_or_prune_mt5_execution/result_judgment.csv`
