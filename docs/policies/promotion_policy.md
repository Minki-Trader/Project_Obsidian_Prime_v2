# Promotion Policy

- diagnostic evidence can justify a follow-up, but cannot by itself replace the operating line
- `promotion_candidate` (`승격 후보`) may be opened for bounded comparison before every operating gate is closed, as long as the evidence boundary and missing gates are labeled
- `operating_promotion` (`운영 승격`) means incumbent replacement or confirmation and requires:
  - a clear inherited reference
  - primary KPI and guardrail reads
  - a current `selection_status.md`
  - a durable decision memo
- if a new telemetry field is part of the promotion story, the incumbent/reference family must be backfilled first
- handoff verification and runtime parity closure are separate approval gates
- if the candidate depends on a contract-aligned runtime lane, parity status must be stated explicitly
- `runtime_probe` (`런타임 탐침`) may observe runtime behavior without claiming runtime parity closure
- `runtime_authority` (`런타임 권위`) means runtime parity closure, bundle handoff authority, or live-like readiness and requires the relevant hard-gate evidence
- when the evidence is useful but not promotion-worthy, close with an explicit `no promotion` read instead of leaving ambiguity
- `promotion-ineligible` does not mean `idea-dead`; exploration closure requires negative-result memory, salvage value, and reopen condition
- Tier B and Tier C local research may inform future exploration, but they do not become promotion arguments unless a later promotion packet explicitly opens the required gates
