# Stage59F New Model Branch Equity Curve Audit(59F단계 새 모델 분기 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `s59f_v54_coo`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `negative_or_flat_segment;weak_segment_pf;negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk;weak_segment_pf`

## Chronological Thirds(시간 순서 3분할)

- validation_is chronological_third early: net(순손익) `-26.160000`, PF(수익 팩터) `0.967972`, flag(표식) `negative_or_flat_segment;weak_segment_pf`
- validation_is chronological_third mid: net(순손익) `27.090000`, PF(수익 팩터) `1.034820`, flag(표식) `weak_segment_pf`
- validation_is chronological_third late: net(순손익) `-48.070000`, PF(수익 팩터) `0.948428`, flag(표식) `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- oos chronological_third early: net(순손익) `74.440000`, PF(수익 팩터) `1.097752`, flag(표식) `acceptable_measurement_only`
- oos chronological_third mid: net(순손익) `215.36`, PF(수익 팩터) `1.229463`, flag(표식) `acceptable_measurement_only`
- oos chronological_third late: net(순손익) `168.88`, PF(수익 팩터) `1.176041`, flag(표식) `acceptable_measurement_only`

Effect(효과): final net(최종 순손익)만 보지 않고 validation/OOS(검증/표본외) 구간 흔들림, drawdown recovery(낙폭 회복), late flatline risk(후반 정체 위험)를 다음 판정에 반영한다.
