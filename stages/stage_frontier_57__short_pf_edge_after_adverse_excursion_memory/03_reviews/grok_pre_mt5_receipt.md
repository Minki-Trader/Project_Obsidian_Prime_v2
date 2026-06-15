# Grok Receipt(그록 영수증): pre_mt5(MT5 전)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier57_pre_mt5_review`
- classification(분류): `needs_local_verification(로컬 검증 필요)`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
# Frontier57 Pre-MT5 Review — External Second Opinion

**Review size:** medium (제한 스냅샷 + 집중 질문 3개)
**Claim boundary respected:** runtime probe observation only — no completion/baseline/promotion claims.

---

## 1. Invalid before MT5, or weak-but-valid runtime probe?

**Classification: `accepted` — weak-but-valid runtime probe, not invalid.**

| Criterion | Evidence | Verdict |
|-----------|----------|---------|
| ONNX parity | passed, max_abs_diff ≈ 2.76e-07 | Packaging path is credible |
| Feature identity | 58 features, hash pinned | Runtime input contract is defined |
| Threshold / policy | score_q 0.90, direct threshold, short-only, max hold 6 | Executable probe spec exists |
| Proxy economics | Validation PF &lt; 1 (all-signal 0.94, filtered 0.95); OOS PF barely &gt; 1 (1.05 / 1.02) | Weak — not disqualifying for *probe* |
| Label sparsity | train positive rate ~10.8% | Sparse but not empty; density target plausible |

**Why not invalid:** Nothing in the bounded evidence shows broken parity, missing feature contract, or an undefined runtime policy. Validation weakness is a *signal-quality* concern, not a *setup-integrity* failure.

**Why weak:** Validation PF &lt; 1 on both proxy views, with DD still material (filtered validation DD ~6.9%). OOS uplift is thin and could be sample/noise. The hypothesis (train fast-exit label → MT5 PF source) is *unproven*, not *blocked*.

**Effect:** Codex may proceed with a narrow MT5 runtime probe under the stated claim boundary — observation only, no promotion language.

---

## 2. Failure modes Codex must separate in the record

If proceeding, log these four modes **explicitly and orthogonally** (직교적으로 분리 기록):

### A. `source_no_transfer` (원천 전이 실패) — **primary**

- **Meaning:** Train fast-exit positive label does not manifest as MT5 trade-level PF edge.
- **Probe signals:** MT5 PF ≤ proxy OOS (~1.02–1.05) or worse; win/loss shape unlike proxy; score→trade mapping shows no selective lift at q90.
- **Record:** Compare MT5 PF, trade count, avg hold, exit reason mix vs proxy OOS — not vs validation.

### B. `density_align_economics_collapse` (밀도 정렬 뒤 경제성 붕괴) — **primary**

- **Meaning:** Trade/day lands near proxy (~3.1 filtered / ~7.1 all-signal) but PF collapses.
- **Probe signals:** trades/day within ~±30% of proxy target yet PF &lt; 1 or DD worse than proxy OOS.
- **Record:** Density match **without** economics match = this mode, not `source_no_transfer` alone.

### C. `proxy_still_misaligned` (프록시 여전히 불정렬) — **secondary**

- **Meaning:** MT5 and Python proxy diverge beyond tolerance despite parity pass.
- **Probe signals:** Material KPI gap (PF, DD, trades/day) with same threshold/policy; or hold/exit timing mismatch.
- **Record:** Parity passed on 4096 rows — row-level score parity ≠ sequential execution parity. Keep this separate from A.

### D. `parity_fail` (동등성 실패) — **conditional**

- **Meaning:** Runtime ONNX/score path breaks vs packaged artifact.
- **Pre-MT5 status:** **Not triggered** — parity already passed.
- **Record:** Only if MT5 re-check fails (score drift, feature order mismatch, threshold application bug). Do not bucket weak economics here unless parity actually breaks.

**Recommended logging template:**

```
failure_mode_observed: <none | source_no_transfer | density_align_economics_collapse | proxy_still_misaligned | parity_fail>
density_match: <yes/no + trades/day delta>
economics_match: <yes/no + PF/DD delta vs proxy OOS>
parity_recheck: <pass/fail/not_run>
```

**Priority if MT5 is weak:** Distinguish **B** (density OK, PF bad) from **A** (no edge at all) before blaming proxy (**C**).

---

## 3. Pre-MT5 local checks still missing?

**Classification: `needs_local_verification` for several items — bounded evidence does not cover them.**

| Check | In snapshot? | Risk if skipped |
|-------|--------------|-----------------|
| ONNX parity (4096 rows) | Yes | — |
| Feature hash / count | Yes | — |
| Threshold + policy spec | Yes | — |
| Proxy validation/OOS KPIs | Yes | — |
| **Tier A / Tier B separate + combined** | **No** | Cannot label full vs partial context |
| **Sequential proxy vs ONNX-scored path** | **No** | Parity ≠ bar-by-bar execution replay |
| **Hold-limit / max-hold alignment (label 4 vs policy 6)** | **No** | Exit timing skew |
| **Score distribution at q90 on OOS / probe window** | **No** | Threshold may be ultra-sparse live |
| **Filtered vs all-signal proxy definition** | **No** | Wrong comparator at MT5 closeout |
| **EA .set / run_manifest / module hash** | **No** | Runtime identity not pinned |
| **Spread / commission / modeling mode** | **No** | Forensics gap vs proxy |
| **Short-only enforcement path** | **No** | Policy leak = invalid probe |
| **Adverse-excursion memory (F56) runtime wiring** | **No** | Hypothesis chain not evidenced here |

**Minimum adds before or tightly coupled with MT5 probe:**

1. **Execution replay** — same bars, threshold, hold rules as MT5; one KPI line vs both proxy views.
2. **Hold policy note** — explicit mapping: label `hold_limit=4` vs runtime `max_hold=6`.
3. **q90 sparsity** — signal rate and trades/day implied at 0.6182… on the probe window.
4. **Run identity** — `.set`, manifest, ONNX path, feature hash in one handoff line.
5. **Tier routing** — Tier A / B / combined per project rule, or `missing_required` with reason.
6. **F56 memory hook** — one line: how adverse-excursion memory enters runtime (or “not wired in this probe”).

**Effect:** These gaps do not block a *narrow* probe, but without them Codex cannot cleanly assign failure modes 2A–2C after MT5.

---

## Summary for Codex

| Question | Grok classification | Action |
|----------|---------------------|--------|
| 1. Invalid vs weak-valid? | **Accepted:** weak-but-valid probe | Proceed with narrow MT5 probe |
| 2. Failure modes? | **Accepted:** log all four; prioritize A vs B vs C | Use orthogonal template above |
| 3. Missing pre-MT5 checks? | **Needs local verification** | Tier split, replay, hold alignment, q90 sparsity, run identity, F56 wiring |

**Claim boundary:** Grok does not authorize promotion, baseline selection, or runtime authority. MT5 output is observation input for Codex local verification only.
