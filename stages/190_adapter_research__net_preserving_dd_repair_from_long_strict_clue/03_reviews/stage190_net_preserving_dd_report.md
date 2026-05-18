# Stage190 Net-Preserving DD Repair Report(190단계 순손익 보존 낙폭 수정 보고서)

- stage(단계): `190_adapter_research__net_preserving_dd_repair_from_long_strict_clue`
- run(실행): `run190A_stage190_net_preserving_dd_repair_from_long_strict_clue_v1`
- source_stage(원천 단계): `189_adapter_research__stage188_context_feature_followup_review`
- source_run(원천 실행): `run189A_stage189_stage188_context_feature_followup_review_v1`
- source_adapter(원천 어댑터): `s188_long_strict_dd_clue_plus_s188_bctl_net_reference`
- source_stage189_closeout_commit(원천 189단계 종료 커밋): `b4e635088439ee28eab74daf17aad9256a4c41a7`
- source_stage189_hash_record_commit(원천 189단계 해시 기록 커밋): `32ed138ef171461d5cadc0be054a227ca8bd4f77`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage191_bounded_followup_due_to_net_preserving_dd_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage188(188단계) long_strict(롱 강화)는 DD(낙폭)를 낮췄지만 net/mid PF(순손익/중반 수익요인)를 손상했다. Risk lift(위험 상향) 또는 TP lift(익절 상향)가 net(순손익)을 회복하면서 DD(낙폭)를 허용 범위에 둘 수 있는지 본다.
- action(행동): context gate(문맥 게이트)는 control(대조군)과 long_strict(롱 강화)만 쓰고, short_relief/gate_off(숏 완화/게이트 해제)는 반복하지 않았다. Risk(위험)와 TP(익절)만 좁게 조합했다.
- effect(효과): failure memory(실패 기억)를 지키면서 34D(34D) KPI(핵심 성과 지표)에 가까운 net/DD(순손익/낙폭) 균형을 확인한다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | risk(위험) | TP(익절) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s190_bctl | bctl | 0.0325 | 4.50 | 1.690000 | 1012.75 | 13.3347 | 1.485500 | 1.910000 | 7.9373 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s190_ls_r0365 | ls_r0365 | 0.0365 | 4.50 | 1.660000 | 1074.06 | 14.1773 | 1.356009 | 1.860000 | 8.1363 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s190_ls_tp475 | ls_tp475 | 0.0325 | 4.75 | 1.700000 | 978.36 | 12.6421 | 1.386547 | 1.890000 | 7.2701 | validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s190_ls_r0365_tp475 | ls_r0365_tp475 | 0.0365 | 4.75 | 1.690000 | 1167.26 | 14.1540 | 1.375235 | 1.900000 | 8.1188 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s190_bctl`
- validation_net(검증 순손익): `1012.75`
- validation_pf(검증 수익요인): `1.690000`
- validation_dd(검증 낙폭): `13.3347`
- validation_mid_pf(검증 중반 수익요인): `1.485500`
- oos_pf(표본외 수익요인): `1.910000`
- quality_flags(품질 표식): `validation_balance_dd_above_34d;validation_mid_pf_below_34d`

## Judgment(판정)

Stage190(190단계)는 research/development only(연구개발 전용)입니다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않습니다.
