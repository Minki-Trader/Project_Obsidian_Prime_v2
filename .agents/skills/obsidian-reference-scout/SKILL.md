---
name: obsidian-reference-scout
description: Find and use external references for correct API usage, syntax, implementation patterns, MQL5 behavior, library behavior, quant methods, and idea scouting. Use when project memory is not enough, an API may be version-sensitive, or alpha/research ideas need external examples.
---

# Obsidian Reference Scout

Use this skill when outside references can improve correctness or idea quality.

This skill is for scouting and grounding, not copying.

## When To Use

- correct function, API, or syntax usage is uncertain
- library behavior may depend on version
- MQL5 or MT5 tester behavior is unclear
- LightGBM, pandas, sklearn, numpy, or another library usage needs confirmation
- implementation patterns from maintained GitHub projects may help
- alpha exploration is stuck and outside examples may suggest new ideas
- forum posts may reveal practical edge cases

## Source Priority

1. Official documentation or vendor docs.
2. Maintained source repository, examples, release notes, or issue discussions.
3. Well-scoped GitHub examples with readable code and recent maintenance.
4. Forum or community posts, including MQL5 forum, only as idea candidates or practical warnings.

## Required Output

- `question`: what usage, idea, or pattern was researched
- `sources_checked`: which sources were checked
- `source_quality`: official, maintained code, example, issue, forum, or weak
- `found_pattern`: the useful pattern or warning
- `project_fit`: how it fits or conflicts with this repo's contracts
- `do_not_copy`: what should not be copied directly
- `recommended_use`: adopt, adapt, treat as idea, or reject

## Guardrails

- Prefer official docs for API and syntax questions.
- Do not copy external code wholesale into this repo.
- Do not trust forum performance claims as evidence.
- Do not let external examples override project contracts for time axis, dataset identity, split policy, artifact identity, or runtime authority.
- If a source is old, version-specific, or unclear, say so.
- If browsing or source lookup was not performed, do not present the answer as externally verified.

## Example

If MQL5 file handoff behavior is unclear, scout official MQL5 docs first, then relevant forum or GitHub examples. The useful result might be a pattern such as waiting for file size stability, but the implementation still needs to fit this project's runtime parity and artifact identity rules.
