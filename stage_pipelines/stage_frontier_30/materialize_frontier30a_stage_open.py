from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_29 import frontier29d_stage_closeout as f29d


STAGE_ID = "stage_frontier_30__train_density_preserving_selector_before_loss_veto_or_exit_shape_pivot_onnx_scout"
RUN_ID = "frontier30A_stage_open_train_density_preserving_selector_or_exit_shape_pivot_hypothesis_design_v1"
RUN_NUMBER = "frontier30A"
PARENT_RUN_ID = f29d.RUN_ID
NEXT_RUN_ID = "frontier30B_train_density_preserving_preselector_before_loss_veto_proxy_scout_v1"
STATUS = "opened_frontier30_train_density_preserving_preselector_no_authority"
JUDGMENT = "stage_opened_after_grok_accepted_density_preserving_preselector_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_30/materialize_frontier30a_stage_open.py")
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_30_train_density_preserving_preselector_open.md")

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier30_stage_open/small_review")
F29_SELECTION = Path("stages") / f29d.STAGE_ID / "04_selected" / "selection_status.md"
F29A_REPORT = Path("stages") / f29d.STAGE_ID / "03_reviews" / (
    "frontier29A_stage_open_train_only_loss_concentration_veto_pf_dd_balance_hypothesis_design_v1_report.md"
)
F29B_REPORT = Path("stages") / f29d.STAGE_ID / "03_reviews" / (
    "frontier29B_train_only_loss_concentration_veto_proxy_scout_v1_report.md"
)
F29C_REPORT = Path("stages") / f29d.STAGE_ID / "03_reviews" / (
    "frontier29C_loss_concentration_veto_repair_or_closeout_decision_v1_report.md"
)
F29D_REPORT = Path("stages") / f29d.STAGE_ID / "03_reviews" / f"{f29d.RUN_ID}_report.md"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

LOCKS = {
    "selection_split": "train_only",
    "forward_splits": "validation_oos_read_only",
    "active_changed_variable": "train_density_preserving_preselector_before_loss_veto",
    "hypothesis_delta": "move density preservation before loss veto instead of relaxing F29 veto thresholds",
    "source_surface": "f28_f29_reference_surface_only_not_inherited_baseline",
    "exit_shape_pivot_role": "reference_fallback_only_not_active_changed_variable",
    "pipeline_order": [
        "F28_reference_union_surface",
        "train_only_density_preserving_preselector",
        "same_family_train_only_loss_veto",
        "read_only_validation_oos_diagnostics",
    ],
    "preselector_contract": {
        "score_grain": "source_union_level_train_only",
        "required_train_inputs": [
            "train_trades_per_day",
            "train_profit_factor",
            "train_dd_risk",
            "train_loss_count",
            "train_loss_capture_sensitivity",
            "removed_train_trade_fraction_sensitivity",
        ],
        "density_target_center": 7.5,
        "density_soft_band": [5.0, 10.0],
        "density_preservation_floor": 5.0,
        "source_keep_cap": 160,
        "source_keep_rule": "top_160_by_train_only_preselector_score",
        "candidate_branches": [
            "source_no_veto_density_preservation_branch",
            "top_density_preserving_loss_veto_variant_per_source",
        ],
        "max_removed_train_trade_fraction_after_veto": 0.28,
        "rank_formula": (
            "train_density_margin + train_pf_balance + train_dd_containment "
            "+ loss_capture_per_removed_trade - density_thinning_penalty"
        ),
        "no_validation_oos_rank_inputs": True,
        "no_post_hoc_edits": True,
        "all_variants_recorded": True,
    },
    "forbidden_primary_path": [
        "retune_f29_loss_veto_thresholds_to_rescue_near_scout_rows",
        "select_by_validation_or_oos_pf_dd_density",
        "use_f29b_0274_forward_metrics_to_set_preselector_cutoffs",
        "activate_exit_shape_pivot_in_f30b_proxy",
        "inherit_f28_or_f29_winner_baseline_promotion_runtime_authority",
        "onnx_mt5_wfo_before_handoff_candidate_and_pre_expensive_grok",
    ],
    "success_boundary": {
        "scout_clue": "validation_oos_read_only_positive_density_pf_dd_signal",
        "seed_surface": "forward_read_only_pf_ge_1_20_dd_le_18_density_5_to_10",
        "handoff_candidate": "forward_read_only_pf_ge_1_50_dd_le_12_smoothness_pass",
        "not_completion": "final_goal_gates_not_applicable_until_final_completion_review",
    },
    "runtime_probe_rule": "record runtime probe status every stage; execute MT5 only after handoff candidate and pre-expensive Grok",
    "tier_pair_boundary": "Tier B and Tier A+B are missing_required until explicitly materialized in this frontier",
}

