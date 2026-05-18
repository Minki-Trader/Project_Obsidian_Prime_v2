# Stage158 Validation PF Margin Repair Report(158단계 검증 수익요인 여유 수리 보고)

- stage(단계): `158_adapter_research__stage156_validation_pf_margin_repair`
- run(실행): `run158A_stage158_stage156_validation_pf_margin_repair_v1`
- source_stage157(원천 157단계): `157_adapter_research__stage156_dd_compression_followup_review`
- source_stage157_closeout_commit(원천 157단계 종료 커밋): `77feffe561844259589615160a2ddc35af0f83c8`
- source_stage157_hash_record_commit(원천 157단계 해시 기록 커밋): `bdb14b2b482a03b90c8ac73905fa8406334cb7ba`
- primary_seed(주 씨앗): `s156_low_edge_risk0300_h3_cd5_sht54_lng52`
- backup_seed(예비 씨앗): `s156_low_edge_risk0325_h3_cd5_sht54_lng52`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_stage159_stage158_followup_review_due_to_validation_pf_or_oos_damage_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can the Stage156(156단계) DD compression(낙폭 압축) candidate lift validation PF(검증 수익요인) above 34D target(34D 목표) while preserving OOS DD/PF/net/mid PF(표본외 낙폭/수익요인/순손익/중반 수익요인)?

Effect(효과): DD(낙폭)를 다시 키우지 않고 validation(검증) 품질만 보강한다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS mid PF(표본외 중반 수익요인) | read(판독) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s158_valpf_lng53_risk0300_h3_cd5_sht54_lng53 | 1.550000 | 1037.79 | 10.23 | 1.850000 | 1032.34 | 11.92 | 1.659175838 | needs_followup_or_repair |
| s158_valpf_sht55_risk0300_h3_cd5_sht55_lng52 | 1.550000 | 1037.79 | 10.23 | 1.850000 | 1032.34 | 11.92 | 1.659175838 | needs_followup_or_repair |
| s158_valpf_sht55_lng53_risk0300_h3_cd5_sht55_lng53 | 1.550000 | 1037.79 | 10.23 | 1.850000 | 1032.34 | 11.92 | 1.659175838 | needs_followup_or_repair |
| s158_valpf_lng53_risk0325_h3_cd5_sht54_lng53 | 1.540000 | 1179.05 | 11.05 | 1.840000 | 1164.82 | 12.84 | 1.661090810 | needs_followup_or_repair |

## Judgment(판정)

- best_adapter(최선 어댑터): `s158_valpf_lng53_risk0325_h3_cd5_sht54_lng53`
- best_validation_pf(최선 검증 수익요인): `1.540000`
- best_oos_pf(최선 표본외 수익요인): `1.840000`
- best_oos_net(최선 표본외 순손익): `1164.82`
- best_oos_dd(최선 표본외 낙폭): `12.84`
- best_oos_mid_pf(최선 표본외 중반 수익요인): `1.661090810`
- legacy_34d_pf_target(레거시 34D 수익요인 목표): `1.583157`

Stage158(158단계)는 research/development only(연구개발 전용)다. Effect(효과): 수리 후보가 좋아 보여도 final package(최종 패키지), deployment(배포), live readiness(실거래 준비)를 주장하지 않는다.
