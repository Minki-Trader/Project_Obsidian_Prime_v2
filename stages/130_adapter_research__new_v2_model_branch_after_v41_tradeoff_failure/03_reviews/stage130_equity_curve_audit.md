# Stage130 Equity Curve Audit(130단계 자금 곡선 감사)

- flagged_segment_rows(표시된 구간 행): `17`
- read(판독): final net(최종 순손익)만 보지 않고 validation/OOS(검증/미래구간), drawdown(드로다운), cost expectancy(비용 기대값), MFE/MAE(최대 유리/불리 이동)를 같이 본다.
- effect(효과): 한 번의 spike(급등)나 late flatline(후반 정체)에 기대는 후보를 Stage131(131단계)에서 다시 압박한다.

- `s130_v42_veto_sd2_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `weak_segment_pf`
- `s130_v42_veto_sd2_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s130_v42_veto_sd2_h2_mr03_wideatr` `oos` `chronological_third` `mid`: `weak_segment_pf`
- `s130_v42_veto_sd2_h2_mr03_wideatr` `oos` `chronological_third` `late`: `weak_segment_pf`
- `s130_v43_direction_sd2_h2_mr03_wideatr` `validation_is` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf`
- `s130_v43_direction_sd2_h2_mr03_wideatr` `validation_is` `chronological_third` `mid`: `negative_or_flat_segment;weak_segment_pf`
- `s130_v43_direction_sd2_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- `s130_v43_direction_sd2_h2_mr03_wideatr` `oos` `chronological_third` `mid`: `weak_segment_pf`
- `s130_v43_direction_sd2_h2_mr03_wideatr` `oos` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf`
- `s130_v44_topup_veto_sd2_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- `s130_v44_topup_veto_sd2_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s130_v44_topup_veto_sd2_h2_mr03_wideatr` `oos` `chronological_third` `mid`: `negative_or_flat_segment;weak_segment_pf`
- `s130_v44_topup_veto_sd2_h2_mr03_wideatr` `oos` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf`
- `s130_v45_withb_veto_sd2_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `weak_segment_pf`
- `s130_v45_withb_veto_sd2_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s130_v45_withb_veto_sd2_h2_mr03_wideatr` `oos` `chronological_third` `mid`: `weak_segment_pf`
- `s130_v45_withb_veto_sd2_h2_mr03_wideatr` `oos` `chronological_third` `late`: `weak_segment_pf`
