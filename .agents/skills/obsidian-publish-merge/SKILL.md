﻿---
name: obsidian-publish-merge
description: Finish Project Obsidian Prime v2 work by pushing the working branch and merging into main in one safe pass when the user explicitly asks for it or when a verified implementation pass finishes with tracked changes and no publish opt-out.
---

# Obsidian Publish Merge

Use this skill when the user explicitly asks for branch push plus `main` merge completion in the same pass, or when a verified implementation pass finishes with tracked changes and the user has not asked to keep the work branch-only.

## Trigger Phrases

- `브랜치랑 메인머지까지`
- `메인까지 올려줘`
- equivalent explicit wording that asks for push plus `main` completion

## Default Auto Trigger

Also trigger by default when all of the following are true:

- the current pass materially changed tracked files
- the requested implementation work is complete enough to close the turn
- the relevant verification for the touched surface finished successfully
- the user did not ask to stop at analysis, branch push, or PR-only state
- the working tree is clean enough for a safe publish flow

## Required Flow

1. Confirm the intended work scope from the current thread and repository status.
2. Make sure the requested implementation work is finished before starting the publish flow.
3. Stage only the intended files.
4. Commit with a scope-matching message.
5. Run the narrowest sufficient verification for the touched surface.
6. Push the working branch first.
7. Fetch the latest remote `main`.
8. Merge into local `main` only after the branch is ready and the working tree is clean.
9. Push `origin/main` in the same pass when the merge is clean.

## Safety Rules

- Do not merge into `main` when the user only asked for a branch push or a draft PR.
- Do not auto-merge into `main` for analysis-only, question-only, or partial-progress turns.
- Do not merge into `main` from a dirty working tree.
- Do not force-push `main`.
- If remote `main` moved and a clean fast-forward is impossible, stop and explain whether rebase, merge, or conflict resolution is needed.
- If the branch contains unrelated changes, stop and surface the mixed scope before merging.

## Verification

- Re-run the most relevant local verification after any final merge-preparation change.
- If the change touches MT5 execution, runtime parity, tester orchestration, or another environment-dependent path, follow the verification escalation rule from `docs/policies/agent_trigger_policy.md`.
