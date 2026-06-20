# F93 Runtime Learning Probe Backfill Closeout

## Conclusion
F93 was repaired into a runtime learning observation, not a completed runtime probe. MT5 status: `completed`. The source surface is proxy_score_sample, so runtime_probe_completed remains blocked.

## What changed
- Added F93 runtime learning backfill script and MT5 artifacts.
- Deduplicated the best diagnostic side-balance/cost-exposure proxy sample into a one-feature runtime learning signal.
- Recorded Godel micro consult as advisory_only_no_reviewed_pass.

## What gates passed
- runtime_learning_probe_decision_gate is expected to pass after the decision artifact is audited.
- mt5_runtime_probe_contract_audit passes for runtime_probe_observation when both reports complete.
- test_gate is recorded after py_compile, pytest, script run, and decision gate execution.

## What gates were not applicable
- runtime_evidence_gate is not applicable to runtime authority or economics claims because those claims are not requested.

## What is still not enforced
- Full F93 side-balance/cost-exposure decision surface regeneration over the standard periods was not performed in this packet.
- Sample coverage remains sparse and side-imbalanced: this is learning evidence, not completion evidence.

## Allowed claims
- runtime_learning_probe_decision_recorded
- f93_repair_attempt_recorded
- runtime_probe_observation
- runtime_learning_record
- completion_claim_guard_recorded

## Forbidden claims
- runtime_probe_completed
- runtime_verified
- economics_pass
- selected_baseline
- promotion_candidate
- runtime_authority
- operating_promotion
- live_readiness
- Goal Achieve

## Next hardening step
If F93 is revisited, regenerate the `ridge_regime_dense_cost_norm_side25_q85` surface over the full standard validation_is and oos windows before requesting runtime_probe_completed.

## Metrics Snapshot
```json
{
  "validation_is": {
    "net_profit": 818.49,
    "profit_factor": 6.59,
    "max_drawdown_percent": 27.8,
    "trade_count": 18,
    "gross_profit": 964.83,
    "gross_loss": -146.34,
    "win_rate_percent": 66.67,
    "expectancy": 45.47,
    "recovery_factor": 2.53,
    "long_trade_count": 9,
    "short_trade_count": 9
  },
  "oos": {
    "net_profit": 611.31,
    "profit_factor": 12.1,
    "max_drawdown_percent": 46.47,
    "trade_count": 19,
    "gross_profit": 666.38,
    "gross_loss": -55.07,
    "win_rate_percent": 73.68,
    "expectancy": 32.17,
    "recovery_factor": 1.62,
    "long_trade_count": 7,
    "short_trade_count": 12
  }
}
```
