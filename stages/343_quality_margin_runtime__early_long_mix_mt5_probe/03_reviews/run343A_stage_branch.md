# run343A Stage Branch(343A 단계 분기)

## Decision(결정)

`stage343A_open_run343B_execute_early_long_quality_margin_mix_probe`

## Reason(이유)

Stage 342(342단계)는 hard firewall(강한 방화벽), soft-window(부드러운 구간), quality/margin package(품질/마진 패키지)까지 담아 무거워졌다. 사용자가 stage branch(단계 분기)를 요청했으므로 MT5 runtime execution(MT5 런타임 실행)은 Stage 343(343단계)에서 시작한다.

Action(행동): `run342I_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`를 직접 이어가지 않고 `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`로 retarget(재지정)했다.
Effect(효과): run342H package(342H 패키지)는 보존하고, 다음 MT5 evidence(MT5 근거)는 새 stage ledger(단계 장부)에 쌓인다.

## Handoff(인계)

- source_package(원천 패키지): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342H/runtime_probe_attempt_package.csv`
- new_queue(새 대기열): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343A/run343B_queue.csv`
- attempts(시도): `8`
- package_rows(패키지 행): `5827`
- feature_count(피처 수): `53`
- side_filter_blocked_rows(사이드 필터 차단 행): `54`
- preview_signal_trade_count_range(미리보기 신호 거래수 범위): `114`-`131`
- preview_side_balance_range(미리보기 롱/숏 균형 범위): `0.01724138`-`0.12931034`

## Claim Boundary(주장 경계)

`state_sync_stage_branch_quality_margin_runtime_handoff_only_no_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

No MT5 execution(새 MT5 실행 없음), no Goal Achieve(목표 달성 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음).
