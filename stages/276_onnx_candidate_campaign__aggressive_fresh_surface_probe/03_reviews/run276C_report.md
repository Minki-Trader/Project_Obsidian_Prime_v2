# run276C Aggressive Fresh Surface MT5 Signal Replay(276C 공격형 새 표면 MT5 신호 재생)

- status(상태): `completed_aggressive_fresh_surface_mt5_signal_replay_no_candidate_selection`
- run_id(실행 ID): `run276C_aggressive_fresh_surface_mt5_signal_replay_v1`
- source_run(원천 실행): `run276B_materialize_aggressive_fresh_surface_probe_payloads_v1`
- attempts(시도): `48/48`
- planned_attempts(계획 시도): `48`
- KPI records(KPI 기록): `48`
- external_verification_status(외부 검증 상태): `completed`
- judgment(판정): `runtime_probe_completed_inconclusive_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run276D_review_aggressive_fresh_surface_mt5_probe`

## Plain Result(쉬운 결과)

run276C(276C 실행)는 run276B(276B 실행)의 `route_signal_value`를 one-feature EBM table(단일 피처 EBM 표)로 바꿔 MT5(MetaTrader 5, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA)에 넣었다.
효과(effect, 효과): cp275A/cp275B/cp275D(275A/275B/275D 패키지)의 aggressive branch(공격형 분기)가 Python payload(파이썬 페이로드)에만 머물지 않고 Strategy Tester(전략 테스터) 경계까지 이동했는지 기록한다.

## Signal Policy(신호 정책)

- `-1`: short(매도)
- `0`: flat(무포지션)
- `1`: long(매수)
- known difference(알려진 차이): 아직 Adapter package(어댑터 패키지)나 ONNX runtime(ONNX 런타임)이 아니라 signal replay(신호 재생) 탐침이다.

## KPI Preview(KPI 미리보기)

| record_view(기록 보기) | tier(티어) | split(분할) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | status(상태) |
|---|---|---|---:|---:|---:|---|
| `mt5_cp275A_q01_base_surface_tier_a_validation_is` | `Tier A` | `validation_is` | 141.65 | 1.05 | 728 | `completed` |
| `mt5_cp275A_q01_base_surface_tier_a_oos` | `Tier A` | `oos` | 415.71 | 1.21 | 496 | `completed` |
| `mt5_cp275A_q02_score_q70_focus_tier_a_validation_is` | `Tier A` | `validation_is` | 27.18 | 1.01 | 649 | `completed` |
| `mt5_cp275A_q02_score_q70_focus_tier_a_oos` | `Tier A` | `oos` | 88.56 | 1.05 | 435 | `completed` |
| `mt5_cp275A_q03_q04_distance_focus_tier_a_validation_is` | `Tier A` | `validation_is` | 49.37 | 1.02 | 479 | `completed` |
| `mt5_cp275A_q03_q04_distance_focus_tier_a_oos` | `Tier A` | `oos` | 323.89 | 1.26 | 295 | `completed` |
| `mt5_cp275A_q04_risk_q70_focus_tier_a_validation_is` | `Tier A` | `validation_is` | 27.18 | 1.01 | 649 | `completed` |
| `mt5_cp275A_q04_risk_q70_focus_tier_a_oos` | `Tier A` | `oos` | 88.56 | 1.05 | 435 | `completed` |
| `mt5_cp275B_q01_base_surface_tier_a_validation_is` | `Tier A` | `validation_is` | -158.57 | 0.97 | 1570 | `completed` |
| `mt5_cp275B_q01_base_surface_tier_a_oos` | `Tier A` | `oos` | -508.35 | 0.82 | 952 | `completed` |
| `mt5_cp275B_q02_score_q70_focus_tier_a_validation_is` | `Tier A` | `validation_is` | 79.52 | 1.02 | 1280 | `completed` |
| `mt5_cp275B_q02_score_q70_focus_tier_a_oos` | `Tier A` | `oos` | -339.38 | 0.89 | 976 | `completed` |
| `mt5_cp275B_q03_q04_distance_focus_tier_a_validation_is` | `Tier A` | `validation_is` | -172.95 | 0.95 | 1154 | `completed` |
| `mt5_cp275B_q03_q04_distance_focus_tier_a_oos` | `Tier A` | `oos` | -493.95 | 0.77 | 571 | `completed` |
| `mt5_cp275B_q04_risk_q70_focus_tier_a_validation_is` | `Tier A` | `validation_is` | -99.08 | 0.97 | 1286 | `completed` |
| `mt5_cp275B_q04_risk_q70_focus_tier_a_oos` | `Tier A` | `oos` | -299.82 | 0.9 | 939 | `completed` |
| `mt5_cp275D_q01_base_surface_tier_a_validation_is` | `Tier A` | `validation_is` | -17.74 | 1.0 | 1291 | `completed` |
| `mt5_cp275D_q01_base_surface_tier_a_oos` | `Tier A` | `oos` | -265.52 | 0.92 | 1003 | `completed` |
| `mt5_cp275D_q02_score_q70_focus_tier_a_validation_is` | `Tier A` | `validation_is` | 11.34 | 1.0 | 1191 | `completed` |
| `mt5_cp275D_q02_score_q70_focus_tier_a_oos` | `Tier A` | `oos` | 65.5 | 1.02 | 904 | `completed` |
| `mt5_cp275D_q03_q04_distance_focus_tier_a_validation_is` | `Tier A` | `validation_is` | -83.39 | 0.97 | 1030 | `completed` |
| `mt5_cp275D_q03_q04_distance_focus_tier_a_oos` | `Tier A` | `oos` | -432.48 | 0.85 | 770 | `completed` |
| `mt5_cp275D_q04_risk_q70_focus_tier_a_validation_is` | `Tier A` | `validation_is` | -41.33 | 0.99 | 1040 | `completed` |
| `mt5_cp275D_q04_risk_q70_focus_tier_a_oos` | `Tier A` | `oos` | -194.92 | 0.92 | 763 | `completed` |

## Gate Coverage(게이트 커버리지)

- runtime_attempt_gate(런타임 시도 게이트): `passed`
- mt5_output_gate(MT5 출력 게이트): `passed`
- final_claim_guard(최종 주장 방어): `passed_no_selected_candidate_no_onnx_no_goal_achieve`

## Boundary(경계)

This run(이번 실행)은 selected candidate(선택 후보), ONNX readiness(ONNX 준비), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), Goal Achieve(목표 달성)를 주장하지 않는다.

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
