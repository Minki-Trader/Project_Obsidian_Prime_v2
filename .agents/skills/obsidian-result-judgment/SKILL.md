---
name: obsidian-result-judgment
description: Judge project results with the correct boundary before claiming positive, negative, invalid, blocked, promotion candidate, operating promotion, runtime probe, or runtime authority.
---

# Obsidian Result Judgment

Use this skill when a result, run, experiment, model, package, backtest, PR, or stage outcome is interpreted for the user or written into a register.

## Must Read

- `docs/policies/result_judgment_policy.md`
- `docs/policies/promotion_policy.md`
- `docs/policies/run_result_management.md` when run status changes
- `docs/policies/kpi_measurement_standard.md` when KPI is involved

## Required Output

- `result_subject`: what is being judged
- `evidence_available`: KPI, report, artifact, registry row, test, backtest, or runtime output
- `evidence_missing`: what is absent or weak
- `judgment_label`: positive, negative, invalid, inconclusive, blocked, exploratory, promotion_candidate, operating_promotion, runtime_probe, runtime_authority, or not_applicable
- `claim_boundary`: what can be said now and what cannot
- `next_condition`: smallest condition that could strengthen, weaken, or close the judgment
- `user_explanation_hook`: plain-language meaning for `obsidian-answer-clarity`

## Guardrails

- Do not call a result positive only because a script ran.
- Do not call a result negative when the run is invalid or missing evidence.
- Do not turn promotion_candidate into operating_promotion.
- Do not turn runtime_probe into runtime_authority.
- Pair final user-facing judgment with `obsidian-claim-discipline` and `obsidian-answer-clarity`.
