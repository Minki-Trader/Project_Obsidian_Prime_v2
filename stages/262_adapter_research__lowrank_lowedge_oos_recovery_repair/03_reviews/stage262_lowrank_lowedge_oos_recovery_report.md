# Stage262 Lowrank Lowedge OOS Recovery Repair(262단계 낮은 순위 낮은 가장자리 표본외 회복 수리)

- stage(단계): `262_adapter_research__lowrank_lowedge_oos_recovery_repair`
- run(실행): `run262A_stage262_lowrank_lowedge_oos_recovery_repair_v1`
- source_stage(원천 단계): `261_adapter_research__stage260_tight_plus_highedge_pf_oos_followup_review`
- source_run(원천 실행): `run261A_stage261_stage260_tight_plus_highedge_pf_oos_followup_review_v1`
- source_stage260_evidence_commit(원천 260단계 근거 커밋): `eb99d51a9d38093e9ed2c97932f93b10127edb49`
- source_stage260_hash_record_commit(원천 260단계 해시 기록 커밋): `8cdeb8526ed3fbb1aae24a25a990aab846916332`
- source_stage261_evidence_commit(원천 261단계 근거 커밋): `828bab50d0958374cca8d27670491813c52980b0`
- source_stage261_hash_record_commit(원천 261단계 해시 기록 커밋): `0fc87d22f0ae38594c601a146a8670e5e5b2ade9`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage263_bounded_followup_due_to_stage262_oos_validation_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can the Stage260 `s260_lowrank_lowedge_filter` validation(검증) gain be preserved while recovering OOS(표본외) net/PF(순손익/수익 팩터) by splitting only the low-rank low-edge short block(낮은 순위 낮은 가장자리 숏 차단)?

## Design(설계)

- fixed(고정): score table(점수 표면), thresholds(문턱값) `0.54/0.52`, lifecycle(생명주기) hold 3/cooldown 8, ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험 비율) cap(상한) `0.0305`.
- changed(변경): only low-rank low-edge short supply(낮은 순위 낮은 가장자리 숏 공급) is split into outer half(바깥 절반) and inner half(안쪽 절반).
- not done(하지 않음): ONNX hardening(ONNX 경화), deployment(배포), live readiness(실거래 준비), operating promotion(운영 승격).

## KPI Matrix(KPI 핵심 성과 지표 행렬)

| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | DD%(손실률) | mid PF(중간 수익 팩터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | pass(통과) |
|---|---:|---:|---:|---:|---:|---:|---|
| s262_highedge_reference | 1.56 | 1204.24 | 9.0307 | 1.5342048177397174 | 1.7 | 828.96 | False |
| s262_lowrank_control | 1.61 | 1291.28 | 9.0536 | 1.6003645706247935 | 1.7 | 775.97 | True |
| s262_lowrank_outer_half_filter | 1.54 | 1163.47 | 9.0779 | 1.5342048177397174 | 1.74 | 857.64 | False |
| s262_lowrank_inner_half_filter | 1.62 | 1336.78 | 9.0447 | 1.6003645706247935 | 1.66 | 745.71 | True |

## Easy Read(쉬운 해석)

- reference(기준): `s262_lowrank_control` validation PF(검증 수익 팩터) `1.61`, validation net(검증 순손익) `1291.28`, OOS net(표본외 순손익) `775.97`.
- best_read(최선 해석): `s262_lowrank_inner_half_filter` validation PF(검증 수익 팩터) `1.62`, validation net(검증 순손익) `1336.78`, OOS net(표본외 순손익) `745.71`.
- final claim(최종 주장)은 금지다. Stage263(263단계) review-only(검토 전용)에서 이 절충을 다시 판정해야 한다.

## Judgment(판정)

- result_subject(판정 대상): `run262A_stage262_lowrank_lowedge_oos_recovery_repair_v1`
- evidence_available(사용 근거): MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) reports(보고서), KPI matrix(KPI 행렬), monthly/segment KPI(월별/구간별 핵심 성과 지표), probability telemetry(확률 원격측정), risk/ATR telemetry(위험/ATR 원격측정).
- evidence_missing(부족 근거): Stage263(263단계) follow-up review(후속 검토), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- claim_boundary(주장 경계): research/development only(연구개발 전용).
- next_condition(다음 조건): `263_adapter_research__stage262_lowrank_lowedge_oos_followup_review`에서 OOS 회복과 검증 보존이 같이 성립했는지 판정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
