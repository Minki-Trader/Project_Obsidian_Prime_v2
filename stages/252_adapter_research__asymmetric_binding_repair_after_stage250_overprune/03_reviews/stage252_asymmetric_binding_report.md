# Stage252 Asymmetric Binding Repair(252단계 비대칭 결합 수리)

- stage(단계): `252_adapter_research__asymmetric_binding_repair_after_stage250_overprune`
- run(실행): `run252A_stage252_asymmetric_binding_repair_after_stage250_overprune_v1`
- source_stage(원천 단계): `251_adapter_research__stage250_decision_binding_followup_review`
- source_run(원천 실행): `run251A_stage251_stage250_decision_binding_followup_review_v1`
- source_stage250_evidence_commit(원천 250단계 근거 커밋): `70625d3b9651397a9c24ed4399483691f221780c`
- source_stage251_hash_record_commit(원천 251단계 해시 기록 커밋): `5cdb2cd2f0445e82e7311b30fd65df46fb31607f`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage253_bounded_followup_due_to_asymmetric_binding_no_gain_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can asymmetric binding(비대칭 결합) preserve Stage250 control trade supply(250단계 기준 거래 공급) while improving validation/OOS net, PF, DD, and mid-window behavior(검증/표본외 순손익, 수익요인, 낙폭, 중간 구간 행동)?

## Easy Read(쉬운 판독)

- Stage252(252단계)는 Stage250(250단계)의 broad flat tilt(넓은 플랫 기울임)를 반복하지 않았다.
- changed(변경): short-only/long-only(숏 전용/롱 전용) low-rank score/gate(낮은 순위 점수/게이트)를 좁게 시험했다.
- reference(기준): `s252_binding_control` validation net(검증 순손익) `972.15`, DD(낙폭) `12.9281`, mid PF(중간 수익요인) `1.5166508780878818`.
- best_read(최선 판독): `s252_binding_control` validation net(검증 순손익) `972.15`, DD(낙폭) `12.9281`, mid PF(중간 수익요인) `1.5166508780878818`, OOS net(표본외 순손익) `776.02`.
- ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율)는 유지됐다. 하지만 final adapter(최종 어댑터) 주장은 금지다.

## KPI Matrix(KPI 핵심 성과 지표 행렬)

| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | DD%(낙폭률) | mid PF(중간 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | pass(통과) |
|---|---:|---:|---:|---:|---:|---:|---|
| s252_binding_control | 1.59 | 972.15 | 12.9281 | 1.5166508780878818 | 1.78 | 776.02 | False |
| s252_short_low_score006 | 1.58 | 830.35 | 9.3294 | 1.485525742389342 | 1.81 | 710.44 | False |
| s252_long_low_score006 | 1.57 | 905.08 | 12.3387 | 1.5456462731160536 | 1.76 | 726.7 | False |
| s252_short_low_gate | 1.53 | 336.96 | 12.9535 | 1.513601221723776 | 1.87 | 386.49 | False |
| s252_long_low_gate | 1.52 | 611.36 | 8.8768 | 1.8760338034946316 | 1.7 | 488.04 | False |

## Judgment(판정)

- result_subject(판정 대상): `run252A_stage252_asymmetric_binding_repair_after_stage250_overprune_v1`
- evidence_available(사용 근거): MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) reports(보고서), KPI matrix(KPI 행렬), probability binding(확률 결합), risk/ATR telemetry(위험/ATR 기록).
- evidence_missing(누락 근거): Stage253(253단계) follow-up review(후속 검토), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- claim_boundary(주장 경계): research/development only(연구개발 전용).
- next_condition(다음 조건): `253_adapter_research__stage252_asymmetric_binding_followup_review`에서 Stage252(252단계) tradeoff(상충)를 판정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
