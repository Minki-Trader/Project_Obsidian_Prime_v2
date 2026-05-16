# Stage59AO Equity Curve Audit(59AO단계 자금 곡선 감사)

- flagged_segment_rows(표시된 구간 행): `7`
- read(판독): Stage59AO(59AO단계)는 final net(최종 순손익)만 보지 않고 chronological third(시간순 3분할), PF(수익 팩터), MFE capture(MFE 포착), drawdown(손실폭)을 함께 본다.

Effect(효과): single spike dependence(단일 급등 의존)와 late flatline risk(후반 정체 위험)를 다음 단계 판정에 넘긴다.
- `s59ao_v46_t57_sd2` `validation_is` `chronological_third` `mid`: `weak_segment_pf`
- `s59ao_v46_t57_sd2` `validation_is` `chronological_third` `late`: `weak_segment_pf`
- `s59ao_v46_t57_sd2` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s59ao_v46_t60_sd2` `validation_is` `chronological_third` `mid`: `weak_segment_pf`
- `s59ao_v46_t60_sd2` `validation_is` `chronological_third` `late`: `weak_segment_pf`
- `s59ao_v46_t60_sd2` `oos` `chronological_third` `early`: `negative_or_flat_segment;weak_segment_pf;oos_early_pf_weak`
- `s59ao_v46_t57_sd5` `validation_is` `chronological_third` `mid`: `weak_segment_pf`
