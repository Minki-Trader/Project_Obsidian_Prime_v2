# Stage233 Side Session Context Repair Report(233단계 방향/세션/문맥 수리 보고서)

- stage(단계): `233_adapter_research__side_session_context_repair_after_lifecycle_failure`
- run(실행): `run233A_stage233_side_session_context_repair_after_lifecycle_failure_v1`
- source_stage(원천 단계): `232_adapter_research__stage231_lifecycle_followup_review`
- source_run(원천 실행): `run232A_stage232_stage231_lifecycle_followup_review_v1`
- decision(판정): `open_stage234_bounded_followup_due_to_side_session_context_tradeoff_candidate_not_final`
- external_verification_status(외부 검증 상태): `completed`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 설명)

Stage233(233단계)는 hold/cooldown(보유/대기)만 다시 만지지 않는다. Stage231(231단계)에서 OOS(표본외)를 지킨 `s231_session_ref_h3_cd8`을 기준으로 두고, long(롱) 쪽 session/context(세션/문맥) gate(게이트)를 좁게 바꿔 validation(검증) early/mid PF(초반/중반 수익요인)와 net(순손익)이 회복되는지 본다.

Effect(효과): legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)로만 쓰고, v2-native(브이투 고유) 방향/세션/문맥 축이 KPI(핵심 성과 지표)를 실제로 끌어올리는지 분리해서 본다.

## KPI Table(KPI 핵심 성과 지표 표)

| adapter(어댑터) | axis(축) | hold(보유) | cooldown(대기) | validation net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | validation DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s233_session_ref_h3_cd8 | session_ref_h3_cd8 | 3 | 8 | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | 1.740000 | 9.2072 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s233_session_p5_h3_cd8 | session_p5_h3_cd8 | 3 | 8 | 891.20 | 1.655408 | 1.393086 | 12.1890 | 671.23 | 1.710000 | 9.2451 | validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_net_materially_below_stage171_primary |
| s233_session_p10_h3_cd8 | session_p10_h3_cd8 | 3 | 8 | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | 1.740000 | 9.2072 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s233_cashopen_long_h3_cd8 | cashopen_long_h3_cd8 | 3 | 8 | 731.84 | 1.531641 | 1.678066 | 9.6957 | 602.79 | 1.850000 | 12.8696 | validation_net_below_34d;validation_early_pf_below_34d;oos_net_materially_below_stage171_primary |

## Judgment(판정)

- best_candidate(최선 후보): `s233_session_ref_h3_cd8`
- full_stage_pass(전체 통과): `False`
- reason(이유): validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), validation DD(검증 낙폭), OOS net/PF/DD(표본외 순손익/수익요인/낙폭)를 동시에 본다.
- next(다음): `234_adapter_research__stage233_side_session_context_followup_review`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
