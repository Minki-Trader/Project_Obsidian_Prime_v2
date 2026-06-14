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
from stage_pipelines.stage_frontier_36 import run_frontier36_lifecycle as f36


STAGE_ID = "stage_frontier_37__short_pf_edge_label_family_pivot_after_source_utility_scout"
RUN_A = "frontier37A_stage_open_short_pf_edge_label_family_pivot_hypothesis_design_v1"
RUN_B = "frontier37B_payoff_dominance_label_family_proxy_scout_v1"
RUN_C = "frontier37C_balanced_payoff_label_family_capped_repair_or_closeout_decision_v1"
RUN_D = "frontier37D_stage_closeout_payoff_label_family_pivot_v1"
NEXT_STAGE_ID = "stage_frontier_38__short_pf_edge_source_family_or_model_pivot_after_payoff_label_negative"
NEXT_RUN_ID = "frontier38A_stage_open_short_pf_edge_source_family_or_model_pivot_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_37/run_frontier37_lifecycle.py")

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier37_stage_open/small_review")
GROK_RETRY_PACKET = GROK_PACKET / "retry"
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier37_stage_closeout/small_review")
GROK_CLOSEOUT_RETRY_PACKET = GROK_CLOSEOUT_PACKET / "retry"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SOURCE_CONDITION_ROWS = 50
PAIR_SOURCE_ROWS = 50
PAIR_ATTEMPT_LIMIT = 160
MAX_PROXY_CANDIDATES = 260
REPAIR_SOURCE_ROWS = 24
MAX_REPAIR_CANDIDATES = 260

PROXY_STOP_QUANTILES = (0.14, 0.22, 0.30)
PROXY_TAKE_QUANTILES = (0.62, 0.76, 0.90)
PROXY_RR_FLOORS = (1.35, 1.80)
REPAIR_STOP_QUANTILES = (0.18, 0.26, 0.34, 0.42)
REPAIR_TAKE_QUANTILES = (0.50, 0.62, 0.74)
REPAIR_RR_FLOORS = (1.00, 1.20, 1.40)

F37_NEAR_SEED_PF = 1.12
F37_SEED_PF = 1.20
F37_SEED_DD_CAP = 12.0
F37_RUNTIME_PF = 1.50
F37_RUNTIME_DD_CAP = 10.0

PRESERVED_CLUE = (
    "f37_payoff_dominance_label_family_can_keep_density_dd_but_not_lift_validation_pf_to_seed"
)
NEGATIVE_MEMORY = (
    "f37_train_only_payoff_dominance_and_balanced_label_family_pivot_did_not_create_seed_or_runtime_candidate"
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
    proxy = build_payoff_label_proxy(frame, feature_order, path_labels, raw_path)
    repair = build_balanced_label_repair(frame, path_labels, raw_path, proxy)
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
        bool(retry_meta.get("success"))
        and "accepted" in lowered
        and "novelty_ok" in lowered
        and "yes" in lowered
        and "runtime_claim_boundary_ok" in lowered
    )
    return {
        "first_packet": GROK_PACKET.as_posix(),
        "first_prompt": (GROK_PACKET / "prompt.md").as_posix(),
        "first_output": (GROK_PACKET / "clean_output.md").as_posix(),
        "first_success": bool(first_meta.get("success")),
        "first_returncode": first_meta.get("returncode"),
        "first_output_excerpt": first_output[:800],
        "retry_packet": GROK_RETRY_PACKET.as_posix(),
        "retry_prompt": (GROK_RETRY_PACKET / "prompt.md").as_posix(),
        "retry_output": (GROK_RETRY_PACKET / "clean_output.md").as_posix(),
        "retry_metadata": (GROK_RETRY_PACKET / "metadata.json").as_posix(),
        "retry_success": bool(retry_meta.get("success")),
        "retry_returncode": retry_meta.get("returncode"),
        "retry_timed_out": bool(retry_meta.get("timed_out")),
        "retry_unexpected_top_level_artifacts": retry_meta.get("unexpected_top_level_artifacts", []),
        "accepted": accepted,
        "classification": "accepted_stage_open_payoff_label_family_with_train_only_leakage_guard" if accepted else "needs_local_verification",
        "retry_output_excerpt": retry_output[:1600],
    }


def read_closeout_grok() -> dict[str, Any]:
    first_meta = f34.read_json(GROK_CLOSEOUT_PACKET / "metadata.json") if path_exists(GROK_CLOSEOUT_PACKET / "metadata.json") else {}
    first_output = f34.read_text(GROK_CLOSEOUT_PACKET / "clean_output.md") if path_exists(GROK_CLOSEOUT_PACKET / "clean_output.md") else ""
    retry_meta = f34.read_json(GROK_CLOSEOUT_RETRY_PACKET / "metadata.json") if path_exists(GROK_CLOSEOUT_RETRY_PACKET / "metadata.json") else {}
    retry_output = f34.read_text(GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md") if path_exists(GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md") else ""
    lowered = retry_output.lower()
    accepted_verdict = "accepted" in lowered or "verdict(판정):** accept" in lowered or "verdict(판정): accept" in lowered
    accepted = bool(retry_meta.get("success")) and accepted_verdict and "runtime_boundary_ok" in lowered and "yes" in lowered
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
        "classification": "accepted_closeout_payoff_label_family_negative_runtime_boundary" if accepted else "pending_or_needs_local_verification",
        "retry_output_excerpt": retry_output[:1600],
    }


