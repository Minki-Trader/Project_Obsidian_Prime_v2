# Stage59AM Equity Curve Audit(59AM단계 자금 곡선 감사)

- flagged_segment_rows(표시된 구간 행): `10`
- read(판독): Stage59AM(59AM단계)는 final net(최종 순손익)만 보지 않고 chronological third(시간순 3분할), PF(수익 팩터), MFE capture(MFE 포착), drawdown(손실폭)을 함께 본다.

Effect(효과): single spike dependence(단일 급등 의존)나 late flatline risk(후반 정체 위험)를 다음 단계 판단에 남긴다.
- `s59am_v50_topup_sd2_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- `s59am_v50_topup_sd2_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s59am_v51_topup_sd3_h2_mr03_wideatr` `validation_is` `chronological_third` `early`: `weak_segment_pf`
- `s59am_v51_topup_sd3_h2_mr03_wideatr` `validation_is` `chronological_third` `mid`: `weak_segment_pf`
- `s59am_v51_topup_sd3_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- `s59am_v51_topup_sd3_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s59am_v51_topup_sd3_h2_mr03_wideatr` `oos` `chronological_third` `mid`: `weak_segment_pf`
- `s59am_v49_midcov_sd3_h2_mr03_wideatr` `validation_is` `chronological_third` `mid`: `weak_segment_pf`
- `s59am_v49_midcov_sd3_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `weak_segment_pf`
- `s59am_v49_midcov_sd3_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
