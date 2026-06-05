# Stage 343(343단계)

Stage 343(343단계)는 run342H early-long quality/margin mix package(342H 초반 롱 품질/마진 혼합 패키지)를 실제 MT5 runtime probe(MT5 런타임 탐침)로 실행하고 검토하는 가벼운 단계다.

- current_run(현재 실행): `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- branch_run(분기 실행): `run343A_branch_stage342_to_quality_margin_runtime_probe_without_db_v1`
- source(원천): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- source_package(원천 패키지): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342H/runtime_probe_attempt_package.csv`

Effect(효과): package(패키지) 제작과 MT5 execution(실행)을 분리해 장부와 보고서가 너무 무거워지는 일을 줄인다.

## run343B Early Long Quality Margin Mix MT5 Probe(343B 초반 롱 품질/마진 혼합 MT5 탐침)

- run_id(실행 ID): `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- summary(요약): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343B/early_long_quality_margin_mix_mt5_probe_summary.csv`
- diff(차이): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343B/proxy_mt5_runtime_difference.csv`
- effect(효과): run343C(343C 실행) review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.
## run343C Early Long Quality Margin Mix Review(343C 초반 롱 품질/마진 혼합 검토)

- run_id(실행 ID): `run343C_review_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343C/quality_margin_review_scorecard.csv`
- failure_memory(실패 기억): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343C/failure_memory.csv`
- next_queue(다음 대기열): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343C/run343D_trade_shape_rescue_quality_margin_blend_queue.csv`
- effect(효과): run343D(343D 실행)가 수익 앵커와 거래 형태 복구를 함께 시험한다.
## run343C Early Long Quality Margin Mix Review(343C 초반 롱 품질/마진 혼합 검토)

- run_id(실행 ID): `run343C_review_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343C/quality_margin_review_scorecard.csv`
- failure_memory(실패 기억): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343C/failure_memory.csv`
- next_queue(다음 대기열): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343C/run343D_trade_shape_rescue_quality_margin_blend_queue.csv`
- effect(효과): run343D(343D 실행)가 수익 앵커와 거래 형태 복구를 함께 시험한다.

## run343D Trade Shape Rescue Package(343D 거래 형태 복구 패키지)

- run_id(실행 ID): `run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1`
- queue(대기열): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343D/run343E_queue.csv`
- effect(효과): Stage342(342단계)의 무거운 탐색을 Stage343(343단계)의 좁은 런타임 탐침 실행으로 분기한다.

## run343E Trade Shape Rescue MT5 Probe(343E 거래 형태 복구 MT5 탐침)

- run_id(실행 ID): `run343E_execute_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- summary(요약): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343E/trade_shape_rescue_quality_margin_blend_mt5_probe_summary.csv`
- diff(차이): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343E/proxy_mt5_runtime_difference.csv`
- effect(효과): run343F(343F 실행) review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.

## run343E Trade Shape Rescue MT5 Probe(343E 거래 형태 복구 MT5 탐침)

- run_id(실행 ID): `run343E_execute_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- summary(요약): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343E/trade_shape_rescue_quality_margin_blend_mt5_probe_summary.csv`
- diff(차이): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343E/proxy_mt5_runtime_difference.csv`
- effect(효과): run343F(343F 실행) review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.
## run343F Trade Shape Rescue Review(343F 거래 형태 복구 검토)

- run_id(실행 ID): `run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343F/trade_shape_rescue_review_scorecard.csv`
- failure_memory(실패 기억): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343F/failure_memory.csv`
- next_queue(다음 대기열): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343F/run343G_directional_long_supply_quality_surface_queue.csv`
- effect(효과): run343G(343G 실행)가 minute block(분 차단)이 아니라 directional long quality surface(방향성 롱 품질 표면)를 탐색한다.
## run343F Trade Shape Rescue Review(343F 거래 형태 복구 검토)

- run_id(실행 ID): `run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343F/trade_shape_rescue_review_scorecard.csv`
- failure_memory(실패 기억): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343F/failure_memory.csv`
- next_queue(다음 대기열): `stages/343_quality_margin_runtime__early_long_mix_mt5_probe/02_runs/run343F/run343G_directional_long_supply_quality_surface_queue.csv`
- effect(효과): run343G(343G 실행)가 minute block(분 차단)이 아니라 directional long quality surface(방향성 롱 품질 표면)를 탐색한다.

## Stage344 Branch Handoff(344단계 분기 인계)

- branch_run(분기 실행): `run344A_branch_stage343_to_directional_long_supply_quality_surface_without_db_v1`
- next_stage(다음 단계): `344_directional_long_quality__supply_surface_probe`
- next_run(다음 실행): `run344B_design_directional_long_supply_quality_surface_without_db_v1`
- effect(효과): Stage343(343단계)은 trade shape rescue review(거래 형태 복구 검토)에서 멈추고, directional long quality surface(방향성 롱 품질 표면)를 새 단계로 넘긴다.
