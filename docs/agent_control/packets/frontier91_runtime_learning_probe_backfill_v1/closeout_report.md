# F91 Runtime Learning Probe Backfill Closeout

## Conclusion
F91 was repaired into a runtime learning observation, not a completed runtime probe. MT5 status: `completed`. The source surface is proxy_score_sample, so runtime_probe_completed remains blocked.

## What changed
- Added F91 runtime learning backfill script and MT5 artifacts.
- Materialized the best diagnostic regime-density-cost proxy side column into a one-feature runtime learning signal.
- Recorded Einstein micro consult as advisory_only_no_reviewed_pass.

## What gates passed
- runtime_learning_probe_decision_gate is expected to pass after the decision artifact is audited.
- mt5_runtime_probe_contract_audit passes for runtime_probe_observation when both reports complete.
- test_gate is recorded after py_compile, pytest, script run, and decision gate execution.

## What gates were not applicable
- runtime_evidence_gate is not applicable to runtime authority or economics claims because those claims are not requested.

## What is still not enforced
- Full F91 regime-density-cost decision surface regeneration over the standard periods was not performed in this packet.
- Sample coverage remains sparse and side-imbalanced: this is learning evidence, not completion evidence.

## Allowed claims
- runtime_learning_probe_decision_recorded
- f91_repair_attempt_recorded
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
If F91 is revisited, regenerate the `ridge_regime_dense_q85` surface over the full standard validation_is and oos windows before requesting runtime_probe_completed.

## Metrics Snapshot
```json
{
  "validation_is": {
    "net_profit": 378.09,
    "profit_factor": 1.83,
    "max_drawdown_percent": 27.46,
    "trade_count": 29,
    "gross_profit": 831.32,
    "gross_loss": -453.23,
    "win_rate_percent": 44.83,
    "expectancy": 13.04,
    "recovery_factor": 1.17,
    "long_trade_count": 15,
    "short_trade_count": 14
  },
  "oos": {
    "net_profit": -366.89,
    "profit_factor": 0.46,
    "max_drawdown_percent": 95.06,
    "trade_count": 25,
    "gross_profit": 307.03,
    "gross_loss": -673.92,
    "win_rate_percent": 56.0,
    "expectancy": -14.68,
    "recovery_factor": -0.46,
    "long_trade_count": 10,
    "short_trade_count": 15
  }
}
```
