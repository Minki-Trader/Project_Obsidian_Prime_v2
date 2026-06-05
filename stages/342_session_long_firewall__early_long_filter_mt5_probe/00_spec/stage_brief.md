# Stage 342 Brief(342단계 개요)

## Stage ID(단계 ID)

`342_session_long_firewall__early_long_filter_mt5_probe`

## Question(질문)

Can session-long firewall(세션 롱 방화벽), especially early-long block(초반 롱 차단), improve q01/q09(큐01/큐09) MT5 runtime probe(MT5 런타임 탐침) quality without turning the clue into overfiltering(과필터링)?

## Scope(범위)

- source_stage(원천 단계): `341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue`
- source_review_run(원천 검토 실행): `run341D_review_f01_stability_cost_regime_validation_without_db_v1`
- branch_run(분기 실행): `run342A_branch_stage341_to_session_long_firewall_probe_without_db_v1`
- superseded_run(대체된 실행): `run341E_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1`
- next_run(다음 실행): `run342B_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1`

Action(행동): Stage 341(341단계)의 validation review(검증 검토) 뒤 MT5 package(MT5 패키지) 작업을 Stage 342(342단계)로 분리한다.
Effect(효과): Stage 341(341단계)을 더 키우지 않고, session-long firewall(세션 롱 방화벽)만 좁게 압박 시험한다.

## Evidence Boundary(근거 경계)

This stage branch(단계 분기)는 no new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음)이다.

## run342C F01 Session-Long Firewall MT5 Probe(342C F01 세션 롱 방화벽 MT5 탐침)

- run_id(실행 ID): `run342C_execute_f01_session_long_firewall_mt5_probe_without_db_v1`
- attempts(시도): `5`
- matched_rows(일치 행): `29135/29135`
- best_attempt(최고 시도): `e04_q09_blk_early_long`
- effect(효과): Stage342(342단계) package(패키지)를 실제 MT5(메타트레이더5) 근거로 바꾼다.

## run342D F01 Session-Long Firewall Review(342D F01 세션 롱 방화벽 검토)

- run_id(실행 ID): `run342D_review_f01_session_long_firewall_mt5_probe_without_db_v1`
- best_profit_attempt(최고 수익 시도): `e04_q09_blk_early_long`
- next(다음): `run342E_materialize_soft_session_long_firewall_mt5_probe_package_without_db_v1`
- effect(효과): hard firewall(강한 방화벽)은 단서로 보존하고 softer firewall(부드러운 방화벽) 탐색으로 넘긴다.

## run342E Soft Session-Long Firewall Package(342E 부드러운 세션 롱 방화벽 패키지)

- run_id(실행 ID): `run342E_materialize_soft_session_long_firewall_mt5_probe_package_without_db_v1`
- attempts(시도): `7`
- side_filter_blocked_rows(사이드 필터 차단 행): `68`
- next(다음): `run342F_execute_soft_session_long_firewall_mt5_probe_without_db_v1`
- effect(효과): hard firewall(강한 방화벽)의 수익 단서를 soft-window(부드러운 구간) MT5 실행으로 넘긴다.

## run342F Soft Session-Long Firewall MT5 Probe(342F 부드러운 세션 롱 방화벽 MT5 탐침)

- run_id(실행 ID): `run342F_execute_soft_session_long_firewall_mt5_probe_without_db_v1`
- attempts(시도): `7`
- matched_rows(일치 행): `40789/40789`
- best_attempt(최고 시도): `e04_q09_blk_early45`
- effect(효과): soft-window(부드러운 구간) package(패키지)를 실제 MT5(메타트레이더5) 근거로 바꾼다.

## run342G Soft Firewall Review(342G 부드러운 방화벽 검토)

- run_id(실행 ID): `run342G_review_soft_session_long_firewall_mt5_probe_without_db_v1`
- best_attempt(최고 시도): `e04_q09_blk_early45`
- next(다음): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- effect(효과): soft-window(부드러운 구간) 반복을 닫고 quality/margin(품질/마진) 탐색으로 넘긴다.

## run342H Early Long Quality Margin Mix Package(342H 초반 롱 품질/마진 혼합 패키지)

- run_id(실행 ID): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- attempts(시도): `8`
- side_filter_blocked_rows(사이드 필터 차단 행): `54`
- next(다음): `run342I_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- effect(효과): soft-window(부드러운 구간) 실패 기억을 quality/margin(품질/마진) MT5 실행으로 넘긴다.

## Stage343 Branch Handoff(343단계 분기 인계)

- branch_run(분기 실행): `run343A_branch_stage342_to_quality_margin_runtime_probe_without_db_v1`
- next_stage(다음 단계): `343_quality_margin_runtime__early_long_mix_mt5_probe`
- next_run(다음 실행): `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- effect(효과): Stage 342(342단계)를 run342H package(342H 패키지)에서 멈추고, MT5 runtime probe(MT5 런타임 탐침)를 새 장부에서 시작한다.
