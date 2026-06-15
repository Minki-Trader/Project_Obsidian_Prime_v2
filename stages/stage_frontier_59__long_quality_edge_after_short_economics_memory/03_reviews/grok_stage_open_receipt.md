# Grok Receipt(그록 영수증): stage_open(단계 개방)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier59_stage_open_snapshot`
- classification(분류): `needs_local_verification(로컬 검증 필요)`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
## Grok Review Classification(그록 검토 분류)

**Verdict on opening F59:** `accepted_with_boundary` — direction is **materially novel enough** to open as a **scout / seed-surface** stage, but novelty is **axis-and-framing novelty**, not proof that the F53–F58 failure class is solved.

**Novelty claim:** `needs_local_verification` only for whether the long label/feature recipe is truly distinct from any prior long experiments in-repo. From this prompt alone, that distinction is **plausible but unproven**.

---

## Is F59 Materially Novel Enough?(F59가 실질적으로 충분히 새로운가?)

**Yes, at frontier scout level(탐색 단계 수준에서는 예).** Three reasons:

1. **Direction pivot is real, not cosmetic(방향 전환은 미세 변형이 아님).**
   F53–F58 repeated the same pattern on the **short** axis: aligned features/signals, ONNX parity, then MT5 economics collapse. F59 explicitly moves to a **long-only `p_long` surface**, avoids another short label micro-variant, and refuses old long winner inheritance. That is a **material research-axis change**, not a relabel tweak.

2. **Claim boundary is appropriately weak(주장 경계가 적절히 낮음).**
   Scout clue, seed surface, runtime probe observation only — no baseline, promotion, runtime authority, or live readiness. That matches what negative memory from F58 actually supports.

3. **Hypothesis is logically motivated(가설 동기는 타당함).**
   After repeated short-side runtime collapse, testing whether **long-side quality/path-survival framing** transfers better is a justified pivot — not random axis hopping.

**What is *not* novel enough by itself(그것만으로는 부족한 점):**

- Same **3-output ONNX shell** `[p_short, p_flat, p_long]` with parity is continuity, not novelty.
- Historical long-side asymmetry is only a **preserved clue**, and those old reports already had trade-shape / DD / trade-count problems. F59 can still recreate “proxy looks fine, runtime dies” on the long side.
- F58’s closed judgment was **`microstructure_friction_source_did_not_transfer`**. F59 changes **direction**, not yet a **new friction/economics hypothesis**. So novelty is enough to **open**, not enough to expect transfer.

**Bottom line:** Open F59 as a bounded scout. Treat it as **novel enough to run**, not **novel enough to expect MT5 rescue**.

---

## Sharpest Pre-MT5 Failure Risk(비싼 MT5 전 가장 날카로운 실패 위험)

**Risk:** **Direction-flip substitution(방향만 바꿔 끼우기).**

Codex may treat “short failed, try long” as if it addresses the demonstrated failure mode. F58 already showed:

- Proxy PF can look weak-positive (`~1.07 / ~1.10`)
- ONNX parity can pass
- `feature_ready_diff` and `signal_diff` can be `0/0`
- MT5 economics can still collapse hard (`PF 0.36 / 0.68`, DD `34.43% / 11.38%`)

So the sharpest pre-MT5 failure is **building another proxy-positive long model that never stress-tests economics transfer**, then spending MT5 probe budget to rediscover the same gap on a new axis.

More specifically, the likely pre-MT5 break point is:

**`path-survival / favorable-movement labels optimistically encode fills and excursion paths that MT5 tester economics do not grant at entry/exit.`**

A long-only quality score trained on ATR-bounded survival can look strong in validation/OOS density/PF/DD while still selecting trades whose **edge lives in microstructure-sensitive shapes** — the same class F58 said did not transfer.

---

## What Codex Should Guard Before MT5(코덱스가 MT5 전에 지켜야 할 것)

Priority order:

1. **Economics-transfer preflight, not parity preflight(동등성만 보지 말고 경제성 전이 사전점검).**
   ONNX parity and zero signal diff are **necessary, not sufficient** — F53–F58 already proved that. Before MT5, require proxy-side evidence that asks: *would this long surface survive spread/slippage/adverse-entry sensitivity?*

2. **Trade-shape forensics on proxy winners(프록시 승자 거래 형태 검증).**
   Check whether PF/DD improvements come from:
   - few large winners vs many small losers
   - entry timing sensitive to adverse excursion
   - density pushed toward 5–10 trades/day that erodes selectivity
   Old long clues already warned about trade-shape / DD / count issues. Repeat that check **before** MT5.

3. **Label-time vs decision-time audit(라벨 시점 vs 의사결정 시점 감사).**
   For ATR-bounded survival, favorable movement, and adverse-movement control, verify the label does not use information or path assumptions unavailable at live-like decision time. This is the cheapest place to catch “proxy lies.”

4. **Density–quality tension gate(밀도–품질 긴장 게이트).**
   Success wants ~5–10 trades/day **and** weak-positive PF with low DD. Long-quality surfaces often fail one side:
   - too selective → under-density → invalid scout
   - density forced → quality diluted → hidden runtime fragility
   Decide which failure is acceptable **before** MT5.

5. **Explicit negative-memory guardrail(명시적 부정 기억 가드레일).**
   If pre-MT5 proxy looks good but stress rows widen badly, or trade-shape resembles F53–F58 short patterns on the long side, close as **`negative_memory_long_axis_did_not_escape_friction_class`** rather than running MT5 by reflex.

---

## Direct Answers(직접 답변)

| Question | Grok answer |
|---|---|
| Materially novel enough to open? | **Yes**, as a **bounded long-axis scout** after short-side negative memory. |
| Novel enough to imply MT5 transfer? | **No.** Direction change does not yet answer F58’s friction-source non-transfer. |
| Sharpest pre-MT5 failure risk? | **Assuming axis flip fixes an economics-transfer failure** while labels/proxy KPIs still encode MT5-nonportable path/fill optimism. |
| Codex guard focus? | **Economics-aware proxy stress + trade-shape forensics + label-timing audit**, not ONNX parity alone. |

**Classification summary:** `accepted` to open F59 with stated claim boundary; `needs_local_verification` for true distinctness from prior long work and for whether pre-MT5 economics stress is actually implemented; `rejected` only if Codex tries to treat long-axis novelty as runtime-authority evidence without closing the friction-transfer question first.
