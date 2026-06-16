# F67A DD Basis Crosswalk Report(F67A 손실폭 기준 대조 보고서)

- stage_id(단계 ID): `stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk`
- run_id(실행 ID): `frontier67A_dd_basis_crosswalk_execution_v1`
- source_table(원천 표): `stages/stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64/03_reviews/frontier66_proxy_runtime_gap_by_split_review.csv`
- row_count(행 수): `64`
- claim_boundary(주장 경계): `dd_basis_crosswalk_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Read(판독)

Action(행동): F66 split rows(F66 분할 행)의 proxy DD(프록시 손실폭)와 runtime DD percent(런타임 손실폭 %)를 같은 row grain(행 단위)에서 비교했다.

Effect(효과): F67B config parity(설정 동등성)와 F67C order-intent economics(주문 의도 경제성)로 가기 전에, DD gap(손실폭 차이)이 단순 scale/unit bug(스케일/단위 버그)인지 heterogeneous measurement basis(이질 측정 기준)인지 좁혔다.

- delta median(차이 중앙값): `10.4811`
- delta p25/p75(차이 25/75분위): `5.0462` / `18.2482`
- delta min/max(차이 최소/최대): `-43.5116` / `45.4939`
- runtime/proxy DD ratio median(런타임/프록시 손실폭 비율 중앙값): `2.1297`
- runtime DD > 10 rows(런타임 손실폭 10 초과 행): `60/64`
- proxy DD > 10 rows(프록시 손실폭 10 초과 행): `31/64`
- both DD < 10 rows(둘 다 손실폭 10 미만 행): `3/64`
- runtime breaks DD10 while proxy under10(프록시 10 미만인데 런타임 10 초과): `22/64`

## Basis Read Counts(기준 판독 수)

```json
{
  "missing_dd_basis": 8,
  "near_aligned_within_1pp": 5,
  "proxy_much_worse_ge10pp": 1,
  "proxy_worse_lt10pp": 5,
  "runtime_breaks_dd10_proxy_under10": 22,
  "runtime_much_worse_ge10pp": 17,
  "runtime_worse_lt10pp": 6
}
```

## Proxy DD Families(프록시 손실폭 계열)

```json
{
  "drawdown_named_proxy_dd": {
    "rows": 2,
    "delta_summary": {
      "count": 2,
      "min": -43.51162980005735,
      "p25": -33.96318414139733,
      "median": -24.414738482737306,
      "p75": -14.866292824077284,
      "max": -5.3178471654172625
    },
    "runtime_dd_gt10_rows": 2,
    "proxy_dd_gt10_rows": 2,
    "basis_reads": {
      "proxy_much_worse_ge10pp": 1,
      "proxy_worse_lt10pp": 1
    }
  },
  "generic_proxy_dd": {
    "rows": 2,
    "delta_summary": {
      "count": 2,
      "min": -0.0714950456166008,
      "p25": -0.06764302874697181,
      "median": -0.06379101187734282,
      "p75": -0.059938995007713824,
      "max": -0.05608697813808483
    },
    "runtime_dd_gt10_rows": 2,
    "proxy_dd_gt10_rows": 2,
    "basis_reads": {
      "near_aligned_within_1pp": 2
    }
  },
  "missing_proxy_dd_field": {
    "rows": 8,
    "delta_summary": {
      "count": 0
    },
    "runtime_dd_gt10_rows": 7,
    "proxy_dd_gt10_rows": 0,
    "basis_reads": {
      "missing_dd_basis": 8
    }
  },
  "other_proxy_dd_field": {
    "rows": 44,
    "delta_summary": {
      "count": 44,
      "min": -7.853187780935224,
      "p25": 5.430557689184888,
      "median": 10.956036411549512,
      "p75": 24.552384352861075,
      "max": 45.493944994930516
    },
    "runtime_dd_gt10_rows": 41,
    "proxy_dd_gt10_rows": 25,
    "basis_reads": {
      "near_aligned_within_1pp": 3,
      "proxy_worse_lt10pp": 4,
      "runtime_breaks_dd10_proxy_under10": 16,
      "runtime_much_worse_ge10pp": 16,
      "runtime_worse_lt10pp": 5
    }
  },
  "risk_percent_proxy_dd": {
    "rows": 8,
    "delta_summary": {
      "count": 8,
      "min": 6.8831614492915705,
      "p25": 9.889866586507596,
      "median": 12.403922530483776,
      "p75": 17.45879753808314,
      "max": 18.02737672047134
    },
    "runtime_dd_gt10_rows": 8,
    "proxy_dd_gt10_rows": 2,
    "basis_reads": {
      "runtime_breaks_dd10_proxy_under10": 6,
      "runtime_much_worse_ge10pp": 1,
      "runtime_worse_lt10pp": 1
    }
  }
}
```

## Next Action(다음 행동)

F67A does not close(마감 아님). Next action(다음 행동)은 F67B config parity depth pilot(설정 동등성 깊이 파일럿)에서 spread/commission/slippage/modeling/deposit/leverage(스프레드/수수료/슬리피지/모델링/예치금/레버리지)를 row sample(행 표본) 기준으로 대조하는 것이다. F67 closeout(마감) 전에는 별도 MT5 Runtime Probe(MT5 런타임 탐침)가 필요하다.
