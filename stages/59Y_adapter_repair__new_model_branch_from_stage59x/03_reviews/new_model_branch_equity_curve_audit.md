# Stage59Y New Model Branch Equity Curve Audit(59Y단계 새 모델 분기 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `s59y_v64_gap14_h2_sd5`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk;weak_segment_pf`

## Chronological Thirds(시간 순서 3분할)

- validation_is chronological_third early: net(순손익) `33.810000`, PF(수익 팩터) `1.033666`, flag(표식) `weak_segment_pf`
- validation_is chronological_third mid: net(순손익) `249.55`, PF(수익 팩터) `1.209521`, flag(표식) `acceptable_measurement_only`
- validation_is chronological_third late: net(순손익) `-5.950000`, PF(수익 팩터) `0.996723`, flag(표식) `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- oos chronological_third early: net(순손익) `82.320000`, PF(수익 팩터) `1.092805`, flag(표식) `acceptable_measurement_only`
- oos chronological_third mid: net(순손익) `88.790000`, PF(수익 팩터) `1.085878`, flag(표식) `acceptable_measurement_only`
- oos chronological_third late: net(순손익) `212.53`, PF(수익 팩터) `1.184976`, flag(표식) `acceptable_measurement_only`

Effect(효과): final net(최종 순손익)만 보지 않고 validation/OOS(검증/표본외) 구간 흔들림, drawdown recovery(손실 회복), late flatline risk(후반 정체 위험)를 다음 판정에 반영한다.
