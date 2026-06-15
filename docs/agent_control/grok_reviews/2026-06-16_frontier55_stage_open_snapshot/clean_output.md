# Grok External Review — F55 Frontier Hypothesis (Small, Snapshot-Only)

**Review mode:** small review, snapshot-only. No local verification performed.

---

## Verdict on “new and bounded enough after F54?”

**Classification: accepted (with one needs_local_verification caveat)**

F54’s closed negative memory is specific: **proxy-shaped payoff looked plausible (~PF 1.03–1.07, ~5.5 trades/day), but MT5 runtime did not transfer** (PF 0.41/0.61, ~15 trades/day), even with **signal_diff=0** and **feature_ready_diff=0**.

F55 is **not a rerun of F54**. It shifts the hypothesis from “runtime-shaped score quality” to **admission architecture**:

| F54 implicit question | F55 explicit question |
|---|---|
| Does the runtime-shaped short payoff score work when transferred? | Does **sparse, forward-only, density-aligned admission** make MT5 see the same economic density the proxy implied (~5–10/day)? |

That is a **logical next frontier pass**, not a promotion or baseline claim. Scope is also **bounded**: named levers (per-day/session budget, min bar gap, forward-only admission), dual recording (proxy + MT5, validation + OOS), and explicit non-claims on promotion/runtime authority/live readiness.

**needs_local_verification caveat:** Whether F55 is *fully* non-redundant depends on whether F54 already tested any form of runtime-side sparsification. From this snapshot alone, F55 looks new; if F54 already had sparse export variants, overlap would be higher.

---

## Biggest failure risks *before* MT5 Strategy Tester time

### 1. Wrong root-cause diagnosis — **accepted risk, high severity**

`signal_diff=0` and `feature_ready_diff=0` mean the headline failure may **not** be “too many raw hits/day” alone. Density mismatch (5–6 proxy vs 15+ MT5) is real, but PF collapse at matched signals suggests **execution mapping, thresholding, fill/slippage/spread, or score→action semantics** may dominate.

**Risk:** You spend MT5 time thinning to 5–10/day and still get bad PF because the score’s runtime economics were never fixed—only trade count changed.

### 2. Proxy and MT5 may still evaluate different strategies — **accepted risk, high severity**

F54 proxy density likely came from **overlap/thinning in the proxy path**, not from the same sparse admission F55 proposes at export. If F55 keeps the score “reference only” but changes **which bars become feature rows**, proxy and MT5 are no longer testing the same object unless **the proxy uses identical sparse admission rules first**.

**Risk:** You “fix” density on MT5 while proxy still reads a denser or differently ranked universe → persistent proxy-runtime gap despite success on trades/day.

### 3. Forward-only ranking / session budget leakage — **accepted risk, medium–high**

Per-day/session **score-ranked budgets** are easy to accidentally make **non-causal** (full-day rank, peeking at session outcomes, boundary resets). That can look fine in proxy and fail in MT5.

**Risk:** OOS looks acceptable in Python, MT5 cannot replicate causality → repeat of F54-style non-transfer without obvious parity diffs.

### 4. Session/day boundary contract drift — **needs_local_verification**

Per-day/session budgets need a **single contract** for: trading day start, session splits, timezone, bar indexing, and what happens at day/session edges. Small definition drift can change which trades survive ranking without showing up as `signal_diff`.

**Risk:** Apparent density alignment (5–10/day) with large PF/DD gap remaining.

### 5. Min bar gap + budget may overshoot the target band — **accepted risk, medium**

Gap + budget can push below 5/day or create **different trade selection** than F54’s proxy overlap (not just fewer of the same trades).

**Risk:** You hit a density number but change the payoff sample so much that comparison to F54 is weak.

### 6. Success metric ambiguity — **accepted risk, medium**

“5–10 signals/day if possible” is good as exploration, but **which count** matters: raw score hits, admitted feature rows, EA intents, or filled trades? F54 already showed **runtime trades/day ≠ proxy trades/day** at zero signal diff.

**Risk:** Stage closes with aligned “signals” but misaligned **trades/day** or PF again.

### 7. MT5 before proxy parity on new admission — **accepted recommendation**

Given F54’s cost pattern, the highest-leverage pre-MT5 check is: **implement sparse admission in proxy first** with the same rules, confirm validation/OOS PF/DD/trades/day and that density lands near 5–10, **then** MT5 probe.

**Classification: accepted** — not a rejection of F55, but a sequencing guard to avoid expensive MT5 runs on an unproven admission layer.

---

## Advice summary (accepted / rejected / needs_local_verification)

| Item | Classification |
|---|---|
| F55 is a sufficiently new, bounded frontier hypothesis after F54 | **accepted** |
| F55 directly addresses F54’s density mismatch hypothesis | **accepted** |
| Density alignment alone will likely restore F54 proxy PF in MT5 | **rejected** (possible but not supported by F54 parity facts) |
| Run proxy with identical sparse admission before MT5 | **accepted** |
| Define signal vs trade density metrics upfront | **accepted** |
| Forward-only + session budget are leakage-safe without explicit spec | **needs_local_verification** |
| F55 is redundant with something F54 already tried | **needs_local_verification** (not visible in this snapshot) |

---

## Practical pre-MT5 stop/go checklist (from snapshot only)

**Go toward MT5 only if proxy-first shows:**

1. Sparse admission yields **~5–10/day** on the **same metric** you will use for MT5.
2. Proxy validation/OOS still worth comparing (PF/DD recorded; no need to claim promotion).
3. Admission rules are **forward-only** by construction, not by hope.
4. You explicitly record **proxy-runtime gap** on density *and* PF/DD, not only `signal_diff` / `feature_ready_diff`.

**Stop or narrow scope if proxy-first shows:**

- Density aligns but PF stays poor → admission was not the main F54 failure.
- Proxy cannot implement the same sparse rules MT5 will use → another parity layer is missing.
- Rank/budget logic needs full-day information → MT5 transfer risk remains high.

---

## Bottom line

**F55 is accepted as a sufficiently new and bounded frontier hypothesis after F54**, because it reframes the problem from score transfer to **runtime-density-aligned sparse admission**, with appropriate exploration-only claim boundaries.

The **biggest pre-MT5 failure risk** is treating **trade-density mismatch** as the sole explanation of F54’s collapse when **signal and feature parity were already zero**—so MT5 time may buy alignment on counts without fixing economics unless **proxy and MT5 share the same admission implementation** and **causality/session contracts** are verified first.

I can tighten this into a one-page F55 pre-flight spec (metrics definitions + proxy-first gate) if you want that next—still without opening the repo, unless you lift the snapshot-only rule.
