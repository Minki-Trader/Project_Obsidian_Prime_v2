# Stage267 Run267DV Runtime Gap Aware Fifth Follow-Up/Prune MT5 Execution(267단계 267DV 런타임 공백 반영 5차 후속/가지치기 MT5 실행)

- status(상태): `run267DV_runtime_gap_aware_fifth_followup_or_prune_mt5_batch_partial`
- attempts(시도): `9/9`
- KPI records(KPI 기록): `8`
- init failures(초기화 실패): `1`
- next_action(다음 행동): `run267DW_review_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DV(267DV 실행)는 run267DU(267DU 실행)가 만든 9개 MT5(MetaTrader 5, 메타트레이더5) 입력을 Strategy Tester(전략 테스터)에 넘겼다.
효과: s258_stc table handoff repair(테이블 인계 수리), s258_stc aggressive noncalendar impulse(공격형 비달력 충격), s264_aih explosive shock probe(폭발형 충격 탐침), s264_lc defensive control(방어 대조)이 실제 report(보고서)와 KPI(핵심 성과 지표)로 이어지는지 확인한다.
해석: completed KPI(완료 KPI)는 `8`개이고, init failure(초기화 실패)는 `1`개다. 실패 행은 다음 review(검토)에서 수리 또는 가지치기 대상으로 따로 본다.

## Boundary(경계)

- 이 실행은 runtime probe(런타임 탐침)이며 runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)를 주장하지 않는다.
- Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계) 입력이다. true Tier B fallback(실제 티어 B 대체) 근거로 해석하지 않는다.
- 다음 run267DW(267DW 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 봐야 한다.

## KPI Preview(KPI 미리보기)

| candidate(후보) | profile(프로필) | tier(티어) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | status(상태) |
|---|---|---|---:|---:|---:|---:|---|
| `s258_stc` | `s258_stc_table_handoff_repair_2023h2` | `Tier A` | 1225.63 | 1.75 | 265 | 12.98 | `completed` |
| `s258_stc` | `s258_stc_table_handoff_repair_2025h1` | `Tier A` | 343.7 | 1.17 | 357 | 17.93 | `completed` |
| `s258_stc` | `s258_stc_table_handoff_repair_2025h2` | `Tier A` | 239.86 | 1.15 | 259 | 24.72 | `completed` |
| `s258_stc` | `s258_stc_noncalendar_impulse_2023h2` | `Tier A` | 1544.71 | 1.78 | 264 | 15.6 | `completed` |
| `s258_stc` | `s258_stc_noncalendar_impulse_2025h1` | `Tier A` | 417.0 | 1.18 | 355 | 26.32 | `completed` |
| `s258_stc` | `s258_stc_noncalendar_impulse_2025h2` | `Tier A` | 182.05 | 1.1 | 256 | 25.33 | `completed` |
| `s264_aih` | `s264_aih_202604_explosive_shock_probe` | `Tier A` | -33.16 | 0.55 | 17 | 9.87 | `completed` |
| `s264_lc` | `s264_lc_202604_defensive_control` | `Tier A` | -39.29 | 0.4 | 17 | 10.36 | `completed` |

## Forensics(포렌식)

- forensics rows(포렌식 행): `9`
- tester profile rows(테스터 프로필 행): `9`
- compile status(컴파일 상태): `completed`
- runtime module hashes(런타임 모듈 해시): `7`
- init failure rows(초기화 실패 행): `1`

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DV/runtime_gap_aware_fifth_followup_or_prune_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DV/runtime_gap_aware_fifth_followup_or_prune_mt5_execution/kpi_summary.csv`
- backtest_forensics(백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DV/runtime_gap_aware_fifth_followup_or_prune_mt5_execution/backtest_forensics.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DV/runtime_gap_aware_fifth_followup_or_prune_mt5_execution/runtime_parity_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DV/runtime_gap_aware_fifth_followup_or_prune_mt5_execution/result_judgment.csv`
