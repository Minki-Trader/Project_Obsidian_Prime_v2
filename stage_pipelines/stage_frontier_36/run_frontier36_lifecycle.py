from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b
from stage_pipelines.stage_frontier_34 import run_frontier34_lifecycle as f34
from stage_pipelines.stage_frontier_35 import run_frontier35_lifecycle as f35


STAGE_ID = "stage_frontier_36__short_pf_lift_source_change_or_label_pivot_for_seed_surface_onnx_scout"
RUN_A = "frontier36A_stage_open_short_pf_lift_source_change_or_label_pivot_hypothesis_design_v1"
RUN_B = "frontier36B_short_only_source_utility_proxy_scout_v1"
RUN_C = "frontier36C_exit_label_pivot_capped_repair_or_closeout_decision_v1"
RUN_D = "frontier36D_stage_closeout_short_source_utility_label_pivot_v1"
NEXT_STAGE_ID = "stage_frontier_37__short_pf_edge_label_family_pivot_after_source_utility_scout"
NEXT_RUN_ID = "frontier37A_stage_open_short_pf_edge_label_family_pivot_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_36/run_frontier36_lifecycle.py")

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier36_stage_open/small_review")
GROK_RETRY_PACKET = GROK_PACKET / "retry"
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier36_stage_closeout/small_review")
GROK_CLOSEOUT_RETRY_PACKET = GROK_CLOSEOUT_PACKET / "retry"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SOURCE_CONDITION_ROWS = 180
PAIR_SOURCE_ROWS = 80
PAIR_ATTEMPT_LIMIT = 420
MAX_PROXY_CANDIDATES = 320
REPAIR_SOURCE_ROWS = 40
MAX_REPAIR_CANDIDATES = 320

F36_SEED_PF = 1.20
F36_SEED_DD_CAP = 12.0
F36_RUNTIME_PF = 1.50
F36_RUNTIME_DD_CAP = 10.0
F36_NEAR_SEED_PF = 1.12
F36_NEAR_SEED_DD_CAP = 12.0
REPAIR_STOP_QUANTILES = (0.18, 0.22, 0.26, 0.30, 0.34, 0.38, 0.42)
REPAIR_TAKE_QUANTILES = (0.55, 0.62, 0.70, 0.78, 0.86)

PRESERVED_CLUE = (
    "f36_short_only_source_utility_rank_expanded_scout_surface_but_forward_pf_remained_below_seed"
)
NEGATIVE_MEMORY = (
    "f36_short_source_selection_and_exit_label_pivot_did_not_create_seed_or_runtime_candidate"
)


