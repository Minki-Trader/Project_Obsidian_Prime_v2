# Branch Policy

Use `codex/` branches for agent work unless the user asks for another branch name.

Do not merge to `main` unless the user explicitly asks.

## Worktree Fit Rule

Before editing files, confirm that the current branch or worktree matches the requested work packet.

If the current branch is scoped to a different stage, PR, experiment, or governance task, do not keep working there just because it is already open. Switch to the matching branch/worktree, create a new `codex/` branch from the correct base, or stop and report the mismatch when switching would risk losing unrelated work.

Examples:

- Do not continue Stage 10 implementation on a Stage 09 handoff branch.
- Do not patch governance files on a stage-run code branch unless the user explicitly wants that PR to carry governance changes.
- Do not mix two open PR scopes in one worktree unless the user explicitly asks to combine them.

Effect: branch names and worktree state stay aligned with the actual task, so later PRs and local Codex handoffs do not inherit hidden cross-stage edits.
