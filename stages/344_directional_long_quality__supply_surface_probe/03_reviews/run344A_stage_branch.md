# run344A Stage Branch(344A 단계 분기)

## Decision(결정)

`stage344A_open_run344B_design_directional_long_supply_quality_surface`

## Reason(이유)

Stage343(343단계)은 quality/margin runtime probe(품질/마진 런타임 탐침), trade shape rescue package(거래 형태 복구 패키지), MT5 probe(MT5 탐침), review(검토)까지 포함해 무거워졌다. 다음 질문은 minute block(분 차단) 조정이 아니라 directional long quality surface(방향성 롱 품질 표면)이므로 새 stage(단계)로 분기한다.

Action(행동): `run343G_design_directional_long_supply_quality_surface_without_db_v1`를 직접 이어가지 않고 `run344B_design_directional_long_supply_quality_surface_without_db_v1`로 retarget(재지정)한다.
Effect(효과): Stage343(343단계)의 evidence(근거)는 보존하고, Stage344(344단계)는 long supply recovery(롱 공급 복구) 질문만 받는다.

## Handoff(인계)

- source_best_attempt(원천 최고 시도): `d01_h04_anchor45`
- net_profit(순수익): `152.79`
- profit_factor(수익 팩터): `3.55`
- trade_count(거래수): `22`
- long_short(롱/숏): `2/20`
- queue_rows(대기열 행): `3`
- next_queue(다음 대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344A/run344B_directional_long_supply_quality_surface_queue.csv`

## Claim Boundary(주장 경계)

`state_sync_stage_branch_directional_long_quality_surface_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

No MT5 execution(새 MT5 실행 없음), no Goal Achieve(목표 달성 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음).
