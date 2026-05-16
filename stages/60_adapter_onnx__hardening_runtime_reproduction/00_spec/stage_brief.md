# 60 Brief(60단계 개요)

- stage_id(단계 ID): `60_adapter_onnx__hardening_runtime_reproduction`
- source_stage(원천 단계): `59AR_adapter_repair__new_model_branch_from_stage59aq`
- source_decision(원천 판정): `proceed_to_stage60_onnx_hardening`
- selected_adapter_under_review(검토 중 선택 어댑터): `s59ar_v41_sd8_h3`
- bounded_question(경계 질문): `Can the Stage59AR post-ATR/risk adapter be frozen, exported to ONNX, parity-checked, and reproduced in MT5 runtime without damaging validation/OOS, segment KPI, equity behavior, risk telemetry, or bracket telemetry?`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

Stage60(60단계)은 ONNX(모델 교환 형식) hardening(경화)과 MT5(메타트레이더5) runtime reproduction(런타임 재현)만 다룬다. Effect(효과): Stage59AR(59AR단계)의 강한 연구 후보를 동결·내보내기·동등성·런타임 재현으로 검증하되, deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)는 만들지 않는다.

Required outputs(필수 산출물)는 `onnx_export_report.json`, `onnx_parity_report.json`, `mt5_onnx_runtime_reproduction.md`, `mt5_onnx_runtime_summary.json`, `mt5_onnx_runtime_summary.csv`, `mt5_onnx_segment_kpi_summary.csv`, `mt5_onnx_risk_atr_telemetry.csv`, `stage60_decision.md`다. Effect(효과): ONNX(모델 교환 형식) export(내보내기) 하나만으로 Stage60(60단계)을 닫지 못하게 한다.