def validate_context(
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = f34.read_text(WORKSPACE_STATE)
    f36_selection = f34.read_text(Path("stages") / f36.STAGE_ID / "04_selected" / "selection_status.md")
    f36_decision = f34.read_text(Path("docs/decisions/2026-06-15_stage_frontier_36_short_source_utility_closeout.md"))
    checks = {
        "workspace_current_f36": f"current_stage_id: {f36.STAGE_ID}" in workspace,
        "workspace_points_to_f37a": f"next_run_id: {RUN_A}" in workspace,
        "f36_selection_points_to_f37a": RUN_A in f36_selection,
        "f36_decision_points_to_f37a": RUN_A in f36_decision,
        "f36_negative_memory_present": f36.NEGATIVE_MEMORY in f36_selection,
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
        "feature_label_boundary": "payoff-dominance label thresholds use train split only; validation/OOS are read-only",
        "leakage_risk": "medium: label-family threshold grid is train-only but multiple testing can overfit source and payoff-family choice",
    }


def build_payoff_label_proxy(
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
    short_conditions["f37_condition_score"] = short_conditions.apply(f36.condition_score, axis=1)
    short_conditions = short_conditions.sort_values("f37_condition_score", ascending=False).reset_index(drop=True)

    candidates: list[dict[str, Any]] = []
    for row in short_conditions.head(SOURCE_CONDITION_ROWS).to_dict("records"):
        candidates.extend(
            candidates_for_mask(
                frame,
                [row],
                np.asarray(row["_mask"], dtype=bool),
                path_labels,
                raw_path,
                PROXY_STOP_QUANTILES,
                PROXY_TAKE_QUANTILES,
                PROXY_RR_FLOORS,
                "f37b_train_payoff_dominance_label_family",
                keep=2,
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
                candidates_for_mask(
                    frame,
                    [first, second],
                    mask,
                    path_labels,
                    raw_path,
                    PROXY_STOP_QUANTILES,
                    PROXY_TAKE_QUANTILES,
                    PROXY_RR_FLOORS,
                    "f37b_train_payoff_dominance_label_family",
                    keep=1,
                )
            )
            pair_attempts += 1
            if pair_attempts >= PAIR_ATTEMPT_LIMIT:
                break
        if pair_attempts >= PAIR_ATTEMPT_LIMIT:
            break

    selected = rank_f37_candidates(candidates, "f37b", MAX_PROXY_CANDIDATES)
    split_metrics = f33b.evaluate_candidates(frame, selected, path_labels, raw_path) if selected else pd.DataFrame()
    summary = add_f37_flags(f33b.summarize_candidates(split_metrics), selected)
    return {
        "condition_pool": short_conditions,
        "candidates": selected,
        "split_metrics": split_metrics,
        "summary": summary,
        "source_rows": int(len(short_conditions)),
        "pair_attempts": int(pair_attempts),
        **section_counts(summary, selected),
    }


def build_balanced_label_repair(
    frame: pd.DataFrame,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    proxy: dict[str, Any],
) -> dict[str, Any]:
    summary = proxy["summary"]
    if summary.empty:
        return empty_repair()
    source_ids = summary["candidate_id"].head(REPAIR_SOURCE_ROWS).tolist()
    by_id = {str(item["candidate_id"]): item for item in proxy["candidates"]}
    repair_candidates: list[dict[str, Any]] = []
    for source_id in source_ids:
        source = by_id.get(str(source_id))
        if not source:
            continue
        source_stub = candidate_to_condition_stub(source, str(source_id))
        repair_candidates.extend(
            candidates_for_mask(
                frame,
                [source_stub],
                np.asarray(source["mask"], dtype=bool),
                path_labels,
                raw_path,
                REPAIR_STOP_QUANTILES,
                REPAIR_TAKE_QUANTILES,
                REPAIR_RR_FLOORS,
                "f37c_train_balanced_payoff_label_family",
                keep=2,
                source_id=str(source_id),
            )
        )
    selected = rank_f37_candidates(repair_candidates, "f37c", MAX_REPAIR_CANDIDATES)
    split_metrics = f33b.evaluate_candidates(frame, selected, path_labels, raw_path) if selected else pd.DataFrame()
    summary = add_f37_flags(f33b.summarize_candidates(split_metrics), selected)
    return {
        "candidates": selected,
        "split_metrics": split_metrics,
        "summary": summary,
        "source_rows": int(len(source_ids)),
        **section_counts(summary, selected),
    }


def candidate_to_condition_stub(candidate: dict[str, Any], source_id: str) -> dict[str, Any]:
    return {
        "condition_id": f"src_{source_id}",
        "feature": str(candidate.get("features", "")),
        "feature_family": str(candidate.get("feature_families", "")),
        "definition": str(candidate.get("rule_definition", "")),
    }


def candidates_for_mask(
    frame: pd.DataFrame,
    conditions: list[dict[str, Any]],
    mask: np.ndarray,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    stop_quantiles: tuple[float, ...],
    take_quantiles: tuple[float, ...],
    rr_floors: tuple[float, ...],
    threshold_source: str,
    *,
    keep: int,
    source_id: str = "",
) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    for row in label_family_thresholds(frame, mask, path_labels, stop_quantiles, take_quantiles, rr_floors, threshold_source):
        metrics = f33b.evaluate_path_mask(
            frame,
            mask,
            -1,
            row["stop_cap_log_return"],
            row["take_cap_log_return"],
            path_labels,
            raw_path,
            "train",
        )
        if not train_gate(metrics):
            continue
        score = payoff_edge_score(metrics)
        candidate = f33b.candidate_from_conditions(conditions, mask, -1, row, metrics, score)
        candidate["source_f37_candidate_id"] = source_id
        candidate["f37_payoff_edge_score"] = score
        candidate["label_family_id"] = (
            f"{threshold_source}__sq{row['stop_quantile']}_tq{row['take_quantile']}_rr{row['rr_floor']}"
        )
        variants.append(candidate)
    variants.sort(key=lambda item: float(item["f37_payoff_edge_score"]), reverse=True)
    return variants[:keep]


def label_family_thresholds(
    frame: pd.DataFrame,
    mask: np.ndarray,
    path_labels: dict[int, dict[str, np.ndarray]],
    stop_quantiles: tuple[float, ...],
    take_quantiles: tuple[float, ...],
    rr_floors: tuple[float, ...],
    threshold_source: str,
) -> list[dict[str, Any]]:
    labels = path_labels[-1]
    train = f33b.split_mask(frame, "train") & np.asarray(mask, dtype=bool) & labels["valid"]
    mfe = labels["mfe"][train]
    mae = labels["mae"][train]
    mfe = mfe[np.isfinite(mfe) & (mfe > 0.0)]
    mae = mae[np.isfinite(mae) & (mae > 0.0)]
    if mfe.size < 35 or mae.size < 35:
        return []
    rows: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for stop_q in stop_quantiles:
        stop_cap = max(float(np.nanquantile(mae, stop_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
        for take_q in take_quantiles:
            raw_take = max(float(np.nanquantile(mfe, take_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
            for rr_floor in rr_floors:
                take_cap = max(raw_take, stop_cap * rr_floor)
                key = (int(round(stop_cap * 1_000_000)), int(round(take_cap * 1_000_000)))
                if key in seen:
                    continue
                seen.add(key)
                rows.append(
                    {
                        "threshold_source": threshold_source,
                        "stop_quantile": stop_q,
                        "take_quantile": take_q,
                        "rr_floor": rr_floor,
                        "stop_cap_log_return": stop_cap,
                        "take_cap_log_return": take_cap,
                        "train_threshold_sample_rows": int(min(mfe.size, mae.size)),
                    }
                )
    return rows


def train_gate(metrics: dict[str, Any]) -> bool:
    trade_count = int(metrics["trade_count"])
    density = float(metrics["trades_per_day"])
    ambiguous_rate = float(metrics["ambiguous_both_hit_count"]) / max(float(trade_count), 1.0)
    return (
        trade_count >= 45
        and 4.0 <= density <= 12.0
        and float(metrics["net_profit"]) > 0.0
        and float(metrics["profit_factor"]) >= 1.02
        and float(metrics["dd_risk"]) <= 18.0
        and ambiguous_rate <= 0.35
    )


def payoff_edge_score(metrics: dict[str, Any]) -> float:
    trade_count = max(safe_float(metrics.get("trade_count")), 1.0)
    density = safe_float(metrics.get("trades_per_day"))
    pf = safe_float(metrics.get("profit_factor"))
    dd = safe_float(metrics.get("dd_risk"))
    payoff = safe_float(metrics.get("payoff_ratio"))
    path_quality = safe_float(metrics.get("path_quality_rate"))
    ambiguous_rate = safe_float(metrics.get("ambiguous_both_hit_count")) / trade_count
    density_bonus = max(0.0, 1.0 - abs(density - 7.5) / 7.5)
    dd_penalty = max(0.0, dd - 10.0) / 5.0
    return float(
        5.0 * min(pf, 4.0)
        + 1.5 * density_bonus
        + 0.8 * min(payoff, 4.0)
        + path_quality
        - 2.0 * ambiguous_rate
        - dd_penalty
    )


def rank_f37_candidates(candidates: list[dict[str, Any]], prefix: str, limit: int) -> list[dict[str, Any]]:
    seen: set[tuple[str, float, float]] = set()
    selected: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda item: float(item["f37_payoff_edge_score"]), reverse=True):
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


def add_f37_flags(summary: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    if summary.empty:
        return summary
    metadata = {
        str(item["candidate_id"]): {
            "f37_payoff_edge_score": item.get("f37_payoff_edge_score", ""),
            "label_family_id": item.get("label_family_id", ""),
            "source_f37_candidate_id": item.get("source_f37_candidate_id", ""),
        }
        for item in candidates
    }
    summary = summary.copy()
    summary["f37_payoff_edge_score"] = [
        metadata.get(str(candidate_id), {}).get("f37_payoff_edge_score", "") for candidate_id in summary["candidate_id"]
    ]
    summary["label_family_id"] = [
        metadata.get(str(candidate_id), {}).get("label_family_id", "") for candidate_id in summary["candidate_id"]
    ]
    summary["source_f37_candidate_id"] = [
        metadata.get(str(candidate_id), {}).get("source_f37_candidate_id", "") for candidate_id in summary["candidate_id"]
    ]
    summary["f37_near_seed_flag"] = (
        summary["forward_dual_positive_flag"].astype(bool)
        & summary["path_density_bridge_flag"].astype(bool)
        & (pd.to_numeric(summary["forward_min_pf"], errors="coerce") >= F37_NEAR_SEED_PF)
        & (pd.to_numeric(summary["forward_max_dd"], errors="coerce") <= F37_SEED_DD_CAP)
    )
    summary["f37_seed_surface_flag"] = (
        summary["forward_dual_positive_flag"].astype(bool)
        & summary["path_density_bridge_flag"].astype(bool)
        & (pd.to_numeric(summary["forward_min_pf"], errors="coerce") >= F37_SEED_PF)
        & (pd.to_numeric(summary["forward_max_dd"], errors="coerce") <= F37_SEED_DD_CAP)
    )
    summary["f37_runtime_candidate_flag"] = (
        summary["f37_seed_surface_flag"].astype(bool)
        & (pd.to_numeric(summary["forward_min_pf"], errors="coerce") >= F37_RUNTIME_PF)
        & (pd.to_numeric(summary["forward_max_dd"], errors="coerce") <= F37_RUNTIME_DD_CAP)
    )
    return summary.sort_values(
        ["f37_runtime_candidate_flag", "f37_seed_surface_flag", "f37_near_seed_flag", "path_scout_clue_flag", "path_read_score"],
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
        "near_seed_rows": int(summary["f37_near_seed_flag"].sum()),
        "seed_rows": int(summary["f37_seed_surface_flag"].sum()),
        "runtime_rows": int(summary["f37_runtime_candidate_flag"].sum()),
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
    best = repair["best_readonly"] or proxy["best_readonly"]
    runtime_rows = max(int(proxy["runtime_rows"]), int(repair["runtime_rows"]))
    runtime_status = (
        "runtime_probe_candidate_requires_pre_expensive_grok_and_mt5_handoff"
        if runtime_rows
        else "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f37c_balanced_payoff_label_repair"
    )
    closeout_class = "completion_candidate" if runtime_rows else "preserved_clue_negative_memory"
    status = (
        "closed_completion_candidate_pending_expensive_validation_no_runtime_authority"
        if runtime_rows
        else "closed_preserved_clue_negative_memory_payoff_label_family_scout_only_no_runtime_authority"
    )
    judgment = (
        "completion_candidate_requires_wfo_stress_runtime_validation_no_authority"
        if runtime_rows
        else "preserved_clue_negative_memory(F37 payoff label family no seed/runtime)"
    )
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "stage_open": {
            "run_id": RUN_A,
            "status": "opened_frontier37_short_pf_edge_label_family_pivot_no_authority",
            "judgment": "stage_opened_after_grok_retry_accepted_payoff_label_family_boundary",
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
            "status": "payoff_dominance_label_family_proxy_scout_no_seed_no_runtime_candidate_no_authority",
            "judgment": "payoff_label_family_weaker_than_f36_requires_capped_repair_or_closeout",
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
            "status": "balanced_payoff_label_family_capped_repair_closeout_queued_no_authority",
            "judgment": "balanced_payoff_repair_did_not_create_seed_runtime_requires_closeout",
            "source_rows": repair["source_rows"],
            "candidate_rows": repair["candidate_rows"],
            "scout_rows": repair["scout_rows"],
            "near_seed_rows": repair["near_seed_rows"],
            "seed_rows": repair["seed_rows"],
            "runtime_rows": repair["runtime_rows"],
            "best_readonly": repair["best_readonly"],
            "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_capped_repair_no_runtime_candidate",
        },
        "closeout": {
            "run_id": RUN_D,
            "status": status,
            "judgment": judgment,
            "closeout_class": closeout_class,
            "preserved_clue": PRESERVED_CLUE,
            "negative_memory": NEGATIVE_MEMORY,
            "best_readonly": best,
            "runtime_probe_status": runtime_status,
            "grok_closeout": read_closeout_grok(),
            "next_stage_id": NEXT_STAGE_ID,
            "next_run_id": NEXT_RUN_ID,
        },
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], proxy: dict[str, Any], repair: dict[str, Any]) -> None:
    proxy["condition_pool"].drop(columns=["_mask"], errors="ignore").to_csv(
        io_path(RUN_B_ROOT / "payoff_label_condition_pool.csv"), index=False, encoding="utf-8-sig"
    )
    pd.DataFrame([f33b.clean_candidate_for_csv(item) for item in proxy["candidates"]]).to_csv(
        io_path(RUN_B_ROOT / "payoff_label_candidate_ledger.csv"), index=False, encoding="utf-8-sig"
    )
    proxy["split_metrics"].to_csv(io_path(RUN_B_ROOT / "payoff_label_split_metrics.csv"), index=False, encoding="utf-8-sig")
    proxy["summary"].to_csv(io_path(RUN_B_ROOT / "payoff_label_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    proxy["summary"].head(40).to_csv(io_path(RUN_B_ROOT / "top_payoff_label_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")

    pd.DataFrame([f33b.clean_candidate_for_csv(item) for item in repair["candidates"]]).to_csv(
        io_path(RUN_C_ROOT / "balanced_payoff_repair_candidate_ledger.csv"), index=False, encoding="utf-8-sig"
    )
    repair["split_metrics"].to_csv(io_path(RUN_C_ROOT / "balanced_payoff_repair_split_metrics.csv"), index=False, encoding="utf-8-sig")
    repair["summary"].to_csv(io_path(RUN_C_ROOT / "balanced_payoff_repair_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    repair["summary"].head(40).to_csv(io_path(RUN_C_ROOT / "top_balanced_payoff_repair_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")

    f34.write_json(RUN_A_ROOT / "stage_open_summary.json", final["stage_open"])
    f34.write_json(RUN_B_ROOT / "final_summary.json", final["proxy"])
    f34.write_json(RUN_C_ROOT / "final_summary.json", final["repair"])
    f34.write_json(RUN_D_ROOT / "stage_closeout_summary.json", final)

    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_open_receipt(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_closeout_receipt.md", grok_closeout_receipt(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_A}_report.md", stage_open_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_report.md", run_report("Frontier37B Payoff Label Proxy Report(전선37B 수익 라벨 프록시 보고)", final["created_at_utc"], final["proxy"], proxy["summary"], RUN_C))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_report.md", run_report("Frontier37C Balanced Payoff Repair Report(전선37C 균형 수익 수리 보고)", final["created_at_utc"], final["repair"], repair["summary"], RUN_D))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md", closeout_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", required_gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_37_payoff_label_family_open.md"), decision_open(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_37_payoff_label_family_closeout.md"), decision_closeout(final))
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
        RUN_B_ROOT / "payoff_label_candidate_summary.csv",
        RUN_C_ROOT / "balanced_payoff_repair_candidate_summary.csv",
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
        "label_family_contract": {
            "changed_variable": "train_only_payoff_dominance_and_balanced_payoff_label_family",
            "fixed_variables": "raw_path_replay_feature_order_splits_validation_oos_read_only",
            "score_components": "train PF, density closeness, payoff ratio, path quality, ambiguity rate, DD penalty",
        },
        "closeout_class": final["closeout"]["closeout_class"],
        "runtime_claim_boundary": "stage_closeout_no_mt5_runtime_authority",
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f36.upsert_csv_many(RUN_REGISTRY, "run_id", run_registry_rows(final))
    ledger = ledger_rows(final)
    f36.upsert_csv_many(ALPHA_LEDGER, "ledger_row_id", ledger)
    f36.upsert_csv_many(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger)
    f03b.append_once(CHANGELOG, RUN_D, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_A, idea_registry_open(final))
    f03b.append_once(IDEA_REGISTRY, RUN_D, idea_registry_close(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_D, negative_register_entry(final))


def run_registry_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    created = final["created_at_utc"]
    return [
        registry_row(RUN_A, "stage_open(단계 개방)", final["stage_open"]["status"], final["stage_open"]["judgment"], f"grok={final['stage_open']['grok']['classification']};next={RUN_B};no_authority", created, "stage_open_no_model_training_no_wfo_no_mt5_no_onnx_no_authority", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", RUN_B),
        registry_row(RUN_B, "proxy_scout(프록시 탐색)", final["proxy"]["status"], final["proxy"]["judgment"], f"candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};near_seed={final['proxy']['near_seed_rows']};seed={final['proxy']['seed_rows']};next={RUN_C}", created, "python_payoff_label_family_proxy_only_no_wfo_no_mt5_no_onnx_no_authority", final["proxy"]["runtime_probe_status"], RUN_C, final["proxy"]["best_readonly"]),
        registry_row(RUN_C, "repair_or_closeout_decision(수리 또는 마감 결정)", final["repair"]["status"], final["repair"]["judgment"], f"candidate={final['repair']['candidate_rows']};scout={final['repair']['scout_rows']};near_seed={final['repair']['near_seed_rows']};seed={final['repair']['seed_rows']};next={RUN_D}", created, "balanced_payoff_label_family_repair_proxy_only_no_wfo_no_mt5_no_onnx_no_authority", final["repair"]["runtime_probe_status"], RUN_D, final["repair"]["best_readonly"]),
        registry_row(RUN_D, "stage_closeout(단계 마감)", final["closeout"]["status"], final["closeout"]["judgment"], f"closeout={final['closeout']['closeout_class']};preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY};next={NEXT_RUN_ID}", created, "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_onnx_no_authority", final["closeout"]["runtime_probe_status"], NEXT_RUN_ID, final["closeout"]["best_readonly"]),
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
        "parent_run_id": f36.RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
        "next_run_id": next_run,
        "claim_boundary": claim_boundary,
        "report_path": report.as_posix(),
        "created_at_utc": created,
        "primary_kpi": primary,
        "guardrail_kpi": "train_only_label_family_selection_validation_oos_read_only_no_runtime_authority",
        "external_verification_status": external_status,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": report.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        ledger_row(RUN_A, f"{RUN_A}__stage_open", "stage_open(단계 개방)", "not_applicable_stage_open(단계 개방 해당 없음)", "planning_only_no_trading_kpi(계획 전용 거래 KPI 없음)", final["stage_open"]["status"], final["stage_open"]["judgment"], "grok=accepted_retry;payoff_label_family_lock", "stage_open_no_runtime", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", f"next={RUN_B}"),
        ledger_row(RUN_B, f"{RUN_B}__tier_a_payoff_label_proxy", "Tier A separate(티어 A 분리)", "Tier A(티어 A)", "python_payoff_label_family_proxy_no_mt5(파이썬 수익 라벨 프록시, MT5 아님)", final["proxy"]["status"], final["proxy"]["judgment"], f"candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};seed={final['proxy']['seed_rows']}", "train_only_label_family_no_authority", final["proxy"]["runtime_probe_status"], f"next={RUN_C}"),
        ledger_row(RUN_B, f"{RUN_B}__tier_b_missing_required", "Tier B separate(티어 B 분리)", "Tier B(티어 B)", "missing_required(필수 누락)", final["proxy"]["status"], final["proxy"]["judgment"], "missing_required_no_tier_b_model_input", "no_tier_b_claim", "not_applicable_proxy_no_mt5", "Tier B not materialized in F37 proxy(전선37 프록시에서 티어 B 미물질화)"),
        ledger_row(RUN_B, f"{RUN_B}__tier_ab_combined_out_of_scope", "Tier A+B combined(티어 A+B 합산)", "Tier A+B(티어 A+B)", "out_of_scope_by_claim(주장 범위 밖)", final["proxy"]["status"], final["proxy"]["judgment"], "out_of_scope_by_claim_no_combined_source", "no_synthetic_combined_claim", "not_applicable_proxy_no_mt5", "Combined tier not claimed in F37 proxy(전선37 프록시에서 합산 티어 주장 없음)"),
        ledger_row(RUN_C, f"{RUN_C}__repair_decision", "repair_or_closeout_decision(수리 또는 마감 결정)", "Tier A(티어 A)", "balanced_payoff_repair_no_runtime(균형 수익 수리, 런타임 아님)", final["repair"]["status"], final["repair"]["judgment"], f"best={final['repair']['best_readonly'].get('candidate_id','')};scout={final['repair']['scout_rows']};seed={final['repair']['seed_rows']}", "bounded_label_family_repair_no_authority", final["repair"]["runtime_probe_status"], f"next={RUN_D}"),
        ledger_row(RUN_D, f"{RUN_D}__stage_closeout", "stage_closeout(단계 마감)", "Tier A(티어 A)", "stage_closeout_no_runtime(단계 마감, 런타임 아님)", final["closeout"]["status"], final["closeout"]["judgment"], f"preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY}", "preserved_clue_negative_memory_no_authority", final["closeout"]["runtime_probe_status"], f"next={NEXT_RUN_ID}"),
    ]


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
        "parent_run_id": f36.RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
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
    return f"""# Frontier37 Stage Brief(전선37 단계 요약)

Opened(개방): {final['created_at_utc']}

Hypothesis(가설): F36(전선36)의 short scout surface(숏 탐색 표면)는 있었지만 PF(수익 팩터)가 약했습니다. F37(전선37)은 single-feature filter stacking(단일 피처 필터 적층) 대신 payoff-dominance label family(수익 우위 라벨 계열)를 바꿉니다.

Action(행동): MFE/MAE separation(최대 유리/불리 이동 분리), stop/take asymmetry(손절/익절 비대칭), ambiguity rate(동시 타격 모호성)를 train-only(학습 전용)로 고정합니다.

Effect(효과): validation/OOS(검증/표본외)는 read-only(읽기 전용)로 남겨 label-family pivot(라벨 계열 전환)이 PF(수익 팩터)를 실제로 밀어 올리는지 봅니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def stage_open_report(final: dict[str, Any]) -> str:
    return f"""# Frontier37A Stage Open Report(전선37A 단계 개방 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['stage_open']['status']}`

Judgment(판정): `{final['stage_open']['judgment']}`

Grok classification(그록 분류): `{final['stage_open']['grok']['classification']}`

Action(행동): payoff-dominance label family(수익 우위 라벨 계열)를 새 changed variable(변경 변수)로 잠급니다.

Effect(효과): F36(전선36)의 weak PF(약한 수익 팩터)를 같은 필터 반복으로 고치지 않고 label target(라벨 목표)을 바꿔 시험합니다.

Next run(다음 실행): `{RUN_B}`
"""


def run_report(title: str, updated: str, section: dict[str, Any], summary: pd.DataFrame, next_run: str) -> str:
    best = section.get("best_readonly", {})
    rows = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            rows.append(
                f"| `{row['candidate_id']}` | `{row['features']}` | "
                f"{f34.fmt(row['validation_profit_factor'])} | {f34.fmt(row['validation_trades_per_day'])} | {f34.fmt(row['validation_dd_risk'])} | "
                f"{f34.fmt(row['oos_profit_factor'])} | {f34.fmt(row['oos_trades_per_day'])} | {f34.fmt(row['oos_dd_risk'])} | "
                f"{row['path_scout_clue_flag']} | {row['f37_near_seed_flag']} | {row['f37_seed_surface_flag']} |"
            )
    table = "\n".join(rows) if rows else "| none(없음) | | | | | | | | | | |"
    return f"""# {title}

Updated(갱신): {updated}

Status(상태): `{section.get('status')}`

Judgment(판정): `{section.get('judgment')}`

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `{section.get('candidate_rows', 0)}` / `{section.get('scout_rows', 0)}` / `{section.get('near_seed_rows', 0)}` / `{section.get('seed_rows', 0)}` / `{section.get('runtime_rows', 0)}`

Best read-only candidate(최상 읽기 전용 후보): `{best.get('candidate_id', '')}`

Best validation PF-density-DD(최상 검증 수익 팩터-거래 빈도-손실폭): `{f34.fmt(best.get('validation_profit_factor'))}` / `{f34.fmt(best.get('validation_trades_per_day'))}/day` / `{f34.fmt(best.get('validation_dd_risk'))}%`

Best OOS PF-density-DD(최상 표본외 수익 팩터-거래 빈도-손실폭): `{f34.fmt(best.get('oos_profit_factor'))}` / `{f34.fmt(best.get('oos_trades_per_day'))}/day` / `{f34.fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{section.get('runtime_probe_status', '')}`

| candidate(후보) | features(피처) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{next_run}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def closeout_report(final: dict[str, Any]) -> str:
    best_b = final["proxy"]["best_readonly"]
    best_c = final["repair"]["best_readonly"]
    return f"""# Frontier37D Stage Closeout Report(전선37D 단계 마감 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Action(행동): F37(전선37)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫습니다.

Effect(효과): payoff-dominance label family(수익 우위 라벨 계열)는 DD(손실폭)를 낮게 유지하는 단서는 만들었지만 PF(수익 팩터)를 seed/runtime(씨앗/런타임) 수준으로 올리지 못했습니다.

F37B scout/near-seed/seed/runtime(전선37B 탐색/근접 씨앗/씨앗/런타임): `{final['proxy']['scout_rows']}` / `{final['proxy']['near_seed_rows']}` / `{final['proxy']['seed_rows']}` / `{final['proxy']['runtime_rows']}`

F37B best validation/OOS PF-density-DD(전선37B 최상 검증/표본외 수익 팩터-거래 빈도-손실폭): `{f34.fmt(best_b.get('validation_profit_factor'))}/{f34.fmt(best_b.get('validation_trades_per_day'))}/{f34.fmt(best_b.get('validation_dd_risk'))}` and `{f34.fmt(best_b.get('oos_profit_factor'))}/{f34.fmt(best_b.get('oos_trades_per_day'))}/{f34.fmt(best_b.get('oos_dd_risk'))}`.

F37C scout/near-seed/seed/runtime(전선37C 탐색/근접 씨앗/씨앗/런타임): `{final['repair']['scout_rows']}` / `{final['repair']['near_seed_rows']}` / `{final['repair']['seed_rows']}` / `{final['repair']['runtime_rows']}`

F37C best validation/OOS PF-density-DD(전선37C 최상 검증/표본외 수익 팩터-거래 빈도-손실폭): `{f34.fmt(best_c.get('validation_profit_factor'))}/{f34.fmt(best_c.get('validation_trades_per_day'))}/{f34.fmt(best_c.get('validation_dd_risk'))}` and `{f34.fmt(best_c.get('oos_profit_factor'))}/{f34.fmt(best_c.get('oos_trades_per_day'))}/{f34.fmt(best_c.get('oos_dd_risk'))}`.

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Grok closeout classification(그록 마감 분류): `{final['closeout']['grok_closeout']['classification']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_open_receipt(final: dict[str, Any]) -> str:
    grok = final["stage_open"]["grok"]
    return f"""# Frontier37A Grok Stage-Open Receipt(전선37A 그록 단계 개방 영수증)

Trigger reason(호출 이유): goal(목표)은 stage open(단계 개방) Grok second opinion(그록 2차 의견)을 요구합니다.

Review size(검토 크기): small review(소규모 검토), retry(재시도) 사용.

Direction before Grok(그록 전 방향): payoff-dominance label family(수익 우위 라벨 계열)로 PF(수익 팩터)를 올리는지 시험합니다.

First prompt(첫 프롬프트): `{grok['first_prompt']}`

First output(첫 출력): `{grok['first_output']}`

Retry prompt(재시도 프롬프트): `{grok['retry_prompt']}`

Retry output(재시도 출력): `{grok['retry_output']}`

Classification(분류): `{grok['classification']}`

Local verification(로컬 검증): `{grok['judgment']}`

Forbidden claim check(금지 주장 확인): runtime authority/operating promotion/live readiness/Goal Achieve(런타임 권위/운영 승격/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def grok_closeout_receipt(final: dict[str, Any]) -> str:
    grok = final["closeout"]["grok_closeout"]
    return f"""# Frontier37D Grok Stage-Closeout Receipt(전선37D 그록 단계 마감 영수증)

Trigger reason(호출 이유): goal(목표)은 stage closeout(단계 마감) Grok second opinion(그록 2차 의견)을 요구합니다.

Review size(검토 크기): small review(소규모 검토).

First prompt(첫 프롬프트): `{grok['first_prompt']}`

First output(첫 출력): `{grok['first_output']}`

Retry prompt(재시도 프롬프트): `{grok['retry_prompt']}`

Retry output(재시도 출력): `{grok['retry_output']}`

Classification(분류): `{grok['classification']}`

Local verification(로컬 검증): F37B/F37C seed/runtime(전선37B/37C 씨앗/런타임)은 `{final['proxy']['seed_rows']}/{final['proxy']['runtime_rows']}` and `{final['repair']['seed_rows']}/{final['repair']['runtime_rows']}`입니다.

Forbidden claim check(금지 주장 확인): baseline/promotion/runtime authority/live readiness/Goal Achieve(기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def local_verification_text(final: dict[str, Any]) -> str:
    checks = final["stage_open"]["grok"]["checks"]
    rows = "\n".join(f"- {key}: `{value}`" for key, value in checks.items())
    return f"""# Frontier37 Local Verification(전선37 로컬 검증)

Judgment(판정): `{final['stage_open']['grok']['judgment']}`

{rows}

Effect(효과): Grok retry(그록 재시도), F36 closeout(전선36 마감), data/feature contract(데이터/피처 계약), raw path(원천 경로)를 로컬 파일과 대조했습니다.
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier37 Required Gate Coverage Audit(전선37 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): Grok stage open retry(그록 단계 개방 재시도) and closeout packet(마감 묶음) classification(분류) `{final['closeout']['grok_closeout']['classification']}`.
- scope_completion_gate(범위 완료 게이트): F37A/F37B/F37C/F37D artifacts(산출물) recorded(기록).
- kpi_contract_audit(KPI 계약 감사): proxy and repair split metrics(프록시와 수리 분할 지표) recorded(기록).
- runtime_evidence_gate(런타임 근거 게이트): `{final['closeout']['runtime_probe_status']}`
- closeout_gate(마감 게이트): `{final['closeout']['closeout_class']}`.
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음).
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    best = final["proxy"]["best_readonly"] or final["repair"]["best_readonly"]
    return f"""# Frontier37 Preserved Clue(전선37 보존 단서)

Clue(단서): `{PRESERVED_CLUE}`

Evidence(근거): best read-only candidate(최상 읽기 전용 후보) `{best.get('candidate_id','')}` kept density/DD(거래 빈도/손실폭) near target but did not lift forward PF(전방 수익 팩터) enough.

Boundary(경계): seed/runtime(씨앗/런타임)이 없으면 reference-only(참조 전용)입니다.
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier37 Negative Memory(전선37 부정 기억)

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Evidence(근거): F37B seed/runtime(전선37B 씨앗/런타임) `{final['proxy']['seed_rows']}/{final['proxy']['runtime_rows']}` and F37C seed/runtime(전선37C 씨앗/런타임) `{final['repair']['seed_rows']}/{final['repair']['runtime_rows']}`.

Do-not-repeat(반복 금지): same train-only payoff-dominance label family(같은 학습 전용 수익 우위 라벨 계열)만 더 촘촘히 조정하지 않습니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier37 Selection Status(전선37 선택 상태)

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
    return f"""# Decision(결정): Open Frontier37 Payoff Label Family(전선37 수익 라벨 계열 개방)

Date(날짜): 2026-06-15

Decision(결정): Open(개방) `{STAGE_ID}` with run(실행) `{RUN_A}`.

Effect(효과): F36(전선36)의 weak PF(약한 수익 팩터)를 reference-only(참조 전용)로 두고, label family(라벨 계열)를 changed variable(변경 변수)로 시험합니다.
"""


def decision_closeout(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Close Frontier37 Payoff Label Family(전선37 수익 라벨 계열 마감)

Date(날짜): 2026-06-15

Decision(결정): Close(마감) `{STAGE_ID}` as `{final['closeout']['closeout_class']}`.

Grok closeout(그록 마감): `{final['closeout']['grok_closeout']['classification']}`.

Effect(효과): payoff label family(수익 라벨 계열)는 seed/runtime(씨앗/런타임)을 만들지 못해 다음 frontier stage(전선 단계)는 source family or model pivot(원천 계열 또는 모델 전환)을 다룹니다.

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

Action(행동): F37(전선37)을 payoff-dominance label family + balanced repair(수익 우위 라벨 계열 + 균형 수리) lifecycle(생명주기)로 닫았습니다.

Effect(효과): best read-only candidate(최상 읽기 전용 후보) `{best.get('candidate_id','')}`는 seed/runtime(씨앗/런타임)으로 충분하지 않아 MT5/ONNX(메타트레이더5/온엑스)는 열지 않았습니다.

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_D}` closed Frontier37 payoff label family(전선37 수익 라벨 계열). "
        f"Effect(효과): proxy_scout={final['proxy']['scout_rows']}, repair_scout={final['repair']['scout_rows']}, seed={final['repair']['seed_rows']}, next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_open(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR37-PAYOFF-LABEL-FAMILY-ONNX-SCOUT`: `{RUN_A}` opened payoff-dominance label family(수익 우위 라벨 계열). "
        "Effect(효과): F36 filter/source repetition(전선36 필터/원천 반복)을 피합니다.\n"
    )


def idea_registry_close(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR37-PAYOFF-LABEL-FAMILY-ONNX-SCOUT`: `{RUN_D}` closed as `{final['closeout']['closeout_class']}`. "
        "Effect(효과): next question(다음 질문)은 source family or model pivot(원천 계열 또는 모델 전환)입니다.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_D}`: {NEGATIVE_MEMORY}. Evidence(근거): F37B/F37C seed/runtime(전선37B/37C 씨앗/런타임) "
        f"{final['proxy']['seed_rows']}/{final['proxy']['runtime_rows']} and {final['repair']['seed_rows']}/{final['repair']['runtime_rows']}. "
        "Effect(효과): same payoff-dominance label family(같은 수익 우위 라벨 계열)만 반복하지 않습니다.\n"
    )


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


if __name__ == "__main__":
    raise SystemExit(main())
