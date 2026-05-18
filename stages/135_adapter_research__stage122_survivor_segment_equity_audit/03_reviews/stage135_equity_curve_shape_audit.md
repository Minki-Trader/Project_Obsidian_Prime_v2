# Stage135 Equity Curve Shape Audit(135단계 자금곡선 모양 감사)

- stage(단계): `135_adapter_research__stage122_survivor_segment_equity_audit`
- run(실행): `run135A_stage135_stage122_survivor_segment_equity_audit_v1`
- adapter(어댑터): `s133_stage122_control_cd5_h3_risk035`

## Read(판독)

equity curve(자금곡선)는 최종 손익만 보지 않는다. Effect(효과): 한 구간의 폭발적 수익이나 늦은 평탄화를 따로 잡는다.

| split(분할) | final net(최종 순손익) | closed DD(닫힌 거래 손실폭) | recovered(회복) | longest no-high trades(최장 신고점 없음 거래 수) | flags(표시) |
|---|---:|---:|---|---:|---|
| validation_is | 1392.66 | 184.18 | True | 27 | largest_third_net_share, negative_month_count, pf_below_34d_exact, segment_quality_early, segment_quality_late, segment_quality_mid, trade_count_below_34d, trade_count_gap_to_34d |
| oos | 1102.04 | 160.19 | True | 26 | drawdown_pct_above_34d, negative_month_count, top5_trade_share, trade_count_below_34d, trade_count_gap_to_34d |

## Decision Effect(판정 효과)

`continue_stage136_trade_count_concentration_repair_candidate_not_final`. Stage136(136단계)는 trade count(거래 수)와 concentration(집중)을 수리하되, PF/net(수익 팩터/순손익), drawdown(손실폭), risk/ATR(위험/ATR)을 훼손하면 안 된다.
