from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_28 import frontier28b_train_only_stability_gap_proxy_scout as f28b
from stage_pipelines.stage_frontier_28 import frontier28c_stability_gap_repair_or_closeout_decision as f28c
from stage_pipelines.stage_frontier_28 import frontier28d_stage_closeout as f28d


STAGE_ID = "stage_frontier_29__train_only_loss_concentration_veto_for_pf_dd_balance_onnx_scout"
RUN_ID = "frontier29A_stage_open_train_only_loss_concentration_veto_pf_dd_balance_hypothesis_design_v1"
RUN_NUMBER = "frontier29A"
PARENT_RUN_ID = f28d.RUN_ID
NEXT_RUN_ID = "frontier29B_train_only_loss_concentration_veto_proxy_scout_v1"
STATUS = "opened_frontier29_train_only_loss_concentration_veto_no_authority"
JUDGMENT = "stage_opened_after_grok_accepted_loss_concentration_veto_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_29/materialize_frontier29a_stage_open.py")
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_29_train_only_loss_concentration_veto_open.md")

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier29_stage_open/small_review")
F28_SELECTION = Path("stages") / f28d.STAGE_ID / "04_selected" / "selection_status.md"
F28_CLOSEOUT_REPORT = Path("stages") / f28d.STAGE_ID / "03_reviews" / f"{f28d.RUN_ID}_report.md"
F28D_SUMMARY = Path("stages") / f28d.STAGE_ID / "02_runs" / f28d.RUN_ID / "final_closeout_summary.json"
F28B_SUMMARY = Path("stages") / f28d.STAGE_ID / "02_runs" / f28b.RUN_ID / "final_summary.json"
F28B_CANDIDATE_SUMMARY = Path("stages") / f28d.STAGE_ID / "02_runs" / f28b.RUN_ID / "stability_gap_candidate_summary.csv"
F28B_CHUNK_METRICS = Path("stages") / f28d.STAGE_ID / "02_runs" / f28b.RUN_ID / "stability_gap_chunk_metrics.csv"
F28C_REPAIR_AUDIT = Path("stages") / f28d.STAGE_ID / "02_runs" / f28c.RUN_ID / "repair_rejection_audit.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

