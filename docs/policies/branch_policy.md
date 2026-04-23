# Branch Policy

- create a branch only after a stage brief or equivalent spec exists
- when a tracked implementation pass is materially bounded, prefer one approved task packet per branch
- keep `main` as the current truth anchor; branches are proposal or implementation surfaces and do not replace workspace truth by themselves
- use the prefix `codex/` unless there is a strong reason not to
- make the branch purpose visible in the name
- avoid generic names that hide intent
- keep diagnostic work and operating-candidate work easy to distinguish
- if a branch or PR stays ahead and behind `main`, resolve it explicitly as `merge`, `re-cut-needed`, `superseded`, or `archived` before opening the same intent again
- do not let stale or superseded branch conclusions live only in PR comments or scratch notes
- when a branch closes, update:
  - `docs/workspace/workspace_state.yaml`
  - the active stage `03_reviews/review_index.md`
  - the active stage `04_selected/selection_status.md`
  - a durable decision memo when the branch changes operating meaning
- do not leave the final conclusion only in PR comments, terminal logs, or scratch notes
