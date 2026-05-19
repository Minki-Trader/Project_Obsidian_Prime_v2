# Stage231 Lifecycle Repair Report(231단계 생애주기 수리 보고서)

- stage(단계): `231_adapter_research__midpf_oos_repair_after_guard_blend_failure`
- run(실행): `run231A_stage231_midpf_oos_repair_after_guard_blend_failure_v1`
- source_stage(원천 단계): `230_adapter_research__stage229_guard_blend_followup_review`
- source_run(원천 실행): `run230A_stage230_stage229_guard_blend_followup_review_v1`
- decision(판정): `open_stage232_bounded_followup_due_to_lifecycle_repair_tradeoff_candidate_not_final`
- external_verification_status(외부 검증 상태): `completed`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 판독)

Stage231(231단계)는 Stage229(229단계)의 margin band(마진 구간) 폭을 다시 넓히거나 좁히지 않았다. 대신 validation recovery clue(검증 회복 단서)인 wide guard(넓은 보호)에 hold compression(보유 기간 압축)과 cooldown extension(재진입 대기 연장)을 적용했다.

Effect(효과): mid PF/OOS(중반 수익요인/표본외) 훼손이 오래 보유하거나 같은 방향 재진입 밀도 때문인지 좁게 확인한다.

## KPI Table(KPI 핵심 성과 지표 표)

| adapter(어댑터) | axis(축) | hold(보유) | cooldown(대기) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s231_session_ref_h3_cd8 | session_ref_h3_cd8 | 3 | 8 | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | 1.740000 | 9.2072 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s231_wide_h2_cd8 | wide_lifecycle_h2_cd8 | 2 | 8 | 378.06 | 1.335616 | 1.176651 | 8.8194 | 237.40 | 1.420000 | 11.4320 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_pf_below_34d;oos_net_materially_below_stage171_primary |
| s231_wide_h3_cd12 | wide_lifecycle_h3_cd12 | 3 | 12 | 982.55 | 1.746101 | 1.311845 | 12.7188 | 620.85 | 1.670000 | 13.9720 | validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |
| s231_wide_h2_cd12 | wide_lifecycle_h2_cd12 | 2 | 12 | 366.20 | 1.364981 | 1.212842 | 9.4610 | 238.71 | 1.440000 | 11.6825 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_pf_below_34d;oos_net_materially_below_stage171_primary |

## Judgment(판정)

- best_candidate(최선 후보): `s231_session_ref_h3_cd8`
- full_stage_pass(전체 통과): `False`
- reason(이유): validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), validation DD(검증 낙폭), OOS net/PF/DD(표본외 순손익/수익요인/낙폭)를 동시에 봤다.
- next(다음): `232_adapter_research__stage231_lifecycle_followup_review`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
