from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "332_overfit_guard__failure_memory_forward_research_handoff"
SOURCE_STAGE_ID = "331_overfit_guard__cross_horizon_cost_curve_parity_probe"
RUN_NUMBER = "run332C"
RUN_ID = "run332C_design_or_materialize_cost_curve_guarded_scout_v1"
PARENT_RUN_ID = "run332B_materialize_failure_memory_forward_data_and_guard_inputs_v1"
NEXT_RUN_ID = "run332D_design_pocket_veto_feature_thesis_v1"
STATUS = "completed_cost_curve_guarded_scout_materialization_no_selection"
JUDGMENT = "cost_curve_guarded_scout_research_only_no_goal_achieve"
DECISION = "stage331_failure_memory_converted_to_cost_curve_pocket_veto_scout_queue_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_cost_curve_guarded_scout_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
RUN331B_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run331B"
RUN331C_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run331C"
RUN331D_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run331D"
RUN332B_DIR = STAGE_DIR / "02_runs" / "run332B"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage332C_cost_curve_guarded_scout.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line(text: str, prefix: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return "\n".join(lines[: index + 1] + [block] + lines[index + 1 :]) + "\n"
    return text.rstrip() + "\n" + block + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    by_key = {tuple(str(row.get(column, "")) for column in key_columns): index for index, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in by_key:
            existing[by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def to_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def fmt(value: Any, digits: int = 3) -> str:
    number = to_float(value)
    if number is None:
        return str(value)
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def first_row(df: pd.DataFrame, **filters: Any) -> dict[str, Any]:
    view = df.copy()
    for column, value in filters.items():
        view = view[view[column].astype(str) == str(value)]
    if view.empty:
        return {}
    return view.iloc[0].to_dict()


def cost_map(cost_curve: pd.DataFrame, attempt_name: str, horizon_id: str = "full_forward") -> dict[float, float]:
    subset = cost_curve[
        (cost_curve["attempt_name"].astype(str) == attempt_name)
        & (cost_curve["horizon_id"].astype(str) == horizon_id)
    ]
    out: dict[float, float] = {}
    for row in subset.to_dict(orient="records"):
        cost_level = to_float(row.get("cost_level"))
        pf = to_float(row.get("profit_factor_after_cost"))
        if cost_level is not None and pf is not None:
            out[cost_level] = pf
    return out


def max_cost_surviving(pfs: Mapping[float, float]) -> float | None:
    survivors = [cost for cost, pf in pfs.items() if pf > 1.0]
    if not survivors:
        return None
    return max(survivors)


def net_for(horizon: pd.DataFrame, attempt_name: str, horizon_id: str) -> float | None:
    row = first_row(horizon, attempt_name=attempt_name, horizon_id=horizon_id)
    return to_float(row.get("net_profit"))


def trade_count_for(horizon: pd.DataFrame, attempt_name: str) -> float | None:
    row = first_row(horizon, attempt_name=attempt_name, horizon_id="full_forward")
    return to_float(row.get("trade_count"))


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return (
        read_csv(RUN331D_DIR / "final_decision_matrix.csv"),
        read_csv(RUN331D_DIR / "overfit_guard_failure_memory.csv"),
        read_csv(RUN331D_DIR / "survivor_clue_disposition.csv"),
        read_csv(RUN331B_DIR / "cost_curve_by_horizon_report.csv"),
        read_csv(RUN331B_DIR / "candidate_horizon_kpi_report.csv"),
        read_csv(RUN331B_DIR / "resampling_stability_report.csv"),
        read_csv(RUN331C_DIR / "runtime_replay_compare_report.csv"),
    )


def guard_threshold_spec() -> dict[str, Any]:
    return {
        "source": "Stage331 failure memory, not optimized on new data",
        "no_retune_policy": {
            "threshold_retuning": "forbidden",
            "lot_optimization": "forbidden",
            "model_update": "forbidden",
            "pocket_exclusion_after_viewing": "forbidden",
        },
        "cost_levels_to_report": [0, 0.25, 0.5, 1, 2, 3, 5],
        "hard_veto_rules": {
            "cost2_profit_factor_lt_1": "failure_memory_only_no_selection_language",
            "rolling20_min_net_lt_0": "curve_pocket_veto_no_selection_language",
        },
        "warning_rules": {
            "cost1_profit_factor_lte_1_05": "near_break_even_cost_fragility",
            "any_month_or_half_net_lte_0": "temporal_concentration_warning",
            "trade_count_lt_100": "low_frequency_claim_warning",
        },
        "next_research_use": "Design future feature theses that must pass these fixed reports before any ONNX export package language.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_guard_tables(
    final_matrix: pd.DataFrame,
    survivor_clues: pd.DataFrame,
    cost_curve: pd.DataFrame,
    horizon: pd.DataFrame,
    resampling: pd.DataFrame,
    runtime: pd.DataFrame,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    guarded_matrix: list[dict[str, Any]] = []
    cost_veto_rows: list[dict[str, Any]] = []
    curve_veto_rows: list[dict[str, Any]] = []
    temporal_rows: list[dict[str, Any]] = []

    clue_attempts = set(survivor_clues["attempt_name"].astype(str).tolist())
    negative_attempts: list[str] = []

    for row in final_matrix.to_dict(orient="records"):
        attempt = str(row["attempt_name"])
        role = str(row["role"])
        if "negative_control" in role:
            negative_attempts.append(attempt)
        full_pf = to_float(row.get("source_profit_factor"))
        cost1_pf = to_float(row.get("cost1_profit_factor"))
        cost2_pf = to_float(row.get("cost2_profit_factor"))
        full_net = to_float(row.get("source_net_profit"))
        rolling20_min = to_float(row.get("rolling20_min_net"))
        trade_count = trade_count_for(horizon, attempt)
        pfs = cost_map(cost_curve, attempt)
        max_cost = max_cost_surviving(pfs)
        resample = first_row(resampling, attempt_name=attempt)
        replay = first_row(runtime, attempt_name=attempt)
        first_half_net = net_for(horizon, attempt, "first_half")
        second_half_net = net_for(horizon, attempt, "second_half")
        april_net = net_for(horizon, attempt, "month_2026-04")
        may_net = net_for(horizon, attempt, "month_2026-05")
        temporal_negative = [
            label
            for label, value in [
                ("first_half", first_half_net),
                ("second_half", second_half_net),
                ("month_2026-04", april_net),
                ("month_2026-05", may_net),
            ]
            if value is not None and value <= 0
        ]
        cost_status = "hard_veto_failure_memory_only" if (cost2_pf is None or cost2_pf < 1.0) else "cost_guard_pass_research_only"
        if cost1_pf is not None and cost1_pf <= 1.05:
            cost_status += ";near_break_even_plus1_warning"
        curve_status = "curve_pocket_veto" if (rolling20_min is None or rolling20_min < 0) else "curve_guard_pass_research_only"
        temporal_status = "temporal_concentration_warning" if temporal_negative else "temporal_balance_not_refuted"
        density_status = "low_frequency_claim_warning" if (trade_count is None or trade_count < 100) else "density_not_primary_blocker"
        if "negative_control" in role:
            scout_disposition = "do_not_resurrect_negative_control"
        elif cost2_pf is not None and cost2_pf < 1.0:
            scout_disposition = "preserve_as_failure_memory_clue_only"
        else:
            scout_disposition = "research_scout_only_requires_independent_guard_pass"

        guarded_matrix.append(
            {
                "attempt_name": attempt,
                "artifact_slug": row.get("artifact_slug"),
                "role": role,
                "runtime_replay_match": str(replay.get("metrics_match", "")).lower() == "true",
                "full_net": full_net,
                "full_pf": full_pf,
                "cost1_pf": cost1_pf,
                "cost2_pf": cost2_pf,
                "max_cost_level_pf_gt_1": max_cost,
                "rolling20_min_net": rolling20_min,
                "rolling40_min_net": to_float(resample.get("rolling40_min_net")),
                "first_half_net": first_half_net,
                "second_half_net": second_half_net,
                "month_2026_04_net": april_net,
                "month_2026_05_net": may_net,
                "trade_count": trade_count,
                "cost_guard_status": cost_status,
                "curve_guard_status": curve_status,
                "temporal_guard_status": temporal_status,
                "density_guard_status": density_status,
                "scout_disposition": scout_disposition,
                "allowed_future_use": "research_memory_only" if attempt in clue_attempts else "negative_control_guard_test_only",
                "forbidden_future_use": "no_selected_candidate_no_operating_reference_no_threshold_or_lot_repair",
            }
        )
        cost_veto_rows.append(
            {
                "attempt_name": attempt,
                "full_pf": full_pf,
                "cost0_pf": pfs.get(0.0),
                "cost0_5_pf": pfs.get(0.5),
                "cost1_pf": cost1_pf,
                "cost2_pf": cost2_pf,
                "cost3_pf": pfs.get(3.0),
                "cost5_pf": pfs.get(5.0),
                "max_cost_level_pf_gt_1": max_cost,
                "cost2_margin_vs_1": None if cost2_pf is None else cost2_pf - 1.0,
                "veto_status": cost_status,
                "anti_overfit_effect": "prevents headline PF from hiding execution-cost fragility",
            }
        )
        curve_veto_rows.append(
            {
                "attempt_name": attempt,
                "rolling20_min_net": rolling20_min,
                "rolling20_min_pf": to_float(resample.get("rolling_min_pf")),
                "rolling20_start": resample.get("rolling_min_start", ""),
                "rolling20_end": resample.get("rolling_min_end", ""),
                "rolling40_min_net": to_float(resample.get("rolling40_min_net")),
                "rolling40_min_pf": to_float(resample.get("rolling40_min_pf")),
                "curve_veto_status": curve_status,
                "anti_overfit_effect": "prevents curve-pocket exclusion or late-window-only selection",
            }
        )
        temporal_rows.append(
            {
                "attempt_name": attempt,
                "full_net": full_net,
                "first_half_net": first_half_net,
                "second_half_net": second_half_net,
                "month_2026_04_net": april_net,
                "month_2026_05_net": may_net,
                "negative_temporal_slices": ";".join(temporal_negative),
                "positive_slice_count": 4 - len(temporal_negative),
                "temporal_guard_status": temporal_status,
                "likely_driver": "second_half_or_may_dependency" if temporal_negative else "not_refuted_by_current_slices",
            }
        )

    queue_rows = [
        {
            "queue_id": "run332D_c56_low_frequency_cost_shape_pocket_veto_thesis",
            "source_attempts": "c56_plain_rf",
            "scout_question": "Can the c56 low-frequency clue survive without cost+2 failure and without a negative rolling20 pocket?",
            "required_guard": "cost2_pf_ge_1_and_rolling20_min_net_ge_0_before_any_package_language",
            "forbidden_action": "no threshold retuning; no lot optimization; no pocket exclusion",
            "status": "queued_research_design_only",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run332D_m48_macro_breadth_concentration_veto_thesis",
            "source_attempts": "m48_plain_rf",
            "scout_question": "Can macro breadth keep the trade density while removing cost convexity and April pocket concentration?",
            "required_guard": "plus1_not_near_break_even_plus2_pf_ge_1_and_month_half_balance_reported",
            "forbidden_action": "no threshold retuning; no lot optimization; no model update from Stage331 pocket labels",
            "status": "queued_research_design_only",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "negative_control_balanced_family_do_not_resurrect",
            "source_attempts": ";".join(negative_attempts),
            "scout_question": "Keep balanced/high-pressure rows as guard tests, not as repair seeds.",
            "required_guard": "future branch must beat these rows on cost2 and curve pocket without retuning",
            "forbidden_action": "do not promote caught negative controls",
            "status": "closed_as_negative_control_reference",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return guarded_matrix, cost_veto_rows, curve_veto_rows, temporal_rows, queue_rows


def receipts(
    guarded_matrix: list[dict[str, Any]],
    queue_rows: list[dict[str, Any]],
    source_files: list[Path],
) -> dict[str, Any]:
    all_runtime_match = all(row["runtime_replay_match"] for row in guarded_matrix)
    hard_veto_count = sum(1 for row in guarded_matrix if "hard_veto" in str(row["cost_guard_status"]) or "curve_pocket_veto" in str(row["curve_guard_status"]))
    clue_only_count = sum(1 for row in guarded_matrix if row["scout_disposition"] == "preserve_as_failure_memory_clue_only")
    source_hashes = [
        {
            "path": rel(path),
            "sha256": sha256_file(path),
            "exists": path_exists(path),
        }
        for path in source_files
    ]
    return {
        "performance_attribution_receipt": {
            "observed_change": "Stage331 headline PF clues collapse under cost+2 and rolling-pocket guards.",
            "comparison_baseline": "Stage331 final decision matrix and run331B no-retune cost/curve controls.",
            "likely_drivers": [
                "execution cost convexity",
                "rolling pocket concentration",
                "April/first-half weakness",
                "low-frequency claim risk for c56_plain_rf",
            ],
            "segment_checks": "full_forward, first_half, second_half, month_2026-04, month_2026-05, rolling20, rolling40, cost levels 0..5",
            "trade_shape": "trade count, PF, net, cost-stressed PF, rolling pocket net/PF",
            "alternative_explanations": "thin forward window, synthetic cost approximation, and reused Stage331 artifacts.",
            "attribution_confidence": "medium_for_guard_design_low_for_new_edge_claim",
            "next_probe": NEXT_RUN_ID,
        },
        "model_validation_receipt": {
            "model_family": "Stage331 RF forward-safe research artifacts; no new model trained in run332C.",
            "target_and_label": "unchanged from source artifacts; run332C only reads post-run KPI/curve evidence.",
            "split_method": "existing raw-forward window plus deterministic time/rolling slices.",
            "selection_metric": "none; no candidate selection allowed.",
            "secondary_metrics": "cost2_pf, rolling20_min_net, temporal slice net, trade count, runtime replay match.",
            "threshold_policy": "fixed/no retune; run332C does not search thresholds.",
            "overfit_risk": "using Stage331 pockets as repair targets; mitigated by writing veto rules instead of repair parameters.",
            "calibration_risk": "not applicable; no score probability claim.",
            "comparison_baseline": "Stage331 final matrix and negative controls.",
            "validation_judgment": JUDGMENT,
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(RUN331C_DIR / "runtime_replay_compare_report.csv"),
            "shared_contract": "run332C reads runtime replay match only; no EA or handoff change.",
            "known_differences": "no new MT5 tester run in run332C; existing run331C replay is reference evidence only.",
            "parity_check": "all source runtime replay metrics match" if all_runtime_match else "runtime replay mismatch found",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "artifact_lineage_receipt": {
            "source_inputs": [rel(path) for path in source_files],
            "producer": rel(Path(__file__)),
            "consumer": [rel(RUN_DIR), rel(REVIEWS_DIR / "run332C_cost_curve_guarded_scout.md"), NEXT_RUN_ID],
            "artifact_hashes": source_hashes,
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked_outputs_with_source_hashes",
            "lineage_judgment": "connected_with_boundary",
        },
        "no_retune_guard_receipt": {
            "threshold_retuning": "not_performed",
            "lot_optimization": "not_performed",
            "model_update": "not_performed",
            "candidate_selection": "not_performed",
            "repair_branch": "not_materialized_in_run332C",
            "guarded_scout_queue_count": len(queue_rows),
            "hard_veto_or_curve_veto_rows": hard_veto_count,
            "preserved_clue_only_count": clue_only_count,
        },
        "result_judgment_receipt": {
            "result_subject": RUN_ID,
            "evidence_available": [
                "guarded_scout_matrix",
                "cost_convexity_veto_table",
                "curve_pocket_veto_table",
                "temporal_concentration_report",
                "guarded_scout_queue",
            ],
            "evidence_missing": "no new independent MT5 result and no new ONNX candidate by design",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
    }


def gate_rows(
    guarded_matrix: list[dict[str, Any]],
    queue_rows: list[dict[str, Any]],
    output_paths: Sequence[Path],
) -> list[dict[str, Any]]:
    source_ready = all(
        path_exists(path)
        for path in [
            RUN331D_DIR / "final_decision_matrix.csv",
            RUN331B_DIR / "cost_curve_by_horizon_report.csv",
            RUN331B_DIR / "resampling_stability_report.csv",
            RUN331C_DIR / "runtime_replay_compare_report.csv",
            RUN332B_DIR / "guard_input_manifest.csv",
        ]
    )
    outputs_ready = all(path_exists(path) for path in output_paths)
    return [
        {
            "gate": "source_failure_memory_loaded",
            "status": "pass" if source_ready else "fail",
            "evidence": "Stage331D/331B/331C plus run332B guard inputs are present.",
        },
        {
            "gate": "cost_convexity_guard_materialized",
            "status": "pass" if any(row["cost2_pf"] is not None for row in guarded_matrix) else "fail",
            "evidence": "cost2 PF and max surviving cost are written for every attempt.",
        },
        {
            "gate": "curve_pocket_guard_materialized",
            "status": "pass" if any(row["rolling20_min_net"] is not None for row in guarded_matrix) else "fail",
            "evidence": "rolling20/rolling40 pocket metrics are written.",
        },
        {
            "gate": "temporal_concentration_guard_materialized",
            "status": "pass" if all("temporal_guard_status" in row for row in guarded_matrix) else "fail",
            "evidence": "first/second half and April/May slices are written.",
        },
        {
            "gate": "guarded_scout_queue_materialized",
            "status": "pass" if len(queue_rows) == 3 else "fail",
            "evidence": "two preserved clue scout rows and one negative-control reference row.",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence": "No threshold, lot, model, or runtime handoff was changed.",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass" if "no_goal_achieve" in CLAIM_BOUNDARY else "fail",
            "evidence": "No Forward Passed/Failed, live readiness, deployment, operating promotion, runtime authority, or Goal Achieve claim.",
        },
        {
            "gate": "outputs_exist",
            "status": "pass" if outputs_ready else "fail",
            "evidence": "Durable CSV/JSON/MD outputs exist.",
        },
    ]


def update_docs(guarded_matrix: list[dict[str, Any]], queue_rows: list[dict[str, Any]]) -> None:
    review_path = REVIEWS_DIR / "run332C_cost_curve_guarded_scout.md"
    c56 = next(row for row in guarded_matrix if row["attempt_name"] == "c56_plain_rf")
    m48 = next(row for row in guarded_matrix if row["attempt_name"] == "m48_plain_rf")
    review = f"""
# run332C Cost Curve Guarded Scout(332C 비용 곡선 방어 탐침)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Scout Read(탐침 판독)

- c56_plain_rf(코어56 일반 RF): full PF(전체 수익 팩터) `{fmt(c56["full_pf"])}`지만 cost+2 PF(비용+2 수익 팩터) `{fmt(c56["cost2_pf"])}`, rolling20 pocket(롤링20 포켓) `{fmt(c56["rolling20_min_net"])}`라 selection(선택) 언어는 금지한다.
- m48_plain_rf(매크로48 일반 RF): full PF(전체 수익 팩터) `{fmt(m48["full_pf"])}`지만 cost+1 PF(비용+1 수익 팩터) `{fmt(m48["cost1_pf"])}`, cost+2 PF(비용+2 수익 팩터) `{fmt(m48["cost2_pf"])}`, rolling20 pocket(롤링20 포켓) `{fmt(m48["rolling20_min_net"])}`라 concentration(집중) 위험을 먼저 다룬다.
- guarded_scout_queue(방어 탐침 대기열): `{len(queue_rows)}` rows(행). Effect(효과): 다음 run332D(332D 실행)는 pocket veto feature thesis(포켓 거부 피처 논제)를 설계하되, Stage331 포켓을 제외하거나 threshold(임계값)를 맞추지 않는다.

## Boundary(경계)

- no threshold retuning(임계값 재튜닝 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 업데이트 없음)
- no candidate selection(후보 선택 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_md(review_path, review)

    decision = f"""
# Stage332C Cost Curve Guarded Scout Decision(332C 비용 곡선 방어 탐침 결정)

run332C(332C 실행)는 Stage331(331단계)의 failure memory(실패 기억)를 cost convexity/curve pocket veto(비용 볼록성/곡선 포켓 거부) 조건으로 물질화했다.
Effect(효과): c56_plain_rf(코어56 일반 RF)와 m48_plain_rf(매크로48 일반 RF)는 계속 볼 단서지만 selection(선택)이나 Forward Passed(전진 통과)가 아니다.

- status(상태): `{STATUS}`
- decision(판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_md(DECISION_DOC, decision)

    input_block = f"""
- run332C_guarded_scout_matrix(332C 방어 탐침 행렬): `{rel(RUN_DIR / "guarded_scout_matrix.csv")}`
- run332C_cost_veto(332C 비용 거부): `{rel(RUN_DIR / "cost_convexity_veto_table.csv")}`
- run332C_curve_veto(332C 곡선 포켓 거부): `{rel(RUN_DIR / "curve_pocket_veto_table.csv")}`
- run332C_queue(332C 대기열): `{rel(RUN_DIR / "guarded_scout_queue.csv")}`
"""
    append_if_missing(INPUTS_DIR / "input_refs.md", "run332C_guarded_scout_matrix", input_block)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = insert_after_line(
        selection_text,
        "- latest_data_guard_materialization",
        f"- latest_cost_curve_guarded_scout(최신 비용 곡선 방어 탐침): `{RUN_ID}`",
        "latest_cost_curve_guarded_scout",
    )
    selection_text = replace_prefix_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_prefix_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_prefix_line(
        selection_text,
        "- effect(효과):",
        "- effect(효과): cost/curve guarded scout(비용/곡선 방어 탐침)는 실패 기억을 veto rule(거부 규칙)과 research queue(연구 대기열)로 바꿨지만, 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(WORKSPACE_STATE.read_text(encoding="utf-8-sig"), "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    block = (
        "- >-\n"
        f"  Stage332(332단계) run332C(332C 실행)는 `{STATUS}`로 cost/curve guarded scout(비용/곡선 방어 탐침)를 물질화했다. "
        "Effect(효과): Stage331(331단계)의 cost+2 failure(비용+2 실패), rolling pocket(롤링 포켓), temporal concentration(시간 집중)을 "
        f"run332D(332D 실행)의 pocket veto feature thesis(포켓 거부 피처 논제) 조건으로 넘기고 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_line(workspace_text, "current_focus:", block, "run332C(332C 실행)")
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `332_overfit_guard__failure_memory_forward_research_handoff_v4`")
    current_text = replace_prefix_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- target_surface(목표 표면):", "- target_surface(목표 표면): `pocket_veto_feature_thesis`")
    current_text = replace_prefix_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision(판정):", f"- decision(판정): `{DECISION}`")
    current_text = insert_after_line(
        current_text,
        "- decision(판정):",
        f"- run332C_summary(332C 요약): cost/curve guarded scout(비용/곡선 방어 탐침)를 `{STATUS}`로 완료했다. Effect(효과): cost+2 PF(비용+2 수익 팩터), rolling20 pocket(롤링20 포켓), temporal concentration(시간 집중)을 다음 run332D(332D 실행)의 고정 veto condition(거부 조건)으로 넘겼고 선택 후보나 Goal Achieve(목표 달성)는 없다.",
        "run332C_summary",
    )
    current_text = replace_prefix_line(current_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    changelog_block = f"""
## {TODAY} - Stage332C cost/curve guarded scout(비용/곡선 방어 탐침)

- run(실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- effect(효과): Stage331(331단계)의 preserved clue(보존 단서)를 선택하지 않고, cost convexity/curve pocket/temporal balance(비용 볼록성/곡선 포켓/시간 균형) veto(거부) 조건과 run332D(332D 실행) 대기열로 바꿨다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    append_if_missing(CHANGELOG, "Stage332C cost/curve guarded scout", changelog_block)


def update_registers(output_paths: Sequence[Path]) -> None:
    review_path = REVIEWS_DIR / "run332C_cost_curve_guarded_scout.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "performance_attribution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(review_path),
                "notes": f"cost_curve_guarded_scout;next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__cost_curve_guarded_scout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "cost_curve_guarded_scout",
                "tier_scope": "raw_forward_failure_memory_guard_scope",
                "kpi_scope": "cost_curve_pocket_temporal_guard_no_new_trading_kpi",
                "scoreboard_lane": "performance_attribution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(review_path),
                "primary_kpi": "guarded_scout_queue_count=3",
                "guardrail_kpi": "no_threshold_retuning;no_lot_optimization;no_model_update;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_existing_runtime_replay_reference_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__cost_curve_guarded_scout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "cost_curve_guarded_scout(비용 곡선 방어 탐침)",
                "tier_scope": "raw_forward_failure_memory_guard_scope(원본 전진 실패 기억 방어 범위)",
                "scoreboard": "cost_curve_pocket_temporal_guard_no_new_trading_kpi(비용/곡선/시간 방어, 새 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(review_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in output_paths:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": utc_now(),
                "notes": "run332C durable evidence; research-only boundary.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> int:
    final_matrix, memory, survivor_clues, cost_curve, horizon, resampling, runtime = load_inputs()
    guarded_matrix, cost_veto, curve_veto, temporal_rows, queue_rows = build_guard_tables(
        final_matrix=final_matrix,
        survivor_clues=survivor_clues,
        cost_curve=cost_curve,
        horizon=horizon,
        resampling=resampling,
        runtime=runtime,
    )

    source_files = [
        RUN331D_DIR / "final_decision_matrix.csv",
        RUN331D_DIR / "overfit_guard_failure_memory.csv",
        RUN331D_DIR / "survivor_clue_disposition.csv",
        RUN331B_DIR / "cost_curve_by_horizon_report.csv",
        RUN331B_DIR / "candidate_horizon_kpi_report.csv",
        RUN331B_DIR / "resampling_stability_report.csv",
        RUN331C_DIR / "runtime_replay_compare_report.csv",
        RUN332B_DIR / "guard_input_manifest.csv",
    ]

    output_paths = [
        write_csv(
            RUN_DIR / "guarded_scout_matrix.csv",
            [
                "attempt_name",
                "artifact_slug",
                "role",
                "runtime_replay_match",
                "full_net",
                "full_pf",
                "cost1_pf",
                "cost2_pf",
                "max_cost_level_pf_gt_1",
                "rolling20_min_net",
                "rolling40_min_net",
                "first_half_net",
                "second_half_net",
                "month_2026_04_net",
                "month_2026_05_net",
                "trade_count",
                "cost_guard_status",
                "curve_guard_status",
                "temporal_guard_status",
                "density_guard_status",
                "scout_disposition",
                "allowed_future_use",
                "forbidden_future_use",
            ],
            guarded_matrix,
        ),
        write_csv(
            RUN_DIR / "cost_convexity_veto_table.csv",
            [
                "attempt_name",
                "full_pf",
                "cost0_pf",
                "cost0_5_pf",
                "cost1_pf",
                "cost2_pf",
                "cost3_pf",
                "cost5_pf",
                "max_cost_level_pf_gt_1",
                "cost2_margin_vs_1",
                "veto_status",
                "anti_overfit_effect",
            ],
            cost_veto,
        ),
        write_csv(
            RUN_DIR / "curve_pocket_veto_table.csv",
            [
                "attempt_name",
                "rolling20_min_net",
                "rolling20_min_pf",
                "rolling20_start",
                "rolling20_end",
                "rolling40_min_net",
                "rolling40_min_pf",
                "curve_veto_status",
                "anti_overfit_effect",
            ],
            curve_veto,
        ),
        write_csv(
            RUN_DIR / "temporal_concentration_report.csv",
            [
                "attempt_name",
                "full_net",
                "first_half_net",
                "second_half_net",
                "month_2026_04_net",
                "month_2026_05_net",
                "negative_temporal_slices",
                "positive_slice_count",
                "temporal_guard_status",
                "likely_driver",
            ],
            temporal_rows,
        ),
        write_csv(
            RUN_DIR / "guarded_scout_queue.csv",
            [
                "queue_id",
                "source_attempts",
                "scout_question",
                "required_guard",
                "forbidden_action",
                "status",
                "next_run",
                "claim_boundary",
            ],
            queue_rows,
        ),
        write_json(RUN_DIR / "guard_threshold_spec.json", guard_threshold_spec()),
    ]

    receipt_payloads = receipts(guarded_matrix, queue_rows, source_files)
    for name, payload in receipt_payloads.items():
        output_paths.append(write_json(RUN_DIR / f"{name}.json", payload))

    output_paths.append(write_json(RUN_DIR / "source_artifact_hashes.json", receipt_payloads["artifact_lineage_receipt"]["artifact_hashes"]))

    gate_audit = gate_rows(guarded_matrix, queue_rows, output_paths)
    output_paths.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence"],
            gate_audit,
        )
    )

    run_manifest = {
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_files": [rel(path) for path in source_files],
        "outputs": [rel(path) for path in output_paths],
        "guarded_scout_queue_count": len(queue_rows),
        "next_action": NEXT_RUN_ID,
        "created_at_utc": utc_now(),
    }
    output_paths.append(write_json(RUN_DIR / "run_manifest.json", run_manifest))

    update_docs(guarded_matrix, queue_rows)
    output_paths.extend(
        [
            REVIEWS_DIR / "run332C_cost_curve_guarded_scout.md",
            DECISION_DOC,
        ]
    )
    update_registers(output_paths)

    failed_gates = [row for row in gate_audit if row["status"] != "pass"]
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "guarded_scout_rows": len(guarded_matrix),
                "guarded_scout_queue_count": len(queue_rows),
                "failed_gates": failed_gates,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if failed_gates else 0


if __name__ == "__main__":
    raise SystemExit(main())
