# Stage59J New Model Branch Equity Curve Audit(59J단계 새 모델 분기 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `s59j_v62_trn_h4_sd5`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `negative_or_flat_segment;weak_segment_pf;negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`

## Chronological Thirds(시간 순서 3분할)

- validation_is chronological_third early: net(순손익) `172.59`, PF(수익 팩터) `1.109042`, flag(표식) `acceptable_measurement_only`
- validation_is chronological_third mid: net(순손익) `-29.450000`, PF(수익 팩터) `0.985576`, flag(표식) `negative_or_flat_segment;weak_segment_pf`
- validation_is chronological_third late: net(순손익) `-26.360000`, PF(수익 팩터) `0.987163`, flag(표식) `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- oos chronological_third early: net(순손익) `139.62`, PF(수익 팩터) `1.121863`, flag(표식) `acceptable_measurement_only`
- oos chronological_third mid: net(순손익) `-81.710000`, PF(수익 팩터) `0.941639`, flag(표식) `negative_or_flat_segment;weak_segment_pf`
- oos chronological_third late: net(순손익) `317.56`, PF(수익 팩터) `1.209534`, flag(표식) `acceptable_measurement_only`

Effect(효과): final net(최종 순손익)만 보지 않고 validation/OOS(검증/표본외) 구간 흔들림, drawdown recovery(드로다운 회복), late flatline risk(후반 정체 위험)를 다음 판정에 반영한다.
