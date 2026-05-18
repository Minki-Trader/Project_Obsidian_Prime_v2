# Stage150 Validation Session Guard Repair(150단계 검증 세션 보호문 수리)

- stage(단계): `150_adapter_research__validation_session_guard_repair_after_stage148_tradeoff`
- run(실행): `run150A_stage150_validation_session_guard_repair_after_stage148_tradeoff_v1`
- source_stage(원천 단계): `149_adapter_research__stage148_softsession_repair_followup_review`
- source_stage149_closeout_commit(원천 149단계 종료 커밋): `21c48b7714b07876365eed250000e59d379f4b22`
- source_stage149_hash_record_commit(원천 149단계 해시 기록 커밋): `ce3b740df84f1654d3e3f6a941ecd439cde36140`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_stage151_validation_session_guard_followup_review_due_to_damage_or_no_gain_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can Stage148 session_mid(148단계 세션 중간)의 OOS mid repair(표본외 중반 수리)를 preserve(보존)하면서 validation early/mid quality(검증 초반/중반 품질)를 끌어올릴 수 있는가?

Effect(효과): OOS(표본외)만 좋아 보이는 후보를 최종처럼 보지 않고, 검증 품질 수리만 좁게 시험한다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val PF(검증 수익 팩터) | val early PF(검증 초반 수익 팩터) | val mid PF(검증 중반 수익 팩터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | OOS trades(표본외 거래 수) | OOS mid PF(표본외 중반 수익 팩터) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| s150_session_mid_replay_h3_cd5_sht54_lng52_risk035 | 1.450000 | 1.210793 | 1.453965 | 1.690000 | 1261.68 | 9.65 | 205 | 1.592742 |
| s150_session_mid_margin_restore_h3_cd5_sht54_lng52_risk035 | 1.590000 | 1.459637 | 1.378649 | 1.730000 | 1045.62 | 18.94 | 187 | 1.578473 |
| s150_session_mid_tighter_window_h3_cd5_sht54_lng52_risk035 | 1.430000 | 1.210793 | 1.337210 | 1.670000 | 1225.43 | 9.70 | 207 | 1.425086 |
| s150_session_mid_threshold_guard_h3_cd5_sht55_lng53_risk035 | 1.450000 | 1.210793 | 1.453965 | 1.690000 | 1261.68 | 9.65 | 205 | 1.592742 |

## Judgment(판정)

- best_adapter(최선 어댑터): `s150_session_mid_margin_restore_h3_cd5_sht54_lng52_risk035`
- best_validation_pf(최선 검증 수익 팩터): `1.590000`
- best_oos_pf(최선 표본외 수익 팩터): `1.730000`
- best_oos_mid_pf(최선 표본외 중반 수익 팩터): `1.578473`
- decision_use(판정 용도): Stage151(151단계)에서 이 수리축을 review-only(검토 전용)로 판정하고, 통과가 아니면 새 수리축 또는 demotion(강등)으로 넘긴다.
- overall_goal_complete(전체 목표 완료): `false`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