F29_COUNTS = {
    "f29b_selected_veto_rows": 1438,
    "f29b_density_bridge_rows": 287,
    "f29b_scout_clue_rows": 0,
    "f29b_seed_surface_rows": 0,
    "f29b_handoff_candidate_rows": 0,
    "f29c_near_scout_rows": 9,
    "f29c_dd_ready_pf_blocked_rows": 7,
    "f29c_would_require_posthoc_contract_edit_rows": 11,
    "f29c_valid_train_loss_repair_opportunity_rows": 0,
    "f29a_joinable_candidate_rows": 234,
    "f29a_candidate_rows": 234,
}


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    feature_order = f23b.read_feature_order()
    frame = f23b.load_frame()
    grok = read_grok_packet(GROK_PACKET)
    local = local_verification(frame, feature_order, grok)
    if local["judgment"] != "pass_open_ready_with_density_preselector_locks":
        raise RuntimeError(f"Frontier30A local verification failed: {json.dumps(local, ensure_ascii=False)}")
    summary = build_summary(created_at, frame, feature_order, grok, local)
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
        "runtime_probe_status": summary["runtime_probe_status"],
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
        "verdict: accepted" in lowered
        and "novelty_ok: yes" in lowered
        and "leakage_risk: low" in lowered
        and "frontier_boundary_ok: yes" in lowered
        and "hypothesis_scope_ok: yes" in lowered
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
        "preflight_warnings": metadata.get("preflight_warnings", []),
        "classification": "accepted_density_preselector_single_active_variable_low_leakage" if accepted else "needs_local_verification",
        "accepted": accepted,
        "output_excerpt": output[:3600],
    }


