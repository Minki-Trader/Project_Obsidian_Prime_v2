# ADR-0001 Contract Fidelity Before Built-In Convenience

## Status

- `accepted`

## Context

The legacy project showed that MT5 built-in ATR and Stochastic paths were convenient but not contract-equivalent on the audited runtime surface. That mismatch distorted feature parity and later decision quality interpretation.

## Decision

For v2, model-input and helper/runtime paths must follow the written contract first. Platform built-ins may still be used as helpers or comparison lanes, but they do not become the default truth unless they have already passed contract-equivalence checks on the relevant surface.

## Consequences

- good:
  - parity debugging becomes clearer
  - alpha interpretation is less likely to be polluted by hidden runtime drift
  - contract docs stay meaningful
- trade-offs:
  - custom feature implementations may be slower to build than using platform helpers
  - more fixture and parity work is required up front
- follow-up:
  - define the first v2 parity harness scope
  - record any future built-in equivalence approvals explicitly

## Related Docs

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/decisions/2026-04-16_v2_restart_decision.md`
