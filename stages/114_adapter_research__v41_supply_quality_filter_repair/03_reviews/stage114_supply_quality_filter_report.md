# Stage114 Supply Quality Filter Repair Report(114단계 공급 품질 필터 수리 보고서)

- run(실행): `run114A_stage114_v41_supply_quality_filter_repair_v1`
- source_stage(원천 단계): `113_adapter_research__v41_route_supply_followup_review`
- source_stage113_closeout_commit(원천 113단계 종료 커밋): `903b5fc4ae2abef7bcff6f61b67b59edb38d9bbf`
- source_stage113_latest_commit(원천 113단계 최신 커밋): `83cf8dceba863e768ed821fcd6590c5751fe409f`
- source_adapter(원천 어댑터): `s112_v41_h3_cd9_nogate_lng53`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_supply_quality_filter_repair_review_in_stage115`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage112(112단계)에서 열린 no-gate route supply(무제한 경로 공급)를 유지하되, context rule(문맥 규칙), ET40 margin(ET40 여유폭), session window(세션 구간) 기반 quality filter(품질 필터)로 PF/DD(수익 팩터/손실률) 손상을 줄일 수 있는가?

Effect(효과): Stage114(114단계)는 새 모델 탐색(model hunting, 모델 탐색)이 아니라 Stage112의 공급 손상 원인을 좁게 거르는 bounded repair(경계 수리)다.

## Result Table(결과 표)

| adapter(어댑터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | delta vs Stage110(Stage110 대비 차이) | early PF(초반 수익 팩터) | early net(초반 순손익) |
|---|---:|---:|---:|---:|---:|---:|---:|
| s114_v41_h3_cd9_rule_block_lng53 | 1.370000 | 1668.39 | 19.43 | 253 | 106 | 1.480661 | 496.09 |
| s114_v41_h3_cd9_margin_mid_block_lng53 | 1.430000 | 941.69 | 28.19 | 221 | 74 | 1.259514 | 153.23 |
| s114_v41_h3_cd9_rule_margin_block_lng53 | 1.790000 | 1859.29 | 19.08 | 164 | 17 | 1.613887 | 311.83 |
| s114_v41_h3_cd9_session_margin_block_lng53 | 1.810000 | 2041.72 | 19.10 | 174 | 27 | 1.636306 | 330.79 |

## Best Read(최선 판독)

- best_variant(최선 변형): `s114_v41_h3_cd9_rule_block_lng53`
- oos_pf(표본외 수익 팩터): `1.370000`
- oos_net(표본외 순손익): `1668.39`
- oos_dd_pct(표본외 손실률): `19.43`
- trades(거래 수): `253`
- early_pf(초반 수익 팩터): `1.480661`
- early_net(초반 순손익): `496.09`

## Evidence Files(근거 파일)

- summary(요약): `stages/114_adapter_research__v41_supply_quality_filter_repair/03_reviews/stage114_supply_quality_filter_summary.csv`
- segment_kpi_summary(구간 KPI 요약): `stages/114_adapter_research__v41_supply_quality_filter_repair/03_reviews/stage114_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/114_adapter_research__v41_supply_quality_filter_repair/03_reviews/stage114_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/114_adapter_research__v41_supply_quality_filter_repair/03_reviews/stage114_gate_feature_summary.csv`
- trade_audit(거래 감사): `stages/114_adapter_research__v41_supply_quality_filter_repair/03_reviews/stage114_trade_audit.csv`

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage114 supply quality filter repair(114단계 공급 품질 필터 수리).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리), gate feature summary(게이트 피처 요약).
- evidence_missing(빠진 근거): Stage115(115단계) 후속 검토 전에는 Stage114 결과를 전체 연구 패키지로 보지 않는다.
- judgment_label(판정 라벨): `supply_quality_filter_repair_measured`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
