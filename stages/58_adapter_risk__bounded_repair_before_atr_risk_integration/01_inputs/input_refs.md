# Stage58 Input References(58단계 입력 참조)

- stage57_decision(57단계 판정): `stages/57_adapter_quality__equity_segment_kpi_audit_gate/03_reviews/stage57_decision.md`
- equity_curve_audit(자금 곡선 감사): `stages/57_adapter_quality__equity_segment_kpi_audit_gate/03_reviews/equity_curve_audit.md`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `stages/57_adapter_quality__equity_segment_kpi_audit_gate/03_reviews/segment_kpi_summary.csv`
- monthly_kpi_summary(월별 핵심 성과 지표 요약): `stages/57_adapter_quality__equity_segment_kpi_audit_gate/03_reviews/monthly_kpi_summary.csv`
- source_adapter_spec(원천 어댑터 명세): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/04_selected/baseline_adapter_ba14_spec.json`
- source_runtime_summary(원천 런타임 요약): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50CA_baseline_adapter_onnx_runtime_reproduction_summary.csv`

Effect(효과): Stage58(58단계)는 final net(최종 순손익)이 아니라 segment stability(구간 안정성), risk telemetry(위험 텔레메트리), bracket telemetry(브래킷 텔레메트리), validation/OOS consistency(검증/표본외 일관성)를 기준으로 판단한다.
