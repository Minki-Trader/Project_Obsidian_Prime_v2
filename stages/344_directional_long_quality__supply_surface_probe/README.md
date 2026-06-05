# Stage 344(344단계)

Stage344(344단계)는 directional long quality surface(방향성 롱 품질 표면)만 다룬다.

- current_run(현재 실행): `run344B_design_directional_long_supply_quality_surface_without_db_v1`
- branch_run(분기 실행): `run344A_branch_stage343_to_directional_long_supply_quality_surface_without_db_v1`
- source_review(원천 검토): `run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- retargeted_queue(재지정 대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344A/run344B_directional_long_supply_quality_surface_queue.csv`

Effect(효과): minute block micro-tuning(분 차단 미세조정)을 Stage343(343단계)에서 더 반복하지 않고, long supply quality(롱 공급 품질)를 새 질문으로 분리한다.

## run344C Directional Long Quality Surface Package(344C 방향성 롱 품질 표면 패키지)

- package(패키지): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344C/runtime_probe_attempt_package.csv`
- queue(대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344C/run344D_queue.csv`
- effect(효과): Stage344(344단계)가 MT5 실행 단계로 넘어갈 준비를 마쳤다.

## run344D Directional Long Quality Surface MT5 Probe(344D 방향성 롱 품질 표면 MT5 탐침)

- run_id(실행 ID): `run344D_execute_directional_long_supply_quality_surface_mt5_probe_without_db_v1`
- summary(요약): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344D/directional_long_quality_surface_mt5_probe_summary.csv`
- diff(차이): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344D/proxy_mt5_runtime_difference.csv`
- effect(효과): run344E(344E 실행) review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.

## run344E Directional Long Quality Surface Review(344E 방향성 롱 품질 표면 검토)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344E_directional_long_quality_surface_mt5_probe_review.md`
- scorecard(점수표): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344E/directional_long_quality_surface_review_scorecard.csv`
- next_queue(다음 대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344E/run344F_s07_trend_confirmed_forward_cost_stability_validation_queue.csv`
- effect(효과): positive clue(긍정 단서)와 failure memory(실패 기억)를 분리함.

## run344E Directional Long Quality Surface Review(344E 방향성 롱 품질 표면 검토)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344E_directional_long_quality_surface_mt5_probe_review.md`
- scorecard(점수표): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344E/directional_long_quality_surface_review_scorecard.csv`
- next_queue(다음 대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344E/run344F_queue.csv`
- effect(효과): positive clue(긍정 단서)와 failure memory(실패 기억)를 분리함.

## run344F s07 Validation Design(344F s07 검증 설계)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344F_s07_forward_cost_stability_validation_design.md`
- validation_plan(검증 계획): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344F/s07_validation_surface_plan.csv`
- next_queue(다음 대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344F/run344G_queue.csv`
- effect(효과): run344G materialization(물질화)을 열고 운영 주장은 닫음.

## run344G s07 Validation Package(344G s07 검증 패키지)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344G_s07_forward_cost_stability_validation_package.md`
- attempt_package(시도 패키지): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344G/runtime_probe_attempt_package.csv`
- next_queue(다음 대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344G/run344H_queue.csv`
- effect(효과): MT5 실행으로 바로 이어질 수 있게 파일을 고정.

## run344G s07 Validation Package(344G s07 검증 패키지)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344G_s07_forward_cost_stability_validation_package.md`
- attempt_package(시도 패키지): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344G/runtime_probe_attempt_package.csv`
- next_queue(다음 대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344G/run344H_queue.csv`
- effect(효과): MT5 실행으로 바로 이어질 수 있게 파일을 고정.

## run344H s07 Validation MT5 Probe(344H s07 검증 MT5 탐침)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344H_s07_forward_cost_stability_validation_mt5_probe.md`
- summary(요약): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344H/s07_forward_cost_stability_mt5_probe_summary.csv`
- diff(차이): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344H/proxy_mt5_runtime_difference.csv`
- effect(효과): MT5 runtime evidence(런타임 근거)를 생성했다.

## run344I s07 Validation Review(344I s07 검증 검토)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344I_s07_forward_cost_stability_validation_review.md`
- cost_scorecard(비용 점수판): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344I/cost_stress_scorecard.csv`
- comparator_review(대조 검토): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344I/comparator_review_scorecard.csv`
- effect(효과): s07의 긍정 단서와 실패 기억을 분리했다.

## run344I s07 Validation Review(344I s07 검증 검토)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344I_s07_forward_cost_stability_validation_review.md`
- cost_scorecard(비용 점수판): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344I/cost_stress_scorecard.csv`
- comparator_review(대조 검토): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344I/comparator_review_scorecard.csv`
- effect(효과): s07의 긍정 단서와 실패 기억을 분리했다.

## run344J Deal-Level Replay Design(344J 거래별 재생 설계)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344J_s07_deal_level_cost_session_forward_replay_design.md`
- feasibility(가능성): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344J/deal_extraction_feasibility.csv`
- queue(대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344J/run344K_queue.csv`
- effect(효과): signal-only stability(신호 전용 안정성)를 trade-level PnL(거래별 손익) 검증으로 넘겼다.

## run344K Deal-Level Materialization(344K 거래별 물질화)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344K_s07_deal_level_cost_session_forward_replay_materialization.md`
- trades(거래): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344K/trade_level_records.csv`
- session_pnl(세션 손익): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344K/session_pnl_scorecard.csv`
- cost_replay(비용 재생): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344K/cost_replay_scorecard.csv`
- effect(효과): 거래별 손익 판정을 위한 산출물을 만들었다.

## run344L s07 Deal-Level Review(344L s07 거래별 검토)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344L_s07_deal_level_cost_session_forward_replay_review.md`
- review_scorecard(검토 점수판): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344L/review_scorecard.csv`
- concentration_review(집중 검토): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344L/segment_concentration_review.csv`
- cost_review(비용 검토): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344L/cost_survival_review.csv`
- effect(효과): s07 긍정 단서와 집중 위험을 분리했다.

## run344L s07 Deal-Level Review(344L s07 거래별 검토)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344L_s07_deal_level_cost_session_forward_replay_review.md`
- review_scorecard(검토 점수판): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344L/review_scorecard.csv`
- concentration_review(집중 검토): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344L/segment_concentration_review.csv`
- cost_review(비용 검토): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344L/cost_survival_review.csv`
- effect(효과): s07 긍정 단서와 집중 위험을 분리했다.

## run344M Cash-Open Decomposition Design(344M 현금장 초반 분해 설계)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344M_cash_open_long_quality_short_carry_decomposition_design.md`
- variant_grid(변형 격자): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344M/variant_grid_contract.csv`
- cost_floor(비용 하한): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344M/heavy_cost_recovery_floor_contract.csv`
- effect(효과): run344N materialization(물질화)을 열었다.

## run344N Cash-Open Runtime Package(344N 현금장 런타임 패키지)

- report(보고서): `stages/344_directional_long_quality__supply_surface_probe/03_reviews/run344N_cash_open_long_quality_short_carry_decomposition_package.md`
- attempt_package(시도 패키지): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344N/runtime_probe_attempt_package.csv`
- packageability(포장 가능성): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344N/packageability_matrix.csv`
- effect(효과): 단일 사이드 필터 한계를 기록하고 실행 가능한 변형을 포장했다.
