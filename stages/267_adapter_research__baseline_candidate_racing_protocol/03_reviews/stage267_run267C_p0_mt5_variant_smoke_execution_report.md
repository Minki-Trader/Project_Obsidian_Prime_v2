# Stage267 Run267C P0 MT5 Variant Smoke/Batch Execution(267단계 267C 우선순위 0 MT5 변형 스모크/묶음 실행)

- action(행동): `30`개 P0 diagnostic MT5 attempt(우선순위 0 진단 MT5 시도)를 `full P0 batch(전체 우선순위 0 묶음 실행)`로 실행했다.
- effect(효과): materialized input(물질화된 입력)이 실제 MT5 Strategy Tester(전략 테스터)까지 이어지는지 확인했고 상태는 `completed`이다.
- completed_reports(완료 보고서): `30`
- kpi_records(KPI 기록): `30`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델링) `4`, date range(기간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): `Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5`; module hashes(모듈 해시)는 execution result(실행 결과)에 기록했다.
- report_identity(보고서 정체성): execution result(실행 결과) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p0_mt5_variants/p0_mt5_variant_smoke_execution_result.json`, forensics(포렌식) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p0_mt5_variants/p0_mt5_variant_smoke_backtest_forensics.csv`.
- cost_assumptions(비용 가정): tester broker environment(테스터 브로커 환경)의 spread/commission/slippage(스프레드/수수료/슬리피지)를 따른다.
- backtest_judgment(백테스트 판정): `completed`.

## KPI Read(KPI 판독)

| record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) |
| --- | ---: | ---: | ---: | ---: |
| `mt5_ta_s264_aih_julyblk_historical_2024_tier_a_train_era_stress` | 217.51 | 1.12 | 317 | 25.9 |
| `mt5_rt_s264_aih_julyblk_historical_2024_tier_a_train_era_stress` | 217.51 | 1.12 | 317 | 25.9 |
| `mt5_ta_s264_lc_julyblk_historical_2024_tier_a_train_era_stress` | 188.34 | 1.11 | 314 | 26.12 |
| `mt5_rt_s264_lc_julyblk_historical_2024_tier_a_train_era_stress` | 188.34 | 1.11 | 314 | 26.12 |
| `mt5_ta_s262_lih_julyblk_historical_2024_tier_a_train_era_stress` | 173.52 | 1.1 | 315 | 27.71 |
| `mt5_rt_s262_lih_julyblk_historical_2024_tier_a_train_era_stress` | 173.52 | 1.1 | 315 | 27.71 |
| `mt5_ta_s264_aia_julyblk_historical_2024_tier_a_train_era_stress` | 204.16 | 1.11 | 318 | 26.03 |
| `mt5_rt_s264_aia_julyblk_historical_2024_tier_a_train_era_stress` | 204.16 | 1.11 | 318 | 26.03 |
| `mt5_ta_s258_stc_julyblk_historical_2024_tier_a_train_era_stress` | 281.84 | 1.13 | 337 | 29.72 |
| `mt5_rt_s258_stc_julyblk_historical_2024_tier_a_train_era_stress` | 281.84 | 1.13 | 337 | 29.72 |
| `mt5_ta_s264_aih_lateblk_historical_2024_tier_a_train_era_stress` | 231.42 | 1.14 | 308 | 22.94 |
| `mt5_rt_s264_aih_lateblk_historical_2024_tier_a_train_era_stress` | 231.42 | 1.14 | 308 | 22.94 |
| `mt5_ta_s264_lc_lateblk_historical_2024_tier_a_train_era_stress` | 207.8 | 1.13 | 305 | 22.87 |
| `mt5_rt_s264_lc_lateblk_historical_2024_tier_a_train_era_stress` | 207.8 | 1.13 | 305 | 22.87 |
| `mt5_ta_s262_lih_lateblk_historical_2024_tier_a_train_era_stress` | 172.83 | 1.11 | 307 | 25.78 |
| `mt5_rt_s262_lih_lateblk_historical_2024_tier_a_train_era_stress` | 172.83 | 1.11 | 307 | 25.78 |
| `mt5_ta_s264_aia_lateblk_historical_2024_tier_a_train_era_stress` | 222.17 | 1.14 | 309 | 22.96 |
| `mt5_rt_s264_aia_lateblk_historical_2024_tier_a_train_era_stress` | 222.17 | 1.14 | 309 | 22.96 |
| `mt5_ta_s258_stc_lateblk_historical_2024_tier_a_train_era_stress` | 230.24 | 1.13 | 328 | 26.48 |
| `mt5_rt_s258_stc_lateblk_historical_2024_tier_a_train_era_stress` | 230.24 | 1.13 | 328 | 26.48 |
| `mt5_ta_s264_aih_vollowblk_historical_2024_tier_a_train_era_stress` | 436.26 | 1.35 | 257 | 16.31 |
| `mt5_rt_s264_aih_vollowblk_historical_2024_tier_a_train_era_stress` | 436.26 | 1.35 | 257 | 16.31 |
| `mt5_ta_s264_lc_vollowblk_historical_2024_tier_a_train_era_stress` | 416.59 | 1.34 | 255 | 17.77 |
| `mt5_rt_s264_lc_vollowblk_historical_2024_tier_a_train_era_stress` | 416.59 | 1.34 | 255 | 17.77 |
| `mt5_ta_s262_lih_vollowblk_historical_2024_tier_a_train_era_stress` | 416.59 | 1.34 | 255 | 17.77 |
| `mt5_rt_s262_lih_vollowblk_historical_2024_tier_a_train_era_stress` | 416.59 | 1.34 | 255 | 17.77 |
| `mt5_ta_s264_aia_vollowblk_historical_2024_tier_a_train_era_stress` | 436.26 | 1.35 | 257 | 16.31 |
| `mt5_rt_s264_aia_vollowblk_historical_2024_tier_a_train_era_stress` | 436.26 | 1.35 | 257 | 16.31 |
| `mt5_ta_s258_stc_vollowblk_historical_2024_tier_a_train_era_stress` | 459.04 | 1.34 | 270 | 21.38 |
| `mt5_rt_s258_stc_vollowblk_historical_2024_tier_a_train_era_stress` | 459.04 | 1.34 | 270 | 21.38 |

## Boundary(경계)

- 이 execution(실행)은 full P0 batch(전체 우선순위 0 묶음 실행)이다. Effect(효과): 모든 P0 진단 변형을 실제 MT5로 확인했지만, 진단 hard block(강제 차단) 결과라 후보 선택이나 ONNX 준비로 쓰지 않는다.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267C_review_p0_mt5_full_batch_results`.
