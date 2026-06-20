# F92 Runtime Learning Probe Backfill Closeout

## Conclusion
F92 was repaired into a runtime learning observation, not a completed runtime probe. MT5 status: `completed`. The source surface is proxy_score_sample, so runtime_probe_completed remains blocked.

## What changed
- Added F92 runtime learning backfill script and MT5 artifacts.
- Materialized the best diagnostic path-shape proxy side column into a one-feature runtime learning signal.
- Recorded Maxwell micro consult as advisory_only_no_reviewed_pass.

## What gates passed
- runtime_learning_probe_decision_gate is expected to pass after the decision artifact is audited.
- mt5_runtime_probe_contract_audit passes for runtime_probe_observation when both reports complete.
- test_gate is recorded after py_compile, pytest, script run, and decision gate execution.

## What gates were not applicable
- runtime_evidence_gate is not applicable to runtime authority or economics claims because those claims are not requested.

## What is still not enforced
- Full F92 path-shape decision surface regeneration over the standard periods was not performed in this packet.
- Sample coverage remains sparse and side-imbalanced: this is learning evidence, not completion evidence.

## Allowed claims
- runtime_learning_probe_decision_recorded
- f92_repair_attempt_recorded
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
If F92 is revisited, regenerate the `path_first_touch_atr_m15_h48_cost2__extratrees_full58_q90` surface over the full standard validation_is and oos windows before requesting runtime_probe_completed.

## Metrics Snapshot
```json
{
  "validation_is": {
    "net_profit": -39.16,
    "profit_factor": 0.92,
    "max_drawdown_percent": 54.76,
    "trade_count": 6,
    "gross_profit": 430.3,
    "gross_loss": -469.46,
    "win_rate_percent": 33.33,
    "expectancy": -6.53,
    "recovery_factor": -0.07,
    "long_trade_count": 2,
    "short_trade_count": 4
  },
  "oos": {
    "net_profit": -494.58,
    "profit_factor": 0.05,
    "max_drawdown_percent": 99.11,
    "trade_count": 6,
    "gross_profit": 23.75,
    "gross_loss": -518.33,
    "win_rate_percent": 16.67,
    "expectancy": -82.43,
    "recovery_factor": -0.82,
    "long_trade_count": 2,
    "short_trade_count": 4
  }
}
```