def local_verification(frame: pd.DataFrame, feature_order: list[str], grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f29_selection = read_text(F29_SELECTION)
    f29a_report = read_text(F29A_REPORT)
    f29b_report = read_text(F29B_REPORT)
    f29c_report = read_text(F29C_REPORT)
    f29d_report = read_text(F29D_REPORT)
    lock_json = json.dumps(LOCKS, ensure_ascii=False)
    split_counts = frame["split"].astype(str).value_counts().to_dict()
    checks = {
        "workspace_current_frontier29_closed_or_frontier30a": (
            f"current_stage_id: {f29d.STAGE_ID}" in workspace
            and f"current_run_id: {f29d.RUN_ID}" in workspace
        ) or (
            f"current_stage_id: {STAGE_ID}" in workspace
            and f"current_run_id: {RUN_ID}" in workspace
        ),
        "workspace_next_stage_frontier30_or_current_frontier30": f"next_stage_id: {STAGE_ID}" in workspace
        or f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier30a_or_frontier30b": f"next_run_id: {RUN_ID}" in workspace
        or f"next_run_id: {NEXT_RUN_ID}" in workspace,
        "f29_selection_no_authority": "no selected baseline" in f29_selection.lower()
        and "runtime probe blocker" in f29_selection.lower(),
        "f29a_joinability_234_recorded": "`234` / `234`" in f29a_report,
        "f29a_min_train_losses_recorded": "min train losses" in f29a_report.lower(),
        "f29b_counts_recorded": "`1438` / `287` / `0` / `0` / `0`" in f29d_report
        and "Screened/selected rows" in f29b_report,
        "f29c_repair_zero_recorded": "valid_train_loss_repair_opportunity_rows" in f29c_report
        and "`0`" in f29c_report,
        "f29d_next_action_frontier30": RUN_ID in f29d_report,
        "f29d_runtime_probe_blocker_recorded": "runtime_probe_ineligible_no_handoff_candidate_after_f29c_repair_decision" in f29d_report,
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepted_low_leakage": grok["accepted"] and grok["classification"].startswith("accepted"),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "feature_count_58": len(feature_order) == 58,
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "dataset_has_required_splits": all(split in split_counts for split in ("train", "validation", "oos")),
        "lock_changed_variable_density_preselector": LOCKS["active_changed_variable"] == "train_density_preserving_preselector_before_loss_veto",
        "lock_exit_shape_reference_only": LOCKS["exit_shape_pivot_role"] == "reference_fallback_only_not_active_changed_variable",
        "lock_blocks_forward_selection": "select_by_validation_or_oos_pf_dd_density" in lock_json,
        "lock_blocks_f29_threshold_rescue": "retune_f29_loss_veto_thresholds_to_rescue_near_scout_rows" in lock_json,
        "lock_blocks_exit_shape_activation": "activate_exit_shape_pivot_in_f30b_proxy" in lock_json,
        "lock_defers_runtime_until_handoff": "handoff candidate" in LOCKS["runtime_probe_rule"],
    }
    classification = {
        "accepted": [
            "open F30 as train-only density-preserving preselector before loss veto",
            "keep exit-shape pivot as reference fallback only",
            "keep validation/OOS read-only",
            "record runtime probe status every stage",
        ],
        "needs_local_verification": [
            "F30B must publish actual preselector variant ledger",
            "F30B must materialize source surface and avoid F29 threshold rescue",
            "pre-expensive Grok is required before any MT5/ONNX/WFO handoff path",
        ],
        "rejected": [
            "validation/OOS-driven preselector ranking",
            "using f29b_0274 forward metrics to set cutoffs",
            "activating exit-shape pivot inside F30B",
            "claiming completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve",
        ],
    }
    return {
        "judgment": "pass_open_ready_with_density_preselector_locks" if all(checks.values()) else "needs_manual_review",
        "checks": checks,
        "grok_advice_classification": classification,
        "split_counts": {str(key): int(value) for key, value in split_counts.items()},
    }


def build_summary(
    created_at: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    grok: dict[str, Any],
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
            "F29 loss veto created density bridge fragments but over-thinned forward density; "
            "a train-only preselector before veto may preserve 5-10/day forward density reads while improving PF/DD balance."
        ),
        "hypothesis": (
            "A train-density-preserving preselector, computed only on train split source-union diagnostics before loss veto, "
            "can reduce the density-thinning failure mode that made F29 scout rows zero."
        ),
        "decision_use": "decide whether density-preserving preselection deserves proxy scout, repair, or handoff consideration",
        "comparison_baseline": "F28/F29 surfaces are reference-only clues, not inherited baselines",
        "control_variables": [
            "US100 M5 Tier A dataset",
            "feature_set_v2 58 features",
            "fwd12 label horizon",
            "F28/F29 source-union semantics as reference only",
            "validation/OOS read-only",
        ],
        "changed_variables": [
            LOCKS["active_changed_variable"],
            "train_density_margin",
            "loss_capture_per_removed_trade",
            "density_thinning_penalty",
        ],
        "sample_scope": "Tier A US100 M5 model_input_dataset.parquet, frozen train/validation/oos split",
        "success_criteria": LOCKS["success_boundary"],
        "failure_criteria": [
            "zero scout, seed, and handoff rows under frozen density-preserving preselector contract",
            "apparent forward improvement only from validation/OOS-targeted density tuning",
            "density preservation keeps trades but PF/DD does not improve enough for scout clue",
        ],
        "invalid_conditions": [
            "validation/OOS used for preselector threshold or rank selection",
            "F29 veto thresholds relaxed to rescue near_scout rows",
            "exit-shape pivot activated in F30B proxy",
            "feature hash mismatch",
        ],
        "stop_conditions": [
            "handoff rows >0 triggers pre-expensive Grok before ONNX/MT5/WFO",
            "seed or scout only triggers repair-or-closeout decision",
            "zero seed and zero handoff after capped repair closes negative memory",
        ],
        "locks": LOCKS,
        "f29_counts": F29_COUNTS,
        "grok": grok,
        "local_verification": local,
        "runtime_probe_status": "out_of_scope_by_claim_stage_open_no_handoff_candidate",
        "onnx_status": "onnx_branch_unattempted_stage_open_no_handoff_candidate",
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "dataset_rows": int(len(frame)),
        "split_counts": local["split_counts"],
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "density_preserving_preselector_lock.json", {"locks": summary["locks"]})
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "density_preserving_preselector_lock_spec.md", lock_spec(summary))
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
        F29_SELECTION,
        F29A_REPORT,
        F29B_REPORT,
        F29C_REPORT,
        F29D_REPORT,
        GROK_PACKET / "metadata.json",
        GROK_PACKET / "clean_output.md",
        RUN_ROOT / "stage_open_summary.json",
        RUN_ROOT / "density_preserving_preselector_lock.json",
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
            "source": "F28/F29 reference surfaces only",
            "selection": "train-only density-preserving preselector before same-family loss veto",
            "forbidden": "no validation/OOS selection, no F29 threshold rescue, no exit-shape activation, no ONNX/MT5/WFO before handoff",
        },
        "claim_boundary": summary["claim_boundary"],
    }


