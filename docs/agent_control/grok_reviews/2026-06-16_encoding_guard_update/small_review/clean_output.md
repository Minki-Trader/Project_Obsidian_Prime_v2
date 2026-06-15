Proposed encoding guard rules need a quick pass against existing project policy and the Grok wrapper — I'll read those sources first.
**Verdict: accepted** (with two small wording additions)

The rule is acceptable. It targets **environment/reproducibility discipline(환경·재현성 규율)**, not gate thresholds or evidence standards — so it does not weaken gates.

**Why it fits**
- `PYTHONIOENCODING=utf-8` directly addresses the observed Windows `cp949` `UnicodeEncodeError` on stdout.
- Prompt files align with existing `grok_review_wrapper` (`--prompt-file`, UTF-8 writes) and avoid PowerShell here-string fidelity loss.
- Mojibake → encoding-repair → `py_compile` → artifact inspect is a sensible repair loop; precedent exists (Stage11 mojibake recovery in changelog).
- Long-path is already covered; no overlap conflict.

**Concise wording to add**

1. **Scope boundary(범위 경계)** — one line in AGENTS.md:
   > Console/shell encoding guards apply to agent execution only; they do not relax gates, thresholds, or evidence requirements.

2. **Verification recipe(검증 절차)** — in reproducibility skill, pair with long-path guard:
   > After Korean template rewrite, re-read via `foundation.control_plane.ledger.io_path` with `utf-8-sig`; do not trust native PowerShell `Get-Content` alone for fidelity check.

3. **PowerShell form(파워셸 형식)** — since shell is PowerShell:
   > `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONPATH='.'`

4. **BOM tie-in(BOM 연계)** — cross-reference existing rule:
   > Repaired Korean `.md`/`.txt` must remain UTF-8 with BOM.

**needs_local_verification (optional, not blocking)**
- Whether wrapper should set `PYTHONIOENCODING` internally so agents cannot forget — one trial on the failing Grok command path would confirm, but the proposed agent-side rule is sufficient to adopt now.
