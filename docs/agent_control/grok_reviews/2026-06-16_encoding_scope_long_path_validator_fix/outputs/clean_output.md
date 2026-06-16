## Grok Review — F67B encoding-scope long-path failure

**Review size:** medium (bounded snapshot + one focused design question)
**Claim boundary:** I am not verifying `io_path` API surface, test harness, or other validator call sites. Classifications below are from the snapshot only.

---

### Executive verdict

The fix direction is **sound and aligned** with the project’s Windows long-path rule: one API can read while another says “missing.” Patching `check_encoding_scope` to use `io_path` for existence/read-sensitive checks is an **accepted candidate**, not a gate/threshold relaxation.

The main gap is **scope**: fixing one function without a **validator-wide long-path policy** risks the same failure on the next deep `stages/*` artifact.

---

### Accepted candidates (수용 후보)

| # | Recommendation | Rationale |
|---|----------------|-----------|
| A1 | Route **file-scope** existence through `io_path(...).is_file()` (or equivalent long-path-safe helper) before any encoding read | Matches observed failure mode: `io_path` reads + BOM confirmed while `path.exists()` / `path.is_file()` fail. |
| A2 | Keep **repo-relative paths** in errors, reports, and CLI args; use `io_path` only as execution helper | Preserves durable artifact identity per architecture invariants; avoids `\\?\` leaking into document identity. |
| A3 | **Directory scopes:** long-path-safe existence first, then traversal | Snapshot already flags dir vs file risk; existence-first ordering avoids “dir missing” false negatives before `rglob()`. |
| A4 | Add a **regression test** that exercises the long-path-safe code path | Without it, Windows MAX_PATH regressions will recur silently on the next frontier stage. |
| A5 | Treat this as **infrastructure parity**, not encoding-rule relaxation | BOM/UTF-8 rules stay strict; only path resolution changes. |

**A4 detail (accepted with constraint):** Prefer a test that **forces** ordinary `Path.exists()` → False while the helper still resolves the file (mock/monkeypatch or a fixture at/near MAX_PATH). A test that only passes on short paths does not prove the fix.

---

### Needs local verification (로컬 검증 필요)

| # | Item | Why Codex must verify locally |
|---|------|-------------------------------|
| V1 | **`io_path` API coverage** for everything `check_encoding_scope` uses today (`exists`, `is_file`, `rglob`, open/read, iterdir) | Risk in snapshot: `io_path` may not mirror full `Path` API; partial adoption could leave `rglob()` broken on deep trees. |
| V2 | **Directory traversal strategy** if `io_path` has no `rglob` | Options: `rg --files` preflight (project rule), extended-path wrapper around `rglob`, or narrow scope to explicit file list for encoding checks. Pick one after reading `io_path` implementation. |
| V3 | **Other validator entry points** using raw `Path.exists()` / `is_file()` / `rglob()` on user-supplied scope paths | Fixing only `check_encoding_scope` may not stop recurrence; audit `validate_agent_settings.py` (and siblings) for the same pattern. |
| V4 | **False-negative guard:** ensure `io_path` success cannot mask truly missing paths (typo, wrong repo root, deleted file) | Broad swap without “missing stays missing” tests could hide real gaps. |
| V5 | **F67B report path** as concrete regression fixture | Confirm post-patch: `--encoding-scope <that repo-relative path>` passes BOM check and emits repo-relative identity in output. |

---

### Rejected (거절)

| # | Proposal | Reason |
|---|----------|--------|
| R1 | Skip encoding-scope validation for paths over N characters | Weakens gate; treats symptom as policy exception. |
| R2 | Document identity or errors using `\\?\` extended prefixes | Conflicts with project rule: extended prefix as local helper only. |
| R3 | “If `exists()` fails, assume OK if file is in git status” | Git presence ≠ filesystem accessibility; wrong trust model. |
| R4 | Repo-wide `Path` → `io_path` blind replace in one change | High risk of hiding true missing files and unrelated regressions; too broad for this packet. |
| R5 | Lower claim boundary (“encoding gate blocked by Windows, inconclusive OK”) without fixing validator | External verification anti-deferral: fix tool or record `blocked` with repair plan, don’t normalize the failure. |

---

### Critique of the proposed design (focused)

**What works**

- Failure is **classical Win32 MAX_PATH split-brain**: enumerate/read succeeds via one helper, stdlib `pathlib` fails. That is exactly what the project’s long-path rule describes.
- Scoping the patch to **read-sensitive checks** in `check_encoding_scope` is proportionate: encoding validation is I/O-bound, not a semantic gate change.
- Regression test requirement is non-negotiable for **future stages**; deep `stages/stage_frontier_*` paths will keep growing.

**What is underspecified**

1. **`rglob()` on directory scopes** — likely the next failure after `exists()` is fixed. The design says “long-path safe traversal if available” but does not name the mechanism. Codex should verify whether `io_path` exposes recursive walk or whether encoding-scope for directories should delegate to `rg --files` + per-file `io_path` open (consistent with Agents.md preflight).
2. **Single-function vs validator policy** — recurrence prevention needs a **documented rule**: “user-supplied repo-relative paths in agent settings validation MUST go through `io_path` (or ledger I/O layer) for existence and read.” One function fix fixes F67B; policy fixes frontier 68+.
3. **Error messaging** — when long-path helper succeeds but stdlib path fails, errors should not imply “file does not exist”; prefer “resolved via io_path” internally while user-facing text stays repo-relative. Avoid confusing “missing” with “unreachable by pathlib.”

---

### Recurrence prevention (future stages)

To stop this class of bug from coming back:

1. **Centralize** repo-relative path resolution for validators: thin `resolve_repo_path(scope_path) -> io_path` used by all scope checks.
2. **Regression matrix:** (a) mocked `exists=False` + readable file, (b) real deep path under `stages/.../03_reviews/` if feasible, (c) directory scope with nested UTF-8 BOM `.md`.
3. **Preflight in skill/docs** for `obsidian-architecture-guard`: encoding-scope examples must use repo-relative paths; note that validators use `io_path`, not raw `Path.exists()`.
4. **Optional follow-up (V3):** grep validators/control_plane for `.exists()` on stage-scoped paths — same bug class, different command.

---

### Classification summary

| Proposed element | Classification |
|------------------|----------------|
| `check_encoding_scope` uses `io_path` for file existence/read | **Accepted candidate** |
| Repo-relative identity in errors/reports | **Accepted candidate** |
| Dir: existence via helper, then safe traversal | **Accepted candidate** (traversal mechanism **needs local verification**) |
| No relaxation of encoding/gate/threshold/claim | **Accepted candidate** |
| Regression test for pathlib-fail / helper-success | **Accepted candidate** |
| Full `io_path` API assumption without reading implementation | **Needs local verification** |
| Fix only this function, no validator audit | **Needs local verification** (likely insufficient for recurrence) |
| Skip validation / extended path in docs / git-based waiver | **Rejected** |

---

### Recommended Codex next steps (for local owner, not Grok)

1. Read `foundation.control_plane.ledger.io_path` and list APIs used by `check_encoding_scope`.
2. Implement minimal patch: file scope via `io_path`; dir scope via verified traversal strategy.
3. Add regression test per A4.
4. Re-run `--encoding-scope` on the F67B report path (V5).
5. Short audit of `validate_agent_settings.py` for duplicate `Path.exists()` patterns (V3).

**Bottom line:** Accept the fix **direction**; do not accept “done” until traversal strategy, test realism, and validator-wide policy are locally verified. That trio is what prevents recurrence in future frontier stages, not a one-line `exists()` swap alone.
