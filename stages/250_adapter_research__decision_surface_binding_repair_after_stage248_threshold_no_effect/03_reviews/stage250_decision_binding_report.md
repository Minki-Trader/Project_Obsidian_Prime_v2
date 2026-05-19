# Stage250 Decision Surface Binding Repair(250단계 결정 표면 결합 수리)

- stage(단계): `250_adapter_research__decision_surface_binding_repair_after_stage248_threshold_no_effect`
- run(실행): `run250A_stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect_v1`
- source_stage(원천 단계): `249_adapter_research__stage248_entry_source_followup_review`
- source_stage248_evidence_commit(원천 248단계 근거 커밋): `ab50acc695fdc069cb25dece7a66a38bb89bc925`
- source_stage249_evidence_commit(원천 249단계 근거 커밋): `6d2d94850638410e6456c3a8fadf5d3518220da4`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage251_bounded_followup_due_to_decision_binding_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can rank-conditioned score binding(순위 조건 점수 결합) make the decision/source controls(결정/원천 제어) actually change accepted MT5(MetaTrader 5, 메타트레이더5) decisions after Stage248(248단계) threshold-only no-effect(임계값 전용 효과 없음)?

Effect(효과): Stage248(248단계)의 작은 threshold(임계값) 반복이 아니라, score surface(점수 표면)를 실제 decision surface(결정 표면)에 닿게 만든다.

## Design(설계)

- fixed(고정): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험 비율) cap(상한) `0.0305`, hold(보유) `3`, cooldown(대기) `8`.
- changed(변경): low/mid rank bucket(낮은/중간 순위 구간)에 flat tilt(무포지션 쪽 점수 기울기)를 줘서 threshold(임계값) 앞의 probability(확률)를 바꿨다.
- not done(하지 않음): ONNX hardening(ONNX 경화), live readiness(실거래 준비), deployment(배포).

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | pass(통과) |
|---|---:|---:|---:|---:|---:|---|
| s250_stage248_binding_control | 972.15 | 12.9281 | 1.516651 | 776.02 | 1.780000 | false |
| s250_low_flat020 | 206.53 | 12.7710 | 1.476931 | 261.62 | 1.840000 | false |
| s250_low_flat025 | 130.73 | 13.0190 | 1.222766 | 186.09 | 1.820000 | false |
| s250_lowmid_flat025_015 | 112.88 | 11.4408 | 1.275592 | 200.67 | 2.150000 | false |

## Binding Telemetry(결합 기록)

- directional_threshold_pass_rows(방향 임계값 통과 행): `1939`
- threshold_or_margin_not_met_rows(임계값/마진 미충족 행): `67773`
- side_filter_block_rows(방향 필터 차단 행): `826`
- probability_binding_summary(확률 결합 요약): `stages/250_adapter_research__decision_surface_binding_repair_after_stage248_threshold_no_effect/03_reviews/stage250_probability_binding_summary.csv`
- model_score_audit(모델 점수 감사): `stages/250_adapter_research__decision_surface_binding_repair_after_stage248_threshold_no_effect/03_reviews/stage250_model_score_audit.csv`

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s250_stage248_binding_control`
- hard_quality_pass(강한 품질 통과): `false`
- overall_goal_complete(전체 목표 완료): `false`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준).