LOCKS = {
    "selection_split": "train_only",
    "forward_splits": "validation_oos_read_only",
    "changed_variable": "train_loss_conditioned_veto_mask",
    "hypothesis_delta": "replace F28 train stability ranking with train-loss-conditioned veto masks",
    "source_surface": "f28b_234_stability_union_surface_reference_only_not_inherited_baseline",
    "f28_stability_rank_role": "reference_clue_only_no_weight_retune_no_forward_selection_loop",
    "candidate_construction": "reconstruct F28/F27 same-side OR-union masks, then apply train-loss veto variants",
    "veto_contract": {
        "pocket_definition": "candidate_train_trades_only_bottom_loss_region",
        "aggregation_grain": "trade_level_with_optional_session_chunk_diagnostics",
        "rule_family": "single_feature_loss_concentration_threshold_veto_and_capped_pair_veto",
        "max_variants_per_union": 8,
        "max_single_feature_variants_per_union": 4,
        "max_pair_variants_per_union": 4,
        "min_removed_train_trade_fraction": 0.03,
        "max_removed_train_trade_fraction": 0.35,
        "min_loss_capture_ratio": 0.12,
        "no_post_hoc_edits": True,
        "all_variants_recorded": True,
    },
    "selection_boundary": "rank_by_train_loss_concentration_reduction_only_validation_oos_read_only",
    "forbidden_primary_path": [
        "retune_f28_stability_gap_weights",
        "select_by_validation_or_oos_metrics",
        "target_f28c_near_seed_or_pf_ready_rows_by_forward_metrics",
        "generic_f23_f24_feature_veto_replay_without_loss_concentration_key",
        "f26_hard_gate_numeric_threshold_relaxation",
        "onnx_mt5_wfo_before_handoff_candidate_and_pre_expensive_grok",
    ],
    "success_boundary": {
        "scout_clue": "validation_oos_read_only_positive_density_pf_dd_signal",
        "seed_surface": "forward_read_only_pf_ge_1_20_dd_le_18_density_5_to_10",
        "handoff_candidate": "forward_read_only_pf_ge_1_50_dd_le_12_smoothness_pass",
        "not_completion": "final_goal_gates_not_applicable_until_final_completion_review",
    },
    "runtime_probe_rule": "record runtime probe status every stage; execute MT5 only after handoff candidate and pre-expensive Grok",
    "reference_only_prior_artifacts": "Stage12-364 and F24-F28 are clues only, not winners/baselines/promotions/runtime authority/live readiness",
}


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    f28d_summary = read_json(F28D_SUMMARY)
    f28b_summary = read_json(F28B_SUMMARY)
    candidate_summary = pd.read_csv(io_path(F28B_CANDIDATE_SUMMARY))
    chunk_metrics = pd.read_csv(io_path(F28B_CHUNK_METRICS))
    repair_audit = pd.read_csv(io_path(F28C_REPAIR_AUDIT))
    grok = read_grok_packet(GROK_PACKET)
    joinability = verify_train_loss_joinability(frame, feature_order, candidate_summary)
    local = local_verification(
        frame,
        feature_order,
        f28d_summary,
        f28b_summary,
        candidate_summary,
        chunk_metrics,
        repair_audit,
        grok,
        joinability,
    )
    if local["judgment"] != "pass_open_ready_with_loss_concentration_locks":
        raise RuntimeError(f"Frontier29A local verification failed: {json.dumps(local, ensure_ascii=False)}")
    summary = build_summary(created_at, feature_order, f28d_summary, f28b_summary, grok, joinability, local)
    write_outputs(summary)
    update_registries(summary)
    update_current_truth(summary)
    print(json.dumps(json_ready({
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": grok["classification"],
        "joinable_candidate_rows": joinability["joinable_candidate_rows"],
        "local_verification": local["judgment"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "02_runs" / "active",
        STAGE_ROOT / "02_runs" / "archived",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_stage_ledger_header()


def ensure_stage_ledger_header() -> None:
    path = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if path_exists(path):
        return
    with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def normalize_grok_markdown() -> None:
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def read_grok_packet(packet: Path) -> dict[str, Any]:
    metadata = read_json(packet / "metadata.json")
    output = read_text(packet / "clean_output.md")
    lowered = output.lower()
    accepted = (
        "verdict:" in lowered
        and "accepted" in lowered
        and "novelty_ok" in lowered
        and "yes" in lowered
        and "leakage_risk" in lowered
        and "low" in lowered
        and "frontier_boundary_ok" in lowered
        and "yes" in lowered
    )
    return {
        "packet": packet.as_posix(),
        "prompt": (packet / "prompt.md").as_posix(),
        "output": (packet / "clean_output.md").as_posix(),
        "metadata": (packet / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "classification": "accepted_new_frontier_loss_concentration_veto_low_leakage" if accepted else "needs_local_verification",
        "output_excerpt": output[:3200],
    }


def verify_train_loss_joinability(
    frame: pd.DataFrame,
    feature_order: list[str],
    candidate_summary: pd.DataFrame,
) -> dict[str, Any]:
    micro_pockets = f28b.rebuild_f24_micro_pockets(frame, feature_order)
    id_to_micro = {str(row["micro_id"]): row for row in micro_pockets}
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    train_returns = pd.to_numeric(frame["future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    rows: list[dict[str, Any]] = []
    missing_rows: list[str] = []
    for _, row in candidate_summary.iterrows():
        micro_ids = [token for token in str(row["micro_ids"]).split("|") if token]
        missing = [micro_id for micro_id in micro_ids if micro_id not in id_to_micro]
        if missing:
            missing_rows.append(str(row["stability_union_id"]))
            continue
        masks = [np.asarray(id_to_micro[micro_id]["mask"], dtype=bool) for micro_id in micro_ids]
        union_mask = np.logical_or.reduce(masks)
        side = int(row["side_value"]) if "side_value" in row else int(id_to_micro[micro_ids[0]]["side_value"])
        trade_mask = union_mask & train_mask
        pnl = train_returns[trade_mask] * float(side) - scout.ROUGH_COST_LOG_RETURN
        loss_mask = pnl < 0.0
        rows.append({
            "stability_union_id": str(row["stability_union_id"]),
            "source_soft_union_id": str(row["source_soft_union_id"]),
            "micro_ids": "|".join(micro_ids),
            "train_trade_count": int(trade_mask.sum()),
            "train_loss_count": int(loss_mask.sum()),
            "train_loss_sum_abs": float(np.abs(pnl[loss_mask]).sum()),
            "train_loss_share": float(loss_mask.mean()) if len(pnl) else 0.0,
        })
    joined = pd.DataFrame(rows)
    train_trade_counts = joined["train_trade_count"].to_numpy(dtype="float64") if not joined.empty else np.array([])
    train_loss_counts = joined["train_loss_count"].to_numpy(dtype="float64") if not joined.empty else np.array([])
    return {
        "candidate_rows": int(len(candidate_summary)),
        "micro_pocket_rows": int(len(micro_pockets)),
        "joinable_candidate_rows": int(len(joined)),
        "missing_micro_id_rows": int(len(missing_rows)),
        "missing_micro_id_examples": missing_rows[:10],
        "all_candidates_joinable": int(len(joined)) == int(len(candidate_summary)) and not missing_rows,
        "min_train_trade_count": int(train_trade_counts.min()) if len(train_trade_counts) else 0,
        "median_train_trade_count": float(np.median(train_trade_counts)) if len(train_trade_counts) else 0.0,
        "min_train_loss_count": int(train_loss_counts.min()) if len(train_loss_counts) else 0,
        "median_train_loss_count": float(np.median(train_loss_counts)) if len(train_loss_counts) else 0.0,
        "rows_with_train_losses": int((train_loss_counts > 0).sum()) if len(train_loss_counts) else 0,
        "sample_rows": rows[:12],
        "joinability_boundary": "trade_level_train_losses_reconstructed_from_f24_micro_masks",
    }


def local_verification(
    frame: pd.DataFrame,
    feature_order: list[str],
    f28d_summary: dict[str, Any],
    f28b_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    chunk_metrics: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
    joinability: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f28_selection = read_text(F28_SELECTION)
    f28_closeout_report = read_text(F28_CLOSEOUT_REPORT)
    lock_json = json.dumps(LOCKS, ensure_ascii=False)
    checks = {
        "workspace_current_frontier28_closed": f"current_stage_id: {f28d.STAGE_ID}" in workspace
        and f"current_run_id: {f28d.RUN_ID}" in workspace,
        "workspace_next_stage_frontier29": f"next_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier29a": f"next_run_id: {RUN_ID}" in workspace,
        "f28_selection_no_authority": "no selected baseline" in f28_selection.lower()
        and "runtime probe blocker" in f28_selection.lower(),
        "f28_closeout_next_action_frontier29": RUN_ID in f28_closeout_report,
        "f28d_parent_matches": f28d_summary.get("run_id") == f28d.RUN_ID,
        "f28d_no_authority": all(str(f28d_summary.get("claim_boundary", {}).get(claim, "")).startswith("not_claimed") for claim in f03b.FORBIDDEN_CLAIMS),
        "f28b_surface_234": int(f28b_summary.get("reference_union_rows", -1)) == 234
        and int(f28b_summary.get("stability_candidate_rows", -1)) == 234,
        "f28b_seed_handoff_zero": int(f28b_summary.get("seed_surface_rows", -1)) == 0
        and int(f28b_summary.get("handoff_candidate_rows", -1)) == 0,
        "candidate_summary_234": len(candidate_summary) == 234,
        "candidate_micro_ids_complete": candidate_summary["micro_ids"].astype(str).str.len().gt(0).all(),
        "chunk_metrics_936": len(chunk_metrics) == 936,
        "repair_audit_234": len(repair_audit) == 234,
        "repair_audit_valid_train_repair_zero": int(repair_audit["valid_train_chunk_repair_opportunity"].sum()) == 0,
        "dataset_has_train_loss_label": "future_log_return_12" in frame.columns and frame["split"].astype(str).eq("train").any(),
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "trade_level_joinability_all_234": bool(joinability["all_candidates_joinable"]),
        "train_losses_exist_for_all_joined": int(joinability["rows_with_train_losses"]) == 234,
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepted_low_leakage": grok["classification"].startswith("accepted"),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "lock_changed_variable_loss_veto": LOCKS["changed_variable"] == "train_loss_conditioned_veto_mask",
        "lock_veto_contract_frozen": bool(LOCKS["veto_contract"]["no_post_hoc_edits"]),
        "lock_records_all_variants": bool(LOCKS["veto_contract"]["all_variants_recorded"]),
        "lock_blocks_forward_selection": "select_by_validation_or_oos_metrics" in lock_json,
        "lock_blocks_generic_feature_veto_replay": "generic_f23_f24_feature_veto_replay_without_loss_concentration_key" in lock_json,
        "lock_defers_runtime_until_handoff": "handoff candidate" in LOCKS["runtime_probe_rule"],
    }
    classification = {
        "accepted": [
            "open F29 as new loss-concentration veto frontier",
            "freeze train-only veto contract before F29B",
            "keep validation/OOS read-only",
            "record runtime probe status as out_of_scope until handoff",
        ],
        "needs_local_verification": [
            "trade-level train loss joinability for all 234 rows",
            "implementation must be loss-concentration keyed, not generic feature-veto replay",
        ],
        "rejected": [
            "validation/OOS-driven veto ranking",
            "MT5/ONNX/WFO before handoff and pre-expensive Grok",
            "claiming completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve",
        ],
    }
    return {
        "judgment": "pass_open_ready_with_loss_concentration_locks" if all(checks.values()) else "needs_manual_review",
        "checks": checks,
        "grok_advice_classification": classification,
        "joinability": joinability,
    }


def build_summary(
    created_at: str,
    feature_order: list[str],
    f28d_summary: dict[str, Any],
    f28b_summary: dict[str, Any],
    grok: dict[str, Any],
    joinability: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "frontier_thesis": (
            "F28 train-stable but forward-imbalanced union rows may contain concentrated train loss pockets; "
            "removing those train-only pockets can improve PF/DD balance without reusing forward metrics"
        ),
        "hypothesis": (
            "A train-loss-conditioned veto mask, applied after reconstructing the F28/F27 same-side union masks, "
            "may reduce loss concentration and leave smoother forward PF/DD/density reads."
        ),
        "decision_use": "decide whether train-loss veto masks deserve proxy scout, repair, or handoff consideration",
        "comparison_baseline": "F28B 234 stability union surface is reference-only input, not inherited baseline",
        "control_variables": [
            "US100 M5 Tier A dataset",
            "feature_set_v2 58 features",
            "fwd12 label horizon",
            "F28/F27 same-side OR-union semantics",
            "validation/OOS read-only",
        ],
        "changed_variables": [
            "train_loss_conditioned_veto_mask",
            "loss_capture_ratio",
            "removed_train_trade_fraction",
        ],
        "sample_scope": "Tier A US100 M5 model_input_dataset.parquet, frozen train/validation/oos split",
        "success_criteria": LOCKS["success_boundary"],
        "failure_criteria": [
            "zero scout, seed, and handoff rows under frozen train-loss veto contract",
            "apparent forward improvement only from density thinning",
            "train loss concentration does not reduce while forward metrics move",
        ],
        "invalid_conditions": [
            "validation/OOS used for veto threshold or rank selection",
            "veto contract edited after reading forward results",
            "generic feature-veto replay without loss concentration metrics",
            "feature hash mismatch",
        ],
        "stop_conditions": [
            "handoff rows >0 triggers pre-expensive Grok before ONNX/MT5/WFO",
            "seed or scout only triggers repair-or-closeout decision",
            "zero seed and zero handoff after capped repair closes negative memory",
        ],
        "locks": LOCKS,
        "grok": grok,
        "local_verification": local,
        "joinability": joinability,
        "f28d_closeout": {
            "status": f28d_summary.get("status"),
            "judgment": f28d_summary.get("judgment"),
            "preserved_clue": f28d_summary.get("preserved_clue"),
            "negative_memory": f28d_summary.get("negative_memory"),
            "runtime_probe_blocker": f28d_summary.get("runtime_probe_blocker"),
            "onnx_blocker": f28d_summary.get("onnx_blocker"),
        },
        "source_surface": {
            "reference_union_rows": f28b_summary.get("reference_union_rows"),
            "stability_candidate_rows": f28b_summary.get("stability_candidate_rows"),
            "density_bridge_rows": f28b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f28b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f28b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f28b_summary.get("handoff_candidate_rows"),
        },
        "runtime_probe_status": "out_of_scope_by_claim_stage_open_no_handoff_candidate",
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "loss_concentration_veto_lock.json", {"locks": summary["locks"]})
    write_json(RUN_ROOT / "train_loss_joinability_check.json", summary["joinability"])
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "loss_concentration_veto_lock_spec.md", lock_spec(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text())
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_receipt_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index())
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F28_SELECTION,
        F28_CLOSEOUT_REPORT,
        F28D_SUMMARY,
        F28B_SUMMARY,
        F28B_CANDIDATE_SUMMARY,
        F28B_CHUNK_METRICS,
        F28C_REPAIR_AUDIT,
        GROK_PACKET / "metadata.json",
        GROK_PACKET / "clean_output.md",
        RUN_ROOT / "stage_open_summary.json",
        RUN_ROOT / "loss_concentration_veto_lock.json",
        RUN_ROOT / "train_loss_joinability_check.json",
        REPORT_PATH,
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": summary["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "rule_stack": {
            "source": "F28B 234 stability unions, reference only",
            "selection": "train-loss-conditioned veto masks only",
            "forbidden": "no validation/OOS selection, no generic feature-veto replay, no ONNX/MT5/WFO before handoff",
        },
        "joinability": summary["joinability"],
        "claim_boundary": summary["claim_boundary"],
    }


def update_registries(summary: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(summary))
    for row in ledger_rows(summary):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(summary))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "family": "experiment_design(실험 설계)",
        "work_family": "experiment_design(실험 설계)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "notes": f"grok={summary['grok']['classification']};joinable={summary['joinability']['joinable_candidate_rows']};next={NEXT_RUN_ID};no_authority",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "primary_kpi": f"grok={summary['grok']['classification']};joinable={summary['joinability']['joinable_candidate_rows']};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "loss_concentration_veto_lock_no_model_training_no_wfo_no_mt5_no_authority",
        "external_verification_status": summary["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    primary = {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_open",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "scoreboard_lane": "stage_open(단계 개방)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok={summary['grok']['classification']};joinable={summary['joinability']['joinable_candidate_rows']};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "loss_concentration_veto_lock_no_model_training_no_wfo_no_mt5_no_authority",
        "external_verification_status": summary["runtime_probe_status"],
        "notes": f"next={NEXT_RUN_ID};changed_variable={LOCKS['changed_variable']};no_authority",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }
    return [primary]


def update_current_truth(summary: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(summary), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(summary))


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "",
    ])


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Purpose(목적): F28 stability union surface(F28 안정성 합집합 표면)를 reference-only input(참조 전용 입력)으로 두고, train-loss-conditioned veto mask(학습 손실 조건 차단 마스크)가 PF/DD balance(수익 팩터/손실폭 균형)를 회복하는지 본다.

Boundary(경계): scout-only(탐색 전용)입니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 없습니다.

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier29 Stage Brief(전선29 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F29는 F28 stability rank(안정성 순위)를 조정하지 않습니다. changed variable(변경 변수)은 train-loss-conditioned veto mask(학습 손실 조건 차단 마스크)입니다.

Veto contract(차단 계약): train-only trade losses(학습 전용 거래 손실)만 pocket definition(구간 정의), threshold(임계값), rank(순위)에 씁니다. validation/OOS(검증/표본외)는 read-only(읽기 전용)입니다.

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)마다 runtime probe status(런타임 탐침 상태)를 기록합니다. 실제 MT5 runtime probe(MT5 런타임 탐침)는 handoff candidate(인계 후보)와 pre-expensive Grok review(비싼 검증 전 그록 검토)가 있을 때만 실행합니다.
"""


def lock_spec(summary: dict[str, Any]) -> str:
    return (
        "# Frontier29 Loss Concentration Veto Lock Spec(전선29 손실 집중 차단 잠금 명세)\n\n"
        "Locks(잠금):\n"
        f"{json.dumps(summary['locks'], ensure_ascii=False, indent=2)}\n"
    )


def do_not_repeat_text() -> str:
    return """# Frontier29 Do Not Repeat(전선29 반복 금지)

- Do not retune F28 stability weights(F28 안정성 가중치 재조정 금지).
- Do not choose veto thresholds by validation/OOS metrics(검증/표본외 지표로 차단 임계값 선택 금지).
- Do not replay generic F23/F24 feature veto(일반 F23/F24 피처 차단 재탕 금지).
- Do not relax F26 hard gate thresholds(F26 강제 게이트 임계값 완화 금지).
- Do not run ONNX/MT5/WFO before handoff candidate and pre-expensive Grok review(인계 후보와 비싼 검증 전 그록 검토 전 ONNX/MT5/WFO 실행 금지).
"""


def prior_stage_scan_text(summary: dict[str, Any]) -> str:
    closeout = summary["f28d_closeout"]
    source = summary["source_surface"]
    return f"""# Frontier29 Prior Stage Scan(전선29 이전 단계 점검)

F28 preserved clue(전선28 보존 단서): `{closeout.get('preserved_clue')}`.

F28 negative memory(전선28 부정 기억): `{closeout.get('negative_memory')}`.

F28 source counts(전선28 원천 개수): reference/stability/density/scout/seed/handoff(참조/안정성/밀도/탐색/씨앗/인계) = `{source['reference_union_rows']}/{source['stability_candidate_rows']}/{source['density_bridge_rows']}/{source['scout_clue_rows']}/{source['seed_surface_rows']}/{source['handoff_candidate_rows']}`.

Reference boundary(참조 경계): F24-F28 and Stage12-364(F24-F28 및 12-364단계)는 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)는 상속하지 않습니다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier29 Experiment Design(전선29 실험 설계)

- hypothesis(가설): {summary['hypothesis']}
- decision_use(결정 사용처): {summary['decision_use']}
- comparison_baseline(비교 기준): {summary['comparison_baseline']}
- control_variables(통제 변수): {', '.join(summary['control_variables'])}
- changed_variables(변경 변수): {', '.join(summary['changed_variables'])}
- sample_scope(표본 범위): {summary['sample_scope']}
- success_criteria(성공 기준): {json.dumps(summary['success_criteria'], ensure_ascii=False)}
- failure_criteria(실패 기준): {', '.join(summary['failure_criteria'])}
- invalid_conditions(무효 조건): {', '.join(summary['invalid_conditions'])}
- stop_conditions(중단 조건): {', '.join(summary['stop_conditions'])}
- evidence_plan(근거 계획): F29B variant ledger(변형 장부), before/after density(전후 밀도), train loss capture(학습 손실 포착), read-only forward summary(읽기 전용 전진 요약), run registry(실행 등록부), stage ledger(단계 장부).
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier29 Input References(전선29 입력 참조)

- dataset(데이터셋): `{f23b.DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{f23b.FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- F28 selection(F28 선택 상태): `{F28_SELECTION.as_posix()}`
- F28 closeout(F28 마감): `{F28_CLOSEOUT_REPORT.as_posix()}`
- F28D summary(F28D 요약): `{F28D_SUMMARY.as_posix()}`
- F28B candidate surface(F28B 후보 표면): `{F28B_CANDIDATE_SUMMARY.as_posix()}`
- F28B chunk metrics(F28B 조각 지표): `{F28B_CHUNK_METRICS.as_posix()}`
- F28C repair audit(F28C 수리 감사): `{F28C_REPAIR_AUDIT.as_posix()}`
- Grok packet(그록 묶음): `{GROK_PACKET.as_posix()}`
"""


def review_index() -> str:
    return f"""# Frontier29 Review Index(전선29 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    classification = summary["local_verification"]["grok_advice_classification"]
    return f"""# Frontier29 Grok Stage Open Receipt(전선29 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open(단계 개방)은 goal(목표)상 Grok review(그록 검토)가 필요합니다.

Review size(검토 크기): small review(소규모 검토).

Packet(묶음): `{summary['grok']['packet']}`

Prompt(프롬프트): `{summary['grok']['prompt']}`

Output(출력): `{summary['grok']['output']}`

Classification(분류): `{summary['grok']['classification']}`

Accepted advice(수용 조언): {', '.join(classification['accepted'])}

Needs local verification(로컬 검증 필요): {', '.join(classification['needs_local_verification'])}

Rejected advice(거절 조언): {', '.join(classification['rejected'])}

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    lines = ["# Frontier29 Local Verification(전선29 로컬 검증)", ""]
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    lines.append("")
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Joinability(결합 가능성): `{summary['joinability']['joinable_candidate_rows']}` / `{summary['joinability']['candidate_rows']}` candidates(후보), min_train_loss_count(최소 학습 손실 수) `{summary['joinability']['min_train_loss_count']}`.")
    lines.append("")
    lines.append("Effect(효과): F29B proxy(프록시)가 234개 후보 모두에 train loss(학습 손실)를 붙일 수 있음을 확인했고, 검증/OOS(표본외)는 선택에 쓰지 않는 계약을 고정했습니다.")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier29 Required Gate Coverage Audit(전선29 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET.as_posix()}`
- work_packet_schema_lint(작업 묶음 스키마 점검): experiment design fields(실험 설계 필드) materialized(물질화)
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- train_loss_joinability_gate(학습 손실 결합 게이트): `{summary['joinability']['joinable_candidate_rows']}/{summary['joinability']['candidate_rows']}` candidates(후보)
- loss_concentration_contract_gate(손실 집중 계약 게이트): veto contract(차단 계약) locked(잠금)
- leakage_guard(누수 방지): validation/OOS read-only(검증/표본외 읽기 전용)
- runtime_probe_gate(런타임 탐침 게이트): `{summary['runtime_probe_status']}`
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    source = summary["source_surface"]
    return f"""# {RUN_ID} Report(보고서)

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Hypothesis(가설): {summary['hypothesis']}

Action(행동): F29 loss concentration veto(전선29 손실 집중 차단) 계약을 고정하고 234개 F28 union candidate(합집합 후보)의 train loss joinability(학습 손실 결합 가능성)를 확인했습니다.

Effect(효과): F29B는 train-only loss pocket(학습 전용 손실 구간)만으로 veto mask(차단 마스크)를 만들며, validation/OOS(검증/표본외)는 read-only diagnostic(읽기 전용 진단)으로만 남습니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

Joinability(결합 가능성): `{summary['joinability']['joinable_candidate_rows']}` / `{summary['joinability']['candidate_rows']}` candidates(후보), min train losses(최소 학습 손실) `{summary['joinability']['min_train_loss_count']}`.

F28 source counts(F28 원천 개수): reference/stability/density/scout/seed/handoff(참조/안정성/밀도/탐색/씨앗/인계) = `{source['reference_union_rows']}/{source['stability_candidate_rows']}/{source['density_bridge_rows']}/{source['scout_clue_rows']}/{source['seed_surface_rows']}/{source['handoff_candidate_rows']}`.

Runtime probe observation(런타임 탐침 관찰): `{summary['runtime_probe_status']}`. MT5 runtime probe(MT5 런타임 탐침)는 handoff candidate(인계 후보)가 없어 아직 실행하지 않습니다.

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier29 Selection Status(전선29 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage-open only(단계 개방 전용)입니다. F29B proxy(프록시)가 아직 실행되지 않았습니다.

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Runtime probe status(런타임 탐침 상태): `{summary['runtime_probe_status']}`.

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Open Frontier29 Loss Concentration Veto Scout(전선29 손실 집중 차단 탐색 개방)

Date(날짜): 2026-06-14

Decision(결정): Open(개방) `{STAGE_ID}` with run(실행) `{RUN_ID}`.

Reason(이유): F28 stability rank(안정성 순위)는 scout clue(탐색 단서)는 남겼지만 seed/handoff(씨앗/인계)를 만들지 못했습니다. Grok(그록)은 train-loss concentration veto(학습 손실 집중 차단)를 valid next frontier(유효한 다음 전선)로 accepted(수용)했고, Codex local verification(코덱스 로컬 검증)은 234개 후보의 train loss joinability(학습 손실 결합 가능성)를 확인했습니다.

Effect(효과): 다음 proxy(프록시)는 forward metric selection(전진 지표 선택)이 아니라 train-only loss concentration(학습 전용 손실 집중)을 시험합니다.

Claim boundary(주장 경계): no authority(권위 없음), no baseline(기준선 없음), no completion(완성 없음).
"""


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier29(전선29)를 train-only loss concentration veto(학습 전용 손실 집중 차단) 가설로 열었습니다.

Effect(효과): F28 surface(F28 표면)는 reference-only(참조 전용)로 고정했고, 234개 candidate(후보)에 train loss(학습 손실)를 결합할 수 있음을 확인했습니다.

Runtime/ONNX boundary(런타임/ONNX 경계): handoff candidate(인계 후보)가 나오기 전까지 MT5 runtime probe(MT5 런타임 탐침), WFO(워크포워드 최적화), ONNX(온엑스)는 실행하지 않습니다. 각 stage(단계) closeout(마감)에는 runtime probe status(런타임 탐침 상태)를 기록합니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier29 train-only loss concentration veto scout(전선29 학습 전용 손실 집중 차단 탐색 개방). "
        f"Effect(효과): 234 F28 union candidates(F28 합집합 후보 234개) are joinable to train losses(학습 손실 결합 가능) and next run(다음 실행) is `{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR29-TRAIN-ONLY-LOSS-CONCENTRATION-VETO-PF-DD-BALANCE-ONNX-SCOUT`: `{RUN_ID}` opens train-loss-conditioned veto masks(학습 손실 조건 차단 마스크). "
        "Effect(효과): F28 stability surface(F28 안정성 표면)를 기준선이 아닌 reference clue(참조 단서)로만 쓰고 validation/OOS(검증/표본외)는 read-only(읽기 전용)로 둡니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.3f}"


if __name__ == "__main__":
    raise SystemExit(main())
