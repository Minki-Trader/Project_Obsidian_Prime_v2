## Grok Review — F75D Pre-MT5 Negative-Control Runtime Probe

**Advice classification (조언 분류):** **accepted with minor modification (수용, 소폭 수정)**

**Claim boundary (주장 경계):** This is gap-documentation and stage-discipline evidence only — not alpha proof, not promotion, not runtime authority.

---

### 1. Accept, reject, or modify the negative-control MT5 Runtime Probe plan?

**Accept, with one framing modification.**

The `/goal` asks for an MT5 Runtime Probe per frontier stage unless logic impossibility or zero signal blocks it. F75 is not zero-signal: F75B has **one cross-split scout clue** (`f75b_0551`). That is weak, but it is enough to justify a probe.

A **negative-control probe** fits here because:
- meaningful signal count = **0**
- F75C repair produced **0** scout clues
- parent F74 negative memory already flags **weak runtime economics**
- the honest purpose is **proxy/runtime gap evidence**, not “find a winner”

**Modification:** Codex should write the probe’s **success criterion** as *observation completed with recorded gap*, not *positive PF/trades*. Weak or near-zero runtime is **expected and informative** for F75 closeout — as long as execution/parity is valid.

**Do not reject** solely because proxy is weak; that is exactly why negative-control is appropriate.

**Do not upgrade** to a “best-effort alpha hunt” by swapping targets or loosening gates pre-MT5.

---

### 2. Probe target: `f75b_0551`, `f75c_0286`, or both?

**Target `f75b_0551` only.**

| Candidate | Why / why not |
|-----------|----------------|
| **`f75b_0551`** | Only **cross-split scout clue**; keeps the original **compression** hypothesis; weakest-but-valid negative control. |
| **`f75c_0286`** | **No scout clue** (validation PF ~1.01); OOS > validation is **non-confirmatory** and risks a misleading “repair worked in OOS” story. |
| **Both** | Adds MT5 cost without a clean claim: mixed hypothesis (compression scout vs repair rule) and mixed proxy quality. |

If Codex ever runs `f75c_0286`, it should be a **separate labeled packet** (repair-path inconclusive control), not bundled into this F75D negative-control probe.

---

### 3. Proxy/runtime gap risks to record before execution

Record these **before** MT5 run:

1. **Density gap** — proxy tpd ~**0.9–1.0** vs target **5.0**; MT5 may collapse further under spread, session, and fill rules.
2. **PF optimism gap** — validation PF **1.88** vs OOS **1.20**; F74 parent memory says runtime PF/DD/tpd often weaken again at MT5.
3. **Scout ≠ runtime** — cross-split proxy positivity does **not** imply MT5 edge; negative runtime is an expected outcome, not surprise failure.
4. **Gate parity risk** — `hv_q35_compression` and `cash_all` may not match Python counting/session boundaries in EA.
5. **Model parity risk** — `extra_trees_d7_l80` + `all58` is a **large export/inference surface**; small drift can erase thin OOS edge.
6. **Short-only asymmetry** — US100 M5 short fills, spread widening, and stop logic may hurt shorts more than proxy assumes.
7. **Horizon/exit mismatch** — 18-bar horizon may not match realized MT5 SL/TP/MAE-MFE behavior unless F75A label/sim repair is fully parity-bound.
8. **Threshold/routing mismatch** — scout ranking used proxy sim economics; MT5 may apply different trade gating and reject most signals.
9. **Overfitting read risk** — `f75c_0286`-style “OOS strong, validation flat” must not be reinterpreted as runtime hope during F75D.
10. **Negative-control mislabel risk** — weak MT5 must be logged as **expected gap evidence**, not “idea dead” or “probe failed.”

---

### Repair priority (수리 우선순위) for post-probe, if Codex continues F75

1. Keep **SL/TP + MAE/MFE in labels/proxy sim** (F75A accepted priority) before any future probe retarget.
2. If runtime is weak, prefer **parity forensics** (gates, features, threshold, exits) over new model sweeps.
3. Do **not** promote `f75c_0286` on OOS alone without validation confirmation.

---

**Final Codex direction (최종 Codex 방향):** Proceed with **single-target negative-control MT5 Runtime Probe on `f75b_0551`**, explicit negative-control success criteria, and pre-recorded gap risks above. **needs_local_verification** for parity manifest, EA export identity, and actual MT5 KPI — Grok cannot verify those from this snapshot.
