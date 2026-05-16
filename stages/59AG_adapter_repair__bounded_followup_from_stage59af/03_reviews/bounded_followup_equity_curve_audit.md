# Stage59AG Bounded Follow-Up Equity Curve Audit(59AG단계 경계 후속 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `s59ag_risk5`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `negative_or_flat_segment;weak_segment_pf;negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk;weak_segment_pf`

## Chronological Thirds(시간 순서 3분할)

- validation_is chronological_third early: net(순손익) `36.160000`, PF(수익 팩터) `1.016874`, flag(표식) `weak_segment_pf`
- validation_is chronological_third mid: net(순손익) `-12.910000`, PF(수익 팩터) `0.994275`, flag(표식) `negative_or_flat_segment;weak_segment_pf`
- validation_is chronological_third late: net(순손익) `-0.900000`, PF(수익 팩터) `0.999710`, flag(표식) `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- oos chronological_third early: net(순손익) `369.03`, PF(수익 팩터) `1.197110`, flag(표식) `acceptable_measurement_only`
- oos chronological_third mid: net(순손익) `529.56`, PF(수익 팩터) `1.155253`, flag(표식) `acceptable_measurement_only`
- oos chronological_third late: net(순손익) `1551.16`, PF(수익 팩터) `1.222301`, flag(표식) `acceptable_measurement_only`

Effect(효과): model-risk cap(모델 위험 한도)이 final net(최종 순손익)만 바꿨는지, 아니면 validation/OOS(검증/표본외) 구간 품질과 drawdown recovery(손실 회복)를 같이 개선했는지 판정 근거로 남긴다.
