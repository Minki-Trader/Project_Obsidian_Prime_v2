# Stage212 Segment Equity Audit(212단계 구간/잔고곡선 감사)

- stage(단계): `212_adapter_research__stage210_candidate_segment_equity_audit`
- run(실행): `run212A_stage212_stage210_candidate_segment_equity_audit_v1`
- source_stage(원천 단계): `211_adapter_research__stage210_oos_net_recovery_followup_review`
- source_run(원천 실행): `run211A_stage211_stage210_oos_net_recovery_followup_review_v1`
- source_stage211_evidence_commit(원천 211단계 근거 커밋): `6beda2e88076605ba2cb81e805ceb24f0c675b49`
- source_stage211_hash_record_commit(원천 211단계 해시 기록 커밋): `749fc3a09534b99d1f1afa185f798571a586704c`
- selected_anchor(선택 후보): `s210_ls_r0315`
- decision(판정): `open_stage213_bounded_oos_monthly_concentration_repair_for_s210_r0315_candidate_not_final`
- external_verification_status(외부 검증 상태): `review_only_source_stage210_mt5_reports_completed`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## KPI Read(KPI 핵심 성과 지표 판독)

- validation net(검증 순손익): `1200.27`
- validation PF(검증 수익요인): `1.7`
- validation DD(검증 낙폭): `12.6726` with margin vs 34D(34D 대비 여유) `0.236536`
- validation mid PF(검증 중반 수익요인): `1.695877099`
- OOS net(표본외 순손익): `714.86`
- OOS PF(표본외 수익요인): `1.74`
- OOS DD(표본외 낙폭): `9.2909`
- OOS delta vs Stage171 primary(Stage171 주 후보 대비 표본외 차이): `-120.92`

## Audit Read(감사 판독)

- Segment thirds(3분할 구간): validation/OOS(검증/표본외) 모두 net positive(순손익 양수)다.
- Monthly behavior(월별 행동): validation(검증)은 negative month(음수 월)가 없고, OOS(표본외)는 `2`개 negative month(음수 월)가 있다: `2025.12,2026.04`.
- Concentration risk(집중 위험): validation flags(검증 표식) `thin_validation_dd_margin;final_balance_not_new_high`, OOS flags(표본외 표식) `top5_concentration_watch;late_quarter_concentration_watch;final_balance_not_new_high`.
- Risk/ATR telemetry(위험/ATR 기록): mandatory telemetry(필수 기록)는 존재하고 min lot floor(최소 lot 바닥) 영향은 0이다.

## Judgment(판정)

`s210_ls_r0315` remains active research candidate(활성 연구 후보 유지) but is not final(최종 아님).

Effect(효과): Stage213(213단계)은 OOS monthly loss(표본외 월별 손실), concentration watch(집중 주의), thin validation DD margin(얇은 검증 낙폭 여유)을 좁게 수리한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
