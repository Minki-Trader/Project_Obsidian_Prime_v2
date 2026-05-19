# Stage248 Entry/Source Quality Repair(248단계 진입/원천 품질 수리)

- stage(단계): `248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff`
- run(실행): `run248A_stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff_v1`
- source_stage247_evidence_commit(원천 247단계 근거 커밋): `afc675cb7036ea69e9fa4655e5c23831e11a52be`
- source_stage247_hash_record_commit(원천 247단계 해시 기록 커밋): `319aa8a5e0ad03d54526f697a474b861aaa98253`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage249_bounded_followup_due_to_entry_source_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 판독)

- Stage248(248단계)는 soft guard(부드러운 보호문)를 더 강하게 하지 않았다.
- 대신 short/long entry threshold(숏/롱 진입 임계값)를 좁게 올려 weak entry(약한 진입)를 줄일 수 있는지 봤다.
- ATR SL/TP(ATR 손절/익절), model-controlled risk%(모델 제어 위험 비율), risk cap(위험 상한) `0.0305`, hold(보유) `3`, cooldown(대기) `8`은 고정했다.
- 결과적으로 모든 threshold variant(임계값 변형)가 reference(참고값)와 같은 KPI(핵심 성과 지표)를 냈다. Effect(효과): 이 축은 decision surface(의사결정 표면)를 실제로 바꾸지 못한 no-effect failure(효과 없음 실패)로 본다.

## KPI Matrix(KPI 핵심 성과 지표 행렬)

| adapter(어댑터) | val net(검증 순손익) | DD%(낙폭) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | flags(표식) |
|---|---:|---:|---:|---:|---|
| s248_cap0305_reference | 976.67 | 12.9428 | 1.522877250708345 | 775.76 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s248_short055 | 976.67 | 12.9428 | 1.522877250708345 | 775.76 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s248_short056 | 976.67 | 12.9428 | 1.522877250708345 | 775.76 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s248_long053 | 976.67 | 12.9428 | 1.522877250708345 | 775.76 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s248_balanced055_053 | 976.67 | 12.9428 | 1.522877250708345 | 775.76 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d |

## Judgment(판정)

- result_subject(판정 대상): `run248A_stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff_v1`
- evidence_available(사용 근거): `stages/248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff/03_reviews/stage248_entry_source_kpi_summary.csv`, `stages/248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff/03_reviews/stage248_quality_matrix.csv`, `stages/248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff/03_reviews/stage248_segment_kpi_summary.csv`, `stages/248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff/03_reviews/stage248_risk_atr_telemetry.csv`.
- evidence_missing(부족 근거): Stage249(249단계) follow-up review(후속 검토), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- judgment_label(판정 라벨): `entry_source_repair_measured_candidate_not_final(진입/원천 수리 측정됨, 최종 아님)`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`
- next_condition(다음 조건): `249_adapter_research__stage248_entry_source_followup_review`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
