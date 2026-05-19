# Stage258 Short Tight Margin PF Repair(258단계 숏 좁은 마진 PF 수리)

- stage(단계): `258_adapter_research__short_tight_margin_pf_repair_after_stage256_tradeoff`
- run(실행): `run258A_stage258_short_tight_margin_pf_repair_after_stage256_tradeoff_v1`
- source_stage(원천 단계): `257_adapter_research__stage256_source_feature_followup_review`
- source_run(원천 실행): `run257A_stage257_stage256_source_feature_followup_review_v1`
- source_stage256_evidence_commit(원천 256단계 근거 커밋): `c5e1c2f8bd930f1a5c9f025b1e67630897e5ab10`
- source_stage256_hash_record_commit(원천 256단계 해시 기록 커밋): `d5e503be2fbb26b773eb61b5caf16e7d602f784a`
- source_stage257_evidence_commit(원천 257단계 근거 커밋): `fc0d2d3d782caa56518f3a38f00db15b8f0f5c0f`
- source_stage257_hash_record_commit(원천 257단계 해시 기록 커밋): `6f500110d081158c6e6081994906e17ec16e479d`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage259_bounded_followup_due_to_short_tight_margin_pf_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can short-margin edge guards(숏 마진 가장자리 차단문) preserve Stage256 short_tight_margin(256단계 숏 좁은 마진) net/DD/OOS gains(순수익/낙폭/표본외 개선) while repairing PF and mid-window behavior(PF와 중간 구간 행동), without repeating threshold/binding/lifecycle over-tuning(임계값/결합/생명주기 과조정)?

## Design(설계)

- fixed(고정): score table(점수표), thresholds(임계값) `0.54/0.52`, lifecycle(생명주기) hold 3/cooldown 8(3봉 보유/8봉 대기), ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험비율) cap(상한) `0.0305`.
- changed(변경): short margin edge guard(숏 마진 가장자리 차단문) only(전용). Variants(분기)는 short_tight_control(숏 좁은 마진 대조군), tight_plus_lowedge(좁은+낮은 가장자리), tight_plus_highedge(좁은+높은 가장자리), lowedge_only(낮은 가장자리 전용), highedge_only(높은 가장자리 전용)이다.
- not done(하지 않음): ONNX hardening(ONNX 경화), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격).

## KPI Matrix(KPI 핵심 성과 지표 행렬)

| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순수익) | DD%(낙폭률) | mid PF(중간 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순수익) | pass(통과) |
|---|---:|---:|---:|---:|---:|---:|---|
| s258_short_tight_control | 1.48 | 1043.99 | 9.0087 | 1.510763553290572 | 1.69 | 950.22 | False |
| s258_tight_plus_lowedge | 1.48 | 815.42 | 9.8955 | 1.5564586910894866 | 1.76 | 892.99 | False |
| s258_tight_plus_highedge | 1.56 | 1204.24 | 9.0307 | 1.5342048177397174 | 1.7 | 828.96 | False |
| s258_lowedge_only | 1.23 | 436.04 | 13.9439 | 1.1430835593608053 | 1.55 | 889.95 | False |
| s258_highedge_only | 1.3 | 707.04 | 11.911 | 1.1123595505617978 | 1.52 | 836.62 | False |

## Easy Read(쉬운 해석)

- reference(기준): `s258_short_tight_control` validation net(검증 순수익) `1043.99`, DD(낙폭) `9.0087`, mid PF(중간 수익요인) `1.510763553290572`, OOS net(표본외 순수익) `950.22`.
- best_read(최선 해석): `s258_tight_plus_highedge` validation net(검증 순수익) `1204.24`, DD(낙폭) `9.0307`, mid PF(중간 수익요인) `1.5342048177397174`, OOS net(표본외 순수익) `828.96`.
- ATR/risk(ATR/위험)는 유지됐지만 final adapter(최종 어댑터) 주장은 금지다.

## Judgment(판정)

- result_subject(판정 대상): `run258A_stage258_short_tight_margin_pf_repair_after_stage256_tradeoff_v1`
- evidence_available(사용 근거): MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) reports(보고서), KPI matrix(KPI 행렬), probability telemetry(확률 원격측정), risk/ATR telemetry(위험/ATR 원격측정).
- evidence_missing(부족 근거): Stage259(259단계) follow-up review(후속 검토), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- claim_boundary(주장 경계): research/development only(연구개발 전용).
- next_condition(다음 조건): `259_adapter_research__stage258_short_tight_margin_pf_followup_review`에서 Stage258(258단계) PF repair tradeoff(PF 수리 절충)를 판정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
