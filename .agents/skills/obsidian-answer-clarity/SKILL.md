---
name: obsidian-answer-clarity
description: Explain Project Obsidian Prime v2 work in plain, beginner-readable language without shrinking the substance. Use when writing user-facing answers, summaries, reviews, PR explanations, decision notes, or status updates that contain project terms, trading terms, engineering terms, or agent-policy terms.
---

# Obsidian Answer Clarity

Use this skill whenever the answer is meant for the user, not only for another engineer.

## Purpose

Make the answer easy enough for a non-developer and trading non-specialist to follow, while keeping the full meaning.

Do not treat Korean parallel notation as explanation by itself. A term like `runtime_authority(런타임 권위)` still needs a plain meaning.

## Required Behavior

1. When using a specialist term, add the simple meaning near it.
2. Explain why the point matters.
3. Explain the effect on the project or the next decision.
4. Separate what is true now from what is not yet true.
5. Keep the answer complete; do not make it short by removing important reasoning.
6. Use a simple analogy when it makes the idea easier, but do not let the analogy replace the actual project meaning.
7. When explaining a finding, say:
   - what is wrong
   - why it can hurt the project
   - what a safe fix does

## Preferred Shape

- Start with the plain answer.
- Then unpack the project meaning.
- Then name the practical effect.
- Then list the exact file, PR, run, stage, or artifact when needed.

## Do Not

- Do not answer with term pairs only, such as `runtime authority(런타임 권위)`, without a plain explanation.
- Do not hide uncertainty behind formal wording.
- Do not use a defensive phrase like "noted for future work" unless the missing work, blocker, and next condition are clear.
- Do not over-compress the answer when the user is asking for understanding.

## Example Standard

Instead of:

`runtime_authority` is not closed.

Write:

`runtime_authority(런타임 권위)` is not closed. Plainly, this means the project has not yet proven that the live or MT5 runtime path can be trusted as an operating handoff. The effect is that we can still use the current artifact for research planning, but we should not describe it as ready for live-like operation.
