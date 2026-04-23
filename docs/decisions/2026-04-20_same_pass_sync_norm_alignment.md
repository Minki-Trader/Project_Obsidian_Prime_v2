# 2026-04-20 Same-Pass Sync Norm Alignment

## Status

- decided_on: `2026-04-20`
- stage: `05_exploration_kernel_freeze`
- decision_type: `policy-skill-reporter synchronization discipline alignment`

## Decision

- set `docs/policies/agent_trigger_policy.md` as the canonical same-pass synchronization norm source for stage-level durable meaning changes
- explicitly include `docs/registers/artifact_registry.csv` in the same-pass required list when dataset, bundle, runtime, or report identity rows are added or superseded
- align `.agents/skills/obsidian-stage-transition/SKILL.md` to that canonical norm
- reduce runtime parity reporter `gate_before_closure` wording to a policy-link anchor plus short summary instead of repeating policy text inline

## Why

- the same-pass requirement had begun to drift between policy, skill text, and runtime-report guidance
- keeping one canonical norm source lowers maintenance overhead and avoids conflicting operator interpretation
- `artifact_registry.csv` already carries durable identity closure evidence, so its same-pass handling needs to be explicit in the canonical norm
- the reporter should reinforce policy routing without becoming a second policy source

## Consequences

- future stage-transition or closure-read edits should update the policy first, then inherit wording from that policy in skills/reports
- same-pass closure gating now consistently includes identity-register updates when identity rows change
- runtime parity report follow-up guidance now references policy directly, reducing repeated prose drift risk
