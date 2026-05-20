# Stage267 Historical 2024 MT5 Execution Report(267단계 2024 MT5 실행 보고)

- action(행동): `10` MT5 Strategy Tester(전략 테스터) attempt(시도)를 실행했다.
- effect(효과): 2024 historical stress(2024 과거 압박)가 input-only(입력만 있음)에서 `completed` evidence(근거) 상태로 이동했다.
- completed_reports(완료 보고서): `10`
- kpi_records(KPI 기록): `10`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Backtest Forensics(백테스트 포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `C:\Program Files\MetaTrader 5\terminal64.exe`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델링) `4`, date range(기간) `2024.01.02` to `2025.01.01`.
- ea_identity(EA 정체성): `Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5`; module hash(모듈 해시)는 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/execution_result.json`에 기록했다.
- report_identity(보고서 정체성): reports(보고서)는 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/mt5/reports` 아래에 수집한다.
- cost_assumptions(비용 가정): tester broker environment(테스터 브로커 환경)의 spread/commission/slippage(스프레드/수수료/슬리피지)를 따른다. 세부 비용은 개별 HTML report(HTML 보고서)에서 확인해야 한다.
- backtest_judgment(백테스트 판정): `completed`.

## KPI Read(KPI 판독)

| record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) |
| --- | ---: | ---: | ---: | ---: |
| `mt5_ta_s264_aih_historical_2024_tier_a_train_era_stress` | 95.56 | 1.05 | 353 | 36.68 |
| `mt5_rt_s264_aih_historical_2024_tier_a_train_era_stress` | 95.56 | 1.05 | 353 | 36.68 |
| `mt5_ta_s264_lc_historical_2024_tier_a_train_era_stress` | 71.34 | 1.04 | 350 | 37.52 |
| `mt5_rt_s264_lc_historical_2024_tier_a_train_era_stress` | 71.34 | 1.04 | 350 | 37.52 |
| `mt5_ta_s262_lih_historical_2024_tier_a_train_era_stress` | 44.49 | 1.02 | 352 | 40.13 |
| `mt5_rt_s262_lih_historical_2024_tier_a_train_era_stress` | 44.49 | 1.02 | 352 | 40.13 |
| `mt5_ta_s264_aia_historical_2024_tier_a_train_era_stress` | 87.07 | 1.05 | 354 | 36.9 |
| `mt5_rt_s264_aia_historical_2024_tier_a_train_era_stress` | 87.07 | 1.05 | 354 | 36.9 |
| `mt5_ta_s258_stc_historical_2024_tier_a_train_era_stress` | 102.89 | 1.05 | 378 | 40.43 |
| `mt5_rt_s258_stc_historical_2024_tier_a_train_era_stress` | 102.89 | 1.05 | 378 | 40.43 |

## Judgment(판정)

- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- operating meaning(운영 의미): `none`
- next_condition(다음 조건): balance/equity curve(잔액/평가금 곡선), monthly/session/time-slice KPI(월별/세션별/시간대별 KPI), trade quality(거래 품질)를 보고 후보별 깨짐 정도를 판정한다.
