# Grok Receipt(그록 영수증): pre_mt5(MT5 전)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier59_pre_mt5_review`
- classification(분류): `needs_local_verification(로컬 검증 필요)`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
# Grok Review — Frontier59 Pre-MT5 Probe Validity

**Review size:** medium (제한 스냅샷 + 집중 질문 1개)
**Classification:** **accepted with boundary** (경계부 수용) — probe is justified; failure interpretation must stay narrow.

---

## 1. Is this setup valid to probe under the stated claim boundary?

**Yes — probe-valid, not promotion-valid.** (탐침 유효, 승격 유효 아님)

Under the boundary you stated — **MT5 runtime probe for observation and proxy-runtime gap recording, not promotion** — this setup is internally consistent and worth running.

| Check | Verdict |
|-------|---------|
| ONNX parity passed | Minimum technical handoff for a probe is met |
| Claim boundary = observation / gap, not completion | Matches weak proxy economics; no overclaim |
| Frontier stage rule requires MT5 probe | Probe serves governance, not alpha confirmation |
| Stage-open warning (direction flip ≠ economics fix) | Still binding; probe must not re-test that false equivalence |

**What “valid to probe” means here:** Codex may spend MT5 cost to answer a narrow question: *does this long-quality seed surface survive runtime friction at all, and where does it diverge from proxy?*
**What it does not mean:** the proxy numbers justify expecting MT5 PF ≥ 1 or DD ≤ proxy.

The proxy read already flags the right pre-probe posture:
- weak positive PF (약한 양수 PF),
- validation DD > 10%,
- OOS stress PF < 1,

so MT5 is **calibration instrumentation**, not a tie-breaker for a completion candidate.

**One precondition to keep the probe honest:** runtime policy must mirror the stated contract — raw direct `threshold_margin`, no lifecycle compression, `max_hold_bars=6`, ATR SL/TP on, probability mapping `[0,0,score]`. Any drift turns a gap-reading probe into an unlabeled mixed experiment.

---

## 2. Failure interpretation Codex must guard

If MT5 PF collapses or DD expands, default to **proxy-runtime gap + economics-transfer skepticism**, not “long quality failed” or “direction flip fixed economics.”

### A. If MT5 PF collapses (especially < 1)

Guard these interpretations, in priority order:

1. **Expected parity gap, not surprise failure**
   Proxy OOS stress PF is already `< 1` (`0.959`). A sub-1 MT5 PF is **consistent with bounded evidence**, not a new crisis.
   **Do not** upgrade this to “model broken” or “idea dead.”

2. **Economics-transfer failure on the long side (F58 rhyme)**
   Stage-open warned: flipping direction does not prove economics transfer.
   Collapse may mean **the same failure mode** — gross edge does not survive realistic costs / hold policy — on long instead of short.
   **Label:** `economics_transfer_negative_on_long`, not `directional_quality_invalid`.

3. **Policy mismatch: no lifecycle compression**
   Proxy compressed/sequential PF is materially stronger (`1.14 / 1.01` vs raw `1.06 / 1.02`). MT5 runs **without** compression.
   If MT5 PF lands near raw proxy but far below compressed proxy, that is **documented policy gap**, not hidden alpha loss.

4. **Mechanical/runtime divergence**
   Threshold margin behavior, bar timing, spread/slippage, ATR SL/TP implementation, trade density (`~5.5 trades/day`) can shift PF without invalidating ONNX parity.
   **Label:** `runtime_mechanical_gap` until forensics narrow it.

5. **Forbidden upward misread**
   **Do not** interpret collapse as proof the long hypothesis was wrong **if** proxy was already non-completion.
   **Do not** interpret survival of ONNX parity as evidence the economics story improved.

**Safe closeout sentence:**
> “MT5 probe observed negative economics under declared runtime policy; proxy-runtime gap consistent with weak OOS stress; does not establish MT5-transferable seed surface for this candidate.”

### B. If MT5 DD expands (especially beyond proxy validation ~11.4%)

1. **Not automatically a bug**
   Validation DD already exceeds 10%. Expansion under tester friction is **aligned with proxy weakness**, not proof of implementation error.

2. **Density + short hold can amplify path risk**
   ~5.5 trades/day with `max_hold_bars=6` and no compression can cluster losses in MT5 even when per-trade edge looks similar.
   **Label:** `path_risk_amplification`, not “risk model failure.”

3. **Separate DD expansion from PF collapse**
   - DD up, PF ~1: **friction / clustering / tail trades**
   - DD up, PF < 1: **economics fail under runtime** — stronger negative on transferability
   **Do not** treat DD alone as inconclusive if PF also fails.

4. **Do not use compressed proxy DD (~4.5%) as the MT5 benchmark**
   That used a different lifecycle. Comparing MT5 to compressed DD is a **category error**.

### C. Combined failure (PF collapse + DD expansion)

Strongest allowed negative read:

> **This candidate does not produce an MT5-transferable economics seed under the declared raw policy, consistent with F58-style transfer skepticism after a direction flip.**

Still **not** allowed:
- operating promotion,
- runtime authority,
- “long quality source validated,”
- “F58 problem solved by direction change.”

---

## 3. What success would be allowed (so Codex does not over-claim either)

Even strong MT5 numbers would only support:

- `runtime_probe_observed` (런타임 탐침 관측됨),
- `proxy_runtime_gap_bounded` or `gap_smaller_than_expected`,
- maybe `promotion_ineligible_seed_surface` (승격 부적격 씨앗 표면) — **not** operating promotion.

Required recorded artifacts for any outcome:
- Tier routing if applicable (A / B / combined),
- tester settings parity note,
- explicit proxy vs MT5 KPI delta,
- restatement that proxy was already non-completion.

---

## 4. Advice classification

| Item | Classification |
|------|----------------|
| Proceed with MT5 probe under observation-only boundary | **accepted** |
| Treat proxy as completion justification | **rejected** |
| Read direction flip as economics-transfer fix | **rejected** |
| Exact MT5 PF/DD thresholds for pass-fail | **needs_local_verification** (not in prompt; Codex must set from stage packet / forensics skill) |
| Whether collapse is mechanical vs economic | **needs_local_verification** after tester forensics |

---

## 5. Direct answers

**Q1 — Valid to probe?**
**Yes**, under the stated boundary: ONNX parity + weak proxy + explicit non-promotion intent + frontier MT5 requirement = a legitimate **gap-measurement probe**, not a premature validation.

**Q2 — Guard which failure interpretation?**
Guard against **(1)** surprise framing, **(2)** direction-flip-as-fix narrative, **(3)** compressed-proxy benchmarking, **(4)** idea-death from a probe that was never completion-bound.
Prefer **economics-transfer negative on long under raw runtime policy** and **proxy-runtime mechanical gap** as the default labels when PF collapses or DD expands.

**Bottom line:** Run MT5 to learn transfer friction, not to rescue a proxy that Codex already judged non-completion. The main intellectual trap is the same as stage-open: **direction change is the experiment; economics survival is what MT5 must falsify, not confirm.**
