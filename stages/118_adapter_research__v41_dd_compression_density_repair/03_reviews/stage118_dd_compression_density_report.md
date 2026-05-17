# Stage118 DD Compression Density Repair Report(118단계 손실률 압축 밀도 수리 보고서)

- run(실행): `run118A_stage118_v41_dd_compression_density_repair_v1`
- source_stage(원천 단계): `117_adapter_research__v41_density_quality_followup_review`
- source_stage117_closeout_commit(원천 117단계 종료 커밋): `df51abd7602801dc78cf3e23172bf03b13688557`
- source_stage117_latest_commit(원천 117단계 최신 커밋): `f3263eaf79a5d5eb55c25ff7c3b35ec42544fa6c`
- source_stage116_latest_commit(원천 116단계 최신 커밋): `c115268a398da4c8334b2c21530016f110b8e927`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_dd_compression_followup_review_in_stage119`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage116(116단계)의 strong PF/net(강한 수익 팩터/순손익)을 크게 훼손하지 않으면서, model-risk cap(모델 위험 상한)만 낮춰 DD%(손실률)를 Stage110 reference(110단계 참조점) 또는 34D target(34D 목표)에 더 가깝게 압축할 수 있는가?

Effect(효과): Stage118(118단계)은 threshold-only density recovery(임계값만 낮추는 밀도 회복)를 반복하지 않고, ATR/bracket(ATR/괄호 주문)과 model-controlled risk%(모델 제어 위험 퍼센트)를 유지한 채 위험 상한만 좁게 시험한다.

## Result Table(결과 표)

| adapter(어댑터) | source(원천) | risk cap(위험 상한) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | DD delta(손실률 차이) | trades(거래 수) | early PF(초반 수익 팩터) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| s118_v41_h3_cd9_session_margin_risk040_lng52 | s116_v41_h3_cd9_session_margin_lng52 | 0.0400 | 1.820000 | 1495.80 | 16.24 | -2.86 | 174 | 1.660824 |
| s118_v41_h3_cd9_session_margin_risk035_lng52 | s116_v41_h3_cd9_session_margin_lng52 | 0.0350 | 1.830000 | 1195.83 | 14.39 | -4.71 | 174 | 1.677162 |
| s118_v41_h3_cd9_session_margin_risk030_lng52 | s116_v41_h3_cd9_session_margin_lng52 | 0.0300 | 1.830000 | 923.09 | 12.43 | -6.67 | 174 | 1.677859 |
| s118_v41_h3_cd8_session_margin_risk035_lng53 | s116_v41_h3_cd8_session_margin_lng53 | 0.0350 | 1.730000 | 1070.61 | 14.75 | -4.84 | 176 | 1.622275 |

## Best Read(최선 판독)

- best_variant(최선 변형): `s118_v41_h3_cd9_session_margin_risk035_lng52`
- oos_pf(표본외 수익 팩터): `1.830000`
- oos_net(표본외 순손익): `1195.83`
- oos_dd_pct(표본외 손실률): `14.39`
- dd_delta_vs_stage116(116단계 대비 손실률 차이): `-4.71`
- trades(거래 수): `174`

## Judgment(판정)

- result_subject(판정 대상): Stage118 risk-cap DD compression(118단계 위험 상한 손실률 압축).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): 34D trade count(34D 거래 수) `404`에 가까운 density(밀도) 회복과 더 넓은 equity-shape audit(자본 곡선 형태 감사).
- judgment_label(판정 라벨): `dd_compression_measured_not_final`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

## Evidence Files(근거 파일)

- summary(요약): `stages/118_adapter_research__v41_dd_compression_density_repair/03_reviews/stage118_dd_compression_density_summary.csv`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `stages/118_adapter_research__v41_dd_compression_density_repair/03_reviews/stage118_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/118_adapter_research__v41_dd_compression_density_repair/03_reviews/stage118_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/118_adapter_research__v41_dd_compression_density_repair/03_reviews/stage118_gate_feature_summary.csv`
- trade_audit(거래 감사): `stages/118_adapter_research__v41_dd_compression_density_repair/03_reviews/stage118_trade_audit.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
