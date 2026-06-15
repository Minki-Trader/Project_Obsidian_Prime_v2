# Frontier62 Stage Open Review — Grok Verdict

## Classification

**Verdict: `accepted`**

---

## Rationale

### Novelty vs F52 / F60 / F61

| Prior stage | What it tested | F62 overlap | F62 delta |
|-------------|----------------|-------------|-----------|
| **F52** | Lifecycle-only tightening (close-on-flat, entry-transition, cooldown, ATR SLTP) | Reuses lifecycle levers | F52 showed DD could fall but **lifecycle alone did not create PF**. F62 does not reopen that claim; it reframes the question around **proxy–runtime density alignment** and **event-compressed representation**. |
| **F60** | (Not detailed in snapshot) | Unknown overlap | Cannot judge F60 repetition from this packet alone; F62’s stated pivot is F61-driven, not F60-driven. |
| **F61** | Side-allocation + runtime PF failure | Same model/handoff stack | F61’s local read is specific: **signal diff = 0, feature diff = 0**, yet **proxy ~4.8/day vs MT5 ~11–12/day**. F62 targets that gap as primary hypothesis, not side-allocation authority. |

F62 is **not** a bare rerun of F52 lifecycle experiments. It is a **bounded follow-on** to F61’s diagnosed failure mode: *runtime took every same-side signal as a trade event*, producing overtrading despite clean handoff.

The distinguishing variables are:

1. **Event-compressed runtime representation** as the organizing frame (not lifecycle tightening for DD alone).
2. **Event-compressed sequential proxy** + **density-band penalty** for seed selection (proxy metric change, not just runtime knobs).
3. **Explicit success criterion**: narrow proxy–runtime density gap toward **5–10/day**, with signal/feature diff near zero.

That is a **testable, narrower question** than F52 (“can lifecycle reduce DD?”) or F61 (“does side allocation work at runtime?”).

### Boundedness

Strengths:

- Single `stage_id`, single runtime probe after pre-MT5 review.
- Clear control stack: 58-feature contract, US100 M5, existing RuntimeProbeEA, no new EA.
- Explicit failure criteria (PF &lt; 1, DD &gt; 10, density far outside band, handoff mismatch).
- Claim boundary correctly capped at `runtime_probe_observation` — no promotion, baseline, or authority.

Weakness (minor, not blocking): success criterion “PF/DD better than F61 enough to be a preserved clue” is qualitative. Acceptable for exploration open; tighten at closeout.

### Adversarial risks (accepted with eyes open)

1. **Lever reuse**: close-on-flat / entry-transition / cooldown echo F52. Mitigation: F62 bundles them under **density-gap closure**, not lifecycle-only PF hope.
2. **PF may stay &lt; 1 even if density aligns**: compressing events may fix representation mismatch without creating edge. Failure criteria cover that → honest negative memory path.
3. **Proxy retrain “only if needed”**: slightly soft. Acceptable at open if Codex defines “needed” before proxy selection (e.g. only if no frozen seed passes density-band screen under event-compressed proxy).

---

## Smallest change (only if this were `rejected`)

Not required for `accepted`. If forced to one precondition:

> **Lock proxy-selection protocol before any train/run**: document event-compressed sequential proxy definition, density-band penalty formula, and “retrain only if” gate in the F62 open packet so F52 matrix is not silently duplicated.

---

## Summary

F62 asks a **sufficiently novel and bounded** question: *Can event-compressed runtime representation close F61’s proxy–runtime density gap without handoff failure, and is any side-allocation signal still visible at aligned density?*  

It responds to F61’s diagnosis rather than repeating F52’s lifecycle-only PF bet or F61’s side-allocation frame. **Open F62** under the stated claim boundary.
