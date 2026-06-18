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
- `runtime_evidence_identity`: dataset_id, feature_set_id, label_id, split_id, ONNX hash, EA source/binary hash, set/ini hash, feature_order_hash, tester identity, report/trade-list/telemetry hash(데이터셋 ID/피처 묶음 ID/라벨 ID/분할 ID/온엑스 해시/EA 원천·실행파일 해시/설정 해시/피처 순서 해시/테스터 정체성/보고서·거래목록·텔레메트리 해시)
- `runtime_claim_boundary`: research-only, runtime_probe, runtime_authority_candidate, blocked, or not_applicable

## Guardrails

- Do not treat Python success as runtime authority.
- Do not treat MetaEditor compile as a substitute for tester or runtime output.
- When runtime/materialization/handoff/economics claims(런타임/물질화/인계/경제성 주장) are protected, prefer the narrow sufficient runtime_probe(좁고 충분한 런타임 탐침) over procedural expansion/advisory loops/deferred checkpoints(절차 확장/자문 반복/지연 점검).
- Do not skip runtime_probe(런타임 탐침) because it is costly/expensive(비용이 듦). Attempt it in the same packet(같은 묶음), or after a recovery attempt(복구 시도) lower `runtime_claim_boundary(런타임 주장 경계)` to blocked, inconclusive, or out_of_scope_by_claim(차단/불충분/주장 범위 밖).
- Do not change EA entrypoints for parameter-only experiments.
- Do not hide runtime differences in file names; record identities and hashes.
- On Windows deep stage/MT5 artifact paths, do not classify a native PowerShell/Python path failure as parity failure, missing evidence, invalid setup, or blocked until repo-relative `rg --files`/`rg` has been attempted; when content or mechanical CSV/JSON reads are needed, retry through `foundation.control_plane.ledger.io_path` and record the retry outcome before judging.
- If PowerShell `Import-Csv`, `Measure-Object`, or recursive `Get-ChildItem` reports `Could not find a part of the path` on a known-deep frontier artifact, stop repeating that cmdlet; use `cmd /c dir /x` only to discover a local 8.3 short path, or read through `foundation.control_plane.ledger.io_path` in Python, while preserving repo-relative paths in reports.
