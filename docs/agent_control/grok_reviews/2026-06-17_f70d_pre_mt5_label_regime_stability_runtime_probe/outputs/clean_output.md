# F70D Pre-MT5 Runtime Probe Review — Grok Second Opinion

**Advice classification(조언 분류):** `accepted` on direction, with `needs_local_verification` on probe packaging and parity gates before any runtime read.

**Claim boundary(주장 경계):** This review supports **runtime probe observation(런타임 탐침 관찰)** only. It does not support completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve.

---

## 1. Is MT5 probe honest despite `joint-soft=0`?

**Yes — if framed as diagnostic observation, not as scout success.**

From the snapshot alone:

- F70B/F70C both show **joint-soft=0** and **final-like=0**, so proxy scout never found a config that meets the coupled relaxation floor.
- Axis A and B are **near-miss(아깝게 빗나감)** axes, not promoted winners.
- Frontier stage policy still expects an **MT5 Runtime Probe(MT5 런타임 탐침)** before closeout from proxy alone.

That combination is honest when Codex records upfront:

| Record upfront | Why |
|---|---|
| `joint-soft=0`, `final-like=0` | Proxy never cleared production-like coupling |
| Axis A: reference-only, density below scout floor | Not the hypothesis carrier |
| Axis B: PF below meaningful floor on OOS | Weak economic proxy read |
| Probe purpose = **proxy/runtime gap cause(프록시/런타임 간극 원인)** | Not “these axes passed scout” |

**Rejected framing(거절 프레이밍):** Treating either axis as “good enough because OOS PF looks okay” — especially Axis B at OOS PF 1.12 and Axis A with weak validation PF 1.17 vs stronger OOS 1.57.

**Verdict:** Probe is honest as **narrow observation under admitted proxy weakness**, not as validation of scout success.

---

## 2. Probe both axes, or only one?

**Probe both — narrow, paired, role-separated.**

They are not duplicates. Same selection (`vol_expansion_q50`) but different probe jobs:

| Axis | Role | What runtime observation answers |
|---|---|---|
| **A** `f70c_f9a2939acd19` | Reference-quality, ExtraTrees, low-DD | Does the **stable reference signal(안정 참조 신호)** survive MT5 with acceptable trade shape? |
| **B** `f70c_5c8a3021f38f` | Hypothesis-carrier, small MLP, better density | Does the **intended model family(의도한 모델 계열)** behave differently at runtime than the reference? |

**If only one:**

- **A only** → You learn reference stability, not whether the hypothesis carrier (MLP + `repair_vol_expansion` label) is runtime-viable.
- **B only** → You lose the low-DD anchor needed to separate “idea broken” from “carrier/model packaging broken.”

**Resource guardrail:** Keep both probes **minimal** — same regime/session contract, same parity checklist, different model bundle only. No sweep, no threshold hunt, no post-hoc tuning from tester output.

**Verdict:** `accepted` — dual probe is the right diagnostic design.

---

## 3. Negative memory if runtime collapses but parity passes

If **signal/feature parity(신호/피처 동등성)** passes and **runtime KPI collapses**, record at least:

### A. Proxy precondition failure (stage-level)

- F70B/F70C: **420 → 936 candidates**, yet **joint-soft=0**, **final-like=0** throughout.
- Negative memory: *“Regime/session asymmetric value + exit-survival label repair did not produce any proxy config meeting coupled soft floor; runtime probe was observation on nearest axes, not scout-validated configs.”*

### B. Axis-specific proxy warnings confirmed or refuted

- **Axis A:** reference-only, density below scout floor; validation PF 1.17 vs OOS PF 1.57 → large proxy split.
- **Axis B:** OOS PF 1.12 below meaningful floor despite better density.
- Negative memory if both collapse: *“Near-miss reference and carrier both failed runtime translation; proxy optimism (especially A’s OOS) did not carry.”*

### C. Parity-pass / runtime-fail gap taxonomy

Record the **gap cause(간극 원인)** class, not a vague “MT5 bad”:

- threshold / calibration drift at execution boundary  
- trade frequency or density mismatch (scout trades/day vs tester)  
- exit-survival label intent vs EA exit timing  
- spread/fill/slippage sensitivity on `vol_expansion_q50` selection  
- packaging/handoff (bundle, feature order, regime mask), if parity checks were narrow  

Negative memory template: *“Parity passed on [named parity scope from local verification]; runtime collapsed on [named KPI slice]. Gap attributed to [execution/calibration/density/exit-timing/packaging], not to feature math alone.”*

### D. Hypothesis boundary (do not over-close)

- Negative memory: *“F70 sparse/dense fracture reduction claim remains unproven; runtime collapse with parity pass suggests fracture may sit in execution layer or label-to-trade mapping, not in feature replication.”*
- Do **not** write idea-death unless the stage hypothesis scope explicitly closes it.

### E. Preserved clue (only if partial signal exists)

- Both axes share **`vol_expansion_q50`** — if one axis shows partial runtime viability, preserve: *“vol_expansion selection survived on [A/B] under parity; model family or label variant may dominate failure mode.”*
- If both collapse equally: preserved clue downgrades to *“shared selection alone insufficient.”*

---

## Final Codex Direction Assessment

| Question | Grok classification |
|---|---|
| Honest to probe despite `joint-soft=0`? | **Accepted** — as admitted near-miss diagnostic probe |
| Both axes or one? | **Accepted** — both, role-separated |
| Negative memory on parity-pass/runtime-fail? | **Accepted** — record proxy precondition failure, axis-specific warnings, gap cause class, hypothesis boundary |

**Codex should not close F70 from proxy alone.** Proceed to **two narrow MT5 runtime probes** with explicit pre-probe receipt: `joint-soft=0`, `final-like=0`, near-miss axes only, observation-only claim boundary.

**Needs local verification before acting:** exact parity gate list, probe manifest identity (bundle hash, `.set`/EA variant), and tester window parity with proxy OOS/validation splits — not inferable from this snapshot.
