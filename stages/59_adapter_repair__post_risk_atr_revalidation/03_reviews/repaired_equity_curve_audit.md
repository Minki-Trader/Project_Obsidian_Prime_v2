# Stage59 Repaired Equity Curve Audit(59단계 수리 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `s59_mr02_wideatr_sd5`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `weak_segment_pf`

## Chronological Thirds(시간 순서 3분할)

- validation_is chronological_third early: net(순손익) `55.290000`, PF(수익 팩터) `1.071277`, flag(표식) `acceptable_measurement_only`
- validation_is chronological_third mid: net(순손익) `58.240000`, PF(수익 팩터) `1.064200`, flag(표식) `acceptable_measurement_only`
- validation_is chronological_third late: net(순손익) `10.510000`, PF(수익 팩터) `1.009599`, flag(표식) `weak_segment_pf`
- oos chronological_third early: net(순손익) `49.510000`, PF(수익 팩터) `1.078606`, flag(표식) `acceptable_measurement_only`
- oos chronological_third mid: net(순손익) `94.810000`, PF(수익 팩터) `1.146057`, flag(표식) `acceptable_measurement_only`
- oos chronological_third late: net(순손익) `158.49`, PF(수익 팩터) `1.216242`, flag(표식) `acceptable_measurement_only`

Effect(효과): final net(최종 순손익)만 보지 않고 validation/OOS(검증/표본외) 구간 흔들림과 drawdown recovery(낙폭 회복)를 다음 판정에 반영한다.
