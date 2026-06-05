# Stage 343 Brief(343단계 개요)

## Stage ID(단계 ID)

`343_quality_margin_runtime__early_long_mix_mt5_probe`

## Question(질문)

Can the run342H early-long quality/margin mix package(342H 초반 롱 품질/마진 혼합 패키지) survive MT5 runtime probe(MT5 런타임 탐침) with acceptable trade count(거래수), profit factor(수익 팩터), expectancy(기대값), drawdown(낙폭), recovery factor(회복 계수), and long/short balance(롱/숏 균형)?

## Scope(범위)

- source_stage(원천 단계): `342_session_long_firewall__early_long_filter_mt5_probe`
- source_package_run(원천 패키지 실행): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- branch_run(분기 실행): `run343A_branch_stage342_to_quality_margin_runtime_probe_without_db_v1`
- superseded_run(대체된 실행): `run342I_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- next_run(다음 실행): `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`

Action(행동): Stage 342(342단계)의 completed package(완료 패키지)를 Stage 343(343단계)의 MT5 execution input(MT5 실행 입력)으로 넘긴다.
Effect(효과): Stage 342(342단계)를 더 무겁게 만들지 않고, quality/margin runtime probe(품질/마진 런타임 탐침)만 새 단계에서 좁게 검증한다.

## Evidence Boundary(근거 경계)

This stage branch(단계 분기)는 no new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음)이다.

## run343B Early Long Quality Margin Mix MT5 Probe(343B 초반 롱 품질/마진 혼합 MT5 탐침)

- run_id(실행 ID): `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- attempts(시도): `8`
- matched_rows(일치 행): `46616/46616`
- best_attempt(최고 시도): `h04_q02_l515_blk45`
- effect(효과): run342H package(342H 패키지)를 실제 MT5(메타트레이더5) 근거로 바꾼다.
## run343C Early Long Quality Margin Mix Review(343C 초반 롱 품질/마진 혼합 검토)

- run_id(실행 ID): `run343C_review_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- best_attempt(최고 시도): `h04_q02_l515_blk45`
- judgment(판정): `quality_margin_improves_profit_quality_but_does_not_recover_trade_shape_no_selection`
- next(다음): `run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1`
- effect(효과): 수익 품질 단서는 보존하고 trade shape(거래 형태) 미회복을 다음 제약으로 넘긴다.
## run343C Early Long Quality Margin Mix Review(343C 초반 롱 품질/마진 혼합 검토)

- run_id(실행 ID): `run343C_review_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- best_attempt(최고 시도): `h04_q02_l515_blk45`
- judgment(판정): `quality_margin_improves_profit_quality_but_does_not_recover_trade_shape_no_selection`
- next(다음): `run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1`
- effect(효과): 수익 품질 단서는 보존하고 trade shape(거래 형태) 미회복을 다음 제약으로 넘긴다.

## run343E Trade Shape Rescue MT5 Probe(343E 거래 형태 복구 MT5 탐침)

- run_id(실행 ID): `run343E_execute_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- attempts(시도): `10`
- matched_rows(일치 행): `58270/58270`
- best_attempt(최고 시도): `d01_h04_anchor45`
- effect(효과): run343D package(343D 패키지)를 실제 MT5(메타트레이더5) 근거로 바꾼다.

## run343E Trade Shape Rescue MT5 Probe(343E 거래 형태 복구 MT5 탐침)

- run_id(실행 ID): `run343E_execute_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- attempts(시도): `10`
- matched_rows(일치 행): `58270/58270`
- best_attempt(최고 시도): `d01_h04_anchor45`
- effect(효과): run343D package(343D 패키지)를 실제 MT5(메타트레이더5) 근거로 바꾼다.
## run343F Trade Shape Rescue Review(343F 거래 형태 복구 검토)

- run_id(실행 ID): `run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- best_attempt(최고 시도): `d01_h04_anchor45`
- judgment(판정): `trade_shape_rescue_failed_to_improve_anchor_profit_quality_preserved_no_selection`
- next(다음): `run343G_design_directional_long_supply_quality_surface_without_db_v1`
- effect(효과): 수익 앵커는 보존하고, 거래 형태 복구 실패를 다음 방향성 롱 품질 표면 설계의 제약으로 바꾼다.
## run343F Trade Shape Rescue Review(343F 거래 형태 복구 검토)

- run_id(실행 ID): `run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- best_attempt(최고 시도): `d01_h04_anchor45`
- judgment(판정): `trade_shape_rescue_failed_to_improve_anchor_profit_quality_preserved_no_selection`
- next(다음): `run343G_design_directional_long_supply_quality_surface_without_db_v1`
- effect(효과): 수익 앵커는 보존하고, 거래 형태 복구 실패를 다음 방향성 롱 품질 표면 설계의 제약으로 바꾼다.

## Stage344 Branch Handoff(344단계 분기 인계)

- branch_run(분기 실행): `run344A_branch_stage343_to_directional_long_supply_quality_surface_without_db_v1`
- next_stage(다음 단계): `344_directional_long_quality__supply_surface_probe`
- next_run(다음 실행): `run344B_design_directional_long_supply_quality_surface_without_db_v1`
- effect(효과): Stage343(343단계)은 trade shape rescue review(거래 형태 복구 검토)에서 멈추고, directional long quality surface(방향성 롱 품질 표면)를 새 단계로 넘긴다.