def update_registries(summary: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(summary))
    for row in ledger_rows(summary):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
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
        "notes": f"grok={summary['grok']['classification']};next={NEXT_RUN_ID};no_authority",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "primary_kpi": f"grok={summary['grok']['classification']};feature_hash={summary['feature_order_hash']};rows={summary['dataset_rows']}",
        "guardrail_kpi": "density_preselector_lock_no_model_training_no_wfo_no_mt5_no_authority",
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
        "primary_kpi": f"grok={summary['grok']['classification']};feature_hash={summary['feature_order_hash']};rows={summary['dataset_rows']}",
        "guardrail_kpi": "density_preselector_lock_no_model_training_no_wfo_no_mt5_no_authority",
        "external_verification_status": summary["runtime_probe_status"],
        "notes": f"next={NEXT_RUN_ID};changed_variable={LOCKS['active_changed_variable']};no_authority",
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

Purpose(목적): F29(전선29)의 loss veto(손실 차단)가 밀도를 너무 얇게 만든 문제를, veto(차단) 전에 train-only density-preserving preselector(학습 전용 밀도 보존 사전 선택기)로 줄일 수 있는지 봅니다.

Boundary(경계): scout-only(탐색 전용)입니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 없습니다.

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier30 Stage Brief(전선30 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F30(전선30)은 F29(전선29) threshold(임계값)를 완화하지 않습니다. changed variable(변경 변수)은 `{LOCKS['active_changed_variable']}`입니다.

Exit-shape pivot role(청산 형태 전환 역할): `{LOCKS['exit_shape_pivot_role']}`. 이번 proxy(프록시)의 활성 변수(active variable, 활성 변수)가 아닙니다.

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)마다 runtime probe status(런타임 탐침 상태)를 기록합니다. 실제 MT5 runtime probe(MT5 런타임 탐침)는 handoff candidate(인계 후보)와 pre-expensive Grok review(비싼 실행 전 그록 검토)가 있을 때만 실행합니다.
"""


def lock_spec(summary: dict[str, Any]) -> str:
    return (
        "# Frontier30 Density Preserving Preselector Lock Spec(전선30 밀도 보존 사전 선택기 잠금 명세)\n\n"
        "Locks(잠금):\n"
        f"{json.dumps(summary['locks'], ensure_ascii=False, indent=2)}\n"
    )


def do_not_repeat_text() -> str:
    return """# Frontier30 Do Not Repeat(전선30 반복 금지)

