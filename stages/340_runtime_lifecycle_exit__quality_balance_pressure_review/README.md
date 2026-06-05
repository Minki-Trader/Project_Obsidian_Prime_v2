# Stage340 Quality Balance Pressure Review(340단계 품질-균형 압박 검토)

## Canonical Stage ID(정식 단계 ID)

`340_runtime_lifecycle_exit__quality_balance_pressure_review`

## Stage Question(단계 질문)

Can the run339G(339G 실행) quality-balance blend(품질-균형 혼합) MT5 runtime probe(MT5 런타임 탐침) be reviewed and pressure-tested without keeping Stage339(339단계) overloaded?
(run339G(339G 실행)의 품질-균형 혼합 MT5 런타임 탐침을 Stage339(339단계)을 더 무겁게 하지 않고 검토하고 압박 시험할 수 있는가?)

## Source Handoff(원천 인계)

- source_stage(원천 단계): `339_runtime_lifecycle_exit__side_balance_probe_review`
- source_completed_run(완료 원천 실행): `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1`
- source_package_run(원천 패키지 실행): `run339F_materialize_quality_balance_blend_mt5_probe_package_without_db_v1`
- branch_run(분기 실행): `run340A_branch_stage339_to_quality_balance_pressure_review_without_db_v1`
- next_run(다음 실행): `run340B_review_quality_balance_blend_mt5_probe_without_db_v1`

## Raw Preview Boundary(원시 미리보기 경계)

- best_attempt_review_required(검토 필요 최고 시도): `f01_s55_l51_m01_h12`
- net_profit_review_required(검토 필요 순수익): `122.9`
- profit_factor_review_required(검토 필요 수익 팩터): `1.89`
- recovery_factor_review_required(검토 필요 회복 계수): `1.38`
- trade_count_review_required(검토 필요 거래수): `33`

Effect(효과): 숫자는 보존하지만, run340B(340B 실행) 검토 전에는 selection(선정), promotion_candidate(승격 후보), runtime authority(런타임 권위)로 쓰지 않는다.

## Scope(범위)

Stage340(340단계)는 review(검토)와 pressure package design(압박 패키지 설계)에 집중한다.
Effect(효과): Stage339(339단계)의 누적 산출물은 보존하고, 다음 작업 묶음(work packet, 작업 묶음)은 작게 유지한다.

## Forbidden Claims(금지 주장)

No selected model(선정 모델 없음), no baseline(기준선 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## run340B Quality Balance Review(340B 품질-균형 검토)

- run_id(실행 ID): `run340B_review_quality_balance_blend_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340B/quality_balance_review_scorecard.csv`
- queue(대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340B/run340C_queue.csv`
- effect(효과): Stage340(340단계) 탐색을 local floor pressure test(로컬 하한 압박 시험)로 이어간다.

## run340C F01 Local Floor Pressure Package(340C F01 로컬 하한 압박 패키지)

- run_id(실행 ID): `run340C_materialize_f01_local_floor_pressure_mt5_probe_package_without_db_v1`
- queue(대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340C/run340D_queue.csv`
- effect(효과): Stage340(340단계) 탐색을 MT5(메타트레이더5) 실행으로 넘긴다.

## run340D F01 Local Floor Pressure MT5 Probe(340D F01 로컬 하한 압박 MT5 탐침)

- run_id(실행 ID): `run340D_execute_f01_local_floor_pressure_mt5_probe_without_db_v1`
- summary(요약): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340D/f01_local_floor_pressure_mt5_probe_summary.csv`
- diff(차이): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340D/proxy_mt5_runtime_difference.csv`
- effect(효과): run340E(340E 실행)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.

## run340E F01 Pressure Probe Review(340E F01 압박 탐침 검토)

- run_id(실행 ID): `run340E_review_f01_local_floor_pressure_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/f01_pressure_review_scorecard.csv`
- control_audit(대조 감사): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/control_semantics_audit.csv`
- queue(대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/run340F_queue.csv`
- effect(효과): Stage340(340단계)을 corrected close_on_flat_false branch(수정된 평탄 청산 꺼짐 분기)로 이어간다.

## run340E F01 Pressure Probe Review(340E F01 압박 탐침 검토)

- run_id(실행 ID): `run340E_review_f01_local_floor_pressure_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/f01_pressure_review_scorecard.csv`
- control_audit(대조 감사): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/control_semantics_audit.csv`
- queue(대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/run340F_queue.csv`
- effect(효과): Stage340(340단계)을 corrected close_on_flat_false branch(수정된 평탄 청산 꺼짐 분기)로 이어간다.

## run340F F01 Close-On-Flat False Pressure Package(340F F01 평탄 청산 꺼짐 압박 패키지)

- run_id(실행 ID): `run340F_materialize_f01_close_on_flat_false_pressure_mt5_probe_package_without_db_v1`
- queue(대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340F/run340G_queue.csv`
- effect(효과): Stage340(340단계) 탐색을 corrected MT5 run(수정 MT5 실행)으로 이어간다.

## run340G F01 Close-On-Flat False MT5 Probe(340G F01 평탄 청산 꺼짐 MT5 탐침)

- run_id(실행 ID): `run340G_execute_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1`
- summary(요약): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340G/f01_close_on_flat_false_pressure_mt5_probe_summary.csv`
- diff(차이): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340G/proxy_mt5_runtime_difference.csv`
- effect(효과): run340H(340H 실행)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.

## run340H F01 Close-On-Flat False Pressure Review(340H F01 평탄 청산 꺼짐 압박 검토)

- run_id(실행 ID): `run340H_review_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/f01_close_on_flat_false_pressure_review_scorecard.csv`
- seed_queue(씨앗 대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/run341A_seed_queue.csv`
- effect(효과): Stage340(340단계) 압박 질문을 닫고 Stage341(341단계) 안정성 검증으로 넘긴다.

## run341A Stage Branch(341A 단계 분기)

- branch_run(분기 실행): `run341A_branch_stage340_to_f01_stability_cost_regime_validation_without_db_v1`
- new_stage(새 단계): `341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue`
- next_run(다음 실행): `run341B_design_f01_stability_cost_regime_validation_without_db_v1`
- effect(효과): q01/q09(큐01/큐09) 검증을 Stage 341(341단계)에서 이어간다.
