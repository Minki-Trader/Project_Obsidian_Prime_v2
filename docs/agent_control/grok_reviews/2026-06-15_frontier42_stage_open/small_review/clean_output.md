## Grok review (external second opinion only)

**1. verdict:** `accepted`

**2. novelty_ok:** `yes`

**3. leakage_guard_ok:** `needs_local_verification`

**4. runtime_claim_boundary_ok:** `yes`

**5. mandatory guardrails (max 3)**

1. **Timing sweep budget** — Cap the number of timing-gate combinations (broad NY buckets + first/last 30m + diagnostic hour/DOW family). Log attempt count. A row may advance only if it passes the **train-positive lane** first; best forward score alone must not select gates.
2. **Frozen entry-source lock** — The 12 F41 short entry masks are reference-only clues. Any same-entry/source mutation aborts the stage packet and downgrades claims to invalid exploration.
3. **Exit stays finite and subordinate** — Hold 4/6/8/12 plus train-only MFE/MAE quantile stops remain the only exit family. Timing is the primary lever; exit shape must not become a disguised second search axis.

**6. do-not-repeat note (max 3)**

1. Do not treat **exit-shape-only DD compression** as progress if train PF does not stay on a positive track (F41 negative memory).
2. Do not inherit F41’s best observed row (`f40b_0013` … hold04) as an implicit baseline, winner, or promotion anchor for F42 selection.
3. Do not expand into **new feature-threshold mining** or unbounded broker-clock diagnostics under the timing-pivot label; that would be a disguised repair loop, not this stage’s hypothesis.

---

**Rationale (brief):** After F41’s `preserved_clue_negative_memory` — exit shape alone, 94 scout clues, 0 seed/runtime — pivoting to **entry-known session timing contamination** on the same frozen masks is a distinct axis, not another exit-shape repair loop. Claim boundary and tiered success criteria (scout / seed / runtime probe) are appropriately weak. `leakage_guard_ok` stays `needs_local_verification` because bounded evidence does not yet specify sweep cardinality, train-gated selection protocol, or whether the capped diagnostic hour/DOW family stays strictly entry-known at replay time — Codex must verify those locally before strong scout/seed/runtime claims.
