# Stage65 State/Context Branch Review Report(65단계 상태/문맥 분기 검토 보고)

- run(실행): `run65A_stage65_state_context_branch_review_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_adapter(원천 어댑터): `s62_v41_sd8_h5`
- variants(변형): `s65_ctx_margin04_both, s65_ctx_margin08_short, s65_ctx_margin08_long`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_soft_gate_repair_in_stage66`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Legacy 34D(레거시 34D)는 code copy(코드 복사) 대상이 아니다. Effect(효과): Stage65(65단계)는 Stage64(64단계)에서 발견한 margin gate(마진 게이트) 힌트를 더 부드럽게 또는 방향별로 나눠, OOS DD(표본외 손실률) 개선을 유지하면서 validation KPI(검증 핵심 성과 지표)를 되살릴 수 있는지만 본다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s65_ctx_margin04_both | validation_is | 0.8700 | -132.79 | 36.21 | -0.6500 | -0.7132 |
| s65_ctx_margin04_both | oos | 1.0300 | 30.61 | 32.87 | 0.1900 | -0.5532 |
| s65_ctx_margin08_short | validation_is | 1.4400 | 447.38 | 16.10 | 2.2000 | -0.1432 |
| s65_ctx_margin08_short | oos | 1.4000 | 295.18 | 11.41 | 1.8300 | -0.1832 |
| s65_ctx_margin08_long | validation_is | 1.0900 | 158.60 | 20.84 | 0.5100 | -0.4932 |
| s65_ctx_margin08_long | oos | 1.2200 | 347.24 | 33.65 | 1.6000 | -0.3632 |

## Read(판독)

- best_variant(최선 변형): `s65_ctx_margin08_short`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present`
- segment_kpi_summary(구간 KPI 요약): `stages/65_adapter_research__state_context_branch_review/03_reviews/stage65_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/65_adapter_research__state_context_branch_review/03_reviews/stage65_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/65_adapter_research__state_context_branch_review/03_reviews/stage65_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/65_adapter_research__state_context_branch_review/03_reviews/stage65_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
