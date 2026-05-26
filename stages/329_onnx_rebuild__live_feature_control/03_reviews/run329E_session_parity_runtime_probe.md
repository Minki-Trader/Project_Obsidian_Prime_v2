# run329E Session Parity Runtime Probe(329E 세션 동등 런타임 탐침)

- run_id(실행 ID): `run329E_session_parity_forward_signal_payload_and_mt5_runtime_probe_v1`
- status(상태): `blocked_session_parity_runtime_probe_no_completed_mt5_runtime`
- judgment(판정): `runtime_probe_blocked_requires_runtime_repair_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- blockers(차단 사유): `terminal_already_running_config_not_applied`

## Scope(범위)

run329E(329E 실행)는 run329D(329D 실행)의 old_session_parity(기존 세션 동등) prediction(예측) timestamp(타임스탬프)를 그대로 써서 MT5(`MetaTrader 5`, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA) 입력을 만들었다.

Effect(효과): 새 threshold(임계값), 새 decision rule(판단 규칙), 새 lot/risk optimization(랏/위험 최적화)을 만들지 않고, Python/ONNX(파이썬/온엑스) 점수가 MT5 RuntimeProbeEA(런타임 탐침 EA)에서 읽히는지 확인한다.

## Attempt Summary(시도 요약)

| attempt(시도) | candidate(후보) | tester(테스터) | runtime(런타임) | blocker(차단 사유) | model_ok(모델 성공) | orders(주문) | PF(수익 팩터) | trades(거래) |
|---|---|---|---|---|---:|---:|---:|---:|
| c56_bal_sp | c56_bal | blocked | blocked | terminal_already_running_config_not_applied |  |  |  |  |
| c56_plain_sp | c56_plain | not_attempted | not_attempted |  |  |  |  |  |
| m48_bal_sp | m48_bal | not_attempted | not_attempted |  |  |  |  |  |
| m48_plain_sp | m48_plain | not_attempted | not_attempted |  |  |  |  |  |
| u42_bal_sp | u42_bal | not_attempted | not_attempted |  |  |  |  |  |
| u42_plain_sp | u42_plain | not_attempted | not_attempted |  |  |  |  |  |

## Boundary(경계)

- completed_attempt_count(완료 시도 수): `0`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- Forward Passed(전진 통과): `not_claimed`
- effect(효과): tester output(테스터 출력)이 있더라도 다음 run329F(329F 실행)에서 KPI(핵심 성과 지표), curve pocket(곡선 포켓), regime/cost slice(국면/비용 구간)를 다시 판독해야 한다.

`research_development_only_session_parity_mt5_runtime_probe_no_threshold_retuning_no_selected_candidate_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Next(다음)

`repair_stage329E_runtime_probe_blocker_then_rerun`