- Do not retune F29 loss veto thresholds(F29 손실 차단 임계값 재조정 금지).
- Do not rescue F29 near_scout rows(F29 탐색 근접 행 구제 금지).
- Do not rank by validation/OOS PF, DD, or density(검증/표본외 수익 팩터, 손실폭, 밀도 순위화 금지).
- Do not activate exit-shape pivot in F30B(F30B에서 청산 형태 전환 활성화 금지).
- Do not run ONNX/MT5/WFO before handoff candidate and pre-expensive Grok review(인계 후보와 비싼 실행 전 그록 검토 전 ONNX/MT5/WFO 실행 금지).
"""


def prior_stage_scan_text(summary: dict[str, Any]) -> str:
    counts = summary["f29_counts"]
    return f"""# Frontier30 Prior Stage Scan(전선30 이전 단계 점검)

F29 preserved clue(F29 보존 단서): loss veto(손실 차단)는 density bridge(밀도 충족) `{counts['f29b_density_bridge_rows']}`개와 dual positive fragments(양수 조각)를 만들었지만 scout/seed/handoff(탐색/씨앗/인계)는 `0/0/0`개였습니다.

F29 negative memory(F29 부정 기억): frozen train-loss veto contract(고정 학습 손실 차단 계약) 아래 valid repair(유효 수리)는 `{counts['f29c_valid_train_loss_repair_opportunity_rows']}`개였습니다.

F29 joinability clue(F29 결합 단서): F29A(전선29A)는 `234/234` candidate(후보)가 train loss(학습 손실)에 결합 가능하다고 기록했습니다.

Reference boundary(참조 경계): F28/F29와 Stage12-364(12~364단계)는 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)는 상속하지 않습니다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier30 Experiment Design(전선30 실험 설계)

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
- evidence_plan(근거 계획): F30B preselector ledger(사전 선택기 장부), before/after density(전후 밀도), train-only rank inputs(학습 전용 순위 입력), read-only validation/OOS summary(읽기 전용 검증/표본외 요약), runtime probe status(런타임 탐침 상태).
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier30 Input References(전선30 입력 참조)

- dataset(데이터셋): `{f23b.DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{f23b.FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- F29 selection(F29 선택 상태): `{F29_SELECTION.as_posix()}`
- F29A report(F29A 보고서): `{F29A_REPORT.as_posix()}`
- F29B report(F29B 보고서): `{F29B_REPORT.as_posix()}`
- F29C report(F29C 보고서): `{F29C_REPORT.as_posix()}`
- F29D closeout(F29D 마감): `{F29D_REPORT.as_posix()}`
- Grok packet(그록 묶음): `{GROK_PACKET.as_posix()}`
"""


def review_index() -> str:
    return f"""# Frontier30 Review Index(전선30 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    classification = summary["local_verification"]["grok_advice_classification"]
    return f"""# Frontier30 Grok Stage Open Receipt(전선30 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open(단계 개방)은 goal(목표) 규칙상 Grok review(그록 검토)가 필요합니다.

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
    lines = ["# Frontier30 Local Verification(전선30 로컬 검증)", ""]
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    lines.append("")
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Split counts(구간 행 수): `{summary['split_counts']}`")
    lines.append("")
    lines.append("Effect(효과): F30A는 design lock(설계 잠금)과 Grok receipt(그록 영수증)를 확정했고, 실제 candidate materialization(후보 물질화)은 F30B로 넘겼습니다.")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier30 Required Gate Coverage Audit(전선30 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET.as_posix()}`
