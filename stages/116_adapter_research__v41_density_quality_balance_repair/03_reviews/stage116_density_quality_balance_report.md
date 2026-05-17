# Stage116 Density Quality Balance Repair Report(116단계 밀도-품질 균형 수리 보고서)

- run(실행): `run116A_stage116_v41_density_quality_balance_repair_v1`
- source_stage(원천 단계): `115_adapter_research__v41_supply_quality_followup_review`
- source_stage115_closeout_commit(원천 115단계 종료 커밋): `1e3f9f6f245c1c6ebaac6a34003b7d928ed0ca19`
- source_stage115_latest_commit(원천 115단계 최신 커밋): `11cb15dba87ef213aea84a74d9512684fd84a491`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_density_quality_followup_review_in_stage117`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage114(114단계)의 high-quality filters(고품질 필터)에서 거래 수를 회복하거나, density-preserving filter(밀도 보존 필터)의 PF/DD(수익 팩터/손실률)를 보강해서 34D KPI(34D 핵심 성과 지표) 격차를 더 줄일 수 있는가?

Effect(효과): Stage116(116단계)은 새 모델 탐색(model hunting, 모델 탐색)이 아니라 long threshold(롱 임계값)와 cooldown(재진입 대기)만 좁게 흔든다.

## Result Table(결과 표)

| adapter(어댑터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | early PF(초반 수익 팩터) | early net(초반 순손익) |
|---|---:|---:|---:|---:|---:|---:|
| s116_v41_h3_cd9_rule_margin_lng52 | 1.790000 | 1859.29 | 19.08 | 164 | 1.613887 | 311.83 |
| s116_v41_h3_cd8_rule_margin_lng53 | 1.690000 | 1621.47 | 19.54 | 166 | 1.551222 | 291.31 |
| s116_v41_h3_cd9_session_margin_lng52 | 1.810000 | 2041.72 | 19.10 | 174 | 1.636306 | 330.79 |
| s116_v41_h3_cd8_session_margin_lng53 | 1.710000 | 1783.59 | 19.59 | 176 | 1.581398 | 312.74 |

## Best Read(최선 판독)

- best_variant(최선 변형): `s116_v41_h3_cd9_session_margin_lng52`
- oos_pf(표본외 수익 팩터): `1.810000`
- oos_net(표본외 순손익): `2041.72`
- oos_dd_pct(표본외 손실률): `19.10`
- trades(거래 수): `174`

## Evidence Files(근거 파일)

- summary(요약): `stages/116_adapter_research__v41_density_quality_balance_repair/03_reviews/stage116_density_quality_balance_summary.csv`
- segment_kpi_summary(구간 KPI 요약): `stages/116_adapter_research__v41_density_quality_balance_repair/03_reviews/stage116_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/116_adapter_research__v41_density_quality_balance_repair/03_reviews/stage116_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/116_adapter_research__v41_density_quality_balance_repair/03_reviews/stage116_gate_feature_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
