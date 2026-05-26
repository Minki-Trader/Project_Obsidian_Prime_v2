# Run330E Raw-Forward MT5 Runtime Probe Or Block(330E 원본 전진 MT5 런타임 탐침 또는 차단)

- run_id(실행 ID): `run330E_mt5_runtime_probe_or_block_v1`
- status(상태): `blocked_raw_forward_mt5_runtime_probe_no_completed_runtime`
- judgment(판정): `raw_forward_runtime_probe_blocked_requires_runtime_repair_no_goal_achieve`
- decision(결정): `stage330E_forward_blocked_runtime_probe_missing_no_pass_fail_judgment`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- blockers(차단 사유): `terminal_already_running_config_not_applied`

## Scope(범위)

run330E(330E 실행)는 run330B(330B 실행)의 raw_forward(원본 전진) prediction timestamp(예측 타임스탬프), run329B(329B 실행)의 feature order(피처 순서), run329C(329C 실행)의 ONNX(온엑스)를 그대로 MT5(`MetaTrader 5`, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA) 입력으로 만든다.

Effect(효과): 새 학습, threshold retuning(임계값 재조정), D/B rule(D/B 규칙) 변경, lot optimization(로트 최적화) 없이 handoff(인계)와 tester execution(테스터 실행)만 검증한다.

## Attempt Summary(시도 요약)

| attempt(시도) | candidate(후보) | tester(테스터) | runtime(런타임) | blocker(차단 사유) | model_ok(모델 성공) | orders(주문) | PF(수익 팩터) | trades(거래) |
|---|---|---|---|---|---:|---:|---:|---:|
| c56_bal_rf | c56_bal | blocked | blocked | terminal_already_running_config_not_applied |  |  |  |  |
| c56_plain_rf | c56_plain | not_attempted | not_attempted |  |  |  |  |  |
| m48_bal_rf | m48_bal | not_attempted | not_attempted |  |  |  |  |  |
| m48_plain_rf | m48_plain | not_attempted | not_attempted |  |  |  |  |  |
| u42_bal_rf | u42_bal | not_attempted | not_attempted |  |  |  |  |  |
| u42_plain_rf | u42_plain | not_attempted | not_attempted |  |  |  |  |  |

## Boundary(경계)

- completed_attempt_count(완료 시도 수): `0`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_raw_forward_mt5_runtime_probe_no_threshold_retuning_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Next(다음)

`repair_stage330E_runtime_probe_blocker_then_rerun`