- work_packet_schema_lint(작업 묶음 스키마 점검): experiment design fields(실험 설계 필드) materialized(물질화)
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- density_preselector_contract_gate(밀도 보존 사전 선택기 계약 게이트): preselector contract(사전 선택기 계약) locked(잠금)
- leakage_guard(누수 방어): validation/OOS read-only(검증/표본외 읽기 전용)
- exit_shape_scope_guard(청산 형태 범위 방어): `{LOCKS['exit_shape_pivot_role']}`
- runtime_probe_gate(런타임 탐침 게이트): `{summary['runtime_probe_status']}`
- onnx_gate(ONNX 게이트): `{summary['onnx_status']}`
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    counts = summary["f29_counts"]
    return f"""# {RUN_ID} Report(보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): F30(전선30)을 train-only density-preserving preselector before loss veto(학습 전용 밀도 보존 사전 선택기 후 손실 차단) 가설로 열었습니다.

Effect(효과): F29(전선29)의 valid repair(유효 수리)가 `0`개였기 때문에 F29 threshold repair(임계값 수리)를 반복하지 않고, F30B(전선30B)는 preselector order(사전 선택기 순서)를 새 변수로만 시험합니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

F29 reference counts(F29 참조 수치): selected/density/scout/seed/handoff(선택/밀도/탐색/씨앗/인계) = `{counts['f29b_selected_veto_rows']}/{counts['f29b_density_bridge_rows']}/{counts['f29b_scout_clue_rows']}/{counts['f29b_seed_surface_rows']}/{counts['f29b_handoff_candidate_rows']}`.

Changed variable(변경 변수): `{LOCKS['active_changed_variable']}`

Exit-shape pivot(청산 형태 전환): `{LOCKS['exit_shape_pivot_role']}`

Runtime probe observation(런타임 탐침 관찰): `{summary['runtime_probe_status']}`. MT5 runtime probe(MT5 런타임 탐침)는 handoff candidate(인계 후보)가 없어 아직 실행하지 않습니다.

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier30 Selection Status(전선30 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage-open only(단계 개방 전용)입니다. F30B proxy(F30B 프록시)는 아직 실행 전입니다.

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Runtime probe status(런타임 탐침 상태): `{summary['runtime_probe_status']}`.

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Open Frontier30 Density Preserving Preselector Scout(전선30 밀도 보존 사전 선택기 탐색 개방)

Date(날짜): 2026-06-14

Decision(결정): Open(개방) `{STAGE_ID}` with run(실행) `{RUN_ID}`.

Reason(이유): F29(전선29)는 density bridge(밀도 충족) 조각을 만들었지만 scout/seed/handoff(탐색/씨앗/인계)가 0개였습니다. Grok(그록)은 F30을 F29 repair(수리)가 아니라 pre-veto density preservation order(차단 전 밀도 보존 순서)라는 새 hypothesis lifecycle(가설 생명주기)로 accepted(수용)했습니다.

Effect(효과): 다음 proxy(프록시)는 validation/OOS(검증/표본외)를 선택에 쓰지 않고 train-only preselector(학습 전용 사전 선택기)만 시험합니다.

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

Action(행동): Frontier30(전선30)을 train-only density-preserving preselector before loss veto(학습 전용 밀도 보존 사전 선택기 후 손실 차단) 가설로 열었습니다.

Effect(효과): F30B(전선30B)는 F29 threshold repair(F29 임계값 수리)나 exit-shape pivot(청산 형태 전환)이 아니라, train-only preselector(학습 전용 사전 선택기) 하나만 시험합니다.

Runtime probe boundary(런타임 탐침 경계): 각 stage(단계)마다 runtime probe status(런타임 탐침 상태)를 기록합니다. 현재는 handoff candidate(인계 후보)가 없으므로 MT5 runtime probe(MT5 런타임 탐침)는 실행하지 않았습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier30 train-only density-preserving preselector scout(전선30 학습 전용 밀도 보존 사전 선택기 탐색 개방). "
        f"Effect(효과): F30B will test `{NEXT_RUN_ID}` with exit-shape pivot(청산 형태 전환) kept reference-only(참조 전용).\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR30-TRAIN-DENSITY-PRESERVING-PRESELECTOR-BEFORE-LOSS-VETO-ONNX-SCOUT`: `{RUN_ID}` opens train-only density-preserving preselector(학습 전용 밀도 보존 사전 선택기). "
        "Effect(효과): F29 loss-veto density thinning(F29 손실 차단 밀도 축소)을 수리 반복이 아니라 새 순서 가설로 시험합니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: stringify(row.get(column, "")) for column in header}
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            break
    else:
        rows.append(normalized)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: stringify(item.get(column, "")) for column in header})


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def sha256_io(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
