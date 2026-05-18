# Stage135 Concentration Risk Report(135단계 집중 위험 보고서)

- risk_flag_count(위험 표시 수): `9`

| split(분할) | metric(지표) | value(값) | threshold(기준) | notes(메모) |
|---|---|---:|---:|---|
| validation_is | largest_third_net_share | 0.644192 | 0.55 | one chronological third should not dominate the result |
| validation_is | negative_month_count | 1.0 | 0 | negative month count is recorded for curve quality |
| validation_is | trade_count_gap_to_34d | -141.0 | 0 | 34D lesson target used only as KPI target surface |
| oos | top5_trade_share | 0.418379 | 0.4 | top five winning trades should not dominate the result |
| oos | negative_month_count | 1.0 | 0 | negative month count is recorded for curve quality |
| oos | trade_count_gap_to_34d | -225.0 | 0 | 34D lesson target used only as KPI target surface |
| validation_is | segment_quality_early | validation_third_pf_below_repair_target | acceptable_measurement_only | chronological third segment quality flag |
| validation_is | segment_quality_mid | validation_third_pf_below_repair_target | acceptable_measurement_only | chronological third segment quality flag |
| validation_is | segment_quality_late | single_window_profit_concentration | acceptable_measurement_only | chronological third segment quality flag |

Effect(효과): 강한 최종 순손익(net P/L, 순손익)을 보존하되, 한 구간이나 적은 거래 수에 기대는 위험은 Stage136(136단계)로 넘긴다.
