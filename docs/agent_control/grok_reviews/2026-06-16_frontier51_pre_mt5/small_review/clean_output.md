Frontier51 MT5 전 검토 요청이므로, Grok 협업 규칙과 단계 근거를 먼저 확인한 뒤 관찰 전용 MT5 실행 허용 여부를 판단하겠습니다.
## Grok Pre-MT5 Review — Frontier51

**Review size:** small review
**Role:** external second opinion only

---

### Verdict

**accepted** — observation-only MT5 on the best available representative candidate is acceptable and required here.

**accepted** — default closeout should remain `negative_memory` unless MT5 shows an unexpected, scout-threshold-clearing improvement (not just PF > 1.0).

**needs_local_verification** — pick one explicit representative row and confirm MT5 handoff material exists before running.

---

### Why accepted (MT5 observation-only)

1. **Mandatory frontier rule** — Every frontier stage must run an MT5 runtime probe and record proxy/runtime gap, even when there is no scout/seed/runtime candidate. F51 already has `mandatory_runtime_probe_required_select_best_available_after_f51_proxy` and `frontier51Z_runtime_probe_backfill_v1`.

2. **Policy alignment** — `runtime_probe` is allowed without runtime authority (`exploration_mandate.md`, `promotion_policy.md`). F50 precedent (`frontier50Z_runtime_probe_backfill_v1`, candidate `f50c_0064`) did exactly this on a `negative_memory` stage with label `runtime_probe_observation_no_authority`.

3. **Bounded evidence supports representative, not positive, probe** — scout/seed/runtime counts are all 0; best forward PF rows stay well below scout floor (1.05):
   - `f51c_0004`: forward_min_pf ≈ 0.981, DD ≈ 5.31
   - `f51b_0003`: forward_min_pf ≈ 0.969, DD ≈ 5.22
   - closest nonwinner `f51c_0046`: forward_min_pf ≈ 1.037 (still < 1.05)

   MT5 here is gap measurement, not promotion validation.

---

### Why accepted (negative_memory default)

Close as `negative_memory` unless MT5 **unexpectedly** clears scout eligibility (forward_min_pf ≥ 1.05 with acceptable density/DD under the same claim boundary). Weak proxy PF alone does not reopen the stage.

Even if MT5 PF > 1.0, that does not create completion, baseline, promotion, or runtime authority without new scout/seed/runtime flags and full evidence chain.

---

### needs_local_verification (before MT5 run)

Codex must locally fix the representative candidate — your prompt cites `f51c_0004` / `f51b_0003`, but closeout already names:
- train-rank representative: `f51b_0001` (forward_min_pf ≈ 0.913)
- best forward observation: `f51c_0046` (forward_min_pf ≈ 1.037)

Any of these is defensible for observation-only probe if labeled `representative_evidence_only`. Recommend **one primary probe** (likely `f51c_0046` as best forward, or `f51b_0001` as train-rank anchor) plus explicit `selection_basis` in the probe manifest.

Also verify: ONNX/model export, feature contract parity, and tester handoff for the chosen row.

---

### Forbidden-claim check

No operating promotion, runtime authority, live readiness, selected baseline, or Goal Achieve from this probe.

---

### Final Codex direction

Proceed with `frontier51Z_runtime_probe_backfill_v1` as **runtime_probe observation only**; record proxy/runtime gap; keep closeout class `negative_memory` unless MT5 materially clears scout floor under local verification.
