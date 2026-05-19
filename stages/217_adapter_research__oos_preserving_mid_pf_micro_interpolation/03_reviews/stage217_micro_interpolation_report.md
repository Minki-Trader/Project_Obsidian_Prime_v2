# Stage217 Micro Interpolation Report(217단계 미세 보간 보고서)

- stage(단계): `217_adapter_research__oos_preserving_mid_pf_micro_interpolation`
- run(실행): `run217A_stage217_oos_preserving_mid_pf_micro_interpolation_v1`
- source_stage(원천 단계): `216_adapter_research__stage215_mid_pf_recovery_followup_review`
- source_run(원천 실행): `run216A_stage216_stage215_mid_pf_recovery_followup_review_v1`
- source_stage216_evidence_commit(원천 216단계 근거 커밋): `abb5fd5bef288e496cee6cf590715b83f33a22ae`
- source_stage216_hash_record_commit(원천 216단계 해시 기록 커밋): `4c1ec028a8c504bb8f1d0a823470c2bf20289b73`
- source_oos_preserver(원천 표본외 보존): `s215_r031375_s2025_t460`
- source_mid_recovery(원천 중반 회복): `s215_r031375_s2050_t465`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage218_bounded_followup_due_to_micro_interpolation_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): Stage215(215단계)의 OOS-preserving bracket(표본외 보존 브래킷)과 mid-PF recovery bracket(중반 수익요인 회복 브래킷) 사이의 좁은 SL/TP(손절/익절) 보간이 두 KPI(핵심 성과 지표)를 같이 살릴 수 있다.
- comparison_baseline(비교 기준): Stage210 anchor(210단계 기준 후보), Stage215 OOS preserver(215단계 표본외 보존) `s215_r031375_s2025_t460`, Stage215 mid recovery(215단계 중반 회복) `s215_r031375_s2050_t465`다.
- control_variables(고정 변수): thresholds(문턱값), long-session gate(롱 세션 제한), cooldown(대기), hold(보유), model/data(모델/데이터)를 고정했다.
- changed_variables(변경 변수): ATR SL/TP(ATR 손절/익절) midpoint(중간값)와 risk cap(위험 상한) 한 축만 좁게 보간했다.
- stop_condition(정지 조건): 네 개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage217(217단계)를 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | SL/TP(손절/익절) | risk cap(위험 상한) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | val net(검증 순손익) | val DD%(검증 낙폭) | early PF(초반 수익요인) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| s217_r031375_s20325_t4615 | 2.0325/4.615 | 0.031375 | 1.541194 | 719.48 | 952.16 | 12.6953 | 1.563704 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s217_r031375_s20375_t4625 | 2.0375/4.625 | 0.031375 | 1.544016 | 709.04 | 948.72 | 12.6751 | 1.566431 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s217_r031375_s20425_t4635 | 2.0425/4.635 | 0.031375 | 1.541391 | 707.18 | 946.28 | 12.7284 | 1.564497 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s217_r03125_s20375_t4625 | 2.0375/4.625 | 0.031250 | 1.537880 | 708.56 | 941.20 | 12.6680 | 1.567379 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |

## Attribution(성과 원인 분해)

- observed_change(관측 변화): best adapter(최선 어댑터) `s217_r031375_s20325_t4615`는 validation mid PF(검증 중반 수익요인) `1.541194`와 OOS net(표본외 순손익) `719.48`를 기록했다.
- comparison_baseline(비교 기준): Stage215 OOS preserver(215단계 표본외 보존)는 OOS net(표본외 순손익) `726.04`였고, Stage215 mid recovery(215단계 중반 회복)는 validation mid PF(검증 중반 수익요인) `1.690898468`였다.
- likely_drivers(가능 원인): SL/TP(손절/익절) 폭이 mid payoff(중반 보상)와 OOS month stability(표본외 월별 안정성)를 동시에 흔든다.
- alternative_explanations(대체 설명): early PF(초반 수익요인)가 계속 약하면, 브래킷 보간만으로는 34D(34D) 수준 안정성을 만들기 어렵다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage218_review(218단계 검토 전 중간)`이다.

## Judgment(판정)

Stage217(217단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
