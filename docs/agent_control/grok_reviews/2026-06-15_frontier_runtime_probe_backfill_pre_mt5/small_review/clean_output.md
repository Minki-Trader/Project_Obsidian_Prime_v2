Grok review request — I'll read the collaboration skill and project rules, then verify the local frontier inventory before judging whether the backfill policy fits.
## Grok Review Receipt

| Field | Value |
|---|---|
| **trigger_reason** | User-requested pre-MT5 policy review for frontier runtime-probe backfill |
| **review_size** | `medium review` — bounded inventory snapshot + one focused question |
| **direction_before_grok** | Retroactive repair packet; manifest per stage; MT5 only where handoff is recoverable; no authority claims |
| **bounded_evidence** | F01/F16/F17 closeout docs; F16D/F17C probe reports; F18 `run_manifest.json` with missing ONNX; F08 on-disk ONNX; F19–F49 `selection_status.md` blockers; frontier governance + claim discipline |
| **prompt_identity** | `docs/agent_control/grok_reviews/2026-06-15_frontier_runtime_probe_backfill_pre_mt5/small_review/input.prompt` |
| **forbidden_claim_check** | No promotion, baseline, runtime authority, live readiness, or Goal Achieve proposed |

---

## Verdict

**The policy is mostly faithful to project rules. Codex should narrow the executable target set before any MT5 runs — not expand it.**

The four-class manifest, claim boundary, ledger-only recording for no-material stages, and commit/push gating all align with:

- `reference, not inheritance` (frontier governance)
- `runtime_probe ≠ runtime_authority` (claim discipline)
- external verification anti-deferral (try MT5 where recoverable, otherwise record exact blocker)
- repair-within-stage pattern (F16D supplement is the right precedent)

The main risk is treating “best_candidate_row exists in a report/manifest” as “executable_candidate.” Local filesystem checks show that is not always true.

---

## Advice Classification

### Accepted

1. **F16 and F17 = `completed_existing_verify_only`**
   - F16D and F17C already document completed Tier A runtime probe observations with `no_authority`.
   - Verify ledger rows, report paths, ONNX sha256, and KPI excerpts.
   - Do **not** rerun MT5 unless verification finds a concrete identity mismatch.

2. **F20–F49 (and similar) = status recording, not fabrication**
   - Many stages already have `runtime_probe_ineligible_*` in `04_selected/selection_status.md`.
   - Recording `invalid_setup_no_runtime_material` with exact missing inputs is correct.
   - This matches frontier closeout decision weight, not idea death.

3. **Repair framing, not closeout reopening**
   - Use a per-stage supplement packet (e.g. `frontierXX_runtime_probe_backfill_v1`), modeled on F16D.
   - Negative memory and closeout judgment stay unchanged.
   - Only add `runtime_probe_observation` rows.

4. **Tier A/B paired records**
   - For every probe attempt, also write Tier B `missing_required` and combined `missing_required` where Tier B was never materialized.
   - F16/F17 already did this correctly.

5. **Commit/push only after clean gates**
   - Faithful. Do not push if MT5 artifacts, ledger rows, and manifest classifications are inconsistent.

### Rejected

1. **Forced retro probe for F18 (and similarly F19)**
   - F18 closeout explicitly recorded: `no_runtime_handoff_candidate_under_pre_registered_profile_lock`.
   - `run_manifest.json` references an ONNX path, but that file is **missing on disk**.
   - A forced probe would either invent a new handoff contract or rerun a candidate the stage already ruled non-handoff.
   - Classify F18/F19 as `completed_existing_status_recorded` or `missing_artifact_blocked`, not `executable_candidate`.

2. **Bulk “F07–F15 likely materializable” before preflight**
   - Codex inventory overstates on-disk material.
   - F12–F18 stage trees contain **0** `.onnx` files; F18 manifest ONNX is missing.
   - F08 does have 48 ONNX files and parity CSV — that is the exception, not the band.
   - Do not batch-run F07–F15 on optimism.

3. **Treating F25–F29 and F38–F49 as backfill work items**
   - They already have explicit `runtime_probe_ineligible` status.
   - Backfill should **confirm and ledger-link** existing status, not reopen them as MT5 targets.

### Needs Local Verification (Codex must run before MT5)

Only promote a stage to `executable_candidate` if **all** pass:

| Preflight gate | Pass criterion |
|---|---|
| Artifact presence | ONNX (or approved runtime bundle) exists on disk |
| Identity | `onnx_sha256` / `feature_order_hash` match manifest |
| Contract | `signal_contract`, `decision_mode`, threshold, hold bars documented |
| EA compatibility | Contract fits existing `RuntimeProbeEA` without new signal invention |
| Closeout respect | No explicit `no_runtime_handoff_candidate` blocker |
| Tier A material | Validation/OOS split material available |

After preflight, the **plausible** MT5 band is narrow:

- **F02, F04, F08** — ONNX on disk; still need per-stage manifest + contract verification
- **F07, F09–F15** — verify artifact presence first; do not assume from report references alone
- **F11–F15** — closed negative memory without runtime probe; supplement is allowed only if preflight passes and scope stays `runtime_probe_observation_only`

**F01** should be `out_of_scope_by_claim` — archive/governance stage; selection status explicitly excludes MT5.

---

## Recommended Manifest Refinement

Replace one bucket `executable_candidate` with two:

```text
executable_candidate_after_preflight
missing_artifact_blocked
completed_existing_verify_only
completed_existing_status_recorded
invalid_setup_no_runtime_material
blocked_attempt_failed
```

Add per-row fields:

- `closeout_blocker_token` (if any)
- `artifact_check` (onnx_exists, sha256_match, feature_order_hash)
- `retro_policy` (`supplement_allowed` | `supplement_rejected_closeout_blocker` | `verify_only`)
- `tier_b_status` (`missing_required` expected for most early frontiers)

---

## Execution Order (Codex)

1. Build manifest for **F01–F49** from filesystem + `selection_status.md` + closeout reports — not from Codex memory alone.
2. Verify F16/F17 only; write `runtime_probe_backfill_status` as `completed_existing_verify_only`.
3. Record F18–F49 ineligible/no-material stages without MT5.
4. Run preflight on F02–F15 only.
5. MT5 only for stages that pass all gates — likely a **small** set, not a band.
6. Append ledger rows labeled `runtime_probe_backfill_observation_no_authority`.
7. Commit/push if gates clean.

---

## Final Codex Direction

Proceed with the backfill packet, but **narrow before MT5**. The policy shape is rule-faithful; the executable set in the current inventory is too wide. F16/F17 are verify-only. F18/F19 and most F20+ stages are status/blocker recording. F02/F04/F08 are the first real MT5 candidates only after per-stage preflight proves recoverable handoff without inventing a new signal contract.

If you want, Codex can next build the manifest from local scans and return a stage-by-stage table before touching MT5.
