# Stage267 Run267CG Pool-wide Orthogonal Loss-shape/State MT5 Execution(267CG 후보군 전체 직교 손실 형태/상태 MT5 실행)

- status(상태): `run267CG_pool_wide_orthogonal_loss_shape_state_mt5_batch_completed`
- attempts(시도): `20/20`
- KPI records(KPI 기록): `20`
- next_action(다음 행동): `run267CH_review_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## What changed(무엇이 바뀌었나)

- action(행동): run267CF(267CF 실행)의 20개 MT5(MetaTrader 5, 메타트레이더5) 입력을 실행용 profile(프로필)로 다시 만들고 tester(테스터)에 넘겼다.
- effect(효과): loss-shape proxy(손실 형태 대리값)와 similar replacement impulse(유사 대체 임펄스)가 실제 runtime output(런타임 출력)과 KPI(핵심 성과 지표)로 이어지는지 확인할 수 있다.

## Boundary(경계)

- 이 실행은 runtime probe(런타임 탐침)다. runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)는 주장하지 않는다.
- Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계) 입력이다. 실제 Tier B fallback(Tier B 대체) 라우팅 증거로 해석하지 않는다.
- 다음 run267CH(267CH 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 봐야 한다.

## KPI Preview(KPI 미리보기)

| candidate(후보) | profile(프로필) | tier(티어) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | status(상태) |
|---|---|---|---:|---:|---:|---:|---|
| `s264_aih` | `loss_shape_proxy_minimal` | `Tier A` | 694.85 | 1.98 | 194 | 14.68 | `completed` |
| `s264_aih` | `loss_shape_proxy_minimal` | `Tier A+B` | 694.85 | 1.98 | 194 | 14.68 | `completed` |
| `s264_lc` | `loss_shape_proxy_minimal` | `Tier A` | 698.39 | 1.92 | 206 | 11.79 | `completed` |
| `s264_lc` | `loss_shape_proxy_minimal` | `Tier A+B` | 698.39 | 1.92 | 206 | 11.79 | `completed` |
| `s262_lih` | `loss_shape_proxy_minimal` | `Tier A` | 617.93 | 1.71 | 226 | 9.06 | `completed` |
| `s262_lih` | `loss_shape_proxy_minimal` | `Tier A+B` | 617.93 | 1.71 | 226 | 9.06 | `completed` |
| `s264_aia` | `loss_shape_proxy_minimal` | `Tier A` | 565.26 | 1.8 | 194 | 15.0 | `completed` |
| `s264_aia` | `loss_shape_proxy_minimal` | `Tier A+B` | 565.26 | 1.8 | 194 | 15.0 | `completed` |
| `s258_stc` | `loss_shape_proxy_minimal` | `Tier A` | 825.03 | 1.7 | 239 | 14.26 | `completed` |
| `s258_stc` | `loss_shape_proxy_minimal` | `Tier A+B` | 825.03 | 1.7 | 239 | 14.26 | `completed` |
| `s264_aih` | `similar_replacement_impulse` | `Tier A` | 1166.51 | 1.44 | 369 | 24.89 | `completed` |
| `s264_aih` | `similar_replacement_impulse` | `Tier A+B` | 1166.51 | 1.44 | 369 | 24.89 | `completed` |
| `s264_lc` | `similar_replacement_impulse` | `Tier A` | 1568.81 | 1.5 | 408 | 17.43 | `completed` |
| `s264_lc` | `similar_replacement_impulse` | `Tier A+B` | 1568.81 | 1.5 | 408 | 17.43 | `completed` |
| `s262_lih` | `similar_replacement_impulse` | `Tier A` | 1183.13 | 1.47 | 388 | 28.76 | `completed` |
| `s262_lih` | `similar_replacement_impulse` | `Tier A+B` | 1183.13 | 1.47 | 388 | 28.76 | `completed` |
| `s264_aia` | `similar_replacement_impulse` | `Tier A` | 1408.59 | 1.5 | 396 | 28.37 | `completed` |
| `s264_aia` | `similar_replacement_impulse` | `Tier A+B` | 1408.59 | 1.5 | 396 | 28.37 | `completed` |
| `s258_stc` | `similar_replacement_impulse` | `Tier A` | 1414.48 | 1.44 | 419 | 31.65 | `completed` |
| `s258_stc` | `similar_replacement_impulse` | `Tier A+B` | 1414.48 | 1.44 | 419 | 31.65 | `completed` |

## Forensics(포렌식)

- forensics rows(포렌식 행): `20`
- tester profile rows(테스터 프로필 행): `20`
- compile status(컴파일 상태): `completed`
- runtime module hashes(런타임 모듈 해시): `7`

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CG/pool_wide_orthogonal_loss_shape_state_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CG/pool_wide_orthogonal_loss_shape_state_mt5_execution/kpi_summary.csv`
- backtest_forensics(백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CG/pool_wide_orthogonal_loss_shape_state_mt5_execution/backtest_forensics.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CG/pool_wide_orthogonal_loss_shape_state_mt5_execution/runtime_parity_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CG/pool_wide_orthogonal_loss_shape_state_mt5_execution/result_judgment.csv`
