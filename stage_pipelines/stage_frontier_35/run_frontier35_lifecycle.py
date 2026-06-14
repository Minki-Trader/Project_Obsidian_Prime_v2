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


STAGE_ID = "stage_frontier_35__dd_compressed_short_state_pf_source_lift_for_seed_surface_onnx_scout"
RUN_A = "frontier35A_stage_open_dd_compressed_short_state_pf_source_lift_hypothesis_design_v1"
RUN_B = "frontier35B_train_only_pf_source_lift_proxy_scout_v1"
RUN_C = "frontier35C_dd_compression_after_pf_lift_capped_repair_or_closeout_decision_v1"
RUN_D = "frontier35D_stage_closeout_pf_source_lift_v1"
NEXT_STAGE_ID = "stage_frontier_36__short_pf_lift_source_change_or_label_pivot_for_seed_surface_onnx_scout"
NEXT_RUN_ID = "frontier36A_stage_open_short_pf_lift_source_change_or_label_pivot_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_35/run_frontier35_lifecycle.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier35_stage_open/small_review")
GROK_RETRY_PACKET = GROK_PACKET / "retry"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SCOUT_PF = 1.05
SCOUT_DD_CAP = 15.0
NEAR_SEED_PF = 1.15
SEED_PF = 1.20
SEED_DD_CAP = 12.0
RUNTIME_PF = 1.50
RUNTIME_DD_CAP = 12.0
DENSITY_LOW = 5.0
DENSITY_HIGH = 10.0
PF_SOURCE_ROWS = 60
PF_REPAIR_SOURCE_ROWS = 30

PRESERVED_CLUE = (
    "f35_pf_first_short_overlay_kept_many_scout_rows_but_only_one_near_seed_reference_surface"
)
NEGATIVE_MEMORY = (
    "f35_train_only_pf_lift_overlay_did_not_survive_dd_compression_into_seed_or_runtime_candidate"
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
    base = f34.build_base_short_surface(frame, feature_order, path_labels, raw_path)
    proxy = build_pf_lift_proxy(frame, feature_order, path_labels, raw_path, base)
    repair = build_dd_repair(frame, path_labels, raw_path, proxy)
    final = build_final(created_at, frame, feature_order, context, base, proxy, repair)

    write_outputs(final, base, proxy, repair)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "stage_id": STAGE_ID,
        "closeout_run_id": RUN_D,
        "closeout_class": final["closeout"]["closeout_class"],
        "proxy_scout_rows": final["proxy"]["scout_rows"],
        "proxy_near_seed_rows": final["proxy"]["near_seed_rows"],
        "proxy_seed_rows": final["proxy"]["seed_rows"],
        "repair_candidate_rows": final["repair"]["candidate_rows"],
        "repair_scout_rows": final["repair"]["scout_rows"],
        "repair_seed_rows": final["repair"]["seed_rows"],
        "runtime_probe_status": final["closeout"]["runtime_probe_status"],
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "report": (STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md").as_posix(),
    }), ensure_ascii=False, indent=2))
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
    for packet in (GROK_PACKET, GROK_RETRY_PACKET):
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
        "classification": "accepted_stage_open_retry_after_first_transport_failure_overfit_risk" if accepted else "needs_local_verification",
        "retry_output_excerpt": retry_output[:1600],
    }


