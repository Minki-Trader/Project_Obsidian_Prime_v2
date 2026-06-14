# Frontier36 Stage Open Small Review

You are Grok reviewing Project Obsidian Prime v2 as an external second opinion only.

Current truth:
- F35 closed as `preserved_clue_negative_memory`.
- F35B train-only PF source lift proxy produced scout `21`, near-seed `1`, seed/runtime `0/0`.
- F35C DD repair after PF lift produced candidates `4`, scout/seed/runtime `0/0`.
- F35 negative memory: adding single feature filters to the F34/F35 scaffold did not survive DD and density constraints.
- No baseline, promotion, runtime authority, live readiness, or Goal Achieve is inherited or claimed.

Proposed Frontier36 hypothesis:
Stop stacking more filters on the F34/F35 scaffold. Rebuild the short path-native source selection itself with a train-only utility scoring pivot: rank source candidates by PF, density, DD, path quality, stop/take balance, and ambiguity penalties before any validation/OOS readout. Then test whether the changed source selection can create a seed surface closer to validation/OOS PF >= 1.20, density 5-10/day, DD <= 12%.

Changed variable:
- Source scoring / label-selection philosophy changes.
- Exit simulator, raw path data, feature set, splits, and read-only validation/OOS policy stay fixed.

Question:
Is this a valid new frontier hypothesis under reference-not-inheritance, or is it still just repeating F34/F35 filter stacking?

Return exactly five lines:
verdict: accepted / rejected / needs_local_verification
novelty_ok: yes/no
main_leakage_or_overfit_risk: <one sentence>
must_not_repeat: <one sentence>
runtime_claim_boundary_ok: yes/no
