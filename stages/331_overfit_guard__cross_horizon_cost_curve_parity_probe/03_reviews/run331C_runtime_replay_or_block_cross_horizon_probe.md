# run331C Runtime Replay Or Block Cross-Horizon Probe(331C 런타임 재생 또는 차단 교차 기간 탐침)

- run_id(실행 ID): `run331C_runtime_replay_or_block_cross_horizon_probe_v1`
- parent_run_id(부모 실행 ID): `run331B_materialize_no_retune_replay_and_resampling_controls_v1`
- status(상태): `completed_runtime_replay_cross_horizon_probe_no_forward_decision`
- judgment(판정): `runtime_replay_completed_research_only_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- completed_attempt_count(완료 시도 수): `6/6`
- matched_attempt_count(일치 시도 수): `6/6`
- blockers(차단 사유): `none`

## Scope(범위)

run331C는 run330E의 ONNX(온엑스), feature CSV(피처 CSV), feature order(피처 순서), threshold(임계값), fixed lot(고정 로트), max hold(최대 보유), ATR/risk 설정(ATR/위험 설정)을 바꾸지 않았다.
변경한 것은 run331C 전용 report/telemetry(보고서/실행 기록) 경로와 run id(실행 ID)뿐이다.

Effect(효과): 수익을 좋게 만들기 위한 재튜닝(retuning, 재튜닝)이 아니라, 같은 런타임 입력이 새 경로에서도 재현되는지 본다.

## Replay Summary(재생 요약)

| attempt(시도) | tester(테스터) | runtime(런타임) | match(일치) | net delta(순손익 차이) | PF delta(PF 차이) | trades(거래수) |
|---|---|---|---|---:|---:|---:|
| c56_bal_rf | completed | completed | true | 0.0 | 0.0 | 75 |
| c56_plain_rf | completed | completed | true | 0.0 | 0.0 | 77 |
| m48_bal_rf | completed | completed | true | 0.0 | 0.0 | 277 |
| m48_plain_rf | completed | completed | true | 0.0 | 0.0 | 269 |
| u42_bal_rf | completed | completed | true | 0.0 | 0.0 | 323 |
| u42_plain_rf | completed | completed | true | 0.0 | 0.0 | 326 |

## Boundary(경계)

- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_runtime_replay_cross_horizon_probe_no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Next(다음)

`run331D_final_cross_horizon_overfit_guard_decision_v1`
