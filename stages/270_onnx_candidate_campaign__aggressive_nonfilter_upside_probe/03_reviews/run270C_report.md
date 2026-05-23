# Stage270 Run270C Aggressive Probe MT5 Signal Replay(270단계 270C 공격형 탐침 MT5 신호 재생)

- status(상태): `completed_aggressive_probe_mt5_signal_replay_no_candidate_selection`
- run(실행): `run270C_aggressive_probe_mt5_signal_replay_v1`
- source_run(원천 실행): `run270B_aggressive_probe_payload_materialization_v1`
- attempts(시도): `20/20`
- KPI records(KPI 기록): `20`
- judgment(판정): `runtime_probe_completed_inconclusive_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run270D_balance_time_slice_trade_quality_review`

## Plain Result(쉬운 결과)

run270C(270C 실행)는 run270B(270B 실행)의 `variant_decision_flag`를 one-feature EBM table(단일 피처 EBM 표)로 바꿔 MT5(`MetaTrader 5`, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA)에 넣었다.
효과(effect, 효과): 공격형 branch(분기)가 Python payload(파이썬 페이로드)에만 머물지 않고 Strategy Tester(전략 테스터) 시도와 KPI(핵심 성과 지표) 경계까지 이동한다.

## Runtime Boundary(런타임 경계)

- signal policy(신호 정책): `variant_decision_flag=1`은 long(롱), `0`은 flat(무포지션)으로 재생한다.
- known difference(알려진 차이): Stage270(270단계) payload(페이로드)는 short side(숏 방향)를 갖고 있지 않다.
- effect(효과): 이 결과는 long-only runtime probe(롱 전용 런타임 탐침)이며 최종 candidate package(후보 패키지)나 ONNX readiness(온엑스 준비)를 만들지 않는다.

## KPI Preview(KPI 미리보기)

| record_view(기록 보기) | tier(티어) | split(분할) | net_profit(순손익) | PF(수익 팩터) | trades(거래 수) | status(상태) |
|---|---|---|---:|---:|---:|---|
| `mt5_q01_tier_a_validation_is` | `Tier A` | `validation_is` | 154.17 | 1.09 | 374 | `completed` |
| `mt5_q01_tier_a_oos` | `Tier A` | `oos` | 42.56 | 1.03 | 264 | `completed` |
| `mt5_q01_tier_b_validation_is` | `Tier B` | `validation_is` | 154.17 | 1.09 | 374 | `completed` |
| `mt5_q01_tier_b_oos` | `Tier B` | `oos` | 42.56 | 1.03 | 264 | `completed` |
| `mt5_q02_tier_a_validation_is` | `Tier A` | `validation_is` | 15.33 | 1.01 | 405 | `completed` |
| `mt5_q02_tier_a_oos` | `Tier A` | `oos` | -151.87 | 0.88 | 277 | `completed` |
| `mt5_q02_tier_b_validation_is` | `Tier B` | `validation_is` | 15.33 | 1.01 | 405 | `completed` |
| `mt5_q02_tier_b_oos` | `Tier B` | `oos` | -151.87 | 0.88 | 277 | `completed` |
| `mt5_q03_tier_a_validation_is` | `Tier A` | `validation_is` | 223.03 | 1.09 | 579 | `completed` |
| `mt5_q03_tier_a_oos` | `Tier A` | `oos` | -11.74 | 0.99 | 441 | `completed` |
| `mt5_q03_tier_b_validation_is` | `Tier B` | `validation_is` | 223.03 | 1.09 | 579 | `completed` |
| `mt5_q03_tier_b_oos` | `Tier B` | `oos` | -11.74 | 0.99 | 441 | `completed` |
| `mt5_q04_tier_a_validation_is` | `Tier A` | `validation_is` | 176.35 | 1.12 | 307 | `completed` |
| `mt5_q04_tier_a_oos` | `Tier A` | `oos` | -94.25 | 0.92 | 213 | `completed` |
| `mt5_q04_tier_b_validation_is` | `Tier B` | `validation_is` | 176.35 | 1.12 | 307 | `completed` |
| `mt5_q04_tier_b_oos` | `Tier B` | `oos` | -94.25 | 0.92 | 213 | `completed` |
| `mt5_q05_tier_a_validation_is` | `Tier A` | `validation_is` | 117.9 | 1.05 | 546 | `completed` |
| `mt5_q05_tier_a_oos` | `Tier A` | `oos` | -85.39 | 0.95 | 408 | `completed` |
| `mt5_q05_tier_b_validation_is` | `Tier B` | `validation_is` | 117.9 | 1.05 | 546 | `completed` |
| `mt5_q05_tier_b_oos` | `Tier B` | `oos` | -85.39 | 0.95 | 408 | `completed` |

## Required Gate Coverage(필수 게이트 커버리지)

- runtime_evidence_gate(런타임 근거 게이트): `passed`
- scope_completion_gate(범위 완료 게이트): `passed`
- kpi_contract_audit(KPI 계약 감사): `passed`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): `passed`
- final_claim_guard(최종 주장 가드): `passed_no_selected_candidate_no_onnx_no_goal_achieve`

## Boundary(경계)

This run(이 실행)은 deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
