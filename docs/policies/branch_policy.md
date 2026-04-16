# Branch Policy

- create a branch only after a stage brief or equivalent spec exists
- use the prefix `codex/` unless there is a strong reason not to
- make the branch purpose visible in the name
- keep diagnostic work and operating-candidate work easy to distinguish
- when a branch closes, update:
  - `docs/workspace/workspace_state.yaml`
  - the active stage `03_reviews/review_index.md`
  - the active stage `04_selected/selection_status.md`
  - a durable decision memo when the branch changes operating meaning
- do not leave the final conclusion only in PR comments, terminal logs, or scratch notes
