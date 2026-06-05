# Stage 346 Brief(346단계 개요)

## Stage ID(단계 ID)

`346_cash_open_runtime_review__asymmetric_source_pivot`

## Question(질문)

Can the Stage345 cash-open MT5 runtime probe(Stage345 현금장 MT5 런타임 탐침)를 compact review packet(가벼운 검토 묶음)으로 넘기고, asymmetric model/source pivot(비대칭 모델/원천 전환) 씨앗으로 바꿀 수 있는가?

## Scope(범위)

- source_stage(원천 단계): `345_cash_open_decomposition__long_quality_short_carry_runtime_probe`
- source_run(원천 실행): `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- superseded_planned_run(대체된 예정 실행): `run345C_review_cash_open_long_quality_short_carry_mt5_probe_without_db_v1`
- branch_run(분기 실행): `run346A_branch_stage345_to_cash_open_runtime_review_source_pivot_without_db_v1`
- next_run(다음 실행): `run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1`
- source_package(원천 패키지): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`

Action(행동): Stage345(345단계)의 review(검토) 예정 작업을 Stage346(346단계)으로 분기한다.
Effect(효과): MT5 runtime probe(MT5 런타임 탐침) 산출물은 그대로 보존하고, 다음 작업은 새 stage(단계)의 작은 review(검토) 질문에서 시작한다.

## Source Truth(원천 진실)

- best_attempt(최고 시도): `n01_s07_base_control`
- best_net_profit(최고 순수익): `186.67`
- best_profit_factor(최고 수익 팩터): `4.11`
- best_trade_count(최고 거래수): `26`
- matched_rows(일치 행): `34962/34962`

## Evidence Boundary(근거 경계)

This stage branch(단계 분기)는 state sync(상태 동기화)와 handoff(인계)다. No new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)이다.

## Review Charter(검토 헌장)

- positive clue(긍정 단서): exact runtime parity(정확 런타임 동등성)와 `n01_s07_base_control` 기준 성능을 재판독한다.
- failure memory(실패 기억): single side-filter micro-tuning(단일 방향 필터 미세조정)이 개선을 못 만들었는지 기록한다.
- next offensive seed(다음 공격 탐색 씨앗): long quality/short carry(롱 품질/숏 기여)를 asymmetric source split(비대칭 원천 분리)로 전환한다.

## run346B Review Closeout(346B 검토 종료)

- run_id(실행 ID): `run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1`
- decision(결정): `stage346B_close_stage346_open_stage347_cash_open_asymmetric_source_design`
- next_stage(다음 단계): `347_cash_open_asymmetric_source__long_short_head_design`
- next_run(다음 실행): `run347A_design_cash_open_asymmetric_long_short_source_without_db_v1`
- effect(효과): positive clue(긍정 단서)는 asymmetric source seed(비대칭 원천 씨앗)로 넘기고, single side-filter micro-tuning(단일 방향 필터 미세조정)은 failure memory(실패 기억)로 닫았다.
