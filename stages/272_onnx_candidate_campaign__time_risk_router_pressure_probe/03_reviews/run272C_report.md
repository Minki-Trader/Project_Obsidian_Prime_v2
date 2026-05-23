# run272C Time-Risk Router MT5 Signal Replay(272C 시간 위험 라우터 MT5 신호 재생)

- status(상태): `completed_time_risk_router_mt5_signal_replay_no_candidate_selection`
- run_id(실행 ID): `run272C_time_risk_router_mt5_signal_replay_v1`
- source_run(원천 실행): `run272B_materialize_time_risk_router_pressure_probe_payloads_v1`
- attempts(시도): `16/16`
- KPI records(KPI 기록): `16`
- external_verification_status(외부 검증 상태): `completed`
- judgment(판정): `runtime_probe_completed_inconclusive_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run272D_balance_time_slice_trade_quality_review`

## Plain Result(쉬운 결과)

run272C(272C 실행)는 run272B(272B 실행)의 `route_signal_value`를 one-feature EBM table(단일 피처 EBM 표)로 바꿔 MT5(`MetaTrader 5`, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA)에 넣는다.
효과(effect, 효과): time-risk router(시간 위험 라우터)의 short/flat/long(숏/무포지션/롱) 구조가 Python payload(파이썬 페이로드)에만 머물지 않고 Strategy Tester(전략 테스터) 경계까지 이동한다.

## Signal Policy(신호 정책)

- `-1`: short(숏)
- `0`: flat(무포지션)
- `1`: long(롱)
- known difference(알려진 차이): 아직 Adapter package(어댑터 패키지)나 ONNX runtime(온엑스 런타임)이 아니라 signal replay(신호 재생) 탐침이다.

## KPI Preview(KPI 미리보기)

| record_view(기록 보기) | tier(티어) | split(분할) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | status(상태) |
|---|---|---|---:|---:|---:|---|
| `mt5_q01_tier_a_validation_is` | `Tier A` | `validation_is` | 146.38 | 1.06 | 712 | `completed` |
| `mt5_q01_tier_a_oos` | `Tier A` | `oos` | 137.19 | 1.06 | 566 | `completed` |
| `mt5_q01_tier_b_validation_is` | `Tier B` | `validation_is` | 146.38 | 1.06 | 712 | `completed` |
| `mt5_q01_tier_b_oos` | `Tier B` | `oos` | 137.19 | 1.06 | 566 | `completed` |
| `mt5_q02_tier_a_validation_is` | `Tier A` | `validation_is` | 169.09 | 1.08 | 669 | `completed` |
| `mt5_q02_tier_a_oos` | `Tier A` | `oos` | 160.85 | 1.09 | 507 | `completed` |
| `mt5_q02_tier_b_validation_is` | `Tier B` | `validation_is` | 169.09 | 1.08 | 669 | `completed` |
| `mt5_q02_tier_b_oos` | `Tier B` | `oos` | 160.85 | 1.09 | 507 | `completed` |
| `mt5_q03_tier_a_validation_is` | `Tier A` | `validation_is` | 165.41 | 1.06 | 850 | `completed` |
| `mt5_q03_tier_a_oos` | `Tier A` | `oos` | 184.5 | 1.08 | 627 | `completed` |
| `mt5_q03_tier_b_validation_is` | `Tier B` | `validation_is` | 165.41 | 1.06 | 850 | `completed` |
| `mt5_q03_tier_b_oos` | `Tier B` | `oos` | 184.5 | 1.08 | 627 | `completed` |
| `mt5_q04_tier_a_validation_is` | `Tier A` | `validation_is` | 252.88 | 1.15 | 500 | `completed` |
| `mt5_q04_tier_a_oos` | `Tier A` | `oos` | 169.11 | 1.14 | 350 | `completed` |
| `mt5_q04_tier_b_validation_is` | `Tier B` | `validation_is` | 252.88 | 1.15 | 500 | `completed` |
| `mt5_q04_tier_b_oos` | `Tier B` | `oos` | 169.11 | 1.14 | 350 | `completed` |

## Gate Coverage(게이트 커버리지)

- runtime_evidence_gate(런타임 근거 게이트): `passed`
- scope_completion_gate(범위 완료 게이트): `passed`
- kpi_contract_audit(KPI 계약 감사): `passed`
- final_claim_guard(최종 주장 방어): `passed_no_selected_candidate_no_onnx_no_goal_achieve`

## Boundary(경계)

This run(이번 실행)은 selected candidate(선택 후보), ONNX readiness(온엑스 준비), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), Goal Achieve(목표 달성)를 주장하지 않는다.

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
