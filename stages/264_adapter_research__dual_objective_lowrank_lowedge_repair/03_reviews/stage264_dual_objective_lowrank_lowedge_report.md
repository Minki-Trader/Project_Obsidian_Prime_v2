# Stage264 Dual Objective Lowrank Lowedge Repair(264단계 이중목표 낮은 순위 낮은 가장자리 수리)

- stage(단계): `264_adapter_research__dual_objective_lowrank_lowedge_repair`
- run(실행): `run264A_stage264_dual_objective_lowrank_lowedge_repair_v1`
- source_stage(원천 단계): `263_adapter_research__stage262_lowrank_lowedge_oos_followup_review`
- source_run(원천 실행): `run263A_stage263_stage262_lowrank_lowedge_oos_followup_review_v1`
- source_stage262_evidence_commit(원천 262단계 근거 커밋): `8ac5d3953c7665247713cec835bde857c755b2aa`
- source_stage262_hash_record_commit(원천 262단계 해시 기록 커밋): `eb25585d9e0e6ccdd3a1fdb50697b15629f75032`
- source_stage263_evidence_commit(원천 263단계 근거 커밋): `3342cf754631e42903aeee3725e42f98fcf9c260`
- source_stage263_hash_record_commit(원천 263단계 해시 기록 커밋): `bde580c4def71a550fad85c8302230a3b475b28d`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage265_bounded_followup_due_to_stage264_dual_objective_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can a non-calendar micro-band rule(달력 의존 없는 미세 구간 규칙) preserve the validation(검증) strength of the lowrank control(낮은 순위 기준) while recovering the OOS(표본외) net/PF(순손익/수익 팩터) clue from the inner low-edge allowance(안쪽 낮은 가장자리 허용)?

## Design(설계)

- fixed(고정): score table(점수 표면), thresholds(문턱값) `0.54/0.52`, lifecycle(생명주기) hold 3/cooldown 8, ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험 비율) cap(상한) `0.0305`.
- changed(변경): only low-rank low-edge inner band(낮은 순위 낮은 가장자리 안쪽 구간) allowance(허용)를 quarter(사분 구간)로 줄인다.
- not done(하지 않음): ONNX hardening(ONNX 경화), deployment(배포), live readiness(실거래 준비), operating promotion(운영 승격).

## KPI Matrix(KPI 핵심 성과 지표 행렬)

| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | DD%(손실률) | mid PF(중간 수익 팩터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | pass(통과) |
|---|---:|---:|---:|---:|---:|---:|---|
| s264_lowrank_control | 1.61 | 1291.28 | 9.0536 | 1.6003645706247935 | 1.7 | 775.97 | True |
| s264_allow_inner_low_quarter | 1.55 | 1203.25 | 9.0204 | 1.525191366112682 | 1.7 | 777.96 | False |
| s264_allow_inner_high_quarter | 1.59 | 1246.29 | 9.0209 | 1.6464050938891017 | 1.74 | 857.67 | True |
| s264_allow_inner_all_oos_anchor | 1.54 | 1163.47 | 9.0779 | 1.5342048177397174 | 1.74 | 857.64 | False |
| s264_highedge_reference | 1.56 | 1204.24 | 9.0307 | 1.5342048177397174 | 1.7 | 828.96 | False |

## Easy Read(쉬운 해석)

- reference(기준): `s264_lowrank_control` validation PF(검증 수익 팩터) `1.61`, validation net(검증 순손익) `1291.28`, OOS net(표본외 순손익) `775.97`.
- best_read(최선 해석): `s264_lowrank_control` validation PF(검증 수익 팩터) `1.61`, validation net(검증 순손익) `1291.28`, OOS net(표본외 순손익) `775.97`.
- final claim(최종 주장)은 금지다. Stage265(265단계) review-only(검토 전용)에서 절충을 다시 판정해야 한다.

## Judgment(판정)

- result_subject(판정 대상): `run264A_stage264_dual_objective_lowrank_lowedge_repair_v1`
- evidence_available(사용 근거): MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) reports(보고서), KPI matrix(KPI 행렬), monthly/segment KPI(월별/구간별 핵심 성과 지표), probability telemetry(확률 원격측정), risk/ATR telemetry(위험/ATR 원격측정).
- evidence_missing(부족 근거): Stage265(265단계) follow-up review(후속 검토), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- claim_boundary(주장 경계): research/development only(연구개발 전용).
- next_condition(다음 조건): `265_adapter_research__stage264_dual_objective_followup_review`에서 validation(검증) 보존과 OOS(표본외) 회복이 같이 성립했는지 판정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
