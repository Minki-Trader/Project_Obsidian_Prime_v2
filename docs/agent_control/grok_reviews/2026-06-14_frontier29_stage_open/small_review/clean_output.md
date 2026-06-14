Frontier29 개방 검토 요청이므로 Grok 협업 스킬과 F28/F29 관련 근거를 먼저 확인합니다.
## Grok External Review — Frontier29 Stage Open

**verdict:** accepted

**novelty_ok:** yes

**leakage_risk:** low

**frontier_boundary_ok:** yes

**must_watch:**
- Freeze the veto contract before F29B: pocket definition (what counts as a “worst train loss pocket”), aggregation grain (trade / session / chunk), veto rule family, and max variants — no post-hoc edits to chase the 6 near-DD or 2 PF-ready rows from F28C.
- Enforce selection boundary mechanically: veto masks scored only from train-period trade losses; validation/OOS may appear only in read-only forward diagnostics, never in mask scoring, threshold tuning, or row promotion.
- Treat F28/F27 234-union surface as reference-only input, not repair target — do not implicitly optimize toward `f28b_0060` (PF 1.216 / DD 19.786) or other F28C headline rows using forward metrics.
- Do not relabel F28 stability-rank tweaks (weight/threshold/chunk penalty) as F29; changed variable must stay `train-loss-conditioned veto mask`, not another ranking pass.
- Guard researcher degrees of freedom: if many veto variants are tried, pre-register the family and record all variants; picking the variant whose read-only val/OOS looks best is not leakage, but calling that “train-only proof” without a frozen contract is invalid setup.
- Check density side effect: train-loss vetoes can thin trade count and fake PF/DD improvement while breaking the 5–10/day seed gate — report density before and after veto per union.
- Distinguish from prior frontier veto work (F23/F24 feature include/veto): F29 must be loss-pocket / concentration keyed, not a disguised feature-veto replay on the same 19 scout rows.
- Record runtime probe status as `out_of_scope_by_claim` until handoff candidate rows > 0; no MT5/ONNX/WFO before handoff + pre-expensive Grok review.
- If Tier A and Tier B are both evaluated, keep separate A, separate B, and combined reads — do not let Tier B partial context stand in for train-loss veto evidence.

**advice_classification:**
- **accepted(수용):** F29 is a valid next frontier, not capped F28 repair. F28C already closed repair with `valid_train_chunk_repair_opportunity_rows = 0` and diagnosed near rows as train-stable but forward PF/DD imbalanced; pivoting from stability ranking to train-loss concentration veto is a real mechanism change (rank/reorder → exclude/mask), which matches F28D’s preserved next clue.
- **accepted(수용):** Novelty relative to F28 is sufficient. F28 tested chunk-stability dispersion ranking; F29 tests whether removing worst train loss pockets changes forward PF/DD balance on the same reference union surface. That is a new selector, not a stability-weight/threshold retune.
- **accepted(수용):** Leakage risk is low under the stated contract: train-loss-only scoring with read-only validation/OOS is the correct boundary for this hypothesis class, consistent with F28’s accepted train-only scout pattern.
- **accepted(수용):** Success boundary is appropriately weak — scout clue / seed surface / handoff candidate only, with no completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve claims.
- **needs_local_verification(로컬 검증 필요):** Codex must confirm trade-level train loss data exists and is joinable for all 234 union candidates before F29B scout execution; stage-open acceptance is design-only until that materialization check passes.
- **needs_local_verification(로컬 검증 필요):** Codex must verify F29 implementation is loss-concentration keyed and not a thin re-export of F23/F24 feature veto machinery on the F27/F28 union pool.
- **rejected(거절):** Any path that uses validation/OOS PF, DD, or density to choose, rank, or threshold veto masks — that would be F28C-forbidden forward-targeted repair under a new label.
- **rejected(거절):** Any claim that read-only forward improvement alone proves train-loss veto worked without frozen pocket definition, density accounting, and full variant ledger.
- **rejected(거절):** Opening MT5/ONNX or treating scout/seed read as runtime authority before `handoff candidate rows > 0` and pre-expensive Grok review.

---

**Summary for Codex:** Accept Frontier29 stage open on hypothesis design. F28’s negative memory (`stability rank did not create seed/handoff`) plus F28C diagnosis (`near rows train-stable, 0 chunk repair targets`) give a coherent pivot. Codex should open F29A only after local checks on trade-loss materialization and non-duplication vs F23 veto patterns; keep val/OOS strictly read-only through closeout unless a leakage failure is documented.
