# Stage64 State/Context Report(64단계 상태/문맥 보고)

- run(실행): `run64A_stage64_state_context_drawdown_smoothing_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_adapter(원천 어댑터): `s62_v41_sd8_h5`
- variants(변형): `s64_ctx_margin08, s64_ctx_prob48, s64_ctx_session16`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_state_context_branch_repair`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Legacy 34D(레거시 34D)는 code copy(코드 복사) 대상이 아니다. Effect(효과): Stage64(64단계)는 Stage63(63단계) risk3 tight bracket(위험 3% 타이트 브래킷)을 출발점으로 두고, state/context gate(상태/문맥 게이트)가 OOS DD(표본외 손실률)와 early/mid weakness(초기/중간 약점)를 줄이는지만 본다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s64_ctx_margin08 | validation_is | 1.0800 | 28.40 | 22.46 | 0.4200 | -0.5032 |
| s64_ctx_margin08 | oos | 2.0300 | 200.00 | 11.79 | 4.0000 | 0.4468 |
| s64_ctx_prob48 | validation_is | 0.8700 | -3.49 | 3.01 | -0.5000 | -0.7132 |
| s64_ctx_prob48 | oos | 1.0300 | 0.18 | 2.14 | 0.0600 | -0.5532 |
| s64_ctx_session16 | validation_is | 1.1400 | 161.41 | 21.73 | 0.6800 | -0.4432 |
| s64_ctx_session16 | oos | 1.3300 | 279.82 | 27.86 | 1.6500 | -0.2532 |

## Read(판독)

- best_variant(최선 변형): `s64_ctx_margin08`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present;validation_pf_lt_1_10_after_repair`
- segment_kpi_summary(구간 KPI 요약): `stages/64_adapter_research__state_context_drawdown_smoothing/03_reviews/stage64_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/64_adapter_research__state_context_drawdown_smoothing/03_reviews/stage64_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/64_adapter_research__state_context_drawdown_smoothing/03_reviews/stage64_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/64_adapter_research__state_context_drawdown_smoothing/03_reviews/stage64_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
