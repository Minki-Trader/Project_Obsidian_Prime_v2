# Stage59AN Equity Curve Audit(59AN단계 자금 곡선 감사)

- flagged_segment_rows(표시된 구간 행): `6`
- read(판독): Stage59AN(59AN단계)는 final net(최종 순손익)만 보지 않고 chronological third(시간순 3분할), PF(수익 팩터), MFE capture(MFE 포착), drawdown(손실폭)을 함께 본다.

Effect(효과): single spike dependence(단일 급등 의존)나 late flatline risk(후반 정체 위험)를 다음 단계 판단에 남긴다.
- `s59an_v41_agree_sd2_h2_mr03_wideatr` `oos` `chronological_third` `late`: `weak_segment_pf`
- `s59an_v46_sd2` `validation_is` `chronological_third` `mid`: `weak_segment_pf`
- `s59an_v46_sd2` `validation_is` `chronological_third` `late`: `weak_segment_pf`
- `s59an_v46_sd2` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s59an_v47_topup_slot_sd2_h2_mr03_wideatr` `validation_is` `chronological_third` `late`: `negative_or_flat_segment;weak_segment_pf;validation_late_flatline_risk`
- `s59an_v47_topup_slot_sd2_h2_mr03_wideatr` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
