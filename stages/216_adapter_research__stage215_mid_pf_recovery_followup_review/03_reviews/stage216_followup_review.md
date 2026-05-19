# Stage216 Follow-up Review(216단계 후속 검토)

- stage(단계): `216_adapter_research__stage215_mid_pf_recovery_followup_review`
- run(실행): `run216A_stage216_stage215_mid_pf_recovery_followup_review_v1`
- source_stage(원천 단계): `215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain`
- source_run(원천 실행): `run215A_stage215_validation_mid_pf_recovery_preserve_oos_gain_v1`
- source_stage215_evidence_commit(원천 215단계 근거 커밋): `1d6a2a4b1cda23981bb09e3fb4dfefa1cdd85825`
- source_stage215_hash_record_commit(원천 215단계 해시 기록 커밋): `ada5f5d5d1b061aad906028e9e22ae9f94e4da14`
- decision(판정): `open_stage217_bounded_oos_preserving_mid_pf_micro_interpolation_candidate_not_final`
- best_oos_preserver(최선 표본외 보존): `s215_r031375_s2025_t460`
- best_mid_recovery(최선 중반 회복): `s215_r031375_s2050_t465`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## KPI Tradeoff(KPI 핵심 성과 지표 상충)

| adapter(어댑터) | profile(유형) | val net gap(검증 순손익 차이) | mid PF gap(중반 수익요인 차이) | OOS vs 210(210 대비 표본외) | OOS vs 213(213 대비 표본외) | early PF(초반 수익요인) | risk floor(위험 바닥) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| s215_r03125_s2025_t460 | oos_preserved_mid_pf_failed(표본외 보존, 중반 수익요인 실패) | -30.84 | -0.036924 | 5.75 | -29.3 | 1.564734123 | 0 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s215_r03125_s2050_t465 | mid_pf_recovered_oos_failed(중반 수익요인 회복, 표본외 실패) | 66.77 | 0.105555 | -6.6 | -41.65 | 1.5708746 | 0 | validation_early_pf_below_34d;oos_net_materially_below_stage171_primary |
| s215_r031375_s2025_t460 | oos_preserved_mid_pf_failed(표본외 보존, 중반 수익요인 실패) | -31.09 | -0.052144 | 11.18 | -23.87 | 1.567494182 | 0 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s215_r031375_s2050_t465 | mid_pf_recovered_oos_failed(중반 수익요인 회복, 표본외 실패) | 71.68 | 0.107741 | -8.24 | -43.29 | 1.564999609 | 0 | validation_early_pf_below_34d;oos_net_materially_below_stage171_primary |

## Judgment(판정)

- `s215_r031375_s2025_t460`는 OOS net(표본외 순손익) `726.04`로 Stage210(210단계) 기준을 넘겼지만 validation mid PF(검증 중반 수익요인)는 `1.531012848`로 약했다.
- `s215_r031375_s2050_t465`는 validation mid PF(검증 중반 수익요인) `1.690898468`와 validation net(검증 순손익) `1059.28`를 회복했지만 OOS net(표본외 순손익)은 `706.62`로 Stage210(210단계) 기준보다 `-8.24` 낮았다.
- risk floor(위험 바닥)는 0건이라 이번 상충의 주원인으로 보지 않는다.
- Stage216(216단계)는 final(최종), deployment(배포), live readiness(실거래 준비)를 주장하지 않는다.
- Effect(효과): Stage217(217단계)는 넓은 탐색이 아니라 SL/TP(손절/익절)와 risk cap(위험 상한)의 좁은 미세 보간만 시험한다.
