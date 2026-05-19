# Stage215 Validation Mid PF Recovery Report(215단계 검증 중반 수익요인 회복 보고서)

- stage(단계): `215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain`
- run(실행): `run215A_stage215_validation_mid_pf_recovery_preserve_oos_gain_v1`
- source_stage(원천 단계): `214_adapter_research__stage213_oos_monthly_concentration_followup_review`
- source_run(원천 실행): `run214A_stage214_stage213_oos_monthly_concentration_followup_review_v1`
- source_adapter(원천 어댑터): `s213_r03125_s200_t455`
- source_stage214_evidence_commit(원천 214단계 근거 커밋): `333d78643a2539da5e4170d16d6d19ab6ba67213`
- source_stage214_hash_record_commit(원천 214단계 해시 기록 커밋): `fac00f6986d632d64bcf5ae8101d5f8023c11b8e`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage216_bounded_followup_due_to_mid_pf_recovery_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): Stage213(213단계)의 OOS gain(표본외 이득)을 만든 bracket(브래킷)을 조금 느슨하게 하면 validation mid PF(검증 중반 수익요인)를 회복할 수 있다.
- comparison_baseline(비교 기준): Stage210 anchor(210단계 기준 후보) `s210_ls_r0315`와 Stage213 probe(213단계 탐침) `s213_r03125_s200_t455`다.
- control_variables(고정 변수): thresholds(문턱값), long-session gate(롱 세션 제한), cooldown(대기), hold(보유), model/data(모델/데이터)를 고정했다.
- changed_variables(변경 변수): ATR SL/TP(ATR 손절/익절)와 model risk cap(모델 위험 상한)만 보간했다.
- stop_condition(정지 조건): 네 개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage215(215단계)를 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | SL/TP(손절/익절) | risk cap(위험 상한) | mid PF(중반 수익요인) | mid delta(중반 차이) | val net(검증 순손익) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS delta(표본외 차이) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| s215_r03125_s2025_t460 | 2.025/4.60 | 0.031250 | 1.546233 | 0.004870 | 956.76 | 12.6454 | 720.61 | 5.75 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s215_r03125_s2050_t465 | 2.050/4.65 | 0.031250 | 1.688712 | 0.147349 | 1054.37 | 12.5989 | 708.26 | -6.60 | validation_early_pf_below_34d;oos_net_materially_below_stage171_primary |
| s215_r031375_s2025_t460 | 2.025/4.60 | 0.031375 | 1.531013 | -0.010350 | 956.51 | 12.7149 | 726.04 | 11.18 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s215_r031375_s2050_t465 | 2.050/4.65 | 0.031375 | 1.690898 | 0.149536 | 1059.28 | 12.6140 | 706.62 | -8.24 | validation_early_pf_below_34d;oos_net_materially_below_stage171_primary |

## Attribution(성과 원인 분해)

- observed_change(관측 변화): best adapter(최선 어댑터) `s215_r031375_s2050_t465`는 validation mid PF(검증 중반 수익요인) `1.690898`와 OOS net(표본외 순손익) `706.62`를 기록했다.
- comparison_baseline(비교 기준): Stage213 probe(213단계 탐침)는 mid PF(중반 수익요인) `1.541362846`와 OOS net(표본외 순손익) `749.91`였다.
- likely_drivers(가능 원인): SL/TP(손절/익절)를 Stage210(210단계) 쪽으로 느슨하게 돌리면 mid-segment payoff(중반 보상)가 회복될 수 있다.
- alternative_explanations(대체 설명): OOS gain(표본외 이득)이 월별 군집이나 위험 배율 때문이면 mid PF(중반 수익요인) 회복과 동시에 사라질 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage216_review(216단계 검토 전 중간)`이다.

## Judgment(판정)

Stage215(215단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
