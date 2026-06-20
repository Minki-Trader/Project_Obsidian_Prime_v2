# F90 Runtime Learning Probe Backfill Closeout

## Conclusion
F90 was repaired into a runtime learning observation, not a completed runtime probe. MT5 status: `completed`. The source surface is diagnostic_sample, so runtime_probe_completed remains blocked.

## What changed
- Added F90 runtime learning backfill script and MT5 artifacts.
- Materialized the best diagnostic time-to-barrier ordering predicted_event_type column into a one-feature runtime learning signal.
- Recorded Banach micro consult as advisory_only_no_reviewed_pass.

## What gates passed
- runtime_learning_probe_decision_gate is expected to pass after the decision artifact is audited.
- mt5_runtime_probe_contract_audit passes for runtime_probe_observation when both reports complete.
- test_gate is recorded after py_compile, pytest, script run, and decision gate execution.

## What gates were not applicable
- runtime_evidence_gate is not applicable to runtime authority or economics claims because those claims are not requested.

## What is still not enforced
- Full F90 time-to-barrier ordering decision surface regeneration over the standard periods was not performed in this packet.
- Sample coverage remains sparse and side-imbalanced: this is learning evidence, not completion evidence.

## Allowed claims
- runtime_learning_probe_decision_recorded
- f90_repair_attempt_recorded
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
If F90 is revisited, regenerate the `ridge_signed_speed_alpha10` surface over the full standard validation_is and oos windows before requesting runtime_probe_completed.

## Metrics Snapshot
```json
{
  "validation_is": {
    "net_profit": 289.13,
    "profit_factor": 1.7,
    "max_drawdown_percent": 95.68,
    "trade_count": 47,
    "gross_profit": 699.27,
    "gross_loss": -410.14,
    "win_rate_percent": 38.3,
    "expectancy": 6.15,
    "recovery_factor": 0.46,
    "long_trade_count": 28,
    "short_trade_count": 19
  },
  "oos": {
    "net_profit": 254.9,
    "profit_factor": 1.66,
    "max_drawdown_percent": 85.64,
    "trade_count": 39,
    "gross_profit": 639.02,
    "gross_loss": -384.12,
    "win_rate_percent": 53.85,
    "expectancy": 6.54,
    "recovery_factor": 0.55,
    "long_trade_count": 23,
    "short_trade_count": 16
  }
}
```
