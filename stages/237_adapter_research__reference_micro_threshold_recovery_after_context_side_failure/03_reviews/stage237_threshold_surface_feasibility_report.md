# Stage237 Threshold Surface Feasibility Report(237단계 문턱값 표면 가능성 보고서)

- stage(단계): `237_adapter_research__reference_micro_threshold_recovery_after_context_side_failure`
- run(실행): `run237A_stage237_reference_micro_threshold_recovery_after_context_side_failure_v1`
- source_stage(원천 단계): `236_adapter_research__stage235_side_specific_followup_review`
- source_run(원천 실행): `run236A_stage236_stage235_side_specific_followup_review_v1`
- source_stage236_evidence_commit(원천 236단계 근거 커밋): `69bc3e305b7c9a546c3243d7ebfe89480e6913f7`
- source_stage236_hash_record_commit(원천 236단계 해시 기록 커밋): `7fd2b31c4df6567296a3eb1542e9e8f648526994`
- reference_adapter(기준 어댑터): `s235_session_ref_h3_cd8`
- decision(판정): `open_stage238_bounded_score_shape_repair_after_threshold_surface_discrete_candidate_not_final`
- external_verification_status(외부 검증 상태): `review_only_source_stage235_mt5_telemetry_completed`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 설명)

Stage237(237단계)는 새 MT5(MetaTrader 5, 메타트레이더5) 반복을 먼저 돌리지 않았다. 이유는 Stage235(235단계) telemetry(기록)가 이미 threshold surface(문턱값 표면)가 거의 이진형임을 보여 주기 때문이다.

검증/표본외(validation/OOS, 검증/표본외) 모두 directional pass probability(방향 통과 확률)가 `0.5761168848`로 고정되어 있고, near-threshold rows(문턱값 근접 행)는 `0`이다. Effect(효과): `0.52/0.54` 주변의 작은 threshold(문턱값) 조정은 아무 것도 바꾸지 않거나, `0.576` 위로 올리면 신호를 한꺼번에 죽일 가능성이 크다.

## Threshold Audit(문턱값 감사)

| split(분할) | pass rows(통과 행) | near threshold(근접 행) | pass prob(통과 확률) | status(상태) |
|---|---:|---:|---:|---|
| validation_is | 468 | 0 | 0.5761168848 | discrete_no_rank_surface |
| oos | 348 | 0 | 0.5761168848 | discrete_no_rank_surface |

## Score Shape(점수 형태)

- feature0_score_rows(특징0 점수 행): `4`
- implied_winner_prob(암시 승자 확률): `0.5761168848` to `0.5761168848`
- feature1_scores_all_zero(특징1 점수 전부 0): `True`
- score_shape_status(점수 형태 상태): `flat_binary_score_shape_no_micro_rank`

Effect(효과): 다음 수리는 threshold(문턱값)이 아니라 score shape(점수 형태) 또는 model output diversity(모델 출력 다양성)를 직접 다뤄야 한다.

## Route(다음 경로)

- open_stage238_bounded_score_shape_repair_after_threshold_surface_discrete_candidate_not_final: Open Stage238(238단계) for score shape repair(점수 형태 수리) instead of repeating threshold(문턱값) variants. Effect(효과): 현재 확률이 0.5761168848 근처 이산값이라 threshold(문턱값)만으로는 34D(34D 기준) 부족분을 세밀하게 회복할 수 없다는 실패 축을 보존한다.
- do_not_run_threshold_noop_variants: Do not run small long/short threshold(롱/숏 문턱값) sweeps around 0.52/0.54. Effect(효과): Stage225(225단계)와 Stage235(235단계) telemetry(기록)가 이미 no-rank surface(순위 없는 표면)를 보여 주므로 MT5(MetaTrader 5, 메타트레이더5) 시간을 아낀다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
