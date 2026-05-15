# Stage59V Bounded Followup Equity Curve Audit(59V단계 경계 후속 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `s59v_s59s_mr025_sl20_tp30_sd12_h5_rearm002`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `negative_or_flat_segment;weak_segment_pf;weak_segment_pf`

## Chronological Thirds(시간 순서 3분할)

- validation_is chronological_third early: net(순손익) `-73.110000`, PF(수익 팩터) `0.936628`, flag(표식) `negative_or_flat_segment;weak_segment_pf`
- validation_is chronological_third mid: net(순손익) `165.35`, PF(수익 팩터) `1.136961`, flag(표식) `acceptable_measurement_only`
- validation_is chronological_third late: net(순손익) `350.29`, PF(수익 팩터) `1.216252`, flag(표식) `acceptable_measurement_only`
- oos chronological_third early: net(순손익) `67.700000`, PF(수익 팩터) `1.064961`, flag(표식) `acceptable_measurement_only`
- oos chronological_third mid: net(순손익) `43.110000`, PF(수익 팩터) `1.042403`, flag(표식) `weak_segment_pf`
- oos chronological_third late: net(순손익) `414.60`, PF(수익 팩터) `1.284948`, flag(표식) `acceptable_measurement_only`

Effect(효과): final net(최종 순손익)만 보지 않고 validation/OOS(검증/표본외) 구간 흔들림, drawdown recovery(드로다운 회복), late flatline risk(후반 정체 위험)를 다음 판정에 반영한다.
