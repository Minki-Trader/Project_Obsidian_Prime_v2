---
name: obsidian-runtime-parity
description: Check that Python research, packaged artifacts, MT5 EA behavior, Strategy Tester behavior, and live-like runtime handoff carry the same meaning before runtime claims are made.
---

# Obsidian Runtime Parity

Use this skill when work touches MT5, EA modules, runtime packages, model bundles, `.set` files, tester output, handoff files, live-like execution, or comparisons between Python and runtime behavior.

## Required Output

- `research_path`: Python script, model builder, feature calculator, or report path
- `runtime_path`: MT5 EA, include module, package, `.set`, tester profile, or handoff path
- `shared_contract`: features, labels, inputs, outputs, thresholds, and time-axis rules that must match
- `known_differences`: differences that are intentional or unresolved
- `parity_check`: compile, snapshot, file handoff, tester output, row-level comparison, or reason unavailable
- `parity_identity`: module hashes, bundle hash, parameter hash, tester identity, and output path when applicable
- `runtime_claim_boundary`: research-only, runtime_probe, runtime_authority_candidate, blocked, or not_applicable

## Guardrails

- Do not treat Python success as runtime authority.
- Do not treat MetaEditor compile as a substitute for tester or runtime output.
- Do not change EA entrypoints for parameter-only experiments.
- Do not hide runtime differences in file names; record identities and hashes.
