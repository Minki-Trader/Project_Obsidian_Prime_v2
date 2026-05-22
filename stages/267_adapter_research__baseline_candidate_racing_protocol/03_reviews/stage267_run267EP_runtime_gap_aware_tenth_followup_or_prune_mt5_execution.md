# Stage267 Run267EP Runtime Gap Aware Tenth Follow-Up/Prune MT5 Execution(267단계 267EP 런타임 공백 반영 10차 후속/가지치기 MT5 실행)

- status(상태): `run267EP_runtime_gap_aware_tenth_followup_or_prune_mt5_batch_partial`
- attempts(시도): `12/12`
- KPI records(KPI 기록): `8`
- init failures(초기화 실패): `4`
- next_action(다음 행동): `run267EQ_review_runtime_gap_aware_tenth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267EP(267EP 실행)는 run267EO(267EO 실행)가 만든 12개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 Strategy Tester(전략 테스터)에 넣어 본 단계다.
효과는 s258_stc 생존성, s264_aih 제한 수리, 2026.04 공유 매도 취약성, s262/s264_aia feature order(피처 순서), 공격형 handoff(인계)가 실제 tester output(테스터 출력)으로 이어지는지 확인하는 것이다.
해석은 아직 다음 review(검토) 단계가 필요하다. 이번 실행의 KPI records(KPI 기록)는 `8`개이고 init failure(초기화 실패)는 `4`개다.

## Boundary(경계)

- 이 실행은 runtime probe(런타임 탐침)이며 runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)를 주장하지 않는다.
- Tier A+B(Tier A+B 합산)는 duplicate boundary(중복 경계) 입력이다. true Tier B fallback(실제 Tier B 대체) 근거로 해석하지 않는다.
- 다음 run267EQ(267EQ 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 봐야 한다.

## KPI Preview(KPI 미리보기)

| candidate(후보) | profile(프로필) | tier(티어) | net_profit(순손익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | status(상태) |
|---|---|---|---:|---:|---:|---:|---|
| `s264_aih` | `s264_aih_202604_shared_state_pivot` | `Tier A` | -26.02 | 0.43 | 17 | 7.29 | `completed` |
| `s264_lc` | `s264_lc_202604_shared_state_control` | `Tier A` | -23.92 | 0.43 | 17 | 6.67 | `completed` |
| `s262_lih` | `s262_lih_202604_shared_state_pivot` | `Tier A` | -24.58 | 0.42 | 17 | 7.0 | `completed` |
| `s264_aia` | `s264_aia_202604_shared_state_pivot` | `Tier A` | -24.41 | 0.43 | 17 | 6.95 | `completed` |
| `s262_lih` | `s262_lih_validation_identity_receipt` | `Tier A` | 300.2 | 1.22 | 458 | 8.35 | `completed` |
| `s264_aia` | `s264_aia_validation_identity_receipt` | `Tier A` | 300.2 | 1.22 | 458 | 8.35 | `completed` |
| `s258_stc` | `s258_stc_aggressive_nonfilter_reentry` | `Tier A` | 375.98 | 1.21 | 355 | 21.19 | `completed` |
| `s264_aih` | `s264_aih_aggressive_nonfilter_reentry` | `Tier A` | -22.83 | 0.61 | 17 | 7.7 | `completed` |

## Forensics(포렌식)

- forensics rows(포렌식 행): `12`
- tester profile rows(테스터 프로필 행): `12`
- compile status(컴파일 상태): `completed`
- runtime module hashes(런타임 모듈 해시): `7`
- init failure rows(초기화 실패 행): `4`

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EP/runtime_gap_aware_tenth_followup_or_prune_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EP/runtime_gap_aware_tenth_followup_or_prune_mt5_execution/kpi_summary.csv`
- backtest_forensics(백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EP/runtime_gap_aware_tenth_followup_or_prune_mt5_execution/backtest_forensics.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EP/runtime_gap_aware_tenth_followup_or_prune_mt5_execution/runtime_parity_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EP/runtime_gap_aware_tenth_followup_or_prune_mt5_execution/result_judgment.csv`
