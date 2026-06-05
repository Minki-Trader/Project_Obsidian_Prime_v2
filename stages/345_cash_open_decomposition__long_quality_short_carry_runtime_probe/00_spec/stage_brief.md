# Stage 345 Brief(345단계 개요)

## Stage ID(단계 ID)

`345_cash_open_decomposition__long_quality_short_carry_runtime_probe`

## Question(질문)

Can the cash-open long quality/short carry decomposition(현금장 롱 품질/숏 기여 분해) survive an MT5 runtime probe(MT5 런타임 탐침) without turning Stage344(344단계) into a heavier validation sink(검증 싱크)?

## Scope(범위)

- source_stage(원천 단계): `344_directional_long_quality__supply_surface_probe`
- source_package_run(원천 패키지 실행): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- branch_run(분기 실행): `run345A_branch_stage344_to_cash_open_long_quality_short_carry_runtime_probe_without_db_v1`
- superseded_run(대체된 실행): `run344O_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- next_run(다음 실행): `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`

Action(행동): Stage344(344단계)의 run344O runtime probe(런타임 탐침)를 run345B(345B 실행)로 retarget(재지정)한다.
Effect(효과): Stage344(344단계)는 directional long quality surface(방향성 롱 품질 표면)와 package handoff(패키지 인계)까지로 멈추고, MT5 execution(MT5 실행)은 새 stage(단계)에서 읽는다.

## Source Truth(원천 진실)

- package_run(패키지 실행): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- package_status(패키지 상태): `completed_stage344N_cash_open_long_quality_short_carry_package_materialized_no_mt5_execution`
- attempts(시도): `6`
- expected_rows(예상 행): `34962`
- feature_rows(피처 행): `5827`
- common_sync_missing(공용 동기화 누락): `0`
- single_side_filter_limit(단일 사이드 필터 한계): recorded in packageability matrix(포장 가능성 표에 기록됨)

## Evidence Boundary(근거 경계)

This branch(분기)는 state sync(상태 동기화)와 handoff(인계)만 수행한다. No new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음)이다.

## run345B Cash-Open Runtime MT5 Probe(345B 현금장 런타임 MT5 탐침)

- run_id(실행 ID): `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- attempts(시도): `6`
- matched_rows(일치 행): `34962/34962`
- best_attempt(최고 시도): `n01_s07_base_control`
- effect(효과): run344N package(344N 패키지)를 실제 MT5(메타트레이더5) 근거로 바꿨다.

## run346A Review Handoff(346A 검토 인계)

- branch_run(분기 실행): `run346A_branch_stage345_to_cash_open_runtime_review_source_pivot_without_db_v1`
- next_stage(다음 단계): `346_cash_open_runtime_review__asymmetric_source_pivot`
- next_run(다음 실행): `run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1`
- action(행동): Stage345(345단계)의 run345C review(345C 검토)를 Stage346(346단계)으로 이동했다.
- effect(효과): Stage345(345단계)는 runtime probe(MT5 런타임 탐침) 근거까지로 가볍게 멈추고, 검토는 새 stage(단계)에서 이어간다.
