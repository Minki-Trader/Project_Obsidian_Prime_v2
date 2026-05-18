# Stage131 Equity Curve Audit(131단계 자금 곡선 감사)

- flagged_segment_rows(표시된 구간 행): `13`
- read(판독): density repair(밀도 수리)가 순손익만 올리는지, 아니면 drawdown(드로다운)과 cost expectancy(비용 기대값)를 같이 고치는지 본다.
- effect(효과): 후속 단계가 같은 실패를 반복하지 않게 약한 구간을 남긴다.

- `s131_v42_sd5_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `weak_segment_pf`
- `s131_v42_sd5_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s131_v42_sd5_h2_mr03_wideatr` `oos` `chronological_third` `mid`: `weak_segment_pf`
- `s131_v42_sd5_h2_mr03_wideatr` `oos` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf`
- `s131_v42_cd5_sd5_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- `s131_v42_cd5_sd5_h2_mr03_wideatr` `oos` `chronological_third` `early`: `weak_segment_pf;oos_early_pf_weak`
- `s131_v42_cd10_sd10_h2_mr03_wideatr` `validation_is` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf`
- `s131_v42_cd10_sd10_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- `s131_v42_cd10_sd10_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s131_v42_transition_sd5_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `weak_segment_pf`
- `s131_v42_transition_sd5_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s131_v42_transition_sd5_h2_mr03_wideatr` `oos` `chronological_third` `mid`: `negative_or_flat_segment;weak_segment_pf`
- `s131_v42_transition_sd5_h2_mr03_wideatr` `oos` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf`
