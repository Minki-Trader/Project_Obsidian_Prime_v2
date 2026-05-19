# Stage261 Stage260 Tight Plus High Edge PF/OOS Follow-up Review(261단계 260단계 PF/표본외 후속 검토)

- stage(단계): `261_adapter_research__stage260_tight_plus_highedge_pf_oos_followup_review`
- run(실행): `run261A_stage261_stage260_tight_plus_highedge_pf_oos_followup_review_v1`
- source_stage(원천 단계): `260_adapter_research__tight_plus_highedge_pf_oos_recovery_repair`
- source_run(원천 실행): `run260A_stage260_tight_plus_highedge_pf_oos_recovery_repair_v1`
- source_stage260_evidence_commit(원천 260단계 근거 커밋): `eb99d51a9d38093e9ed2c97932f93b10127edb49`
- source_stage260_hash_record_commit(원천 260단계 해시 기록 커밋): `8cdeb8526ed3fbb1aae24a25a990aab846916332`
- decision(판정): `open_stage262_bounded_lowrank_lowedge_oos_recovery_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 해석)

`s260_lowrank_lowedge_filter`는 validation(검증) 기준으로는 34D(레거시 34D) 목표를 넘었다. validation PF(검증 수익 팩터) 1.61, validation net(검증 순수익) 1291.28, mid PF(중간 수익 팩터) 1.6004다.

하지만 OOS(표본외)는 아직 약하다. OOS net(표본외 순수익)이 775.97이고, OOS PF(표본외 수익 팩터)는 1.70이다. 그래서 최종이 아니라 Stage262(262단계)에서 OOS 회복만 좁게 수리한다.

## KPI Tradeoff(KPI 절충)

| adapter(어댑터) | val PF(검증 수익 팩터) | PF gap vs 34D(34D 대비 PF 차이) | val net(검증 순수익) | DD%(손실폭) | mid PF(중간 수익 팩터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순수익) | read(해석) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s260_highedge_control | 1.56 | -0.023157 | 1204.24 | 9.0307 | 1.534204818 | 1.7 | 828.96 | control_reference_not_final |
| s260_lowrank_lowedge_filter | 1.61 | 0.026843 | 1291.28 | 9.0536 | 1.600364571 | 1.7 | 775.97 | best_validation_tradeoff_oos_repair_needed |
| s260_midlow_lowedge_filter | 1.59 | 0.006843 | 972.15 | 12.9281 | 1.516650878 | 1.78 | 776.02 | oos_pf_help_validation_damage |
| s260_vhigh_highedge_relax | 1.56 | -0.023157 | 1204.24 | 9.0307 | 1.534204818 | 1.7 | 828.96 | no_effect_or_duplicate |
| s260_lowrank_filter_vhigh_relax | 1.61 | 0.026843 | 1291.28 | 9.0536 | 1.600364571 | 1.7 | 775.97 | duplicate_best_shape_oos_repair_needed |

## Judgment(판정)

- result_subject(판정 대상): `run261A_stage261_stage260_tight_plus_highedge_pf_oos_followup_review_v1`
- judgment_label(판정 라벨): `useful_validation_tradeoff_not_final`
- evidence_missing(부족 근거): Stage262 OOS recovery repair(262단계 표본외 회복 수리), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- next_condition(다음 조건): `262_adapter_research__lowrank_lowedge_oos_recovery_repair`
- forbidden_claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
