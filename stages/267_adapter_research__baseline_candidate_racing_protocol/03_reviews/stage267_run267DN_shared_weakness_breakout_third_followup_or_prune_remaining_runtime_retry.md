# Stage267 Run267DN Remaining Runtime Retry(267단계 267DN 남은 런타임 재시도)

- status(상태): `run267DN_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry_blocked`
- source_run(원천 실행): `run267DM_stage267_shared_weakness_breakout_third_followup_or_prune_mt5_execution_v1`
- retry_attempts(재시도 시도): `9`
- recovered_kpi_records(회복 KPI 기록): `0`
- next_action(다음 행동): `run267DO_review_run267DM_run267DN_balance_timeslice_trade_quality_with_runtime_gaps`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DN(267DN 실행)은 run267DM(267DM 실행)에서 Strategy Tester report(전략 테스터 보고서)는 있었지만 runtime CSV(런타임 CSV)가 안 잡힌 attempt(시도)만 다시 실행했다.
효과: 같은 후보를 다시 고르는 것이 아니라, runtime handoff(런타임 인계)가 우연히 누락된 것인지 실제 blocker(차단 사유)인지 분리한다.

## Retry Outcome(재시도 결과)

| attempt(시도) | candidate(후보) | profile(프로필) | tier(티어) | runtime(런타임) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) |
|---|---|---|---|---|---:|---:|---:|
| `run267dl_01_s264_aia_similar_dual_session_month_survivor_ta_2024` | `s264_aia` | `s264_aia_similar_dual_session_month_survivor` | `Tier A` | `blocked` |  |  |  |
| `run267dl_01_s264_aia_similar_dual_session_month_survivor_rt_2024` | `s264_aia` | `s264_aia_similar_dual_session_month_survivor` | `Tier A+B` | `blocked` |  |  |  |
| `run267dl_02_s264_aia_ablation_dual_session_month_survivor_ta_2024` | `s264_aia` | `s264_aia_ablation_dual_session_month_survivor` | `Tier A` | `blocked` |  |  |  |
| `run267dl_02_s264_aia_ablation_dual_session_month_survivor_rt_2024` | `s264_aia` | `s264_aia_ablation_dual_session_month_survivor` | `Tier A+B` | `blocked` |  |  |  |
| `run267dl_03_s258_stc_2023h2_supply_threshold_release_ta_2023h2` | `s258_stc` | `s258_stc_explosive_supply_threshold_release` | `Tier A` | `blocked` |  |  |  |
| `run267dl_05_s258_stc_2025h1_supply_threshold_release_ta_2025h1` | `s258_stc` | `s258_stc_explosive_supply_threshold_release` | `Tier A` | `blocked` |  |  |  |
| `run267dl_07_s258_stc_2025h2_supply_threshold_release_ta_2025h2` | `s258_stc` | `s258_stc_explosive_supply_threshold_release` | `Tier A` | `blocked` |  |  |  |
| `run267dl_09_s262_lih_validation_guardrail_crosscheck_ta_2024` | `s262_lih` | `s262_lih_validation_guardrail_crosscheck` | `Tier A` | `blocked` |  |  |  |
| `run267dl_09_s262_lih_validation_guardrail_crosscheck_rt_2024` | `s262_lih` | `s262_lih_validation_guardrail_crosscheck` | `Tier A+B` | `blocked` |  |  |  |

## Boundary(경계)

- 이 실행은 runtime probe(런타임 탐침)이며 runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)를 주장하지 않는다.
- selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 없다.
- 다음 검토는 run267DM/run267DN을 같이 보고 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질), missing runtime gap(누락 런타임 공백)을 분리해야 한다.

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DN/shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DN/shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry/kpi_summary.csv`
- backtest_forensics(백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DN/shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry/backtest_forensics.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DN/shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry/runtime_parity_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DN/shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry/result_judgment.csv`
