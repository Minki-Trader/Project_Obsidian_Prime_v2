Grok 협업 스킬과 현재 거버넌스 스캐폴드를 읽어, 요청하신 bounded review(제한 검토)에 맞춰 검토합니다.
## Grok Small Review — Frontier Governance Foundation

**Verdict:** **Sufficient for governance-scaffold closeout** — with two small doc additions recommended, not blocking.

**Plain meaning:** The scaffold does what it should: it breaks Stage365 continuation, locks in “reference, not inheritance,” and gives `stage_frontier_01` a real opening contract. Codex can mark the governance foundation complete after capturing this review and optional micro-fixes.

**Claim boundary honored:** No model training, MT5 run, candidate selection, baseline, operating promotion, runtime authority, live readiness, or Goal Achieve implied.

---

### Benefits of Current Setup

| Benefit | Effect |
|--------|--------|
| **Breaks numeric continuation** | `stage_frontier_NN` signals a new campaign, not “Stage365 after 364.” |
| **Single policy source of truth** | `frontier_governance.md` centralizes charter, repair, closeout, forbidden imports. |
| **Reuses proven stage anatomy** | `00_spec`–`04_selected` keeps ledgers, re-entry, and selection_status patterns working. |
| **Opening contract is live** | `stage_brief.md` already has thesis, novelty delta, exit rule, claim boundary. |
| **Archive interface started** | `prior_stage_scan.md` cites registers, Stage364 closeout, prior Grok review — not vague “reviewed archive.” |
| **Repair anti-sprawl default** | Repair as subordinate work packets avoids opening a new frontier for every adapter fix. |
| **State sync is honest** | `workspace_state.yaml` and `selection_status.md` show `not_claimed` on all authority fields. |
| **Re-entry wired** | `reentry_order.md` now reads frontier governance during cold start. |

**Classification:** **accepted**

---

### Failure Modes Still Present

1. **Cosmetic rename** — IDs change but behavior still treats preserved clues as implicit baselines.
2. **Archive amnesia** — `prior_stage_scan.md` is still a skeleton; campaign map / DNR list not written yet (expected for `frontier_01` work, not this closeout).
3. **Decision-weight vagueness** — policy names decision weight but has no checklist/rubric; closeout could become prose instead of judgment.
4. **Repair laundering** — subordinate repair packets without `broken_artifact` + `repair_boundary` fields can loop under the same frontier ID.
5. **Frontier micro-sprawl** — if novelty-less repair loop trigger is ignored, `frontier_02`, `frontier_03` reopen for the same axis.
6. **Pipeline discovery gap** — `architecture_invariants.md` assumes `stage_pipelines/stageXX` numeric discovery; first frontier with custom orchestration may hit regex/import friction.
7. **Identity ambiguity** — `workspace_state.yaml` uses `current_stage_id` for a frontier; minor but can blur “archive stage” vs “active frontier.”

**Classification:** **needs_local_verification** for items 3, 4, 6 at first real experiment/repair packet; others are watch items, not scaffold blockers.

---

### Minimum Local Fixes Before Closeout

**Blocking:** none.

**Recommended (5–15 lines total):**

1. **Decision-weight checklist** in `frontier_governance.md` — e.g. thesis resolved / novelty tested / negative memory added / external verification attempted / repair-to-exploration ratio noted.
2. **Repair packet minimum fields** in Repair Rule — `broken_artifact`, `repair_boundary`, `novelty_check`, `exit_or_escalate`.
3. **Optional one-liner** in `architecture_invariants.md`: `stage_frontier_*` lives under `stages/*` as stage-local artifacts.

**Not required for this closeout:** campaign map, DNR list, `active_frontier_id` rename, separate `repair_frontier` lane.

**Classification:** checklist + repair fields → **accepted**; pipeline discovery → **needs_local_verification** when first frontier pipeline is needed.

---

### `stages/` Path — Acceptable?

**Yes — preferred over `frontiers/` or `stages_frontier/`.**

- `architecture_invariants.md` already owns `stages/*` for stage-local artifacts.
- Prior Grok/local verification (2026-06-12) rejected a parallel `stages_frontier/` root because it would split routing, ledgers, re-entry, and audits without an `active_stage_root` contract.
- Keeping `stages/stage_frontier_NN__specific_question/` preserves lineage to `alpha_run_ledger.csv`, `stage_run_ledger.csv`, and `04_selected/selection_status.md`.
- Prefix `stage_frontier_` is enough to distinguish archive numeric stages from active frontier campaigns in sorting and grep.

**Only caveat:** when a frontier needs `stage_pipelines`, define naming (`stage_pipelines/stage_frontier_01/` or stay parameter-only) before first orchestration — not a governance-scaffold blocker.

**Classification:** **accepted**

---

### Repair: Subordinate Packets vs Separate Frontier Lane?

**Keep subordinate work packets as default. Do not open a separate `repair_frontier` lane now.**

| Approach | Why |
|----------|-----|
| **Subordinate packets (current)** | Matches repair-heavy history (adapter_repair, dense cost recovery); avoids 1–2 run repair micro-frontiers; escalation already defined (source/label/runtime/validation change, exit_rule, novelty-less loop). |
| **Separate repair frontier lane (prior Grok option)** | Useful only if repair volume keeps spawning new frontier IDs despite the subordinate default — not needed at foundation time. |

**Strengthen the default:** require repair packets to declare what is broken, what boundary applies, and whether novelty exists — otherwise escalate to new frontier per existing trigger #3.

**Classification:** subordinate default → **accepted**; separate repair lane now → **rejected**; repair packet contract fields → **accepted**

---

### Advice Classification Summary

| Item | Classification |
|------|----------------|
| Governance scaffold sufficient for closeout | **accepted** |
| `reference, not inheritance` + forbidden imports | **accepted** |
| Opening contract fields in policy + `stage_brief` | **accepted** |
| Frontier folders under `stages/` | **accepted** |
| Repair as subordinate work packets by default | **accepted** |
| Separate `repair_frontier` lane at foundation time | **rejected** |
| Add decision-weight checklist | **accepted** |
| Add repair packet minimum fields | **accepted** |
| `stage_pipelines` naming for frontier orchestration | **needs_local_verification** |
| Campaign map / full DNR (frontier_01 execution) | **needs_local_verification** — out of scope for governance-only closeout |

**Forbidden claim check:** pass — no authority, baseline, or Goal Achieve recommended.

---

### Bottom Line for Codex

Mark **governance foundation scaffolded** after:
1. Capturing this review in `docs/agent_control/grok_reviews/2026-06-13_frontier_foundation_setup/`
2. Optionally adding the decision-weight checklist and repair packet fields
3. Running local gates (`state_sync_audit`, `final_claim_guard`)

Do **not** wait for campaign map, experiment runs, or `active_frontier_id` rename to close this packet. Those belong to `frontier_01` execution, not the governance stub.

**Suggested Codex claim (low boundary):** `governance_foundation_scaffolded` + `grok_review_captured` + `no_authority_claimed`.
