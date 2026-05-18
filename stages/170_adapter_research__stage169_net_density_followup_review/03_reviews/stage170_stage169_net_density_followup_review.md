# Stage170 Stage169 Net/Density Follow-up Review(170단계 169단계 순손익/밀도 후속 검토)

- stage(단계): `170_adapter_research__stage169_net_density_followup_review`
- run(실행): `run170A_stage170_stage169_net_density_followup_review_v1`
- source_stage(원천 단계): `169_adapter_research__net_density_lift_pf_preservation`
- source_closeout_commit(원천 종료 커밋): `9717fa54fd32bda22acd0845b80c1dc922e0fc17`
- source_hash_record_commit(원천 해시 기록 커밋): `5a27b8537dfff9fedb4c8961cfe64b7ab9d25b1a`
- external_verification_status(외부 검증 상태): `review_only_source_stage169_completed`
- decision(판정): `open_stage171_segment_stability_equity_curve_audit_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Did Stage169(169단계) move net/density(순손익/밀도) closer to legacy 34D(레거시 34D) while preserving PF/DD/OOS early(수익요인/낙폭/표본외 초반)?

## Simple KPI Read(쉬운 핵심 성과 지표 판독)

Stage169(169단계)는 34D(34D) 근처까지 왔다. 특히 `s169_short_pre_risk0350_h3_cd5_sht54_lng52`는 validation net(검증 순손익) `983.96`으로 34D `987.60`보다 `3.64` 낮고, validation PF(검증 수익요인) `1.61`은 34D `1.583157`보다 높다. OOS DD(표본외 낙폭) `11.03%`도 34D `12.909136%`보다 낮다.

Effect(효과): KPI(핵심 성과 지표) 큰 줄기는 좋아졌지만, final(최종)이나 operating(운영) 주장은 아직 금지한다.

| adapter(어댑터) | role(역할) | val PF(검증 수익요인) | val net(검증 순손익) | gap vs 34D(34D 대비 차이) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | weak segments(약한 구간) | judgment(판정) |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| s169_short_pre_risk0300_h3_cd5_sht54_lng52 | secondary_lower_risk_backup | 1.61 | 777.28 | -210.32 | 1.83 | 667.99 | 9.56 | early;mid | lower_risk_backup_pf_dd_pass_net_gap_remaining |
| s169_short_pre_risk0350_h3_cd5_sht54_lng52 | primary_stage171_segment_equity_audit_anchor | 1.61 | 983.96 | -3.64 | 1.82 | 835.78 | 11.03 | early;mid | near_34d_net_pf_dd_pass_segment_equity_audit_required |
| s169_short_pre_restore_long_risk0300_h3_cd5_sht54_lng52 | negative_long_restore_failure_memory | 1.59 | 950.69 | -36.91 | 1.58 | 568.58 | 13.14 | early;mid | failure_memory_long_restore_oos_pf_dd_damage |

## Segment Warning(구간 경고)

Primary(주 후보) `s169_short_pre_risk0350_h3_cd5_sht54_lng52`는 total KPI(전체 핵심 성과 지표)가 강하지만 validation early/mid(검증 초반/중반) PF(수익요인)가 34D 아래다. Late validation(검증 후반)이 순손익의 큰 비중을 들고 있어, Stage171(171단계)에서 equity curve(자산 곡선), balance curve(잔고 곡선), concentration(집중도), recovery(회복)를 봐야 한다.

| split(분할) | segment(구간) | trades(거래) | net(순손익) | PF(수익요인) | net share(순손익 비중) | flag(표식) |
|---|---|---:|---:|---:|---:|---|
| validation_is | early | 81.0 | 197.72 | 1.481586 | 0.2009 | below_34d_pf |
| validation_is | mid | 81.0 | 244.29 | 1.477427 | 0.2483 | below_34d_pf |
| validation_is | late | 81.0 | 541.95 | 1.788234 | 0.5508 | pf_ok_vs_34d |
| oos | early | 60.0 | 208.22 | 1.749262 | 0.2491 | pf_ok_vs_34d |
| oos | mid | 59.0 | 203.14 | 1.622804 | 0.2431 | pf_ok_vs_34d |
| oos | late | 59.0 | 424.42 | 2.028722 | 0.5078 | pf_ok_vs_34d |

## Attribution(원인 분해)

- action(행동): risk cap(위험 상한)을 `0.025`에서 `0.035`로 올린 변형이 net(순손익)을 크게 올렸다. effect(효과): signal quality(신호 품질) 개선인지 단순 scaling(스케일링)인지 분리 검토가 필요하다.
- action(행동): long restore(롱 복원) 변형을 같이 보존했다. effect(효과): validation net(검증 순손익)은 좋아도 OOS PF/DD(표본외 수익요인/낙폭)가 훼손되면 후보에서 밀어야 한다.
- action(행동): segment KPI(구간 핵심 성과 지표)를 별도 표로 남겼다. effect(효과): 높은 final net(최종 순손익) 하나로 약한 구간을 덮지 않는다.

## Route Decision(경로 판정)

1. primary(주): `stage171_primary_segment_equity_concentration_audit` from `s169_short_pre_risk0350_h3_cd5_sht54_lng52`.
2. secondary(보조): `stage171_lower_risk_backup_comparison` from `s169_short_pre_risk0300_h3_cd5_sht54_lng52`.
3. failure_memory(실패 기억): `preserve_long_restore_oos_damage_memory` from `s169_short_pre_restore_long_risk0300_h3_cd5_sht54_lng52`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
