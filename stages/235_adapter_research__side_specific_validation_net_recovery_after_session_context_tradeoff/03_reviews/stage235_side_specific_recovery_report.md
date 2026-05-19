# Stage235 Side-Specific Validation Net Recovery Report(235단계 방향별 검증 순손익 회복 보고서)

- stage(단계): `235_adapter_research__side_specific_validation_net_recovery_after_session_context_tradeoff`
- run(실행): `run235A_stage235_side_specific_validation_net_recovery_after_session_context_tradeoff_v1`
- source_stage(원천 단계): `234_adapter_research__stage233_side_session_context_followup_review`
- source_run(원천 실행): `run234A_stage234_stage233_side_session_context_followup_review_v1`
- decision(판정): `open_stage236_bounded_followup_due_to_side_specific_tradeoff_candidate_not_final`
- external_verification_status(외부 검증 상태): `completed`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 설명)

Stage235(235단계)는 Stage234(234단계)가 남긴 두 단서만 좁게 시험한다. 하나는 `s233_session_ref_h3_cd8`의 OOS(표본외) 보존 경계이고, 다른 하나는 `s233_cashopen_long_h3_cd8`의 mid PF(중반 수익요인) 단서다. 이번에는 cashopen(현금장 초반)을 45분으로 줄이고, short block(숏 차단)을 켜고 끄며 validation net(검증 순손익)과 early PF(초반 수익요인)가 회복되는지 본다.

Effect(효과): session_p5/session_p10(세션 5분/10분) 반복을 피하고, side-specific(방향별) 수리 축이 34D KPI(핵심 성과 지표)에 가까워지는지 확인한다.

## KPI Table(KPI 핵심 성과 지표 표)

| adapter(어댑터) | axis(축) | hold(보유) | cooldown(대기) | validation net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | validation DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s235_session_ref_h3_cd8 | session_ref_h3_cd8 | 3 | 8 | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | 1.740000 | 9.2072 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s235_cashopen45_h3_cd8 | cashopen45_h3_cd8 | 3 | 8 | 797.87 | 1.598742 | 1.467070 | 11.9477 | 525.69 | 1.610000 | 12.8843 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s235_session_ref_short_open_h3_cd8 | session_ref_short_open_h3_cd8 | 3 | 8 | 510.56 | 1.174219 | 1.174422 | 12.3014 | 470.51 | 1.290000 | 20.1984 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_pf_below_34d;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |
| s235_cashopen45_short_open_h3_cd8 | cashopen45_short_open_h3_cd8 | 3 | 8 | 397.71 | 1.169795 | 1.151900 | 15.7416 | 313.94 | 1.210000 | 22.6806 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_pf_below_34d;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |

## Judgment(판정)

- best_candidate(최선 후보): `s235_session_ref_h3_cd8`
- full_stage_pass(전체 통과): `False`
- reason(이유): validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), validation DD(검증 낙폭), OOS net/PF/DD(표본외 순손익/수익요인/낙폭)를 동시에 본다.
- next(다음): `236_adapter_research__stage235_side_specific_followup_review`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
