## Frontier60 closeout review

### 1. verdict
**accepted**

Codex closeout is consistent with the bounded evidence. Proxy already showed weak OOS PF and sub-target density; MT5 probe completed without parity blocker and confirmed PF failure. `negative_memory` is the right label, not `blocked` or `invalid_setup`.

### 2. closeout_label
**negative_memory**

Long-axis friction escape via admission cadence did not restore PF or density. Narrow DD observation may be preserved as clue only, not as escape success.

### 3. must_record

**Mandatory failure memory**
- **F60 long-axis friction escape failed on PF**: fixed F59 long-quality + entry-transition / close-on-flat / cooldown did not restore profitability.
- **Proxy pre-MT5 was already weak**: OOS PF 0.9961 (&lt;1), density ~2.8/day (below 5–10/day); validation PF 1.0182 with DD 5.66%.
- **MT5 probe worsened PF**: validation PF 0.41, DD 14.89%, 3.61 trades/day; OOS PF 0.51, DD 8.48%, 3.77 trades/day.
- **Cadence worked as designed, not as alpha**: `feature_ready_diff=0`; `signal_diff` matched `entry_policy_suppression_count` (1501 val / 1159 OOS) — expected entry-transition suppression, not feature mismatch.
- **Density target missed end-to-end**: ~3.6–3.8/day in MT5; never reached 5–10/day.
- **Validation DD breach**: MT5 validation DD 14.89% &gt; 10% despite any narrower DD improvement vs F59 raw OOS.

**Preserved clue (narrow, non-promotion)**
- Admission cadence reduced repeated entries and may have improved DD vs F59 raw OOS on some views, but that did not translate into PF recovery or acceptable validation DD.

**Do-not-repeat note**
- Do **not** run an F60 repair ladder or re-tune thresholds inside this stage.
- Do **not** treat long-axis friction rescue (cadence-only on fixed F59 long-quality) as a viable PF restoration path.
- Do **not** relabel, retrain, or validation-guided threshold tune under the F60 “runtime cadence only” lock and call it the same experiment.
- Next frontier should **pivot away** from long-axis friction rescue toward a **new PF source**, not another cadence variant on the same axis.

### 4. forbidden_claims_check
**pass**

Proposed closeout explicitly rejects completion, baseline, promotion, runtime authority, live readiness, and Goal Achieve. MT5 results (PF &lt;1, validation DD &gt;10%, sub-target density) do not support any of those claims. Preserved DD note is scoped as observation only, not escape success or operating promotion.

---

**Summary:** Accept Codex closeout as `negative_memory_long_axis_friction_escape_failed_pf`. Record the failure memory and do-not-repeat bullets above; carry only the narrow DD/cadence observation forward as reference, not as a winner or baseline.
