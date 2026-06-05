# run345A Stage Branch(345A 단계 분기)

## Decision(결정)

`stage345A_open_run345B_execute_cash_open_long_quality_short_carry_mt5_probe`

## Reason(이유)

Stage344(344단계)는 directional long quality surface(방향성 롱 품질 표면), s07 validation(검증), deal-level replay(거래별 재생), cash-open decomposition package(현금장 분해 패키지)까지 담아 무거워졌다. 다음 질문은 새 설계(design, 설계)가 아니라 MT5 runtime probe(MT5 런타임 탐침)이므로 Stage345(345단계)로 분기한다.

Action(행동): `run344O_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`를 직접 이어가지 않고 `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`로 retarget(재지정)한다.
Effect(효과): Stage344(344단계)의 evidence(근거)는 보존하고, Stage345(345단계)는 runtime evidence(런타임 근거) 수집만 받는다.

## Handoff(인계)

- source_package(원천 패키지): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- attempts(시도): `6`
- expected_rows(예상 행): `34962`
- feature_rows(피처 행): `5827`
- common_sync_missing(공용 동기화 누락): `0`
- next_queue(다음 대기열): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/02_runs/run345A/run345B_cash_open_long_quality_short_carry_mt5_probe_queue.csv`

## Claim Boundary(주장 경계)

`state_sync_stage_branch_cash_open_long_quality_short_carry_runtime_probe_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

No MT5 execution(새 MT5 실행 없음), no Goal Achieve(목표 달성 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음).
