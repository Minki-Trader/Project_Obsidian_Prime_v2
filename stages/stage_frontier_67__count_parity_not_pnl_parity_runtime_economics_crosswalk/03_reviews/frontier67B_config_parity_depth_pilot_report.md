# F67B Config Parity Depth Pilot(F67B 설정 동등성 깊이 파일럿)

- stage_id(단계 ID): `stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk`
- run_id(실행 ID): `frontier67B_config_parity_depth_pilot_v1`
- source_attempts(원천 시도 목록): `stages/stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64/02_runs/frontier66C_proxy_signal_mt5_backfill_v1/frontier66_proxy_signal_mt5_attempts.json`
- source_f67a_rows(F67A 원천 행): `stages/stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk/03_reviews/frontier67A_dd_basis_crosswalk_rows_review.csv`
- row_count(행 수): `64`
- claim_boundary(주장 경계): `config_parity_depth_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Read(판독)

Action(행동): F66 MT5 attempts(F66 MT5 시도) `64`개에서 generated `.ini/.set` identity(생성 설정 정체성)와 F67A DD basis rows(F67A 손실폭 기준 행)를 결합했다.

Effect(효과): DD gap(손실폭 간극)이 tester identity drift(테스터 정체성 드리프트)인지, intentional trade-shape config variation(의도된 거래 형태 설정 차이)인지, explicit cost identity missing(명시 비용 정체성 누락)인지 분리했다.

- tester_signature_count(테스터 정체성 서명 수): `1`
- EA core signature count(EA 핵심 설정 서명 수): `1`
- trade_shape_signature_count(거래 형태 설정 서명 수): `7`
- config_gap_read(설정 간극 판독): `tester_identity_uniform_but_explicit_cost_fields_missing`

## Tester Summary(테스터 요약)

```json
{
  "Symbol": {
    "US100": 64
  },
  "Period": {
    "M5": 64
  },
  "Model": {
    "4": 64
  },
  "Deposit": {
    "500": 64
  },
  "Leverage": {
    "1:100": 64
  },
  "Optimization": {
    "0": 64
  },
  "ExecutionMode": {
    "0": 64
  },
  "UseLocal": {
    "1": 64
  },
  "UseRemote": {
    "0": 64
  },
  "UseCloud": {
    "0": 64
  }
}
```

## EA Set Summary(EA 설정 요약)

```json
{
  "InpFixedLot": {
    "0.1": 64
  },
  "InpMaxConcurrentPositions": {
    "1": 64
  },
  "InpMaxHoldBars": {
    "12": 54,
    "2": 4,
    "4": 2,
    "6": 2,
    "8": 2
  },
  "InpAtrSltpEnabled": {
    "false": 22,
    "true": 42
  },
  "InpAtrStopMultiplier": {
    "0.8": 4,
    "1": 36,
    "1.5": 2,
    "missing": 22
  },
  "InpAtrTakeProfitMultiplier": {
    "0": 2,
    "1": 34,
    "1.6": 4,
    "3": 2,
    "missing": 22
  },
  "InpModelBackend": {
    "ebm_table": 64
  },
  "InpFeatureCount": {
    "1": 64
  },
  "InpDecisionMode": {
    "argmax": 64
  }
}
```

## Cost Identity(비용 정체성)

```json
{
  "spread": {
    "missing": 64
  },
  "commission": {
    "missing": 64
  },
  "slippage": {
    "missing": 64
  },
  "swap": {
    "missing": 64
  }
}
```

## DD By Trade Shape(거래 형태별 손실폭)

```json
{
  "by_max_hold_bars": {
    "12": {
      "rows": 54,
      "runtime_dd_gt10_rows": 50,
      "proxy_under10_runtime_gt10_rows": 12,
      "basis_reads": {
        "missing_dd_basis": 8,
        "near_aligned_within_1pp": 5,
        "proxy_much_worse_ge10pp": 1,
        "proxy_worse_lt10pp": 5,
        "runtime_breaks_dd10_proxy_under10": 12,
        "runtime_much_worse_ge10pp": 17,
        "runtime_worse_lt10pp": 6
      }
    },
    "2": {
      "rows": 4,
      "runtime_dd_gt10_rows": 4,
      "proxy_under10_runtime_gt10_rows": 4,
      "basis_reads": {
        "runtime_breaks_dd10_proxy_under10": 4
      }
    },
    "4": {
      "rows": 2,
      "runtime_dd_gt10_rows": 2,
      "proxy_under10_runtime_gt10_rows": 2,
      "basis_reads": {
        "runtime_breaks_dd10_proxy_under10": 2
      }
    },
    "6": {
      "rows": 2,
      "runtime_dd_gt10_rows": 2,
      "proxy_under10_runtime_gt10_rows": 2,
      "basis_reads": {
        "runtime_breaks_dd10_proxy_under10": 2
      }
    },
    "8": {
      "rows": 2,
      "runtime_dd_gt10_rows": 2,
      "proxy_under10_runtime_gt10_rows": 2,
      "basis_reads": {
        "runtime_breaks_dd10_proxy_under10": 2
      }
    }
  },
  "by_atr_sltp_enabled": {
    "false": {
      "rows": 22,
      "runtime_dd_gt10_rows": 22,
      "proxy_under10_runtime_gt10_rows": 0,
      "basis_reads": {
        "near_aligned_within_1pp": 3,
        "proxy_much_worse_ge10pp": 1,
        "proxy_worse_lt10pp": 2,
        "runtime_much_worse_ge10pp": 13,
        "runtime_worse_lt10pp": 3
      }
    },
    "true": {
      "rows": 42,
      "runtime_dd_gt10_rows": 38,
      "proxy_under10_runtime_gt10_rows": 22,
      "basis_reads": {
        "missing_dd_basis": 8,
        "near_aligned_within_1pp": 2,
        "proxy_worse_lt10pp": 3,
        "runtime_breaks_dd10_proxy_under10": 22,
        "runtime_much_worse_ge10pp": 4,
        "runtime_worse_lt10pp": 3
      }
    }
  }
}
```

## Next Action(다음 행동)

F67B does not close(마감 아님). Next action(다음 행동)은 F67C runtime-native order intent economics(런타임 기반 주문 의도 경제성) 또는 narrow MT5 Runtime Probe(MT5 런타임 탐침) 설계 전에, missing explicit spread/commission/slippage identity(명시 스프레드/수수료/슬리피지 정체성 누락)를 tester report/report parser(테스터 보고서/보고서 파서)에서 보강할 수 있는지 확인하는 것이다. F67 closeout(마감) 전에는 별도 MT5 Runtime Probe(MT5 런타임 탐침)가 필요하다.