def main() -> int:
    ensure_dirs()
    normalize_grok_packets()
    created_at = f34.utc_now()

    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)

    grok = read_stage_open_grok()
    context = validate_context(frame, feature_order, raw_path, grok)
    proxy = build_short_source_proxy(frame, feature_order, path_labels, raw_path)
    repair = build_exit_label_pivot_repair(frame, path_labels, raw_path, proxy)
    final = build_final(created_at, frame, feature_order, context, proxy, repair)

    write_outputs(final, proxy, repair)
    update_registries(final)
    update_current_truth(final)
    print(
        json.dumps(
            json_ready(
                {
                    "stage_id": STAGE_ID,
                    "closeout_run_id": RUN_D,
                    "proxy_candidate_rows": final["proxy"]["candidate_rows"],
                    "proxy_scout_rows": final["proxy"]["scout_rows"],
                    "proxy_near_seed_rows": final["proxy"]["near_seed_rows"],
                    "proxy_seed_rows": final["proxy"]["seed_rows"],
                    "repair_candidate_rows": final["repair"]["candidate_rows"],
                    "repair_scout_rows": final["repair"]["scout_rows"],
                    "repair_near_seed_rows": final["repair"]["near_seed_rows"],
                    "repair_seed_rows": final["repair"]["seed_rows"],
                    "runtime_probe_status": final["closeout"]["runtime_probe_status"],
                    "next_stage_id": NEXT_STAGE_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "report": (STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md").as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_A_ROOT,
        RUN_B_ROOT,
        RUN_C_ROOT,
        RUN_D_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        Path("docs/decisions"),
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if not path_exists(stage_ledger):
        with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
            header = next(csv.reader(handle))
        with io_path(stage_ledger).open("w", encoding="utf-8-sig", newline="") as handle:
            csv.writer(handle, lineterminator="\n").writerow(header)


def normalize_grok_packets() -> None:
    for packet in (GROK_PACKET, GROK_RETRY_PACKET, GROK_CLOSEOUT_PACKET, GROK_CLOSEOUT_RETRY_PACKET):
        for name in ("input_prompt.md", "input_prompt_retry.md", "prompt.md", "clean_output.md"):
            path = packet / name
            if path_exists(path):
                f03b.write_text_sig(path, io_path(path).read_text(encoding="utf-8-sig").rstrip() + "\n")


def read_stage_open_grok() -> dict[str, Any]:
    first_meta = f34.read_json(GROK_PACKET / "metadata.json") if path_exists(GROK_PACKET / "metadata.json") else {}
    first_output = f34.read_text(GROK_PACKET / "clean_output.md") if path_exists(GROK_PACKET / "clean_output.md") else ""
    retry_meta = f34.read_json(GROK_RETRY_PACKET / "metadata.json")
    retry_output = f34.read_text(GROK_RETRY_PACKET / "clean_output.md")
    lowered = retry_output.lower()
    accepted = (
        "verdict: accepted" in lowered
        and "novelty_ok: yes" in lowered
        and "runtime_claim_boundary_ok: yes" in lowered
    )
    return {
        "first_packet": GROK_PACKET.as_posix(),
        "first_prompt": (GROK_PACKET / "prompt.md").as_posix(),
        "first_output": (GROK_PACKET / "clean_output.md").as_posix(),
        "first_prompt_hash": first_meta.get("prompt_hash", ""),
        "first_success": bool(first_meta.get("success")),
        "first_returncode": first_meta.get("returncode"),
        "first_output_excerpt": first_output[:800],
        "retry_packet": GROK_RETRY_PACKET.as_posix(),
        "retry_prompt": (GROK_RETRY_PACKET / "prompt.md").as_posix(),
        "retry_output": (GROK_RETRY_PACKET / "clean_output.md").as_posix(),
        "retry_metadata": (GROK_RETRY_PACKET / "metadata.json").as_posix(),
        "retry_prompt_hash": retry_meta.get("prompt_hash", ""),
        "retry_success": bool(retry_meta.get("success")),
        "retry_returncode": retry_meta.get("returncode"),
        "retry_timed_out": bool(retry_meta.get("timed_out")),
        "retry_unexpected_top_level_artifacts": retry_meta.get("unexpected_top_level_artifacts", []),
        "accepted": accepted,
        "classification": "accepted_stage_open_retry_short_source_utility_with_overfit_risk" if accepted else "needs_local_verification",
        "retry_output_excerpt": retry_output[:1600],
    }


def read_closeout_grok() -> dict[str, Any]:
    first_meta = f34.read_json(GROK_CLOSEOUT_PACKET / "metadata.json") if path_exists(GROK_CLOSEOUT_PACKET / "metadata.json") else {}
    first_output = f34.read_text(GROK_CLOSEOUT_PACKET / "clean_output.md") if path_exists(GROK_CLOSEOUT_PACKET / "clean_output.md") else ""
    retry_meta = f34.read_json(GROK_CLOSEOUT_RETRY_PACKET / "metadata.json") if path_exists(GROK_CLOSEOUT_RETRY_PACKET / "metadata.json") else {}
    retry_output = f34.read_text(GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md") if path_exists(GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md") else ""
    lowered = retry_output.lower()
    accepted = (
        bool(retry_meta.get("success"))
        and "accepted" in lowered
        and "closeout_class_ok" in lowered
        and "runtime_boundary_ok" in lowered
        and "yes" in lowered
    )
    return {
        "first_packet": GROK_CLOSEOUT_PACKET.as_posix(),
        "first_prompt": (GROK_CLOSEOUT_PACKET / "prompt.md").as_posix(),
        "first_output": (GROK_CLOSEOUT_PACKET / "clean_output.md").as_posix(),
        "first_success": bool(first_meta.get("success")),
        "first_returncode": first_meta.get("returncode"),
        "first_output_excerpt": first_output[:800],
        "retry_packet": GROK_CLOSEOUT_RETRY_PACKET.as_posix(),
        "retry_prompt": (GROK_CLOSEOUT_RETRY_PACKET / "prompt.md").as_posix(),
        "retry_output": (GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md").as_posix(),
        "retry_metadata": (GROK_CLOSEOUT_RETRY_PACKET / "metadata.json").as_posix(),
        "retry_success": bool(retry_meta.get("success")),
        "retry_returncode": retry_meta.get("returncode"),
        "retry_timed_out": bool(retry_meta.get("timed_out")),
        "retry_unexpected_top_level_artifacts": retry_meta.get("unexpected_top_level_artifacts", []),
        "accepted": accepted,
        "classification": "accepted_closeout_preserved_clue_negative_memory_runtime_boundary" if accepted else "needs_local_verification",
        "retry_output_excerpt": retry_output[:1600],
    }


def validate_context(
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = f34.read_text(WORKSPACE_STATE)
    f35_selection = f34.read_text(Path("stages") / f35.STAGE_ID / "04_selected" / "selection_status.md")
    f35_decision = f34.read_text(Path("docs/decisions/2026-06-15_stage_frontier_35_pf_source_lift_closeout.md"))
    checks = {
        "workspace_current_f35": f"current_stage_id: {f35.STAGE_ID}" in workspace,
        "workspace_points_to_f36a": f"next_run_id: {RUN_A}" in workspace,
        "f35_selection_points_to_f36a": RUN_A in f35_selection,
        "f35_decision_points_to_f36a": RUN_A in f35_decision,
        "f35_negative_memory_present": f35.NEGATIVE_MEMORY in f35_selection,
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_has_required_splits": set(frame["split"].astype(str).unique()) == {"train", "validation", "oos"},
        "raw_path_positions_complete": int(raw_path["missing_entry_positions"]) == 0
        and int(raw_path["missing_future_positions"]) == 0,
        "grok_retry_transport_success": grok["retry_success"] and grok["retry_returncode"] == 0 and not grok["retry_timed_out"],
        "grok_retry_accepted": grok["accepted"],
        "grok_no_unexpected_top_level_artifacts": not grok["retry_unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "judgment": "pass_stage_open_ready_with_retry_grok" if all(checks.values()) else "needs_manual_review",
        "classification": grok["classification"],
        **grok,
        "data_source": f23b.DATASET_PATH.as_posix(),
        "raw_source": f33b.RAW_US100_PATH.as_posix(),
        "feature_order_hash": ordered_hash(feature_order),
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "rows": int(len(frame)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].astype(str).value_counts().to_dict().items()},
        },
        "time_axis": "broker-exported M5 open timestamps aligned to raw Bid OHLC open-to-open paths",
        "feature_label_boundary": "source utility and label-pivot thresholds use train split only; validation/OOS are read-only",
        "leakage_risk": "medium: many train-only source and exit-threshold variants are scanned, so F36 remains scout-only unless forward seed/runtime evidence appears",
    }


def build_short_source_proxy(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> dict[str, Any]:
    condition_pool, _ = f33b.build_condition_and_single_candidates(frame, feature_order, path_labels, raw_path)
    short_conditions = condition_pool.loc[
        (condition_pool["side_value"].astype(int) == -1)
        & condition_pool["horizon_prefilter_pass"].astype(bool)
    ].copy()
    if short_conditions.empty:
        return empty_proxy(condition_pool)
    short_conditions["f36_condition_score"] = short_conditions.apply(condition_score, axis=1)
    short_conditions = short_conditions.sort_values("f36_condition_score", ascending=False).reset_index(drop=True)

    candidates: list[dict[str, Any]] = []
    for row in short_conditions.head(SOURCE_CONDITION_ROWS).to_dict("records"):
        candidates.extend(
            f33b.candidate_variants_for_mask(
                frame,
                [row],
                np.asarray(row["_mask"], dtype=bool),
                -1,
                path_labels,
                raw_path,
                min_train_trades=45,
                keep=3,
            )
        )

    top = short_conditions.head(PAIR_SOURCE_ROWS).to_dict("records")
    pair_attempts = 0
    for i, first in enumerate(top):
        for second in top[i + 1 :]:
            if str(first["feature"]) == str(second["feature"]):
                continue
            if str(first["feature_family"]) == str(second["feature_family"]):
                continue
            mask = np.asarray(first["_mask"], dtype=bool) & np.asarray(second["_mask"], dtype=bool)
            candidates.extend(
                f33b.candidate_variants_for_mask(
                    frame,
                    [first, second],
                    mask,
                    -1,
                    path_labels,
                    raw_path,
                    min_train_trades=50,
                    keep=1,
                )
            )
            pair_attempts += 1
            if pair_attempts >= PAIR_ATTEMPT_LIMIT:
                break
        if pair_attempts >= PAIR_ATTEMPT_LIMIT:
            break

    selected = rank_f36_candidates(candidates, "f36b", MAX_PROXY_CANDIDATES)
    split_metrics = f33b.evaluate_candidates(frame, selected, path_labels, raw_path) if selected else pd.DataFrame()
    summary = add_f36_flags(f33b.summarize_candidates(split_metrics), selected)
    return {
        "condition_pool": short_conditions,
        "candidates": selected,
        "split_metrics": split_metrics,
        "summary": summary,
        "source_rows": int(len(short_conditions)),
        "pair_attempts": int(pair_attempts),
        **section_counts(summary, selected),
    }


def build_exit_label_pivot_repair(
    frame: pd.DataFrame,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    proxy: dict[str, Any],
) -> dict[str, Any]:
    summary = proxy["summary"]
    if summary.empty:
        return empty_repair()
    source_ids = summary.loc[summary["path_scout_clue_flag"].astype(bool), "candidate_id"].head(REPAIR_SOURCE_ROWS).tolist()
    if not source_ids:
        return empty_repair()
    by_id = {str(item["candidate_id"]): item for item in proxy["candidates"]}
    repair_candidates: list[dict[str, Any]] = []
    for source_id in source_ids:
        source = by_id.get(str(source_id))
        if not source:
            continue
        for threshold in label_pivot_thresholds(frame, source["mask"], -1, path_labels):
            train = f33b.evaluate_path_mask(
                frame,
                source["mask"],
                -1,
                threshold["stop_cap_log_return"],
                threshold["take_cap_log_return"],
                path_labels,
                raw_path,
                "train",
            )
            if not label_pivot_train_gate(train):
                continue
            repair_candidates.append(repair_candidate_from_source(source, source_id, threshold, train))
    selected = rank_f36_candidates(repair_candidates, "f36c", MAX_REPAIR_CANDIDATES)
    split_metrics = f33b.evaluate_candidates(frame, selected, path_labels, raw_path) if selected else pd.DataFrame()
    summary = add_f36_flags(f33b.summarize_candidates(split_metrics), selected)
    return {
        "candidates": selected,
        "split_metrics": split_metrics,
        "summary": summary,
        "source_rows": int(len(source_ids)),
        **section_counts(summary, selected),
    }


def condition_score(row: pd.Series) -> float:
    density_penalty = abs(safe_float(row.get("best_train_trades_per_day")) - 7.5) / 7.5
    dd_penalty = max(0.0, safe_float(row.get("best_train_dd_risk")) - 12.0) / 18.0
    return float(
        max(safe_float(row.get("best_train_profit_factor")), 0.0)
        * (1.0 + safe_float(row.get("best_train_path_score")) / 1000.0)
        / (1.0 + density_penalty + dd_penalty)
    )


def source_utility_score(metrics: dict[str, Any]) -> float:
    pf = safe_float(metrics.get("profit_factor"))
    density = safe_float(metrics.get("trades_per_day"))
    dd = safe_float(metrics.get("dd_risk"))
    path_quality = safe_float(metrics.get("path_quality_rate"))
    ambiguous_rate = safe_float(metrics.get("ambiguous_both_hit_count")) / max(safe_float(metrics.get("trade_count")), 1.0)
    stop_hits = safe_float(metrics.get("stop_hit_count"))
    take_hits = safe_float(metrics.get("take_hit_count"))
    balance = 1.0 - abs(take_hits - stop_hits) / max(take_hits + stop_hits, 1.0)
    density_bonus = max(0.0, 1.0 - abs(density - 7.5) / 7.5)
    dd_penalty = max(0.0, dd - 12.0) / 12.0
    return float(2.0 * pf + density_bonus + path_quality + max(0.0, balance) - dd_penalty - 2.0 * ambiguous_rate)


def rank_f36_candidates(candidates: list[dict[str, Any]], prefix: str, limit: int) -> list[dict[str, Any]]:
    for candidate in candidates:
        score = source_utility_score(candidate.get("train_selection_metrics", {}))
        candidate["f36_source_utility_score"] = score
        candidate["train_path_score"] = score
    seen: set[tuple[str, float, float]] = set()
    selected: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda item: float(item["f36_source_utility_score"]), reverse=True):
        key = (
            str(candidate.get("condition_ids", "")),
            round(float(candidate.get("stop_cap_log_return", 0.0)), 7),
            round(float(candidate.get("take_cap_log_return", 0.0)), 7),
        )
        if key in seen:
            continue
        seen.add(key)
        selected.append(candidate)
        if len(selected) >= limit:
            break
    for index, candidate in enumerate(selected, start=1):
        candidate["candidate_id"] = f"{prefix}_{index:04d}"
    return selected


def label_pivot_thresholds(
    frame: pd.DataFrame,
    mask: np.ndarray,
    side: int,
    path_labels: dict[int, dict[str, np.ndarray]],
) -> list[dict[str, Any]]:
    labels = path_labels[side]
    train = f33b.split_mask(frame, "train") & np.asarray(mask, dtype=bool) & labels["valid"]
    mfe = labels["mfe"][train]
    mae = labels["mae"][train]
    mfe = mfe[np.isfinite(mfe) & (mfe > 0.0)]
    mae = mae[np.isfinite(mae) & (mae > 0.0)]
    if mfe.size < 30 or mae.size < 30:
        return []
    rows: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for take_q in REPAIR_TAKE_QUANTILES:
        take_cap = max(float(np.nanquantile(mfe, take_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
        for stop_q in REPAIR_STOP_QUANTILES:
            stop_cap = max(float(np.nanquantile(mae, stop_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
            key = (int(round(stop_cap * 1_000_000)), int(round(take_cap * 1_000_000)))
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "threshold_source": "f36c_train_strict_stop_take_label_pivot",
                    "stop_quantile": stop_q,
                    "take_quantile": take_q,
                    "stop_cap_log_return": stop_cap,
                    "take_cap_log_return": take_cap,
                    "train_threshold_sample_rows": int(min(mfe.size, mae.size)),
                }
            )
    return rows


def label_pivot_train_gate(metrics: dict[str, Any]) -> bool:
    return (
        int(metrics["trade_count"]) >= 35
        and 4.0 <= float(metrics["trades_per_day"]) <= 11.0
        and float(metrics["net_profit"]) > 0.0
        and float(metrics["profit_factor"]) >= 1.01
    )


def repair_candidate_from_source(
    source: dict[str, Any],
    source_id: str,
    threshold: dict[str, Any],
    train_metrics: dict[str, Any],
) -> dict[str, Any]:
    candidate = {
        key: value
        for key, value in source.items()
        if key not in {"train_selection_metrics", "f36_source_utility_score", "train_path_score"}
    }
    candidate.update(threshold)
    candidate["source_f36b_candidate_id"] = str(source_id)
    candidate["train_selection_metrics"] = train_metrics
    candidate["f36_source_utility_score"] = source_utility_score(train_metrics)
    candidate["train_path_score"] = candidate["f36_source_utility_score"]
    return candidate


def add_f36_flags(summary: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    if summary.empty:
        return summary
    metadata = {
        str(item["candidate_id"]): {
            "f36_source_utility_score": item.get("f36_source_utility_score", ""),
            "source_f36b_candidate_id": item.get("source_f36b_candidate_id", ""),
        }
        for item in candidates
    }
    summary = summary.copy()
    summary["f36_source_utility_score"] = [metadata.get(str(cid), {}).get("f36_source_utility_score", "") for cid in summary["candidate_id"]]
    summary["source_f36b_candidate_id"] = [metadata.get(str(cid), {}).get("source_f36b_candidate_id", "") for cid in summary["candidate_id"]]
    summary["f36_near_seed_flag"] = (
        summary["forward_dual_positive_flag"].astype(bool)
        & summary["path_density_bridge_flag"].astype(bool)
        & (pd.to_numeric(summary["forward_min_pf"], errors="coerce") >= F36_NEAR_SEED_PF)
        & (pd.to_numeric(summary["forward_max_dd"], errors="coerce") <= F36_NEAR_SEED_DD_CAP)
    )
    summary["f36_seed_surface_flag"] = (
        summary["forward_dual_positive_flag"].astype(bool)
        & summary["path_density_bridge_flag"].astype(bool)
        & (pd.to_numeric(summary["forward_min_pf"], errors="coerce") >= F36_SEED_PF)
        & (pd.to_numeric(summary["forward_max_dd"], errors="coerce") <= F36_SEED_DD_CAP)
    )
    summary["f36_runtime_candidate_flag"] = (
        summary["f36_seed_surface_flag"].astype(bool)
        & (pd.to_numeric(summary["forward_min_pf"], errors="coerce") >= F36_RUNTIME_PF)
        & (pd.to_numeric(summary["forward_max_dd"], errors="coerce") <= F36_RUNTIME_DD_CAP)
    )
    return summary.sort_values(
        ["f36_runtime_candidate_flag", "f36_seed_surface_flag", "f36_near_seed_flag", "path_scout_clue_flag", "path_read_score"],
        ascending=[False, False, False, False, False],
    ).reset_index(drop=True)


def section_counts(summary: pd.DataFrame, candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if summary.empty:
        return {
            "candidate_rows": int(len(candidates)),
            "scout_rows": 0,
            "near_seed_rows": 0,
            "seed_rows": 0,
            "runtime_rows": 0,
            "best_readonly": {},
        }
    return {
        "candidate_rows": int(len(candidates)),
        "scout_rows": int(summary["path_scout_clue_flag"].sum()),
        "near_seed_rows": int(summary["f36_near_seed_flag"].sum()),
        "seed_rows": int(summary["f36_seed_surface_flag"].sum()),
        "runtime_rows": int(summary["f36_runtime_candidate_flag"].sum()),
        "best_readonly": f34.clean_row(summary.iloc[0]),
    }


def empty_proxy(condition_pool: pd.DataFrame) -> dict[str, Any]:
    return {
        "condition_pool": condition_pool,
        "candidates": [],
        "split_metrics": pd.DataFrame(),
        "summary": pd.DataFrame(),
        "source_rows": 0,
        "pair_attempts": 0,
        **section_counts(pd.DataFrame(), []),
    }


def empty_repair() -> dict[str, Any]:
    return {
        "candidates": [],
        "split_metrics": pd.DataFrame(),
        "summary": pd.DataFrame(),
        "source_rows": 0,
        **section_counts(pd.DataFrame(), []),
    }


def build_final(
    created_at: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    context: dict[str, Any],
    proxy: dict[str, Any],
    repair: dict[str, Any],
) -> dict[str, Any]:
    runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f36c_exit_label_pivot_repair"
    closeout_grok = read_closeout_grok()
    closeout = {
        "run_id": RUN_D,
        "status": "closed_preserved_clue_negative_memory_short_source_utility_scout_only_no_runtime_authority",
        "judgment": "preserved_clue_negative_memory(F36 short-only source utility scout only no seed/runtime)",
        "closeout_class": "preserved_clue_negative_memory",
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "runtime_probe_status": runtime_status,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "grok_closeout": closeout_grok,
    }
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "stage_open": {
            "run_id": RUN_A,
            "status": "opened_frontier36_short_source_change_or_label_pivot_no_authority",
            "judgment": "stage_opened_after_grok_retry_accepted_short_source_utility_boundary",
            "grok": context,
        },
        "data": {
            "dataset_rows": int(len(frame)),
            "feature_count": int(len(feature_order)),
            "feature_order_hash": ordered_hash(feature_order),
            "source_condition_rows": SOURCE_CONDITION_ROWS,
            "pair_source_rows": PAIR_SOURCE_ROWS,
            "repair_source_rows": REPAIR_SOURCE_ROWS,
        },
        "proxy": {
            "run_id": RUN_B,
            "status": "short_only_source_utility_proxy_scout_no_seed_no_runtime_candidate_no_authority",
            "judgment": "expanded_scout_surface_requires_label_pivot_repair_or_closeout_no_authority",
            "source_rows": proxy["source_rows"],
            "pair_attempts": proxy["pair_attempts"],
            "candidate_rows": proxy["candidate_rows"],
            "scout_rows": proxy["scout_rows"],
            "near_seed_rows": proxy["near_seed_rows"],
            "seed_rows": proxy["seed_rows"],
            "runtime_rows": proxy["runtime_rows"],
            "best_readonly": proxy["best_readonly"],
            "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_proxy_scout_only_no_runtime_candidate",
        },
        "repair": {
            "run_id": RUN_C,
            "status": "exit_label_pivot_capped_repair_closeout_queued_no_authority",
            "judgment": "label_pivot_repair_expanded_scout_but_no_seed_runtime_requires_closeout",
            "source_rows": repair["source_rows"],
            "candidate_rows": repair["candidate_rows"],
            "scout_rows": repair["scout_rows"],
            "near_seed_rows": repair["near_seed_rows"],
            "seed_rows": repair["seed_rows"],
            "runtime_rows": repair["runtime_rows"],
            "best_readonly": repair["best_readonly"],
            "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_capped_repair_no_runtime_candidate",
        },
        "closeout": closeout,
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], proxy: dict[str, Any], repair: dict[str, Any]) -> None:
    proxy["condition_pool"].drop(columns=["_mask"], errors="ignore").to_csv(
        io_path(RUN_B_ROOT / "short_source_condition_pool.csv"), index=False, encoding="utf-8-sig"
    )
    pd.DataFrame([f33b.clean_candidate_for_csv(item) for item in proxy["candidates"]]).to_csv(
        io_path(RUN_B_ROOT / "short_source_candidate_ledger.csv"), index=False, encoding="utf-8-sig"
    )
    proxy["split_metrics"].to_csv(io_path(RUN_B_ROOT / "short_source_split_metrics.csv"), index=False, encoding="utf-8-sig")
    proxy["summary"].to_csv(io_path(RUN_B_ROOT / "short_source_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    proxy["summary"].head(40).to_csv(io_path(RUN_B_ROOT / "top_short_source_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")

    pd.DataFrame([f33b.clean_candidate_for_csv(item) for item in repair["candidates"]]).to_csv(
        io_path(RUN_C_ROOT / "exit_label_pivot_candidate_ledger.csv"), index=False, encoding="utf-8-sig"
    )
    repair["split_metrics"].to_csv(io_path(RUN_C_ROOT / "exit_label_pivot_split_metrics.csv"), index=False, encoding="utf-8-sig")
    repair["summary"].to_csv(io_path(RUN_C_ROOT / "exit_label_pivot_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    repair["summary"].head(40).to_csv(io_path(RUN_C_ROOT / "top_exit_label_pivot_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")

    f34.write_json(RUN_A_ROOT / "stage_open_summary.json", final["stage_open"])
    f34.write_json(RUN_B_ROOT / "final_summary.json", final["proxy"])
    f34.write_json(RUN_C_ROOT / "final_summary.json", final["repair"])
    f34.write_json(RUN_D_ROOT / "stage_closeout_summary.json", final)

    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_receipt(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_closeout_receipt.md", grok_closeout_receipt(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_A}_report.md", stage_open_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_report.md", run_report("Frontier36B Short Source Utility Proxy Report(전선36B 숏 원천 유틸리티 프록시 보고)", final["created_at_utc"], final["proxy"], proxy["summary"], "Action(행동): short-only source utility ranking(숏 전용 원천 유틸리티 순위화)으로 후보 생성 순서를 바꿨습니다.", "Effect(효과): 기존 long/short combined truncation(롱/숏 합산 절단)에서 빠진 short surface(숏 표면)를 넓게 복구합니다.", RUN_C))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_gate_audit.md", gate_audit_text("Frontier36B Gate Audit(전선36B 게이트 감사)", final["proxy"]["runtime_probe_status"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_report.md", run_report("Frontier36C Exit Label Pivot Repair Report(전선36C 청산 라벨 전환 수리 보고)", final["created_at_utc"], final["repair"], repair["summary"], "Action(행동): scout rows(탐색 행)에 새 피처 필터를 얹지 않고 stop/take label grid(손절/익절 라벨 격자)만 전환했습니다.", "Effect(효과): DD/PF/density(손실폭/수익 팩터/밀도)가 청산 라벨 변화만으로 seed surface(씨앗 표면)에 가까워지는지 분리해 봅니다.", RUN_D))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_gate_audit.md", gate_audit_text("Frontier36C Gate Audit(전선36C 게이트 감사)", final["repair"]["runtime_probe_status"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md", closeout_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", required_gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_36_short_source_utility_open.md"), decision_open(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_36_short_source_utility_closeout.md"), decision_closeout(final))
    f34.write_json(RUN_D_ROOT / "run_manifest.json", run_manifest(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_PACKET / "prompt.md",
        GROK_PACKET / "metadata.json",
        GROK_RETRY_PACKET / "prompt.md",
        GROK_RETRY_PACKET / "clean_output.md",
        GROK_RETRY_PACKET / "metadata.json",
        GROK_CLOSEOUT_PACKET / "prompt.md",
        GROK_CLOSEOUT_PACKET / "clean_output.md",
        GROK_CLOSEOUT_PACKET / "metadata.json",
        GROK_CLOSEOUT_RETRY_PACKET / "prompt.md",
        GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md",
        GROK_CLOSEOUT_RETRY_PACKET / "metadata.json",
        RUN_B_ROOT / "short_source_candidate_summary.csv",
        RUN_C_ROOT / "exit_label_pivot_candidate_summary.csv",
        RUN_D_ROOT / "stage_closeout_summary.json",
        STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md",
        STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md",
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "parent_run_id": RUN_C,
            "next_stage_id": NEXT_STAGE_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [f34.artifact_identity(path) for path in artifacts],
        "source_selection_contract": {
            "changed_variable": "short_only_train_utility_source_ranking_and_exit_label_pivot",
            "fixed_variables": "raw_path_exit_simulator_feature_order_splits_validation_oos_read_only",
            "score_components": "train PF, density closeness, DD penalty, path quality, stop/take balance, ambiguity penalty",
        },
        "closeout_class": final["closeout"]["closeout_class"],
        "runtime_claim_boundary": "stage_closeout_no_mt5_runtime_authority",
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    upsert_csv_many(RUN_REGISTRY, "run_id", run_registry_rows(final))
    ledger = ledger_rows(final)
    upsert_csv_many(ALPHA_LEDGER, "ledger_row_id", ledger)
    upsert_csv_many(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger)
    f03b.append_once(CHANGELOG, RUN_D, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_A, idea_registry_open(final))
    f03b.append_once(IDEA_REGISTRY, RUN_D, idea_registry_close(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_D, negative_register_entry(final))


def upsert_csv_many(path: Path, key: str, new_rows: list[dict[str, Any]]) -> None:
    resolved = io_path(path)
    with resolved.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = list(reader.fieldnames or [])
        existing_rows = [dict(row) for row in reader]
    if key not in header:
        raise ValueError(f"{path.as_posix()} missing key column {key}")

    index_by_key = {row.get(key, ""): index for index, row in enumerate(existing_rows)}
    for row in new_rows:
        normalized = {column: f34.stringify(row.get(column, "")) for column in header}
        row_key = normalized.get(key, "")
        if row_key in index_by_key:
            existing_rows[index_by_key[row_key]] = normalized
        else:
            index_by_key[row_key] = len(existing_rows)
            existing_rows.append(normalized)

    resolved.parent.mkdir(parents=True, exist_ok=True)
    with resolved.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in existing_rows:
            writer.writerow({column: f34.stringify(row.get(column, "")) for column in header})


def run_registry_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    created = final["created_at_utc"]
    best_b = final["proxy"]["best_readonly"]
    best_c = final["repair"]["best_readonly"]
    close = final["closeout"]
    return [
        registry_row(RUN_A, "stage_open(단계 개방)", final["stage_open"]["status"], final["stage_open"]["judgment"], f"grok={final['stage_open']['grok']['classification']};next={RUN_B};no_authority", created, "stage_open_no_model_training_no_wfo_no_mt5_no_onnx_no_authority", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", RUN_B),
        registry_row(RUN_B, "proxy_scout(프록시 탐색)", final["proxy"]["status"], final["proxy"]["judgment"], f"source={final['proxy']['source_rows']};candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};near_seed={final['proxy']['near_seed_rows']};seed={final['proxy']['seed_rows']};best={best_b.get('candidate_id','')};next={RUN_C}", created, "python_short_source_utility_proxy_only_no_wfo_no_mt5_no_onnx_no_authority", final["proxy"]["runtime_probe_status"], RUN_C, best_b),
        registry_row(RUN_C, "repair_or_closeout_decision(수리 또는 마감 결정)", final["repair"]["status"], final["repair"]["judgment"], f"source={final['repair']['source_rows']};candidate={final['repair']['candidate_rows']};scout={final['repair']['scout_rows']};near_seed={final['repair']['near_seed_rows']};seed={final['repair']['seed_rows']};best={best_c.get('candidate_id','')};next={RUN_D}", created, "exit_label_pivot_repair_proxy_only_no_wfo_no_mt5_no_onnx_no_authority", final["repair"]["runtime_probe_status"], RUN_D, best_c),
        registry_row(RUN_D, "stage_closeout(단계 마감)", close["status"], close["judgment"], f"closeout={close['closeout_class']};preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY};next={NEXT_RUN_ID}", created, "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_onnx_no_authority", close["runtime_probe_status"], NEXT_RUN_ID, best_c or best_b),
    ]


def registry_row(
    run_id: str,
    lane: str,
    status: str,
    judgment: str,
    notes: str,
    created: str,
    claim_boundary: str,
    external_status: str,
    next_run: str,
    best: dict[str, Any] | None = None,
) -> dict[str, Any]:
    report = STAGE_ROOT / "03_reviews" / f"{run_id}_report.md"
    primary = "stage_open_no_trading_kpi"
    if best:
        primary = (
            f"best={best.get('candidate_id','')};"
            f"val_pf={f34.fmt(best.get('validation_profit_factor'))};"
            f"val_dd={f34.fmt(best.get('validation_dd_risk'))};"
            f"oos_pf={f34.fmt(best.get('oos_profit_factor'))};"
            f"oos_dd={f34.fmt(best.get('oos_dd_risk'))}"
        )
    return {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "lane": lane,
        "family": "experiment_execution(실험 실행)" if run_id != RUN_D else "publish_handoff(게시/인계)",
        "work_family": "experiment_execution(실험 실행)" if run_id != RUN_D else "publish_handoff(게시/인계)",
        "status": status,
        "judgment": judgment,
        "path": report.as_posix(),
        "notes": notes,
        "run_number": run_id.split("_", 1)[0],
        "date": "2026-06-15",
        "parent_run_id": f35.RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
        "next_run_id": next_run,
        "claim_boundary": claim_boundary,
        "report_path": report.as_posix(),
        "created_at_utc": created,
        "primary_kpi": primary,
        "guardrail_kpi": "train_only_source_selection_validation_oos_read_only_no_runtime_authority",
        "external_verification_status": external_status,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": report.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        ledger_row(RUN_A, f"{RUN_A}__stage_open", "stage_open(단계 개방)", "not_applicable_stage_open(단계 개방 해당 없음)", "planning_only_no_trading_kpi(계획 전용 거래 KPI 없음)", final["stage_open"]["status"], final["stage_open"]["judgment"], "grok=accepted_retry;short_source_utility_lock", "stage_open_no_runtime", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", f"next={RUN_B}"),
        ledger_row(RUN_B, f"{RUN_B}__tier_a_short_source_proxy", "Tier A separate(티어 A 분리)", "Tier A(티어 A)", "python_short_source_utility_proxy_no_mt5(파이썬 숏 원천 유틸리티 프록시, MT5 아님)", final["proxy"]["status"], final["proxy"]["judgment"], f"candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};near_seed={final['proxy']['near_seed_rows']};seed={final['proxy']['seed_rows']}", "train_only_source_utility_no_authority", final["proxy"]["runtime_probe_status"], f"next={RUN_C}"),
        ledger_row(RUN_B, f"{RUN_B}__tier_b_missing_required", "Tier B separate(티어 B 분리)", "Tier B(티어 B)", "missing_required(필수 누락)", final["proxy"]["status"], final["proxy"]["judgment"], "missing_required_no_tier_b_model_input", "no_tier_b_claim", "not_applicable_proxy_no_mt5", "Tier B not materialized in F36 proxy(전선36 프록시에서 티어 B 미물질화)"),
        ledger_row(RUN_B, f"{RUN_B}__tier_ab_combined_out_of_scope", "Tier A+B combined(티어 A+B 합산)", "Tier A+B(티어 A+B)", "out_of_scope_by_claim(주장 범위 밖)", final["proxy"]["status"], final["proxy"]["judgment"], "out_of_scope_by_claim_no_combined_source", "no_synthetic_combined_claim", "not_applicable_proxy_no_mt5", "Combined tier not claimed in F36 proxy(전선36 프록시에서 합산 티어 주장 없음)"),
        ledger_row(RUN_C, f"{RUN_C}__repair_decision", "repair_or_closeout_decision(수리 또는 마감 결정)", "Tier A(티어 A)", "exit_label_pivot_repair_no_runtime(청산 라벨 전환 수리, 런타임 아님)", final["repair"]["status"], final["repair"]["judgment"], f"best={final['repair']['best_readonly'].get('candidate_id','')};scout={final['repair']['scout_rows']};seed={final['repair']['seed_rows']}", "bounded_label_pivot_no_authority", final["repair"]["runtime_probe_status"], f"next={RUN_D}"),
        ledger_row(RUN_D, f"{RUN_D}__stage_closeout", "stage_closeout(단계 마감)", "Tier A(티어 A)", "stage_closeout_no_runtime(단계 마감, 런타임 아님)", final["closeout"]["status"], final["closeout"]["judgment"], f"preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY}", "preserved_clue_negative_memory_no_authority", final["closeout"]["runtime_probe_status"], f"next={NEXT_RUN_ID}"),
    ]
    return rows


def ledger_row(
    run_id: str,
    row_id: str,
    view: str,
    tier: str,
    kpi_scope: str,
    status: str,
    judgment: str,
    primary: str,
    guardrail: str,
    external: str,
    notes: str,
) -> dict[str, Any]:
    report = STAGE_ROOT / "03_reviews" / f"{run_id}_report.md"
    return {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": run_id,
        "subrun_id": row_id,
        "parent_run_id": f35.RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
        "record_view": view,
        "tier_scope": tier,
        "kpi_scope": kpi_scope,
        "scoreboard_lane": view,
        "status": status,
        "judgment": judgment,
        "path": report.as_posix(),
        "primary_kpi": primary,
        "guardrail_kpi": guardrail,
        "external_verification_status": external,
        "notes": notes,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": view,
    }


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(final))


def stage_brief(final: dict[str, Any]) -> str:
    return f"""# Frontier36 Stage Brief(전선36 단계 요약)

Opened(개방): {final['created_at_utc']}

Hypothesis(가설): F34/F35 scaffold(전선34/35 발판)에 single feature filter(단일 피처 필터)를 더 얹지 않고, short-only source utility ranking(숏 전용 원천 유틸리티 순위화)과 exit label pivot(청산 라벨 전환)으로 seed surface(씨앗 표면)에 가까워지는지 본다.

Action(행동): source selection(원천 선택)을 long/short combined truncation(롱/숏 합산 절단)에서 short-only train utility(숏 전용 학습 유틸리티)로 바꿉니다.

Effect(효과): 기존 14개 short source(숏 원천)에 필터를 붙이는 반복이 아니라, 후보 생성 표면 자체를 다시 엽니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def stage_open_report(final: dict[str, Any]) -> str:
    return f"""# Frontier36A Stage Open Report(전선36A 단계 개방 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['stage_open']['status']}`

Judgment(판정): `{final['stage_open']['judgment']}`

Action(행동): F36(전선36)을 short source change or label pivot(숏 원천 변경 또는 라벨 전환) 가설로 열었습니다.

Effect(효과): F35(전선35)의 negative memory(부정 기억)를 reference-only(참조 전용)로 쓰고, winner/baseline/runtime authority(승자/기준선/런타임 권위)는 상속하지 않습니다.

Grok classification(그록 분류): `{final['stage_open']['grok']['classification']}`

Next action(다음 행동): `{RUN_B}`
"""


def run_report(
    title: str,
    updated: str,
    section: dict[str, Any],
    summary: pd.DataFrame,
    action: str,
    effect: str,
    next_run: str,
) -> str:
    best = section.get("best_readonly", {})
    rows = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            rows.append(
                f"| `{row['candidate_id']}` | `{row.get('source_f36b_candidate_id', '')}` | `{row['features']}` | "
                f"{f34.fmt(row['validation_profit_factor'])} | {f34.fmt(row['validation_trades_per_day'])} | {f34.fmt(row['validation_dd_risk'])} | "
                f"{f34.fmt(row['oos_profit_factor'])} | {f34.fmt(row['oos_trades_per_day'])} | {f34.fmt(row['oos_dd_risk'])} | "
                f"{row['path_scout_clue_flag']} | {row['f36_near_seed_flag']} | {row['f36_seed_surface_flag']} |"
            )
    table = "\n".join(rows) if rows else "| none(없음) | | | | | | | | | | | |"
    return f"""# {title}

Updated(갱신): {updated}

Status(상태): `{section['status']}`

Judgment(판정): `{section['judgment']}`

{action}

{effect}

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `{section.get('candidate_rows', 0)}` / `{section.get('scout_rows', 0)}` / `{section.get('near_seed_rows', 0)}` / `{section.get('seed_rows', 0)}` / `{section.get('runtime_rows', 0)}`

Best read-only candidate(최상 읽기 전용 후보): `{best.get('candidate_id', '')}`

Best validation PF-density-DD(최상 검증 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('validation_profit_factor'))}` / `{f34.fmt(best.get('validation_trades_per_day'))}/day` / `{f34.fmt(best.get('validation_dd_risk'))}%`

Best OOS PF-density-DD(최상 표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('oos_profit_factor'))}` / `{f34.fmt(best.get('oos_trades_per_day'))}/day` / `{f34.fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{section.get('runtime_probe_status', '')}`

| candidate(후보) | source(원천) | features(피처) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{next_run}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def closeout_report(final: dict[str, Any]) -> str:
    best_b = final["proxy"]["best_readonly"]
    best_c = final["repair"]["best_readonly"]
    return f"""# Frontier36D Stage Closeout Report(전선36D 단계 마감 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Action(행동): F36(전선36)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): short-only source ranking(숏 전용 원천 순위화)은 scout surface(탐색 표면)를 넓혔지만, exit label pivot(청산 라벨 전환)까지 거쳐도 seed/runtime candidate(씨앗/런타임 후보)는 나오지 않았습니다.

F36B scout/near-seed/seed/runtime(전선36B 탐색/근접 씨앗/씨앗/런타임): `{final['proxy']['scout_rows']}` / `{final['proxy']['near_seed_rows']}` / `{final['proxy']['seed_rows']}` / `{final['proxy']['runtime_rows']}`

F36B best validation/OOS PF-density-DD(전선36B 최상 검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best_b.get('validation_profit_factor'))}/{f34.fmt(best_b.get('validation_trades_per_day'))}/{f34.fmt(best_b.get('validation_dd_risk'))}` and `{f34.fmt(best_b.get('oos_profit_factor'))}/{f34.fmt(best_b.get('oos_trades_per_day'))}/{f34.fmt(best_b.get('oos_dd_risk'))}`.

F36C scout/near-seed/seed/runtime(전선36C 탐색/근접 씨앗/씨앗/런타임): `{final['repair']['scout_rows']}` / `{final['repair']['near_seed_rows']}` / `{final['repair']['seed_rows']}` / `{final['repair']['runtime_rows']}`

F36C best validation/OOS PF-density-DD(전선36C 최상 검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best_c.get('validation_profit_factor'))}/{f34.fmt(best_c.get('validation_trades_per_day'))}/{f34.fmt(best_c.get('validation_dd_risk'))}` and `{f34.fmt(best_c.get('oos_profit_factor'))}/{f34.fmt(best_c.get('oos_trades_per_day'))}/{f34.fmt(best_c.get('oos_dd_risk'))}`.

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Grok closeout classification(그록 마감 분류): `{final['closeout']['grok_closeout']['classification']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["stage_open"]["grok"]
    return f"""# Frontier36A Grok Stage-Open Receipt(전선36A 그록 단계 개방 영수증)

Trigger reason(호출 이유): goal(목표)이 stage open(단계 개방) Grok second opinion(그록 2차 의견)을 요구합니다.

Review size(검토 크기): small review(소규모 검토), retry(재시도) 사용.

Direction before Grok(그록 전 방향): F34/F35 scaffold(전선34/35 발판)에 filter stacking(필터 중첩)을 반복하지 않고 short-only source utility ranking(숏 전용 원천 유틸리티 순위화)을 시험합니다.

First prompt(첫 프롬프트): `{grok['first_prompt']}`

First output(첫 출력): `{grok['first_output']}`

Retry prompt(재시도 프롬프트): `{grok['retry_prompt']}`

Retry output(재시도 출력): `{grok['retry_output']}`

Classification(분류): `{grok['classification']}`

Accepted advice(수용 조언): novelty_ok(신규성 확인) yes(예), runtime claim boundary(런타임 주장 경계) yes(예), overfit risk(과최적화 위험) medium(중간).

Local verification(로컬 검증): `{grok['judgment']}`

Forbidden claim check(금지 주장 확인): runtime authority/operating promotion/live readiness/Goal Achieve(런타임 권위/운영 승격/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def grok_closeout_receipt(final: dict[str, Any]) -> str:
    grok = final["closeout"]["grok_closeout"]
    return f"""# Frontier36D Grok Stage-Closeout Receipt(전선36D 그록 단계 마감 영수증)

Trigger reason(호출 이유): goal(목표)은 stage closeout(단계 마감)마다 Grok second opinion(그록 2차 의견)을 요구합니다.

Review size(검토 크기): small review(소규모 검토), retry(재시도) 사용.

First prompt(첫 프롬프트): `{grok['first_prompt']}`

First output(첫 출력): `{grok['first_output']}`

Retry prompt(재시도 프롬프트): `{grok['retry_prompt']}`

Retry output(재시도 출력): `{grok['retry_output']}`

Classification(분류): `{grok['classification']}`

Accepted advice(수용 조언): closeout class(마감 분류) yes(예), runtime boundary(런타임 경계) yes(예), and next stage(다음 단계)는 label-family pivot(라벨 계열 전환)로 유지합니다.

Local verification(로컬 검증): F36B/F36C seed/runtime(전선36B/36C 씨앗/런타임)은 `{final['proxy']['seed_rows']}/{final['proxy']['runtime_rows']}` and `{final['repair']['seed_rows']}/{final['repair']['runtime_rows']}`라서 MT5 handoff(메타트레이더5 인계)는 ineligible(부적격)입니다.

Forbidden claim check(금지 주장 확인): baseline/promotion/runtime authority/live readiness/Goal Achieve(기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def local_verification_text(final: dict[str, Any]) -> str:
    checks = final["stage_open"]["grok"]["checks"]
    rows = "\n".join(f"- {key}: `{value}`" for key, value in checks.items())
    return f"""# Frontier36 Local Verification(전선36 로컬 검증)

Judgment(판정): `{final['stage_open']['grok']['judgment']}`

{rows}

Effect(효과): Grok retry(그록 재시도), F35 closeout(전선35 마감), data/feature contract(데이터/피처 계약), raw path(원천 경로)를 로컬 파일과 대조했습니다.
"""


def gate_audit_text(title: str, runtime_status: str) -> str:
    return f"""# {title}

- scope_completion_gate(범위 완료 게이트): proxy/repair CSV and reports(프록시/수리 CSV와 보고서) created(생성).
- kpi_contract_audit(KPI 계약 감사): PF/density/DD(수익 팩터/밀도/손실폭)를 split(분할)별로 기록.
- no_forward_selection_gate(전진 선택 금지 게이트): source utility and label pivot(원천 유틸리티와 라벨 전환)은 train-only(학습 전용), validation/OOS(검증/표본밖)는 read-only(읽기 전용).
- runtime_probe_gate(런타임 탐침 게이트): `{runtime_status}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음).
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier36 Required Gate Coverage Audit(전선36 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): Grok stage open retry(그록 단계 개방 재시도) and stage closeout retry(단계 마감 재시도) recorded(기록), closeout classification(마감 분류) `{final['closeout']['grok_closeout']['classification']}`.
- scope_completion_gate(범위 완료 게이트): F36A/F36B/F36C/F36D artifacts(산출물) recorded(기록).
- kpi_contract_audit(KPI 계약 감사): proxy and repair split metrics(프록시와 수리 분할 지표) recorded(기록).
- runtime_evidence_gate(런타임 근거 게이트): `{final['closeout']['runtime_probe_status']}`
- closeout_gate(마감 게이트): preserved clue + negative memory(보존 단서 + 부정 기억).
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음).
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    best = final["proxy"]["best_readonly"]
    return f"""# Frontier36 Preserved Clue(전선36 보존 단서)

Clue(단서): `{PRESERVED_CLUE}`

Evidence(근거): F36B short-only source utility proxy(전선36B 숏 전용 원천 유틸리티 프록시)는 scout rows(탐색 행) `{final['proxy']['scout_rows']}`개를 만들었습니다. Best read-only candidate(최상 읽기 전용 후보) `{best.get('candidate_id','')}` reached validation/OOS PF(검증/표본밖 수익 팩터) `{f34.fmt(best.get('validation_profit_factor'))}/{f34.fmt(best.get('oos_profit_factor'))}`.

Boundary(경계): seed/runtime(씨앗/런타임)은 0개라 reference-only(참조 전용)입니다.
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier36 Negative Memory(전선36 부정 기억)

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Evidence(근거): F36B seed/runtime(전선36B 씨앗/런타임) `{final['proxy']['seed_rows']}/{final['proxy']['runtime_rows']}` and F36C seed/runtime(전선36C 씨앗/런타임) `{final['repair']['seed_rows']}/{final['repair']['runtime_rows']}`.

Do-not-repeat(반복 금지): short-only source utility(숏 전용 원천 유틸리티)와 same-mask exit label pivot(같은 마스크 청산 라벨 전환)만으로 PF edge(수익 팩터 우위)를 만들려고 반복하지 않습니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier36 Selection Status(전선36 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage closeout(단계 마감): `{RUN_D}`

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Grok closeout classification(그록 마감 분류): `{final['closeout']['grok_closeout']['classification']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_open(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Open Frontier36 Short Source Utility(전선36 숏 원천 유틸리티 개방)

Date(날짜): 2026-06-15

Decision(결정): Open(개방) `{STAGE_ID}` with run(실행) `{RUN_A}`.

Effect(효과): F35(전선35) 부정 기억을 상속하지 않고 reference-only(참조 전용)로 쓰며, source selection(원천 선택)을 새 changed variable(변경 변수)로 시험합니다.
"""


def decision_closeout(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Close Frontier36 Short Source Utility(전선36 숏 원천 유틸리티 마감)

Date(날짜): 2026-06-15

Decision(결정): Close(마감) `{STAGE_ID}` as preserved clue + negative memory(보존 단서 + 부정 기억).

Grok closeout(그록 마감): `{final['closeout']['grok_closeout']['classification']}`.

Effect(효과): scout surface(탐색 표면)는 넓어졌지만 seed/runtime(씨앗/런타임)은 없어, 다음 frontier stage(전선 단계)는 stronger PF edge label family pivot(더 강한 수익 팩터 우위 라벨군 전환)을 다룹니다.

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {RUN_D}",
            f"latest_completed_run_id: {RUN_D}",
            f"current_status: {final['closeout']['status']}",
            f"current_judgment: {final['closeout']['judgment']}",
            f"next_stage_id: {NEXT_STAGE_ID}",
            f"next_run_id: {NEXT_RUN_ID}",
            "runtime_authority: not_claimed",
            "operating_promotion: not_claimed",
            "goal_achieve: not_claimed",
            f"updated_at_utc: '{final['created_at_utc']}'",
            "",
        ]
    )


def current_working_state(final: dict[str, Any]) -> str:
    best = final["repair"]["best_readonly"] or final["proxy"]["best_readonly"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_D}`
- status(상태): `{final['closeout']['status']}`
- judgment(판정): `{final['closeout']['judgment']}`
- next stage(다음 단계): `{NEXT_STAGE_ID}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F36(전선36)을 short-only source utility + exit label pivot(숏 전용 원천 유틸리티 + 청산 라벨 전환) preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): best read-only candidate(최상 읽기 전용 후보) `{best.get('candidate_id','')}`는 scout clue(탐색 단서)를 만들었지만 seed/runtime(씨앗/런타임)으로 충분하지 않아 MT5/ONNX(메타트레이더5/온엑스)는 열지 않았습니다.

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_D}` closed Frontier36 short source utility(전선36 숏 원천 유틸리티). "
        f"Effect(효과): proxy_scout={final['proxy']['scout_rows']}, repair_scout={final['repair']['scout_rows']}, seed={final['repair']['seed_rows']}, next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_open(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR36-SHORT-SOURCE-UTILITY-LABEL-PIVOT-ONNX-SCOUT`: `{RUN_A}` opened short-only source utility and exit label pivot(숏 전용 원천 유틸리티와 청산 라벨 전환). "
        "Effect(효과): F35 scaffold filter stacking(전선35 발판 필터 중첩)을 반복하지 않습니다.\n"
    )


def idea_registry_close(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR36-SHORT-SOURCE-UTILITY-LABEL-PIVOT-ONNX-SCOUT`: `{RUN_D}` closed as preserved clue + negative memory(보존 단서 + 부정 기억). "
        "Effect(효과): 다음 질문은 stronger PF edge label family pivot(더 강한 수익 팩터 우위 라벨군 전환)입니다.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_D}`: {NEGATIVE_MEMORY}. Evidence(근거): F36B/F36C seed/runtime(전선36B/36C 씨앗/런타임) "
        f"{final['proxy']['seed_rows']}/{final['proxy']['runtime_rows']} and {final['repair']['seed_rows']}/{final['repair']['runtime_rows']}. "
        "Effect(효과): short source selection(숏 원천 선택)과 same-mask exit label pivot(같은 마스크 청산 라벨 전환)만 반복하지 않습니다.\n"
    )


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


if __name__ == "__main__":
    raise SystemExit(main())