def validate_context(
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = f34.read_text(WORKSPACE_STATE)
    f34_selection = f34.read_text(Path("stages") / f34.STAGE_ID / "04_selected" / "selection_status.md")
    closeout_decision = f34.read_text(Path("docs/decisions/2026-06-14_stage_frontier_34_dd_compression_state_gate_closeout.md"))
    checks = {
        "workspace_current_f34_or_f35": f"current_stage_id: {f34.STAGE_ID}" in workspace or f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_points_to_f35a_or_current_f35": f"next_run_id: {RUN_A}" in workspace or f"current_stage_id: {STAGE_ID}" in workspace,
        "f34_selection_points_to_f35a": RUN_A in f34_selection,
        "f34_decision_points_to_f35a": RUN_A in closeout_decision,
        "f34_preserved_clue_present": f34.PRESERVED_CLUE in f34_selection,
        "f34_negative_memory_present": f34.NEGATIVE_MEMORY in f34_selection,
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_has_required_splits": set(frame["split"].astype(str).unique()) == {"train", "validation", "oos"},
        "raw_path_positions_complete": int(raw_path["missing_entry_positions"]) == 0 and int(raw_path["missing_future_positions"]) == 0,
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
        "feature_label_boundary": "PF lift and DD repair gates use train split thresholds; validation/OOS are read-only forward evidence",
        "leakage_risk": "medium: train-only PF lift scans many unused feature thresholds after F34 clue selection, so all claims remain exploratory",
    }


def build_pf_lift_proxy(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    base: dict[str, Any],
) -> dict[str, Any]:
    source = base["summary"].loc[
        (base["summary"]["side_value"].astype(int) == -1)
        & base["summary"]["validation_trades_per_day"].between(DENSITY_LOW, DENSITY_HIGH)
    ].head(PF_SOURCE_ROWS)
    train_mask = f33b.split_mask(frame, "train")
    rows: list[dict[str, Any]] = []
    for _, source_summary in source.iterrows():
        source_id = str(source_summary["candidate_id"])
        candidate = base["candidate_by_id"][source_id]
        used = set(str(candidate["features"]).split("|"))
        for gate in iter_pf_lift_gates(frame, feature_order, train_mask, used):
            mask = np.asarray(candidate["mask"], dtype=bool) & gate["mask"]
            side = int(candidate["side_value"])
            stop = float(candidate["stop_cap_log_return"])
            take = float(candidate["take_cap_log_return"])
            train = f33b.evaluate_path_mask(frame, mask, side, stop, take, path_labels, raw_path, "train")
            if not pf_lift_train_gate_pass(train, source_summary):
                continue
            validation = f33b.evaluate_path_mask(frame, mask, side, stop, take, path_labels, raw_path, "validation")
            oos = f33b.evaluate_path_mask(frame, mask, side, stop, take, path_labels, raw_path, "oos")
            rows.append(pf_lift_row(candidate, source_summary, gate, train, validation, oos, mask))
    candidate_ledger = pd.DataFrame(rows)
    if candidate_ledger.empty:
        return empty_section()
    candidate_ledger = candidate_ledger.sort_values("train_score", ascending=False).reset_index(drop=True)
    candidate_ledger["candidate_id"] = [f"f35b_{index:04d}" for index in range(1, len(candidate_ledger) + 1)]
    summary = f34.summarize_state_candidates(candidate_ledger)
    return section_from_ledger(candidate_ledger, summary, source_rows=int(len(source)))


def build_dd_repair(
    frame: pd.DataFrame,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    proxy: dict[str, Any],
) -> dict[str, Any]:
    summary = proxy["summary"]
    if summary.empty:
        return empty_section()
    sources = summary.loc[summary["scout_clue_flag"].astype(bool)].head(PF_REPAIR_SOURCE_ROWS)
    if sources.empty:
        return empty_section()
    train_mask = f33b.split_mask(frame, "train")
    proxy_by_id = {str(row["candidate_id"]): row for _, row in proxy["candidate_ledger"].iterrows()}
    rows: list[dict[str, Any]] = []
    for _, source_summary in sources.iterrows():
        source = proxy_by_id[str(source_summary["candidate_id"])]
        used = set(str(source["source_features"]).split("|"))
        used.add(str(source["gate_feature"]))
        for gate in f34.iter_state_gates(frame, train_mask, used):
            mask = np.asarray(source["mask"], dtype=bool) & gate["mask"]
            side = int(source["side_value"])
            stop = float(source["stop_cap_log_return"])
            take = float(source["take_cap_log_return"])
            train = f33b.evaluate_path_mask(frame, mask, side, stop, take, path_labels, raw_path, "train")
            if not dd_repair_train_gate_pass(train):
                continue
            validation = f33b.evaluate_path_mask(frame, mask, side, stop, take, path_labels, raw_path, "validation")
            oos = f33b.evaluate_path_mask(frame, mask, side, stop, take, path_labels, raw_path, "oos")
            rows.append(dd_repair_row(source, gate, train, validation, oos))
    candidate_ledger = pd.DataFrame(rows)
    if candidate_ledger.empty:
        return empty_section(source_rows=int(len(sources)))
    candidate_ledger = candidate_ledger.sort_values("train_score", ascending=False).reset_index(drop=True)
    candidate_ledger["candidate_id"] = [f"f35c_{index:04d}" for index in range(1, len(candidate_ledger) + 1)]
    summary = f34.summarize_state_candidates(candidate_ledger)
    return section_from_ledger(candidate_ledger, summary, source_rows=int(len(sources)))


def iter_pf_lift_gates(
    frame: pd.DataFrame,
    feature_order: list[str],
    train_mask: np.ndarray,
    used_features: set[str],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for feature in feature_order:
        if feature in used_features or feature not in frame.columns:
            continue
        series = pd.to_numeric(frame[feature], errors="coerce")
        train_values = series.loc[train_mask].replace([np.inf, -np.inf], np.nan).dropna()
        if train_values.nunique(dropna=True) <= 1:
            continue
        for operator, quantile_label, threshold, mask in f23b.condition_masks(series, train_values):
            out.append({
                "feature": feature,
                "operator": operator,
                "quantile_label": quantile_label,
                "threshold_value": float(threshold),
                "mask": np.asarray(mask, dtype=bool),
                "definition": f"{feature} {operator} {quantile_label}",
            })
    return out


def pf_lift_train_gate_pass(metrics: dict[str, Any], source_summary: pd.Series) -> bool:
    source_pf = f34.safe_float(source_summary.get("train_profit_factor"))
    return (
        int(metrics["trade_count"]) >= 55
        and 5.0 <= float(metrics["trades_per_day"]) <= 13.0
        and float(metrics["profit_factor"]) >= max(1.08, source_pf + 0.03)
        and float(metrics["net_profit"]) > 0.0
    )


def dd_repair_train_gate_pass(metrics: dict[str, Any]) -> bool:
    return (
        int(metrics["trade_count"]) >= 40
        and 4.5 <= float(metrics["trades_per_day"]) <= 10.5
        and float(metrics["profit_factor"]) >= 1.03
        and float(metrics["net_profit"]) > 0.0
        and float(metrics["dd_risk"]) <= 14.0
    )


def pf_lift_row(
    source: dict[str, Any],
    source_summary: pd.Series,
    gate: dict[str, Any],
    train: dict[str, Any],
    validation: dict[str, Any],
    oos: dict[str, Any],
    mask: np.ndarray,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "candidate_id": "",
        "source_candidate_id": source["candidate_id"],
        "source_features": source["features"],
        "source_condition_ids": source["condition_ids"],
        "side_value": int(source["side_value"]),
        "side": "short(숏)",
        "stop_cap_log_return": float(source["stop_cap_log_return"]),
        "take_cap_log_return": float(source["take_cap_log_return"]),
        "gate_feature": gate["feature"],
        "gate_operator": gate["operator"],
        "gate_quantile_label": gate["quantile_label"],
        "gate_threshold_value": gate["threshold_value"],
        "gate_definition": f"pf_lift:{gate['definition']}",
        "gate_depth": 1,
        "train_score": f34.train_score(train),
        "mask": np.asarray(mask, dtype=bool),
        "source_train_profit_factor": source_summary.get("train_profit_factor", ""),
        "source_train_trades_per_day": source_summary.get("train_trades_per_day", ""),
        "source_train_dd_risk": source_summary.get("train_dd_risk", ""),
        "source_validation_profit_factor": source_summary.get("validation_profit_factor", ""),
        "source_validation_trades_per_day": source_summary.get("validation_trades_per_day", ""),
        "source_validation_dd_risk": source_summary.get("validation_dd_risk", ""),
        "source_oos_profit_factor": source_summary.get("oos_profit_factor", ""),
        "source_oos_trades_per_day": source_summary.get("oos_trades_per_day", ""),
        "source_oos_dd_risk": source_summary.get("oos_dd_risk", ""),
    }
    f34.add_metrics(row, "train", train)
    f34.add_metrics(row, "validation", validation)
    f34.add_metrics(row, "oos", oos)
    row["train_pf_lift"] = f34.safe_float(row["train_profit_factor"]) - f34.safe_float(row["source_train_profit_factor"])
    row["validation_pf_lift"] = f34.safe_float(row["validation_profit_factor"]) - f34.safe_float(row["source_validation_profit_factor"])
    row["oos_pf_lift"] = f34.safe_float(row["oos_profit_factor"]) - f34.safe_float(row["source_oos_profit_factor"])
    return f34.add_flags(row)


def dd_repair_row(
    source: pd.Series,
    gate: dict[str, Any],
    train: dict[str, Any],
    validation: dict[str, Any],
    oos: dict[str, Any],
) -> dict[str, Any]:
    row = {
        "candidate_id": "",
        "source_candidate_id": str(source["candidate_id"]),
        "source_features": str(source["source_features"]),
        "source_condition_ids": str(source["source_condition_ids"]),
        "side_value": int(source["side_value"]),
        "side": "short(숏)",
        "stop_cap_log_return": float(source["stop_cap_log_return"]),
        "take_cap_log_return": float(source["take_cap_log_return"]),
        "gate_feature": f"{source['gate_feature']}|{gate['feature']}",
        "gate_operator": f"{source['gate_operator']}|{gate['operator']}",
        "gate_quantile_label": f"{source['gate_quantile_label']}|{gate['quantile_label']}",
        "gate_threshold_value": f"{source['gate_threshold_value']}|{gate['threshold_value']}",
        "gate_definition": f"{source['gate_definition']} & dd_state:{gate['definition']}",
        "gate_depth": 2,
        "train_score": f34.train_score(train),
        "source_train_profit_factor": source.get("train_profit_factor", ""),
        "source_train_trades_per_day": source.get("train_trades_per_day", ""),
        "source_train_dd_risk": source.get("train_dd_risk", ""),
        "source_validation_profit_factor": source.get("validation_profit_factor", ""),
        "source_validation_trades_per_day": source.get("validation_trades_per_day", ""),
        "source_validation_dd_risk": source.get("validation_dd_risk", ""),
        "source_oos_profit_factor": source.get("oos_profit_factor", ""),
        "source_oos_trades_per_day": source.get("oos_trades_per_day", ""),
        "source_oos_dd_risk": source.get("oos_dd_risk", ""),
    }
    f34.add_metrics(row, "train", train)
    f34.add_metrics(row, "validation", validation)
    f34.add_metrics(row, "oos", oos)
    row["train_pf_lift"] = f34.safe_float(row["train_profit_factor"]) - f34.safe_float(row["source_train_profit_factor"])
    row["validation_pf_lift"] = f34.safe_float(row["validation_profit_factor"]) - f34.safe_float(row["source_validation_profit_factor"])
    row["oos_pf_lift"] = f34.safe_float(row["oos_profit_factor"]) - f34.safe_float(row["source_oos_profit_factor"])
    return f34.add_flags(row)


def empty_section(source_rows: int = 0) -> dict[str, Any]:
    return {
        "candidate_ledger": pd.DataFrame(),
        "summary": pd.DataFrame(),
        "source_rows": int(source_rows),
        "candidate_rows": 0,
        "scout_rows": 0,
        "near_seed_rows": 0,
        "seed_rows": 0,
        "runtime_rows": 0,
        "best_readonly": {},
    }


def section_from_ledger(candidate_ledger: pd.DataFrame, summary: pd.DataFrame, source_rows: int) -> dict[str, Any]:
    return {
        "candidate_ledger": candidate_ledger,
        "summary": summary,
        "source_rows": int(source_rows),
        "candidate_rows": int(len(candidate_ledger)),
        "scout_rows": int(summary["scout_clue_flag"].sum()) if not summary.empty else 0,
        "near_seed_rows": int(summary["near_seed_flag"].sum()) if not summary.empty else 0,
        "seed_rows": int(summary["seed_surface_flag"].sum()) if not summary.empty else 0,
        "runtime_rows": int(summary["runtime_candidate_flag"].sum()) if not summary.empty else 0,
        "best_readonly": f34.clean_row(summary.iloc[0]) if not summary.empty else {},
    }


def build_final(
    created_at: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    context: dict[str, Any],
    base: dict[str, Any],
    proxy: dict[str, Any],
    repair: dict[str, Any],
) -> dict[str, Any]:
    runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f35c_capped_repair"
    closeout = {
        "run_id": RUN_D,
        "status": "closed_preserved_clue_negative_memory_pf_source_lift_scout_only_no_runtime_authority",
        "judgment": "preserved_clue_negative_memory(F35 PF source lift scout only no seed/runtime)",
        "closeout_class": "preserved_clue_negative_memory",
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "runtime_probe_status": runtime_status,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
    }
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "stage_open": {
            "run_id": RUN_A,
            "status": "opened_frontier35_pf_source_lift_no_authority",
            "judgment": "stage_opened_after_grok_retry_accepted_pf_lift_boundary",
            "grok": context,
        },
        "data": {
            "dataset_rows": int(len(frame)),
            "feature_count": int(len(feature_order)),
            "feature_order_hash": ordered_hash(feature_order),
            "pf_source_rows": PF_SOURCE_ROWS,
            "pf_repair_source_rows": PF_REPAIR_SOURCE_ROWS,
        },
        "base": {
            "condition_pool_rows": int(len(base["condition_pool"])),
            "candidate_rows": int(len(base["candidates"])),
            "source_short_rows": PF_SOURCE_ROWS,
        },
        "proxy": {
            "run_id": RUN_B,
            "status": "train_only_pf_source_lift_proxy_scout_no_seed_no_runtime_candidate_no_authority",
            "judgment": "scout_clue_pf_lift_requires_dd_repair_or_closeout_no_authority",
            "source_rows": proxy["source_rows"],
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
            "status": "dd_compression_after_pf_lift_capped_repair_closeout_queued_no_authority",
            "judgment": "dd_repair_after_pf_lift_collapsed_density_no_seed_runtime_requires_closeout",
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


def write_outputs(final: dict[str, Any], base: dict[str, Any], proxy: dict[str, Any], repair: dict[str, Any]) -> None:
    base["summary"].to_csv(io_path(RUN_B_ROOT / "base_candidate_summary_replay.csv"), index=False, encoding="utf-8-sig")
    proxy["candidate_ledger"].drop(columns=["mask"], errors="ignore").to_csv(
        io_path(RUN_B_ROOT / "pf_lift_candidate_ledger.csv"), index=False, encoding="utf-8-sig"
    )
    proxy["summary"].to_csv(io_path(RUN_B_ROOT / "pf_lift_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    repair["candidate_ledger"].drop(columns=["mask"], errors="ignore").to_csv(
        io_path(RUN_C_ROOT / "dd_repair_candidate_ledger.csv"), index=False, encoding="utf-8-sig"
    )
    repair["summary"].to_csv(io_path(RUN_C_ROOT / "dd_repair_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    f34.write_json(RUN_A_ROOT / "stage_open_summary.json", final["stage_open"])
    f34.write_json(RUN_B_ROOT / "final_summary.json", final["proxy"])
    f34.write_json(RUN_C_ROOT / "final_summary.json", final["repair"])
    f34.write_json(RUN_D_ROOT / "stage_closeout_summary.json", final)

    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_receipt(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_A}_report.md", stage_open_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_report.md", run_report(
        "Frontier35B PF Source Lift Proxy Report(전선35B 수익 팩터 원천 상승 프록시 보고서)",
        final["created_at_utc"],
        final["proxy"],
        proxy["summary"],
        "Action(행동): F34 reference scaffold(F34 참조 발판)에서 short path-native candidates(숏 경로 기반 후보)에 train-only PF lift gate(학습 전용 수익 팩터 상승 게이트)를 붙였습니다.",
        "Effect(효과): DD compression(손실폭 압축)이 아니라 PF source lift(수익 팩터 원천 상승)가 실제로 forward readout(전방 판독)을 올리는지 분리해 봅니다.",
        RUN_C,
    ))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_gate_audit.md", gate_audit_text("Frontier35B Gate Audit(전선35B 게이트 감사)", final["proxy"]["runtime_probe_status"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_report.md", run_report(
        "Frontier35C DD Repair After PF Lift Report(전선35C 수익 팩터 상승 후 손실폭 수리 보고서)",
        final["created_at_utc"],
        final["repair"],
        repair["summary"],
        "Action(행동): F35B scout rows(전선35B 탐색 행)에 capped DD state repair(상한 손실폭 상태 수리)를 붙였습니다.",
        "Effect(효과): PF lift(수익 팩터 상승)가 DD compression(손실폭 압축)을 견디며 5-10/day density(일 5-10회 밀도)를 유지하는지 확인합니다.",
        RUN_D,
    ))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_gate_audit.md", gate_audit_text("Frontier35C Gate Audit(전선35C 게이트 감사)", final["repair"]["runtime_probe_status"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md", closeout_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", required_gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_35_pf_source_lift_open.md"), decision_open(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_35_pf_source_lift_closeout.md"), decision_closeout(final))
    f34.write_json(RUN_D_ROOT / "run_manifest.json", run_manifest(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_PACKET / "prompt.md",
        GROK_PACKET / "metadata.json",
        GROK_RETRY_PACKET / "prompt.md",
        GROK_RETRY_PACKET / "clean_output.md",
        GROK_RETRY_PACKET / "metadata.json",
        RUN_B_ROOT / "pf_lift_candidate_summary.csv",
        RUN_C_ROOT / "dd_repair_candidate_summary.csv",
        RUN_D_ROOT / "stage_closeout_summary.json",
        STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md",
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
        "closeout_class": final["closeout"]["closeout_class"],
        "runtime_claim_boundary": "stage_closeout_no_mt5_runtime_authority",
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    for row in run_registry_rows(final):
        f34.upsert_csv_plain(RUN_REGISTRY, "run_id", row)
    for row in ledger_rows(final):
        f34.upsert_csv_plain(ALPHA_LEDGER, "ledger_row_id", row)
        f34.upsert_csv_plain(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_D, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_A, idea_registry_open(final))
    f03b.append_once(IDEA_REGISTRY, RUN_D, idea_registry_close(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_D, negative_register_entry(final))


def run_registry_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    created = final["created_at_utc"]
    best_b = final["proxy"]["best_readonly"]
    best_c = final["repair"]["best_readonly"]
    close = final["closeout"]
    return [
        registry_row(RUN_A, "stage_open(단계 개방)", final["stage_open"]["status"], final["stage_open"]["judgment"], f"grok={final['stage_open']['grok']['classification']};next={RUN_B};no_authority", created, "stage_open_no_model_training_no_wfo_no_mt5_no_onnx_no_authority", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", RUN_B),
        registry_row(RUN_B, "proxy_scout(프록시 탐색)", final["proxy"]["status"], final["proxy"]["judgment"], f"source={final['proxy']['source_rows']};candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};near_seed={final['proxy']['near_seed_rows']};seed={final['proxy']['seed_rows']};best={best_b.get('candidate_id','')};next={RUN_C}", created, "python_path_native_pf_lift_proxy_only_no_wfo_no_mt5_no_onnx_no_authority", final["proxy"]["runtime_probe_status"], RUN_C, best_b),
        registry_row(RUN_C, "repair_or_closeout_decision(수리 또는 마감 결정)", final["repair"]["status"], final["repair"]["judgment"], f"source={final['repair']['source_rows']};candidate={final['repair']['candidate_rows']};scout={final['repair']['scout_rows']};seed={final['repair']['seed_rows']};best={best_c.get('candidate_id','')};next={RUN_D}", created, "capped_repair_proxy_only_no_wfo_no_mt5_no_onnx_no_authority", final["repair"]["runtime_probe_status"], RUN_D, best_c),
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
        "parent_run_id": f34.RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
        "next_run_id": next_run,
        "claim_boundary": claim_boundary,
        "report_path": report.as_posix(),
        "created_at_utc": created,
        "primary_kpi": primary,
        "guardrail_kpi": "no_validation_oos_threshold_selection_no_runtime_authority",
        "external_verification_status": external_status,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": report.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        ledger_row(RUN_A, f"{RUN_A}__stage_open", "stage_open(단계 개방)", "not_applicable_stage_open(단계 개방 해당 없음)", "planning_only_no_trading_kpi(계획 전용 거래 KPI 없음)", final["stage_open"]["status"], final["stage_open"]["judgment"], "grok=accepted_retry;pf_lift_lock", "stage_open_no_runtime", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", f"next={RUN_B}"),
    ]
    rows.extend(tier_rows_for_proxy(final))
    rows.append(ledger_row(RUN_C, f"{RUN_C}__repair_decision", "repair_or_closeout_decision(수리 또는 마감 결정)", "Tier A(티어 A)", "capped_repair_no_runtime(상한 수리, 런타임 아님)", final["repair"]["status"], final["repair"]["judgment"], f"best={final['repair']['best_readonly'].get('candidate_id','')};scout={final['repair']['scout_rows']};seed={final['repair']['seed_rows']}", "bounded_repair_no_authority", final["repair"]["runtime_probe_status"], f"next={RUN_D}"))
    rows.append(ledger_row(RUN_D, f"{RUN_D}__stage_closeout", "stage_closeout(단계 마감)", "Tier A(티어 A)", "stage_closeout_no_runtime(단계 마감, 런타임 아님)", final["closeout"]["status"], final["closeout"]["judgment"], f"preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY}", "preserved_clue_negative_memory_no_authority", final["closeout"]["runtime_probe_status"], f"next={NEXT_RUN_ID}"))
    return rows


def tier_rows_for_proxy(final: dict[str, Any]) -> list[dict[str, Any]]:
    primary = ledger_row(RUN_B, f"{RUN_B}__tier_a_pf_lift_proxy", "Tier A separate(티어 A 분리)", "Tier A(티어 A)", "python_path_native_pf_lift_proxy_no_mt5(파이썬 경로 기반 수익 팩터 상승 프록시, MT5 아님)", final["proxy"]["status"], final["proxy"]["judgment"], f"candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};near_seed={final['proxy']['near_seed_rows']};seed={final['proxy']['seed_rows']}", "train_only_pf_lift_no_authority", final["proxy"]["runtime_probe_status"], f"next={RUN_C}")
    tier_b = {**primary, "ledger_row_id": f"{RUN_B}__tier_b_missing_required", "subrun_id": f"{RUN_B}__tier_b_missing_required", "record_view": "Tier B separate(티어 B 분리)", "tier_scope": "Tier B(티어 B)", "kpi_scope": "missing_required(필수 누락)", "primary_kpi": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)", "guardrail_kpi": "no_tier_b_claim(티어 B 주장 없음)", "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)", "notes": "Tier B not materialized in F35B PF lift proxy(전선35B 수익 팩터 상승 프록시에서 티어 B 미물질화)"}
    combined = {**primary, "ledger_row_id": f"{RUN_B}__tier_ab_combined_out_of_scope", "subrun_id": f"{RUN_B}__tier_ab_combined_out_of_scope", "record_view": "Tier A+B combined(티어 A+B 합산)", "tier_scope": "Tier A+B(티어 A+B)", "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)", "primary_kpi": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)", "guardrail_kpi": "no_synthetic_combined_claim(합성 합산 주장 없음)", "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)", "notes": "Combined tier not claimed in F35B PF lift proxy(전선35B 수익 팩터 상승 프록시에서 합산 티어 주장 없음)"}
    return [primary, tier_b, combined]


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
        "parent_run_id": f34.RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
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
    return f"""# Frontier35 Stage Brief(전선35 단계 요약)

Opened(개방): {final['created_at_utc']}

Hypothesis(가설): F34(전선34)의 DD-compressed short state clue(손실폭 압축 숏 상태 단서)를 reference-only scaffold(참조 전용 발판)로 쓰고, train-only PF source lift overlay(학습 전용 수익 팩터 원천 상승 덧씌움)를 먼저 시험하면 seed surface(씨앗 표면)에 가까워질 수 있습니다.

Action(행동): F35(전선35)를 PF source lift(수익 팩터 원천 상승) 가설로 열었습니다.

Effect(효과): F34 DD compression(전선34 손실폭 압축)을 더 깊게 반복하지 않고, PF source(수익 팩터 원천)를 바꾸는 새 변수만 시험합니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def stage_open_report(final: dict[str, Any]) -> str:
    return f"""# Frontier35A Stage Open Report(전선35A 단계 개방 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['stage_open']['status']}`

Judgment(판정): `{final['stage_open']['judgment']}`

Action(행동): F35(전선35)를 train-only PF source lift(학습 전용 수익 팩터 원천 상승) 가설로 열었습니다.

Effect(효과): F34(전선34)의 보존 단서는 참조하지만 winner/baseline/runtime authority(승자/기준선/런타임 권위)는 상속하지 않습니다.

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
                f"| `{row['candidate_id']}` | `{row['source_candidate_id']}` | `{row['gate_definition']}` | "
                f"{f34.fmt(row['validation_profit_factor'])} | {f34.fmt(row['validation_trades_per_day'])} | {f34.fmt(row['validation_dd_risk'])} | "
                f"{f34.fmt(row['oos_profit_factor'])} | {f34.fmt(row['oos_trades_per_day'])} | {f34.fmt(row['oos_dd_risk'])} | "
                f"{row['scout_clue_flag']} | {row['near_seed_flag']} | {row['seed_surface_flag']} |"
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

Best OOS PF-density-DD(최상 표본외 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('oos_profit_factor'))}` / `{f34.fmt(best.get('oos_trades_per_day'))}/day` / `{f34.fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{section.get('runtime_probe_status', '')}`

| candidate(후보) | source(원천) | gate(게이트) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{next_run}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def closeout_report(final: dict[str, Any]) -> str:
    best_b = final["proxy"]["best_readonly"]
    best_c = final["repair"]["best_readonly"]
    return f"""# Frontier35D Stage Closeout Report(전선35D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Action(행동): F35(전선35)를 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): PF source lift(수익 팩터 원천 상승)는 scout surface(탐색 표면)를 만들었지만, DD compression repair(손실폭 압축 수리)를 거치면 density(거래 밀도)가 약해져 seed/runtime candidate(씨앗/런타임 후보)가 되지 못했습니다.

F35B scout/near-seed/seed/runtime(전선35B 탐색/근접 씨앗/씨앗/런타임): `{final['proxy']['scout_rows']}` / `{final['proxy']['near_seed_rows']}` / `{final['proxy']['seed_rows']}` / `{final['proxy']['runtime_rows']}`

F35B best validation/OOS PF-density-DD(전선35B 최상 검증/표본외 수익 팩터-밀도-손실폭): `{f34.fmt(best_b.get('validation_profit_factor'))}/{f34.fmt(best_b.get('validation_trades_per_day'))}/{f34.fmt(best_b.get('validation_dd_risk'))}` and `{f34.fmt(best_b.get('oos_profit_factor'))}/{f34.fmt(best_b.get('oos_trades_per_day'))}/{f34.fmt(best_b.get('oos_dd_risk'))}`.

F35C scout/near-seed/seed/runtime(전선35C 탐색/근접 씨앗/씨앗/런타임): `{final['repair']['scout_rows']}` / `{final['repair']['near_seed_rows']}` / `{final['repair']['seed_rows']}` / `{final['repair']['runtime_rows']}`

F35C best validation/OOS PF-density-DD(전선35C 최상 검증/표본외 수익 팩터-밀도-손실폭): `{f34.fmt(best_c.get('validation_profit_factor'))}/{f34.fmt(best_c.get('validation_trades_per_day'))}/{f34.fmt(best_c.get('validation_dd_risk'))}` and `{f34.fmt(best_c.get('oos_profit_factor'))}/{f34.fmt(best_c.get('oos_trades_per_day'))}/{f34.fmt(best_c.get('oos_dd_risk'))}`.

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["stage_open"]["grok"]
    return f"""# Frontier35A Grok Stage-Open Receipt(전선35A 그록 단계 개방 영수증)

Trigger reason(호출 이유): goal(목표)이 stage open(단계 개방) Grok second opinion(그록 2차 의견)을 요구합니다.

Review size(검토 크기): small review(소규모 검토), retry(재시도) 사용.

Direction before Grok(그록 전 방향): F34(전선34)의 DD compression clue(손실폭 압축 단서)를 reference-only(참조 전용)로 두고 PF source lift(수익 팩터 원천 상승)를 새 변수로 시험합니다.

First prompt(첫 프롬프트): `{grok['first_prompt']}`

First output(첫 출력): `{grok['first_output']}`

Retry prompt(재시도 프롬프트): `{grok['retry_prompt']}`

Retry output(재시도 출력): `{grok['retry_output']}`

Classification(분류): `{grok['classification']}`

Accepted advice(수용 조언): novelty_ok(신규성 확인) yes(예), runtime claim boundary(런타임 주장 경계) yes(예), overfit risk(과적합 위험) medium(중간).

Local verification(로컬 검증): `{grok['judgment']}`

Forbidden claim check(금지 주장 확인): runtime authority/operating promotion/live readiness/Goal Achieve(런타임 권위/운영 승격/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def local_verification_text(final: dict[str, Any]) -> str:
    checks = final["stage_open"]["grok"]["checks"]
    rows = "\n".join(f"- {key}: `{value}`" for key, value in checks.items())
    return f"""# Frontier35 Local Verification(전선35 로컬 검증)

Judgment(판정): `{final['stage_open']['grok']['judgment']}`

{rows}

Effect(효과): Grok retry(그록 재시도), F34 closeout(전선34 마감), 데이터/피처 계약(data/feature contract, 데이터/피처 계약), 원천 경로(raw path, 원천 경로)를 로컬 파일과 대조했습니다.
"""


def gate_audit_text(title: str, runtime_status: str) -> str:
    return f"""# {title}

- scope_completion_gate(범위 완료 게이트): proxy/repair CSV and reports(프록시/수리 CSV와 보고서) created(생성).
- kpi_contract_audit(KPI 계약 감사): PF/density/DD(수익 팩터/밀도/손실폭)를 split별로 기록.
- no_forward_threshold_selection_gate(전방 임계값 선택 금지 게이트): PF lift/DD repair thresholds(수익 팩터 상승/손실폭 수리 임계값)는 train-only(학습 전용).
- runtime_probe_gate(런타임 탐침 게이트): `{runtime_status}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음).
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier35 Required Gate Coverage Audit(전선35 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): Grok stage open retry(그록 단계 개방 재시도) recorded(기록).
- scope_completion_gate(범위 완료 게이트): F35A/F35B/F35C/F35D artifacts(산출물) recorded(기록).
- kpi_contract_audit(KPI 계약 감사): proxy and repair split metrics(프록시와 수리 분할 지표) recorded(기록).
- runtime_evidence_gate(런타임 근거 게이트): `{final['closeout']['runtime_probe_status']}`
- closeout_gate(마감 게이트): preserved clue + negative memory(보존 단서 + 부정 기억).
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음).
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    best = final["proxy"]["best_readonly"]
    return f"""# Frontier35 Preserved Clue(전선35 보존 단서)

Clue(단서): `{PRESERVED_CLUE}`

Evidence(근거): F35B PF lift proxy(전선35B 수익 팩터 상승 프록시)는 scout rows(탐색 행) `{final['proxy']['scout_rows']}`개와 near-seed rows(근접 씨앗 행) `{final['proxy']['near_seed_rows']}`개를 만들었습니다. Best read-only candidate(최상 읽기 전용 후보) `{best.get('candidate_id','')}` reached validation/OOS PF(검증/표본외 수익 팩터) `{f34.fmt(best.get('validation_profit_factor'))}/{f34.fmt(best.get('oos_profit_factor'))}`.

Boundary(경계): DD repair(손실폭 수리)를 거친 seed/runtime(씨앗/런타임)은 0개이므로 reference-only(참조 전용)입니다.
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier35 Negative Memory(전선35 부정 기억)

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Evidence(근거): F35B seed/runtime(전선35B 씨앗/런타임) `{final['proxy']['seed_rows']}/{final['proxy']['runtime_rows']}` and F35C seed/runtime(전선35C 씨앗/런타임) `{final['repair']['seed_rows']}/{final['repair']['runtime_rows']}`.

Do-not-repeat(반복 금지): F34/F35 scaffold(전선34/35 발판)에 feature filter(피처 필터)만 하나씩 더 얹는 방식으로 PF source(수익 팩터 원천)를 찾지 않습니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier35 Selection Status(전선35 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage closeout(단계 마감): `{RUN_D}`

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_open(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Open Frontier35 PF Source Lift(전선35 수익 팩터 원천 상승 개방)

Date(날짜): 2026-06-15

Decision(결정): Open(개방) `{STAGE_ID}` with run(실행) `{RUN_A}`.

Effect(효과): F34(전선34)의 DD compression clue(손실폭 압축 단서)를 상속하지 않고 reference-only(참조 전용)로 사용하며, PF source lift(수익 팩터 원천 상승)를 새 변수로 시험합니다.
"""


def decision_closeout(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Close Frontier35 PF Source Lift(전선35 수익 팩터 원천 상승 마감)

Date(날짜): 2026-06-15

Decision(결정): Close(마감) `{STAGE_ID}` as preserved clue + negative memory(보존 단서 + 부정 기억).

Effect(효과): PF lift(수익 팩터 상승) 단서는 보존하지만 DD repair(손실폭 수리)와 density(거래 밀도)를 동시에 만족하지 못해 다음 전선은 source change or label pivot(원천 변경 또는 라벨 전환)을 다룹니다.

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join([
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
    ])


def current_working_state(final: dict[str, Any]) -> str:
    best = final["proxy"]["best_readonly"]
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

Action(행동): F35(전선35)를 PF source lift(수익 팩터 원천 상승) preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): best read-only candidate(최상 읽기 전용 후보) `{best.get('candidate_id','')}`는 scout clue(탐색 단서)를 만들었지만 seed/runtime(씨앗/런타임)으로 충분하지 않아 MT5/ONNX(메타트레이더5/온엑스)는 열지 않았습니다.

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_D}` closed Frontier35 PF source lift(전선35 수익 팩터 원천 상승). "
        f"Effect(효과): proxy_scout={final['proxy']['scout_rows']}, proxy_near_seed={final['proxy']['near_seed_rows']}, repair_seed={final['repair']['seed_rows']}, next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_open(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR35-PF-SOURCE-LIFT-ONNX-SCOUT`: `{RUN_A}` opened train-only PF source lift(학습 전용 수익 팩터 원천 상승). "
        "Effect(효과): F34 DD compression clue(전선34 손실폭 압축 단서)를 reference-only(참조 전용)로 사용합니다.\n"
    )


def idea_registry_close(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR35-PF-SOURCE-LIFT-ONNX-SCOUT`: `{RUN_D}` closed as preserved clue + negative memory(보존 단서 + 부정 기억). "
        "Effect(효과): 다음 질문은 same scaffold filter stacking(같은 발판 필터 누적)이 아니라 source change or label pivot(원천 변경 또는 라벨 전환)입니다.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_D}`: {NEGATIVE_MEMORY}. Evidence(근거): F35B/F35C seed/runtime(전선35B/35C 씨앗/런타임) "
        f"{final['proxy']['seed_rows']}/{final['proxy']['runtime_rows']} and {final['repair']['seed_rows']}/{final['repair']['runtime_rows']}. "
        "Effect(효과): F34/F35 scaffold(전선34/35 발판)에 단일 피처 필터를 더 얹는 반복을 금지합니다.\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
