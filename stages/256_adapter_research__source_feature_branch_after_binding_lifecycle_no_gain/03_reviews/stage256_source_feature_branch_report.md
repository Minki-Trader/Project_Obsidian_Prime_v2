# Stage256 Source/Feature Branch(256단계 소스/피처 분기)

- stage(단계): `256_adapter_research__source_feature_branch_after_binding_lifecycle_no_gain`
- run(실행): `run256A_stage256_source_feature_branch_after_binding_lifecycle_no_gain_v1`
- source_stage(원천 단계): `255_adapter_research__stage254_nonbinding_source_followup_review`
- source_run(원천 실행): `run255A_stage255_stage254_nonbinding_source_followup_review_v1`
- source_stage254_evidence_commit(원천 254단계 근거 커밋): `2a505dea136acb476ff4ae1ca85c4a582f9d0171`
- source_stage254_hash_record_commit(원천 254단계 해시 기록 커밋): `652000348554f7f883bcf06ca3ffe7e513916423`
- source_stage255_evidence_commit(원천 255단계 근거 커밋): `6d2842f265239ed3f0bf55176df10ad82e80515f`
- source_stage255_hash_record_commit(원천 255단계 해시 기록 커밋): `e0a3f4658b3fc41350ccec17f9c629520d086e0a`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage257_bounded_followup_due_to_source_feature_branch_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can a bounded source/feature branch(경계 소스/피처 분기) improve validation/OOS net, PF, DD, and mid-window behavior(검증/표본외 순수익, 수익요인, 낙폭, 중간 구간 행동) without repeating threshold/binding/lifecycle over-tuning(임계값/결합/생명주기 과조정)?

## Design(설계)

- fixed(고정): score table(점수표), thresholds(임계값) `0.54/0.52`, lifecycle(생명주기) hold 3/cooldown 8(3봉 보유/8봉 대기), ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험비율) cap(상한) `0.0305`.
- changed(변경): source gate(소스 차단문) only(전용). Variants(분기)는 long session relax(롱 세션 완화), short margin relax(숏 마진 완화), short session relax(숏 세션 완화), short tight margin(숏 좁은 마진)이다.
- not done(하지 않음): ONNX hardening(ONNX 경화), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격).

## KPI Matrix(KPI 핵심 성과 지표 행렬)

| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순수익) | DD%(낙폭률) | mid PF(중간 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순수익) | pass(통과) |
|---|---:|---:|---:|---:|---:|---:|---|
| s256_stage254_control | 1.59 | 972.15 | 12.9281 | 1.5166508780878818 | 1.78 | 776.02 | False |
| s256_long_session_relax | 1.58 | 1043.74 | 11.8575 | 1.4815196583713737 | 1.65 | 670.98 | False |
| s256_short_margin_relax | 1.25 | 594.2 | 11.8876 | 1.1436693088896401 | 1.52 | 956.46 | False |
| s256_short_session_relax | 1.51 | 993.12 | 14.352 | 1.5427022955758587 | 1.56 | 581.18 | False |
| s256_short_tight_margin | 1.48 | 1043.99 | 9.0087 | 1.510763553290572 | 1.69 | 950.22 | False |

## Easy Read(쉬운 해석)

- reference(기준): `s256_stage254_control` validation net(검증 순수익) `972.15`, DD(낙폭) `12.9281`, mid PF(중간 수익요인) `1.5166508780878818`, OOS net(표본외 순수익) `776.02`.
- best_read(최선 해석): `s256_short_tight_margin` validation net(검증 순수익) `1043.99`, DD(낙폭) `9.0087`, mid PF(중간 수익요인) `1.510763553290572`, OOS net(표본외 순수익) `950.22`.
- ATR/risk(ATR/위험)는 유지됐지만 final adapter(최종 어댑터) 주장은 금지다.

## Judgment(판정)

- result_subject(판정 대상): `run256A_stage256_source_feature_branch_after_binding_lifecycle_no_gain_v1`
- evidence_available(사용 근거): MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) reports(보고서), KPI matrix(KPI 행렬), probability telemetry(확률 원격측정), risk/ATR telemetry(위험/ATR 원격측정).
- evidence_missing(부족 근거): Stage257(257단계) follow-up review(후속 검토), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- claim_boundary(주장 경계): research/development only(연구개발 전용).
- next_condition(다음 조건): `257_adapter_research__stage256_source_feature_followup_review`에서 Stage256(256단계) source/feature tradeoff(소스/피처 절충)를 판정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
