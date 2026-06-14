**1. verdict:** `accepted`

**2. required_guardrail:** Source ranking must use only a **pre-declared, frozen train-only trade-shape metric set** that is **entry-known and closed-bar computable** at selection time; no metric that needs forward/OOS labels, post-entry path, or a post-hoc metric add/reweight after seeing validation/OOS forward results may enter ranking.

**3. do_not_repeat:** Do **not** treat F42 timing gates, the F42 best `session_morning` row, or its near-scout `forward_min_pf ~1.055` as inherited mask/winner/baseline or as reason to reopen **timing** or **session-clock** as the primary lever—even if trade-shape ranking surfaces session-like pockets.

**4. claim_boundary_ok:** `yes`
