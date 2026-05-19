# Stage254 Non-binding Source/Lifecycle Repair(254단계 비결합 원천/생명주기 수리)

- stage(단계): `254_adapter_research__nonbinding_source_repair_after_binding_axis_no_gain`
- run(실행): `run254A_stage254_nonbinding_source_repair_after_binding_axis_no_gain_v1`
- source_stage(원천 단계): `253_adapter_research__stage252_asymmetric_binding_followup_review`
- source_run(원천 실행): `run253A_stage253_stage252_asymmetric_binding_followup_review_v1`
- source_stage253_evidence_commit(원천 253단계 근거 커밋): `e7f7a542e425fb4bdaf340cb669cc5b4dbb75933`
- source_stage253_hash_record_commit(원천 253단계 해시 기록 커밋): `ca9af85eaa28295532018b7b98950f829ca67645`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage255_bounded_followup_due_to_nonbinding_lifecycle_no_gain_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can non-binding lifecycle repair(비결합 생명주기 수리) improve validation/OOS net, PF, DD, and mid-window behavior(검증/표본외 순수익, 수익요인, 낙폭, 중간 구간 행동) without using threshold/binding overprune(임계값/결합 과축소)?

## Design(설계)

- fixed(고정): score/gate surface(점수/게이트 표면), thresholds(임계값) `0.54/0.52`, ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험비율) cap(상한) `0.0305`.
- changed(변경): max_hold_bars(최대 보유 봉), close_on_flat_signal(무포지션 신호 청산), same_direction_reentry_cooldown_bars(동일 방향 재진입 대기).
- not done(하지 않음): ONNX hardening(ONNX 경화), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격).

## KPI Matrix(KPI 핵심 성과 지표 행렬)

| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순수익) | DD%(낙폭률) | mid PF(중간 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순수익) | pass(통과) |
|---|---:|---:|---:|---:|---:|---:|---|
| s254_stage252_control | 1.59 | 972.15 | 12.9281 | 1.5166508780878818 | 1.78 | 776.02 | False |
| s254_hold4 | 1.47 | 776.25 | 12.9109 | 1.2649543476405836 | 1.71 | 691.52 | False |
| s254_hold5 | 1.49 | 937.95 | 14.6927 | 1.2626682379209824 | 1.64 | 695.15 | False |
| s254_hold4_flatclose | 1.08 | 41.68 | 14.4719 | 1.1230524201925076 | 1.51 | 172.47 | False |
| s254_hold4_reentry12 | 1.46 | 687.99 | 12.4614 | 1.2039723693816806 | 1.65 | 598.55 | False |

## Easy Read(쉬운 해석)

- reference(기준): `s254_stage252_control` validation net(검증 순수익) `972.15`, DD(낙폭) `12.9281`, mid PF(중간 수익요인) `1.5166508780878818`, OOS net(표본외 순수익) `776.02`.
- best_read(최선 해석): `s254_stage252_control` validation net(검증 순수익) `972.15`, DD(낙폭) `12.9281`, mid PF(중간 수익요인) `1.5166508780878818`, OOS net(표본외 순수익) `776.02`.
- ATR/risk(ATR/위험)는 유지됐지만 final adapter(최종 어댑터) 주장은 금지다.

## Judgment(판정)

- result_subject(판정 대상): `run254A_stage254_nonbinding_source_repair_after_binding_axis_no_gain_v1`
- evidence_available(사용 근거): MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) reports(보고서), KPI matrix(KPI 행렬), probability telemetry(확률 원격측정), risk/ATR telemetry(위험/ATR 원격측정).
- evidence_missing(부족 근거): Stage255(255단계) follow-up review(후속 검토), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- claim_boundary(주장 경계): research/development only(연구개발 전용).
- next_condition(다음 조건): `255_adapter_research__stage254_nonbinding_source_followup_review`에서 Stage254(254단계) tradeoff(절충)를 판정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
