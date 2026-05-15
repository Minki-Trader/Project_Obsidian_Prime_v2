# Stage59C New Model Source Equity Curve Audit(59C단계 새 모델 원천 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `s59c_v64_control_thr57_mr03_wideatr_sd5`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `weak_segment_pf`

## Chronological Thirds(시간 순서 3분할)

- validation_is chronological_third early: net(순손익) `79.520000`, PF(수익 팩터) `1.066919`, flag(표식) `acceptable_measurement_only`
- validation_is chronological_third mid: net(순손익) `91.490000`, PF(수익 팩터) `1.060274`, flag(표식) `acceptable_measurement_only`
- validation_is chronological_third late: net(순손익) `0.360000`, PF(수익 팩터) `1.000205`, flag(표식) `weak_segment_pf`
- oos chronological_third early: net(순손익) `70.360000`, PF(수익 팩터) `1.071122`, flag(표식) `acceptable_measurement_only`
- oos chronological_third mid: net(순손익) `136.62`, PF(수익 팩터) `1.133375`, flag(표식) `acceptable_measurement_only`
- oos chronological_third late: net(순손익) `272.22`, PF(수익 팩터) `1.201182`, flag(표식) `acceptable_measurement_only`

Effect(효과): final net(최종 순손익)만 보지 않고 validation/OOS(검증/표본외) 구간 흔들림과 drawdown recovery(낙폭 회복)를 다음 판정에 반영한다.
