# F67C Runtime Native Order Intent Economics(F67C 런타임 기반 주문 의도 경제성)

- stage_id(단계 ID): `stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk`
- run_id(실행 ID): `frontier67C_runtime_native_order_intent_economics_v1`
- source_attempts(원천 시도 목록): `stages/stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64/02_runs/frontier66C_proxy_signal_mt5_backfill_v1/frontier66_proxy_signal_mt5_attempts.json`
- source_runtime_rows(원천 런타임 행): `stages/stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64/03_reviews/frontier66_proxy_signal_runtime_rows_review.csv`
- source_config_rows(원천 설정 행): `stages/stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk/03_reviews/frontier67B_config_parity_rows_review.csv`
- row_count(행 수): `64`
- claim_boundary(주장 경계): `runtime_native_order_intent_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Read(판독)

Action(행동): F66 MT5 runtime probe(F66 MT5 런타임 탐침) `64`개를 report deal table(보고서 거래 표), runtime summary(런타임 요약), F67B config rows(F67B 설정 행)와 결합했다.

Effect(효과): signal count parity(신호 수 동등성)가 order/trade economics(주문/거래 경제성)로 전이되는지, 그리고 explicit cost identity missing(명시 비용 정체성 누락)이 실제 비용 0인지 report-only cost(보고서 전용 비용)인지 분리했다.

- report_completed_rows(보고서 완료 행): `64/64`
- runtime_summary_completed_rows(런타임 요약 완료 행): `64/64`
- total_signal_count(총 신호 수): `70032`
- total_order_fill_count(총 주문 체결 수): `33252`
- total_trade_count(총 거래 수): `24284`
- overall_trade_to_signal_ratio(전체 거래/신호 비율): `0.3468`
- trade_to_signal_ratio median(거래/신호 비율 중앙값): `0.3248`
- net_per_signal median(신호당 순손익 중앙값): `0.0432`

## Cost Identity Reinforcement(비용 정체성 보강)

- commission_nonzero_rows(커미션 0 아님 행): `0/64`
- swap_nonzero_rows(스왑 0 아님 행): `54/64`
- deal_commission_sum_total(거래 커미션 합계): `0.0000`
- deal_swap_sum_total(거래 스왑 합계): `-515.9500`
- max_abs_net_reconciliation_error(순손익 재계산 최대 오차): `0.0000`

## Runtime Economics(런타임 경제성)

- net_profit_sum_total(순손익 합계): `2793.8000`
- positive_net_rows(순손익 양수 행): `42/64`
- profit_factor_ge2_rows(수익 팩터 2 이상 행): `1/64`
- drawdown_gt10_rows(손실폭 10 초과 행): `60/64`
- deal_count_equals_2x_trade_rows(거래 표 딜 수=거래 수*2 행): `64/64`
- order_fill_equals_deal_count_rows(주문 체결 수=거래 표 딜 수 행): `11/64`
- deal_minus_order_fill_positive_rows(거래 표 딜 수가 런타임 주문 체결 수보다 큰 행): `53/64`
- deal_minus_order_fill_positive_sum(초과 딜 수 합계): `15316.0000`

## Conversion Reads(전환 판독)

```json
{
  "heavy_lifecycle_compression_lt20pct": 12,
  "loose_lifecycle_compression_gte50pct": 11,
  "moderate_lifecycle_compression_20_to_50pct": 41
}
```

## Economics Reads(경제성 판독)

```json
{
  "negative_net_per_signal_or_pf_dd_fail": 22,
  "pf_ge2_but_dd_gt10": 1,
  "positive_net_per_signal_but_pf_or_dd_fail": 41
}
```

## Group Reads(그룹 판독)

```json
{
  "by_split": {
    "oos": {
      "rows": 32,
      "net_profit_sum": 1274.3400000000001,
      "swap_sum": -185.98,
      "trade_count_sum": 10266,
      "signal_count_sum": 30486,
      "trade_to_signal_ratio_summary": {
        "count": 32,
        "min": 0.09265042681657297,
        "p25": 0.2323689079101281,
        "median": 0.29983869841186694,
        "p75": 0.4659985348234973,
        "max": 0.9915966386554622
      },
      "profit_factor_summary": {
        "count": 32,
        "min": 0.77,
        "p25": 0.9475,
        "median": 1.0750000000000002,
        "p75": 1.15,
        "max": 2.18
      },
      "max_drawdown_percent_summary": {
        "count": 32,
        "min": 3.53,
        "p25": 11.425,
        "median": 18.65,
        "p75": 33.985,
        "max": 60.81
      },
      "conversion_reads": {
        "heavy_lifecycle_compression_lt20pct": 6,
        "loose_lifecycle_compression_gte50pct": 6,
        "moderate_lifecycle_compression_20_to_50pct": 20
      },
      "economics_reads": {
        "negative_net_per_signal_or_pf_dd_fail": 10,
        "pf_ge2_but_dd_gt10": 1,
        "positive_net_per_signal_but_pf_or_dd_fail": 21
      }
    },
    "validation_is": {
      "rows": 32,
      "net_profit_sum": 1519.46,
      "swap_sum": -329.96999999999997,
      "trade_count_sum": 14018,
      "signal_count_sum": 39546,
      "trade_to_signal_ratio_summary": {
        "count": 32,
        "min": 0.09779449478543341,
        "p25": 0.2402344342751603,
        "median": 0.35877723994544075,
        "p75": 0.47240423570471807,
        "max": 0.9875690607734806
      },
      "profit_factor_summary": {
        "count": 32,
        "min": 0.72,
        "p25": 0.98,
        "median": 1.0350000000000001,
        "p75": 1.12,
        "max": 1.47
      },
      "max_drawdown_percent_summary": {
        "count": 32,
        "min": 5.78,
        "p25": 15.217500000000001,
        "median": 23.509999999999998,
        "p75": 35.545,
        "max": 59.46
      },
      "conversion_reads": {
        "heavy_lifecycle_compression_lt20pct": 6,
        "loose_lifecycle_compression_gte50pct": 5,
        "moderate_lifecycle_compression_20_to_50pct": 21
      },
      "economics_reads": {
        "negative_net_per_signal_or_pf_dd_fail": 12,
        "positive_net_per_signal_but_pf_or_dd_fail": 20
      }
    }
  },
  "by_max_hold_bars": {
    "12": {
      "rows": 54,
      "net_profit_sum": 2228.68,
      "swap_sum": -516.64,
      "trade_count_sum": 16904,
      "signal_count_sum": 59684,
      "trade_to_signal_ratio_summary": {
        "count": 54,
        "min": 0.09265042681657297,
        "p25": 0.22382437823614296,
        "median": 0.29232667478984353,
        "p75": 0.43162945201721464,
        "max": 0.580952380952381
      },
      "profit_factor_summary": {
        "count": 54,
        "min": 0.72,
        "p25": 0.955,
        "median": 1.05,
        "p75": 1.15,
        "max": 2.18
      },
      "max_drawdown_percent_summary": {
        "count": 54,
        "min": 3.53,
        "p25": 14.8975,
        "median": 23.509999999999998,
        "p75": 36.415,
        "max": 60.81
      },
      "conversion_reads": {
        "heavy_lifecycle_compression_lt20pct": 12,
        "loose_lifecycle_compression_gte50pct": 3,
        "moderate_lifecycle_compression_20_to_50pct": 39
      },
      "economics_reads": {
        "negative_net_per_signal_or_pf_dd_fail": 21,
        "pf_ge2_but_dd_gt10": 1,
        "positive_net_per_signal_but_pf_or_dd_fail": 32
      }
    },
    "2": {
      "rows": 4,
      "net_profit_sum": 158.06,
      "swap_sum": -0.43,
      "trade_count_sum": 2587,
      "signal_count_sum": 2642,
      "trade_to_signal_ratio_summary": {
        "count": 4,
        "min": 0.966078697421981,
        "p25": 0.9710418586558366,
        "median": 0.9801326532536345,
        "p75": 0.988575955243976,
        "max": 0.9915966386554622
      },
      "profit_factor_summary": {
        "count": 4,
        "min": 1.0,
        "p25": 1.0075,
        "median": 1.045,
        "p75": 1.085,
        "max": 1.1
      },
      "max_drawdown_percent_summary": {
        "count": 4,
        "min": 12.23,
        "p25": 13.092500000000001,
        "median": 13.395,
        "p75": 14.3525,
        "max": 17.18
      },
      "conversion_reads": {
        "loose_lifecycle_compression_gte50pct": 4
      },
      "economics_reads": {
        "positive_net_per_signal_but_pf_or_dd_fail": 4
      }
    },
    "4": {
      "rows": 2,
      "net_profit_sum": 115.53,
      "swap_sum": 0.18,
      "trade_count_sum": 1073,
      "signal_count_sum": 2301,
      "trade_to_signal_ratio_summary": {
        "count": 2,
        "min": 0.46014877789585545,
        "p25": 0.462758642245421,
        "median": 0.4653685065949865,
        "p75": 0.4679783709445521,
        "max": 0.47058823529411764
      },
      "profit_factor_summary": {
        "count": 2,
        "min": 1.04,
        "p25": 1.0550000000000002,
        "median": 1.07,
        "p75": 1.085,
        "max": 1.1
      },
      "max_drawdown_percent_summary": {
        "count": 2,
        "min": 10.75,
        "p25": 11.725,
        "median": 12.7,
        "p75": 13.675,
        "max": 14.65
      },
      "conversion_reads": {
        "moderate_lifecycle_compression_20_to_50pct": 2
      },
      "economics_reads": {
        "positive_net_per_signal_but_pf_or_dd_fail": 2
      }
    },
    "6": {
      "rows": 2,
      "net_profit_sum": 279.57,
      "swap_sum": -0.13999999999999996,
      "trade_count_sum": 1885,
      "signal_count_sum": 3012,
      "trade_to_signal_ratio_summary": {
        "count": 2,
        "min": 0.6131934032983508,
        "p25": 0.6188640632008191,
        "median": 0.6245347231032874,
        "p75": 0.6302053830057558,
        "max": 0.6358760429082241
      },
      "profit_factor_summary": {
        "count": 2,
        "min": 1.02,
        "p25": 1.04,
        "median": 1.06,
        "p75": 1.08,
        "max": 1.1
      },
      "max_drawdown_percent_summary": {
        "count": 2,
        "min": 25.53,
        "p25": 25.872500000000002,
        "median": 26.215,
        "p75": 26.557499999999997,
        "max": 26.9
      },
      "conversion_reads": {
        "loose_lifecycle_compression_gte50pct": 2
      },
      "economics_reads": {
        "positive_net_per_signal_but_pf_or_dd_fail": 2
      }
    },
    "8": {
      "rows": 2,
      "net_profit_sum": 11.960000000000008,
      "swap_sum": 1.08,
      "trade_count_sum": 1835,
      "signal_count_sum": 2393,
      "trade_to_signal_ratio_summary": {
        "count": 2,
        "min": 0.744,
        "p25": 0.7538004307250539,
        "median": 0.7636008614501077,
        "p75": 0.7734012921751615,
        "max": 0.7832017229002154
      },
      "profit_factor_summary": {
        "count": 2,
        "min": 0.91,
        "p25": 0.965,
        "median": 1.02,
        "p75": 1.075,
        "max": 1.13
      },
      "max_drawdown_percent_summary": {
        "count": 2,
        "min": 16.23,
        "p25": 21.7725,
        "median": 27.314999999999998,
        "p75": 32.8575,
        "max": 38.4
      },
      "conversion_reads": {
        "loose_lifecycle_compression_gte50pct": 2
      },
      "economics_reads": {
        "negative_net_per_signal_or_pf_dd_fail": 1,
        "positive_net_per_signal_but_pf_or_dd_fail": 1
      }
    }
  },
  "by_atr_sltp_enabled": {
    "false": {
      "rows": 22,
      "net_profit_sum": 1606.03,
      "swap_sum": -471.45,
      "trade_count_sum": 4960,
      "signal_count_sum": 29649,
      "trade_to_signal_ratio_summary": {
        "count": 22,
        "min": 0.09265042681657297,
        "p25": 0.16737278549302148,
        "median": 0.20388599235314564,
        "p75": 0.2374429223744292,
        "max": 0.2524366471734893
      },
      "profit_factor_summary": {
        "count": 22,
        "min": 0.72,
        "p25": 0.92,
        "median": 1.105,
        "p75": 1.15,
        "max": 2.18
      },
      "max_drawdown_percent_summary": {
        "count": 22,
        "min": 10.87,
        "p25": 34.072500000000005,
        "median": 38.879999999999995,
        "p75": 48.7625,
        "max": 60.81
      },
      "conversion_reads": {
        "heavy_lifecycle_compression_lt20pct": 11,
        "moderate_lifecycle_compression_20_to_50pct": 11
      },
      "economics_reads": {
        "negative_net_per_signal_or_pf_dd_fail": 7,
        "pf_ge2_but_dd_gt10": 1,
        "positive_net_per_signal_but_pf_or_dd_fail": 14
      }
    },
    "true": {
      "rows": 42,
      "net_profit_sum": 1187.77,
      "swap_sum": -44.5,
      "trade_count_sum": 19324,
      "signal_count_sum": 40383,
      "trade_to_signal_ratio_summary": {
        "count": 42,
        "min": 0.19030732860520094,
        "p25": 0.3387323233498561,
        "median": 0.4597210863365606,
        "p75": 0.5025127232878186,
        "max": 0.9915966386554622
      },
      "profit_factor_summary": {
        "count": 42,
        "min": 0.77,
        "p25": 0.98,
        "median": 1.0350000000000001,
        "p75": 1.125,
        "max": 1.66
      },
      "max_drawdown_percent_summary": {
        "count": 42,
        "min": 3.53,
        "p25": 12.1325,
        "median": 16.155,
        "p75": 23.8,
        "max": 38.4
      },
      "conversion_reads": {
        "heavy_lifecycle_compression_lt20pct": 1,
        "loose_lifecycle_compression_gte50pct": 11,
        "moderate_lifecycle_compression_20_to_50pct": 30
      },
      "economics_reads": {
        "negative_net_per_signal_or_pf_dd_fail": 15,
        "positive_net_per_signal_but_pf_or_dd_fail": 27
      }
    }
  }
}
```

## Gap Cause Read(간극 원인 판독)

runtime_gap_cause_read(런타임 간극 원인 판독): `lifecycle_trade_compression_plus_tester_side_exit_deals_plus_report_level_swap_cost_not_config_identity_drift`.

This is an observation only(관찰 전용). F67 closeout(마감) still requires(여전히 필요) a narrow MT5 Runtime Probe(좁은 MT5 런타임 탐침) with explicit cost identity(명시 비용 정체성), order intent receipt(주문 의도 영수증), and proxy/runtime KPI gap(프록시/런타임 KPI 간극).

## Next Action(다음 행동)

`run_narrow_f67_mt5_runtime_probe_with_explicit_cost_identity_and_order_intent_receipt_before_closeout`
