# F87 Runtime Learning Probe Backfill Closeout

## Conclusion
F87 was repaired into a source_replay runtime learning observation only. The repaired surface uses an inner_validation-only threshold of `0.6552855227236055` and does not use OOS to choose the threshold.

## Guardrail
- OOS already reaches 2026-04-13, so no 2026-06 extension is required.
- The ONNX wrapper is a repair artifact, not a learned F87 model artifact.
- runtime_probe_completed, runtime authority, economics pass, materialization-ready, and handoff complete remain forbidden.

## Metrics Snapshot
```json
{
  "validation_is": {
    "status": "completed",
    "net_profit": -515.36,
    "profit_factor": 0.26,
    "max_drawdown_percent": 102.59,
    "trade_count": 11,
    "deal_count": 22,
    "win_rate_percent": 45.45,
    "long_trade_count": 11,
    "short_trade_count": 0,
    "gross_profit": 181.7,
    "gross_loss": -697.06,
    "expectancy": -46.85,
    "recovery_factor": -0.85
  },
  "oos": {
    "status": "completed",
    "net_profit": 12.89,
    "profit_factor": 1.04,
    "max_drawdown_percent": 56.77,
    "trade_count": 31,
    "deal_count": 62,
    "win_rate_percent": 41.94,
    "long_trade_count": 31,
    "short_trade_count": 0,
    "gross_profit": 380.76,
    "gross_loss": -367.87,
    "expectancy": 0.42,
    "recovery_factor": 0.04
  }
}
```
