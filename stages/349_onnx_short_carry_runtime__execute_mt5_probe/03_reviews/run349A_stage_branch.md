# run349A Stage Branch(349A 단계 분기)

## Decision(결정)

`stage349A_open_run349B_execute_onnx_deployable_short_carry_mt5_probe`

## Reason(이유)

Stage348(348단계)은 proxy review(프록시 검토), short-carry seed triage(숏 기여 씨앗 분류), ONNX package materialization(온엑스 패키지 물질화), run348D queue(348D 대기열)까지 담아 무거워졌다. 다음 질문은 review(검토)가 아니라 MT5 runtime execution(MT5 런타임 실행)이므로 Stage349(349단계)로 분기한다.

Action(행동): `run348D_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`를 직접 이어가지 않고 `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`로 retarget(재지정)한다.
Effect(효과): Stage348(348단계)의 evidence(근거)는 보존하고, Stage349(349단계)는 runtime evidence(런타임 근거) 수집만 받는다.

## Handoff(인계)

- source_package(원천 패키지): `run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1`
- attempts(시도): `4`
- expected_rows(예상 행): `23308`
- feature_rows(피처 행): `5827`
- feature_count(피처 수): `53`
- common_sync_missing(공용 동기화 누락): `0`
- missing_mt5_contract_features(누락 MT5 계약 피처): `5`
- cash_open_partial_mapping_attempts(현금장 부분 매핑 시도): `2`
- next_queue(다음 대기열): `stages/349_onnx_short_carry_runtime__execute_mt5_probe/02_runs/run349A/run349B_onnx_short_carry_mt5_probe_queue.csv`
- trade_density_requirement(거래 밀도 요구): `trade_per_day_min_3_to_10_plus_no_trade_splitting`

## Boundary(경계)

`state_sync_stage_branch_onnx_short_carry_runtime_probe_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

No new MT5 execution(새 MT5 실행 없음), no Goal Achieve(목표 달성 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음).
