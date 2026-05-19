# Stage238 Score Shape Repair Report(238단계 점수 형태 수리 보고서)

- stage(단계): `238_adapter_research__score_shape_repair_after_threshold_surface_discrete`
- run(실행): `run238A_stage238_score_shape_repair_after_threshold_surface_discrete_v1`
- source_stage(원천 단계): `237_adapter_research__reference_micro_threshold_recovery_after_context_side_failure`
- source_run(원천 실행): `run237A_stage237_reference_micro_threshold_recovery_after_context_side_failure_v1`
- source_stage237_evidence_commit(원천 237단계 근거 커밋): `b3dc12f65905c2063fc8cac59298fabec8a1a6ce`
- source_stage237_hash_record_commit(원천 237단계 해시 기록 커밋): `b2e16f262369baef1f4d990d90383cfa263d42de`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage239_bounded_followup_due_to_score_shape_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): Stage235(235단계) 기준형의 binary probability(이진 확률)를 margin bucket(마진 구간) 점수로 세분화하면 34D(34D 기준) 부족분을 회복할 수 있다.
- fixed variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험 비율) cap(상한) `0.031375`, hold(보유) `3`, same-direction cooldown(동방향 대기) `8`, Stage235 reference side filter(235단계 기준 방향 필터).
- changed variables(변경 변수): feature1(특징1) margin-rank score(마진 순위 점수)만 neutral(중립), low penalty 0.15(저마진 벌점 0.15), low penalty 0.25(저마진 벌점 0.25), high bonus 0.10(고마진 보너스 0.10)로 바꾼다.
- stop condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage238(238단계)은 닫는다.

Effect(효과): cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) 실패 축을 반복하지 않고 score shape(점수 형태)만 본다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s238_rank3f_neutral_ref | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | 1.740000 | 9.2072 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s238_lowpen015_rank3f | 224.17 | 1.520510 | 1.500036 | 11.3484 | 247.02 | 1.770000 | 6.4430 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s238_lowpen025_rank3f | 122.98 | 1.943496 | 1.235852 | 11.4732 | 145.62 | 1.720000 | 7.1040 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s238_highbonus010_rank3f | 967.85 | 1.562195 | 1.498473 | 13.3771 | 812.80 | 1.780000 | 9.7920 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |

## Judgment(판정)

- best_row(최선 행): `s238_highbonus010_rank3f` with validation net(검증 순손익) `967.85`, early PF(초반 수익요인) `1.562195`, mid PF(중반 수익요인) `1.498473`, OOS net(표본외 순손익) `812.80`.
- decision(판정): `open_stage239_bounded_followup_due_to_score_shape_tradeoff_candidate_not_final`.
- overall_goal_complete(전체 목표 완료): `false`.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선).
