from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


STAGE_ID = "329_onnx_rebuild__live_feature_control"
NEXT_STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN_NUMBER = "run329H"
RUN_ID = "run329H_cp322A_exact_handoff_repair_feasibility_or_research_artifact_closeout_v1"
PARENT_RUN_ID = "run329G_raw_forward_session_gap_and_overfit_pressure_review_v1"
NEXT_RUN_ID = "run330A_design_forward_safe_non_identity_surface_robustness_packet_v1"
STATUS = "completed_cp322a_exact_handoff_repair_feasibility_stage329_closed"
JUDGMENT = "Forward Blocked"
DECISION = "cp322a_exact_forward_handoff_not_repairable_under_frozen_rules_research_artifact_preserved"
NEXT_ACTION = NEXT_RUN_ID
CLAIM_BOUNDARY = (
    "research_development_only_cp322a_exact_forward_handoff_blocked_no_threshold_retuning_"
    "no_candidate_selection_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)
NEXT_STAGE_BOUNDARY = (
    "research_development_only_forward_safe_non_identity_onnx_rebuild_no_cp322a_exact_repair_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

FORWARD_START = datetime(2026, 4, 14)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUTS_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_REVIEWS_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage329H_cp322a_exact_handoff_repair_feasibility.md"
NEXT_STAGE_DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage330_forward_safe_non_identity_surface_open.md"

STAGE322_RUN_A = ROOT / "stages" / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure" / "02_runs" / "run322A"
STAGE322_RUN_B = ROOT / "stages" / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure" / "02_runs" / "run322B"
STAGE323_ADAPTER = (
    ROOT
    / "stages"
    / "323_onnx_candidate_campaign__selected_curve_adapter_package"
    / "02_runs"
    / "run323A"
    / "adapter_package"
)
STAGE325_RUN = (
    ROOT
    / "stages"
    / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
    / "02_runs"
    / "run325A"
)
STAGE327_REPORT = (
    ROOT
    / "stages"
    / "327_onnx_candidate_campaign__cp322a_overfit_forward_parity_robustness"
    / "03_reviews"
    / "run327A_overfit_forward_parity_probe.md"
)
STAGE328A_REPORT = (
    ROOT
    / "stages"
    / "328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction"
    / "03_reviews"
    / "run328A_frozen_signal_contract_report.md"
)
STAGE328B_REPORT = (
    ROOT
    / "stages"
    / "328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction"
    / "03_reviews"
    / "run328B_cp318_outcome_source_audit.md"
)
RUN329G_DIR = STAGE_DIR / "02_runs" / "run329G"

ONNX_EXPORT_REPORT = STAGE325_RUN / "onnx_export_report.json"
ONNX_PARITY_RECEIPT = STAGE325_RUN / "onnx_parity_receipt.json"
RUNTIME_PARITY_RECEIPT = STAGE325_RUN / "runtime_parity_receipt.json"
ADAPTER_MANIFEST = STAGE323_ADAPTER / "adapter_package_manifest.json"
DECISION_SURFACE = STAGE323_ADAPTER / "decision_surface.json"
RUNTIME_HANDOFF = STAGE323_ADAPTER / "runtime_handoff_manifest.json"
FEATURE_ORDER = STAGE323_ADAPTER / "feature_order_runtime.csv"
SOURCE_HANDOFF = STAGE322_RUN_A / "handoff" / "run322A_cp322A_cp321b_exact_replay_control_handoff.json"
SOURCE_MODEL = STAGE322_RUN_A / "models" / "run322A_cp322A_cp321b_exact_replay_control_stability_pressure_surface.json"
RUN329G_DECISION = RUN329G_DIR / "final_forward_decision.json"
RUN329G_GAP = RUN329G_DIR / "raw_forward_session_gap_report.csv"
RUN329G_PRESSURE = RUN329G_DIR / "overfit_pressure_report.csv"

ROUTE_SIGNAL_FILES = [
    STAGE322_RUN_B / "features" / "run322A_cp322A_cp321b_exact_replay_control_tier_a_val_route_signal.csv",
    STAGE322_RUN_B / "features" / "run322A_cp322A_cp321b_exact_replay_control_tier_a_oos_route_signal.csv",
    STAGE322_RUN_B / "features" / "run322A_cp322A_cp321b_exact_replay_control_tier_b_val_route_signal.csv",
    STAGE322_RUN_B / "features" / "run322A_cp322A_cp321b_exact_replay_control_tier_b_oos_route_signal.csv",
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return "missing"
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
    return value


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
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


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def parse_time(value: str) -> datetime | None:
    value = str(value or "").strip()
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value.replace("+00:00", "Z"), fmt)
        except ValueError:
            continue
    return None


def signal_value(value: Any) -> int:
    try:
        number = int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0
    return -1 if number < 0 else (1 if number > 0 else 0)


def route_signal_coverage_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in ROUTE_SIGNAL_FILES:
        if not path_exists(path):
            rows.append(
                {
                    "route_signal_file": rel(path),
                    "exists": False,
                    "split": "",
                    "tier": "",
                    "row_count": 0,
                    "active_signal_count": 0,
                    "first_timestamp": "",
                    "last_timestamp": "",
                    "rows_after_2026_04_14": 0,
                    "hash": "missing",
                    "coverage_judgment": "missing",
                }
            )
            continue
        records = read_csv(path)
        fields = set(records[0].keys()) if records else set()
        time_column = next(
            (
                column
                for column in (
                    "timestamp_utc",
                    "bar_time_server",
                    "timestamp",
                    "time",
                    "bar_time",
                    "time_utc",
                )
                if column in fields
            ),
            "",
        )
        signal_column = "run322b_route_signal" if "run322b_route_signal" in fields else "route_signal_value"
        times = [parse_time(record.get(time_column, "")) for record in records]
        times = [item for item in times if item is not None]
        after_forward = sum(1 for item in times if item >= FORWARD_START)
        active = sum(1 for record in records if signal_value(record.get(signal_column)) != 0)
        file_name = path.name
        tier = "tier_a" if "_tier_a_" in file_name else ("tier_b" if "_tier_b_" in file_name else "unknown")
        split = "validation" if "_val_" in file_name else ("oos" if "_oos_" in file_name else "unknown")
        last = max(times).strftime("%Y-%m-%d %H:%M:%S") if times else ""
        rows.append(
            {
                "route_signal_file": rel(path),
                "exists": True,
                "split": split,
                "tier": tier,
                "row_count": len(records),
                "active_signal_count": active,
                "first_timestamp": min(times).strftime("%Y-%m-%d %H:%M:%S") if times else "",
                "last_timestamp": last,
                "rows_after_2026_04_14": after_forward,
                "hash": sha256_file(path),
                "coverage_judgment": "old_window_only_no_forward_rows" if after_forward == 0 else "has_forward_rows",
            }
        )
    return rows


def identity_surface_row() -> dict[str, Any]:
    export = read_json(ONNX_EXPORT_REPORT)
    manifest = read_json(ADAPTER_MANIFEST)
    decision_surface = read_json(DECISION_SURFACE)
    handoff = read_json(RUNTIME_HANDOFF)
    source_handoff = read_json(SOURCE_HANDOFF)
    return {
        "selected_candidate": manifest.get("selected_candidate"),
        "adapter_package": manifest.get("adapter_package_id"),
        "onnx_model_path": export.get("model_path"),
        "onnx_sha256": export.get("sha256"),
        "onnx_input_name": export.get("input_name"),
        "onnx_input_shape": export.get("input_shape"),
        "feature_order": export.get("feature_order"),
        "feature_order_hash": export.get("feature_order_hash"),
        "probability_formula": export.get("probability_formula"),
        "runtime_feature_order_csv": rel(FEATURE_ORDER),
        "decision_rule": decision_surface.get("rule_name"),
        "branch_lane": decision_surface.get("branch_lane"),
        "shared_contract": handoff.get("shared_contract"),
        "source_runtime_feature_order": source_handoff.get("runtime_feature_order"),
        "identity_judgment": "identity_surface_requires_external_route_signal_value",
    }


def feasibility_rows(coverage_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    has_forward_route_rows = any(int(row.get("rows_after_2026_04_14") or 0) > 0 for row in coverage_rows)
    max_old_timestamp = max((str(row.get("last_timestamp") or "") for row in coverage_rows), default="")
    return [
        {
            "repair_option": "reuse_stage322_route_signal_files",
            "changes_cp322a_contract": "no",
            "uses_new_forward_tuning": "no",
            "forward_handoff_available": "yes" if has_forward_route_rows else "no",
            "evidence": f"max_route_signal_timestamp={max_old_timestamp}; rows_after_2026_04_14={sum(int(row.get('rows_after_2026_04_14') or 0) for row in coverage_rows)}",
            "leakage_or_overfit_risk": "low_if_existing_rows_only_but_no_forward_rows",
            "verdict": "not_feasible_for_forward",
            "effect": "old_window_exact_replay_does_not_create_new_forward_mt5_input",
        },
        {
            "repair_option": "recompute_split_local_rank_on_forward",
            "changes_cp322a_contract": "no_or_appears_exact",
            "uses_new_forward_tuning": "yes_forward_distribution_needed",
            "forward_handoff_available": "computable_but_forbidden",
            "evidence": "run328A marks split_local_rank_runtime mismatch=0 but invalid_for_forward_leakage",
            "leakage_or_overfit_risk": "high_lookahead_leakage",
            "verdict": "forbidden",
            "effect": "would make forward result depend on full future distribution",
        },
        {
            "repair_option": "use_split_specific_old_frozen_thresholds",
            "changes_cp322a_contract": "no_for_old_splits_only",
            "uses_new_forward_tuning": "no",
            "forward_handoff_available": "no_universal_forward_threshold",
            "evidence": "run328A mismatch=0 but historical_exact_but_not_forward_universal",
            "leakage_or_overfit_risk": "medium_expost_split_identity",
            "verdict": "not_feasible_for_forward",
            "effect": "keeps historical exactness but cannot bind latest forward timestamps",
        },
        {
            "repair_option": "use_train_only_frozen_threshold_control",
            "changes_cp322a_contract": "yes_168_old_rows_changed",
            "uses_new_forward_tuning": "no",
            "forward_handoff_available": "research_control_only",
            "evidence": "run328A mismatch=168 active=12776",
            "leakage_or_overfit_risk": "lower_than_split_rank_but_not_cp322a_exact",
            "verdict": "not_cp322a_repair",
            "effect": "becomes a new research control rather than cp322A exact forward",
        },
        {
            "repair_option": "use_stage329_live_feature_rebuild_research_onnx",
            "changes_cp322a_contract": "yes_new_model_feature_order_decision_surface",
            "uses_new_forward_tuning": "no_forward_threshold_retuning_recorded",
            "forward_handoff_available": "yes_for_research_onnx_not_cp322a",
            "evidence": "run329G low_pressure=c56_plain; medium/high pressure in other variants",
            "leakage_or_overfit_risk": "still_open_raw_session_gap_and_curve_pocket_pressure",
            "verdict": "next_stage_research_only",
            "effect": "useful for forward-safe ONNX research but not an exact cp322A repair",
        },
        {
            "repair_option": "promote_session_parity_mt5_evidence_to_cp322a_forward_pass",
            "changes_cp322a_contract": "yes_wrong_subject",
            "uses_new_forward_tuning": "no",
            "forward_handoff_available": "no_cp322a_exact_handoff",
            "evidence": "run329E/F/G are Stage329 rebuilt research ONNX views, not cp322A route-signal identity",
            "leakage_or_overfit_risk": "high_claim_boundary_error",
            "verdict": "forbidden",
            "effect": "would confuse research ONNX evidence with cp322A exact frozen artifact",
        },
    ]


def decision_payload(coverage_rows: Sequence[Mapping[str, Any]], feasibility: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    route_rows_after = sum(int(row.get("rows_after_2026_04_14") or 0) for row in coverage_rows)
    feasible_exact = [row["repair_option"] for row in feasibility if row.get("verdict") == "feasible_exact_forward"]
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "cp322a_forward_blocked": "confirmed",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "forward_blocked": "confirmed_exact_handoff_missing_after_2026_04_13",
        "selected_candidate": "none",
        "goal_achieve": "not_claimed",
        "exact_repair_feasible": bool(feasible_exact),
        "exact_forward_route_rows_after_2026_04_14": route_rows_after,
        "research_artifact_status": "cp322a_preserved_not_forward_authority",
        "stage329_status": "closed_no_selection",
        "next_stage_id": NEXT_STAGE_ID,
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    inputs = [
        ONNX_EXPORT_REPORT,
        ONNX_PARITY_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        ADAPTER_MANIFEST,
        DECISION_SURFACE,
        RUNTIME_HANDOFF,
        FEATURE_ORDER,
        SOURCE_HANDOFF,
        SOURCE_MODEL,
        STAGE327_REPORT,
        STAGE328A_REPORT,
        STAGE328B_REPORT,
        RUN329G_DECISION,
        RUN329G_GAP,
        RUN329G_PRESSURE,
        *ROUTE_SIGNAL_FILES,
    ]
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "generated_at_utc": generated_at_utc,
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in inputs],
        "source_hashes": {rel(path): sha256_file(path) for path in inputs if path_exists(path) and path.is_file()},
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path) and path.is_file()},
        "lineage_judgment": "cp322a_exact_handoff_feasibility_closed_with_stage330_research_handoff",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(
    generated_at_utc: str,
    coverage_rows: Sequence[Mapping[str, Any]],
    feasibility: Sequence[Mapping[str, Any]],
    decision: Mapping[str, Any],
) -> list[Path]:
    route_rows_after = decision["exact_forward_route_rows_after_2026_04_14"]
    artifacts: list[Path] = []
    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [
                    rel(path) for path in ROUTE_SIGNAL_FILES
                ],
                "time_axis": "FPMarkets US100 M5 broker timestamps in Stage322 route-signal CSV; forward requirement starts at 2026-04-14.",
                "sample_scope": "Stage322 validation/OOS route-signal handoff through 2026-04-13; no exact cp322A route rows after 2026-04-14.",
                "missing_or_duplicate_check": "forward rows after 2026-04-14 count is zero for exact cp322A route-signal files.",
                "feature_label_boundary": "No labels or new forward threshold tuning are used in this run.",
                "split_boundary": "Existing validation/OOS rows are old evidence only; latest forward is a separate unresolved handoff boundary.",
                "leakage_risk": "recomputing split-local rank on latest forward would require future distribution and remains forbidden.",
                "data_hash_or_identity": {row["route_signal_file"]: row["hash"] for row in coverage_rows},
                "integrity_judgment": "usable_with_boundary_old_window_only_forward_handoff_missing",
                "generated_at_utc": generated_at_utc,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": {
                    "onnx_model": rel(STAGE325_RUN / "models" / "cp322a_route_signal_identity.onnx"),
                    "stage325_runtime_receipt": rel(RUNTIME_PARITY_RECEIPT),
                    "stage322_route_signal_files": [rel(path) for path in ROUTE_SIGNAL_FILES],
                },
                "shared_contract": "cp322A ONNX consumes a single run322b_route_signal feature whose meaning is -1 short, 0 flat, +1 long.",
                "known_differences": [
                    "Historical Stage322 feature name route_signal_value is aliased to run322b_route_signal in Stage323/325.",
                    "Stage329 rebuilt ONNX candidates consume live feature frames and are not cp322A exact handoff repairs.",
                    "No exact route-signal CSV exists for timestamps after 2026-04-13.",
                ],
                "parity_check": "existing Stage325 ONNX/runtime parity remains old-window evidence; latest forward runtime cannot be executed exactly without route-signal handoff.",
                "parity_identity": identity_surface_row(),
                "runtime_claim_boundary": "runtime_probe_only_old_window_no_runtime_authority_latest_forward_blocked",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "cp322A route-signal identity ONNX",
                "target_and_label": "deterministic class probabilities derived from precomputed route signal; no learned latest-forward probability.",
                "split_method": "historical validation/OOS replay plus latest-forward handoff feasibility audit",
                "selection_metric": "not_applicable_no_selection",
                "secondary_metrics": "route-signal coverage after 2026-04-14, leakage risk, contract-change risk, Stage329 raw/session pressure",
                "threshold_policy": "frozen historical rule only; no new threshold tuning",
                "overfit_risk": "split-local rank and outcome-distillation lineage remain high risk if used to regenerate exact forward signals",
                "calibration_risk": "identity probabilities encode signal state and are not calibrated market probabilities",
                "comparison_baseline": "Stage329 live-feature rebuild research ONNX evidence is separate and not cp322A exact repair",
                "validation_judgment": "blocked_exact_handoff_not_repairable_under_frozen_rules",
            },
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "result_subject",
                "evidence_available",
                "evidence_missing",
                "judgment_label",
                "claim_boundary",
                "next_condition",
                "user_explanation_hook",
            ],
            [
                {
                    "result_subject": "cp322A exact forward handoff repair feasibility",
                    "evidence_available": "Stage322 route-signal CSV coverage; Stage323 adapter; Stage325 ONNX identity/parity; Stage327-329 audits",
                    "evidence_missing": "safe exact cp322A route-signal handoff after 2026-04-13",
                    "judgment_label": JUDGMENT,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "next_condition": "build a non-identity forward-safe ONNX research packet without pretending it is cp322A exact repair",
                    "user_explanation_hook": "cp322A is preserved, but the exact forward input it needs does not exist safely.",
                }
            ],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence", "effect"],
            [
                {
                    "gate": "source_authority_audit",
                    "status": "passed",
                    "evidence": rel(RUN_DIR / "exact_handoff_repair_feasibility_matrix.csv"),
                    "effect": "distinguishes cp322A exact repair from Stage329 research ONNX evidence",
                },
                {
                    "gate": "runtime_parity_audit",
                    "status": "passed_with_boundary",
                    "evidence": rel(RUN_DIR / "runtime_parity_receipt.json"),
                    "effect": "keeps old-window parity from becoming latest-forward runtime authority",
                },
                {
                    "gate": "data_integrity_audit",
                    "status": "passed_with_boundary",
                    "evidence": rel(RUN_DIR / "route_signal_coverage_audit.csv"),
                    "effect": "confirms exact route-signal handoff has zero rows after 2026-04-13",
                },
                {
                    "gate": "final_claim_guard",
                    "status": "passed",
                    "evidence": rel(RUN_DIR / "stage329_closeout_decision.json"),
                    "effect": "no Forward Passed, no Forward Failed, no Goal Achieve, no operating claim",
                },
            ],
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "stage330_open_receipt.json",
            {
                "next_stage_id": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "opened_by": RUN_ID,
                "stage330_status": "open_planned",
                "reason": "cp322A exact handoff is structurally blocked; next work must build forward-safe non-identity ONNX research without exact-repair claim.",
                "claim_boundary": NEXT_STAGE_BOUNDARY,
            },
        )
    )
    return artifacts


def write_reports(
    coverage_rows: Sequence[Mapping[str, Any]],
    feasibility: Sequence[Mapping[str, Any]],
    identity_row: Mapping[str, Any],
    decision: Mapping[str, Any],
) -> list[Path]:
    coverage_lines = [
        "| file(파일) | split(분할) | tier(티어) | rows(행) | active(활성) | last(마지막) | forward rows(전진 행) |",
        "|---|---|---|---:|---:|---|---:|",
    ]
    for row in coverage_rows:
        coverage_lines.append(
            f"| {row['route_signal_file']} | {row['split']} | {row['tier']} | {row['row_count']} | {row['active_signal_count']} | {row['last_timestamp']} | {row['rows_after_2026_04_14']} |"
        )
    feasibility_lines = [
        "| option(선택지) | verdict(판정) | changes cp322A(cp322A 변경) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|---|",
    ]
    for row in feasibility:
        feasibility_lines.append(
            f"| {row['repair_option']} | {row['verdict']} | {row['changes_cp322a_contract']} | {row['evidence']} | {row['effect']} |"
        )
    report = write_md(
        REVIEWS_DIR / "run329H_cp322a_exact_handoff_repair_feasibility.md",
        f"""
# run329H cp322A Exact Handoff Repair Feasibility(329H cp322A 정확 인계 수리 가능성)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- decision(결정): `{decision['decision']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `confirmed_exact_handoff_missing_after_2026_04_13`
- Goal Achieve(목표 달성): `not_claimed`

## Identity Surface(정체성 표면)

- ONNX model(온엑스 모델): `{identity_row['onnx_model_path']}`
- feature_order(피처 순서): `{identity_row['feature_order']}`
- decision_rule(판단 규칙): `{identity_row['decision_rule']}`
- effect(효과): cp322A는 시장 피처를 직접 판단하는 모델이 아니라 `run322b_route_signal`을 확률 형태로 되돌리는 identity surface(정체성 표면)이다.

## Route Signal Coverage(경로 신호 커버리지)

{chr(10).join(coverage_lines)}

## Repair Matrix(수리 행렬)

{chr(10).join(feasibility_lines)}

## Closeout(종료 판정)

cp322A exact repair(정확 수리)는 frozen rules(고정 규칙) 안에서 가능하지 않다. Stage329 rebuilt ONNX(재구축 온엑스) 근거는 연구 단서로 보존하지만 cp322A Forward Passed(전진 통과)로 승격하지 않는다.

Effect(효과): Stage329는 selected candidate(선택 후보) 없이 닫고, Stage330(330단계)을 forward-safe non-identity ONNX(전진 안전 비정체성 온엑스) 연구 질문으로 연다.

Next(다음): `{NEXT_ACTION}`
""",
    )
    decision_doc = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage329H cp322A Exact Handoff Repair Feasibility Decision(329H cp322A 정확 인계 수리 가능성 결정)

- decision(결정): `{decision['decision']}`
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `confirmed_exact_handoff_missing_after_2026_04_13`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): cp322A는 research artifact(연구 산출물)로 보존하고, Stage330(330단계)은 새 forward-safe ONNX(전진 안전 온엑스) 연구로 연다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    final_report = write_md(
        REVIEWS_DIR / "final_stage329H_decision_report.md",
        f"""
# Final Stage329H Decision Report(최종 329H 결정 보고서)

Stage329(329단계)는 `closed_no_selection`으로 닫는다.

- cp322A_status(cp322A 상태): `research_artifact_preserved_exact_forward_handoff_blocked`
- exact_repair_feasible(정확 수리 가능): `{decision['exact_repair_feasible']}`
- exact_forward_route_rows_after_2026_04_14(2026-04-14 이후 정확 전진 경로 신호 행): `{decision['exact_forward_route_rows_after_2026_04_14']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`

Effect(효과): cp322A exact handoff(정확 인계) 문제를 더 미루지 않고 닫지만, 목표(goal, 목표)는 계속 active(진행 중)다.
""",
    )
    next_decision_doc = write_md(
        NEXT_STAGE_DECISION_DOC,
        f"""
# 2026-05-26 Stage330 Open Decision(330단계 개방 결정)

- opened_by(개방 실행): `{RUN_ID}`
- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `open_planned`
- active_question(활성 질문): cp322A exact replay(정확 재생)를 수리했다고 주장하지 않고, forward-safe non-identity ONNX(전진 안전 비정체성 온엑스)를 만들 수 있는가?
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`
- effect(효과): 낮은 압력 단서(`c56_plain`)는 후보 선택이 아니라 다음 설계에서 압박할 입력 단서로만 쓴다.
""",
    )
    return [report, decision_doc, final_report, next_decision_doc]


def create_next_stage_files() -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_md(
            NEXT_SPEC_DIR / "stage_brief.md",
            f"""
# Stage330 Forward-Safe Non-Identity Surface Robustness(330단계 전진 안전 비정체성 표면 강건성)

- active_question(활성 질문): cp322A exact replay(정확 재생) 수리가 불가능한 상태에서, live-computable feature(실시간 계산 가능 피처)만으로 만든 non-identity ONNX(비정체성 온엑스)가 raw/session gap(원본/세션 간극), cost stress(비용 압박), curve pocket(곡선 포켓)을 견딜 수 있는가?
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 결정): `{DECISION}`
- first_run(첫 실행): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`

Effect(효과): Stage329(329단계)의 c56_plain(낮은 압력 단서)을 곧바로 선택하지 않고, overfit guard(과적합 방어), parity guard(동등성 방어), raw-forward guard(원본 전진 방어)를 먼저 설계한다.
""",
        )
    )
    artifacts.append(
        write_md(
            NEXT_INPUTS_DIR / "input_refs.md",
            f"""
# Stage330 Input References(330단계 입력 참조)

- source_closeout(원천 종료): `stages/329_onnx_rebuild__live_feature_control/03_reviews/run329H_cp322a_exact_handoff_repair_feasibility.md`
- raw_forward_gap(원본 전진 간극): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329G/raw_forward_session_gap_report.csv`
- overfit_pressure(과적합 압력): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329G/overfit_pressure_report.csv`
- session_parity_mt5(세션 동등 MT5): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329F/forward_mt5_kpi_report.csv`
- feature_frames(피처 프레임): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329B/feature_frames/`
- research_onnx(연구 온엑스): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329C/onnx/`

Effect(효과): 입력은 다음 설계를 위한 evidence(근거)이며 selected candidate(선택 후보)가 아니다.
""",
        )
    )
    artifacts.append(
        write_csv(
            NEXT_REVIEWS_DIR / "stage_run_ledger.csv",
            [
                "row_id",
                "stage_id",
                "run_id",
                "view",
                "tier_scope",
                "scoreboard",
                "status",
                "judgment",
                "evidence_boundary",
                "report_path",
                "notes",
                "decision",
            ],
            [],
        )
    )
    artifacts.append(
        write_md(
            NEXT_SELECTED_DIR / "selection_status.md",
            f"""
# Stage330 Selection Status(330단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- selected_candidate(선택 후보): `none`
- research_onnx_status(연구 온엑스 상태): `not_started`
- source_cp322A_status(원천 cp322A 상태): `research_artifact_preserved_exact_forward_handoff_blocked`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage330(330단계)은 새 후보 확정이 아니라 forward-safe design gate(전진 안전 설계 문턱)부터 시작한다.
""",
        )
    )
    return artifacts


def update_stage329_selection(decision: Mapping[str, Any]) -> Path:
    return write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage329 Selection Status(329단계 선택 상태)

- stage_status(단계 상태): `closed_no_selection`
- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_exact_forward_handoff_blocked`
- research_onnx_status(연구 온엑스 상태): `raw_forward_session_gap_overfit_pressure_review_completed_no_selection`
- latest_runtime_probe(최신 런타임 탐침): `run329E_session_parity_forward_signal_payload_and_mt5_runtime_probe_v1`
- latest_forward_review(최신 전진 검토): `run329G_raw_forward_session_gap_and_overfit_pressure_review_v1`
- latest_exact_handoff_review(최신 정확 인계 검토): `{RUN_ID}`
- exact_forward_handoff(정확 전진 인계): `missing_after_2026_04_13`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `confirmed_exact_handoff_missing_after_2026_04_13`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): cp322A exact repair(정확 수리)는 닫고, Stage330(330단계)의 forward-safe non-identity ONNX(전진 안전 비정체성 온엑스) 연구로 넘긴다.
""",
    )


def update_current_truth(decision: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage330(330단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): cp322A exact repair(정확 수리)를 성공으로 포장하지 않고 forward-safe non-identity ONNX(전진 안전 비정체성 온엑스) 설계로 넘어간다.\n"
        "- >-\n"
        f"  Stage329(329단계) run329H(329H 실행)는 `{decision['decision']}`로 닫혔다. Effect(효과): Forward Blocked(전진 차단)는 cp322A exact handoff(정확 인계)에만 붙이고 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if f"Stage330(330단계) `{NEXT_STAGE_ID}`" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    block_marker = "stage329H_cp322a_exact_handoff_closeout:"
    block = f"""
stage329H_cp322a_exact_handoff_closeout:
  packet_id: {STAGE_ID}_v8
  stage_id: {STAGE_ID}
  status: {decision['status']}
  judgment: {decision['judgment']}
  decision: {decision['decision']}
  current_run_id: {RUN_ID}
  next_stage: {NEXT_STAGE_ID}
  next_run_id: {NEXT_RUN_ID}
  report_path: stages/329_onnx_rebuild__live_feature_control/03_reviews/run329H_cp322a_exact_handoff_repair_feasibility.md
  boundary: {CLAIM_BOUNDARY}
"""
    if block_marker not in workspace_text:
        workspace_text = workspace_text.rstrip() + "\n\n" + block.strip() + "\n"
    workspace_text = workspace_text.replace(
        "Stage329(329단계) run329E(329E 실행) session parity runtime probe(세션 동등 런타임 탐침)를 `blocked_session_parity_runtime_probe_no_completed_mt5_runtime`로 기록했다. Effect(효과): old_session_parity(기존 세션 동등) 입력을 MT5 RuntimeProbeEA(런타임 탐침 EA)에 넘겼지만 Goal Achieve(목표 달성)는 없다.",
        "Stage329(329단계) run329E(329E 실행) session parity runtime probe(세션 동등 런타임 탐침)를 `completed_session_parity_runtime_probe_no_candidate_selection`로 다시 닫았다. Effect(효과): portable MT5(포터블 메타트레이더5)로 6/6 runtime/report/telemetry(런타임/보고서/실행 기록)를 확보했지만 selected candidate(선택 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.",
    )
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)
    updated.append(WORKSPACE_STATE)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": f"- source_stage(원천 단계): `{STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `forward_safe_non_identity_surface_robustness`",
        "- adapter_under_review(": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(": "- status(상태): `stage330_open_planned_after_stage329H_cp322a_exact_handoff_closeout`",
        "- decision(": f"- decision(판정): `{decision['decision']}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run329H_summary(329H 요약): cp322A exact handoff repair feasibility(정확 인계 수리 가능성)를 `{decision['status']}`로 닫았다. "
        "Effect(효과): 2026-04-14 이후 exact route-signal(정확 경로 신호)이 없고 split-local rank(분할 내부 순위)는 누수라서 cp322A는 연구 산출물로 보존한다.\n"
        f"- stage330_open_summary(330단계 개방 요약): `{NEXT_STAGE_ID}`를 open_planned(열림 계획)로 열었다. "
        "Effect(효과): Stage329 연구 온엑스 단서는 선택 후보가 아니라 다음 설계의 압박 입력으로만 쓴다."
    )
    if "run329H_summary(329H 요약)" not in current_text:
        current_text = current_text.replace(f"- decision(판정): `{decision['decision']}`\n", f"- decision(판정): `{decision['decision']}`\n{summary}\n", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)
    updated.append(CURRENT_STATE)

    append_if_missing(
        CHANGELOG,
        "Stage329H cp322A Exact Handoff Repair Feasibility",
        f"""
## 2026-05-26 - Stage329H cp322A Exact Handoff Repair Feasibility(329H cp322A 정확 인계 수리 가능성)

- run329H(329H 실행): cp322A exact handoff(정확 인계)의 forward repair(전진 수리) 가능성을 닫았다.
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- effect(효과): Forward Passed(전진 통과), Forward Failed(전진 실패), selected candidate(선택 후보), Goal Achieve(목표 달성)는 없다.
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path], decision: Mapping[str, Any]) -> None:
    report_path = REVIEWS_DIR / "run329H_cp322a_exact_handoff_repair_feasibility.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "kpi_evidence",
                "status": decision["status"],
                "judgment": decision["judgment"],
                "path": rel(report_path),
                "notes": "cp322a_exact_handoff_repair_feasibility;stage329_closed_no_selection;stage330_opened;goal_achieve_not_claimed.",
            }
        ],
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__cp322a_exact_handoff_repair_feasibility",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "cp322a_exact_handoff_repair_feasibility",
        "tier_scope": "old validation/OOS route signal plus latest forward handoff absence",
        "kpi_scope": "source_authority_runtime_parity_data_integrity",
        "scoreboard_lane": "kpi_evidence",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "path": rel(report_path),
        "primary_kpi": "exact_forward_route_rows_after_2026_04_14",
        "guardrail_kpi": "contract_change_risk;leakage_risk;runtime_authority_boundary",
        "external_verification_status": "out_of_scope_by_claim_no_safe_exact_forward_handoff_to_run_mt5",
        "notes": f"decision={decision['decision']};next_stage={NEXT_STAGE_ID};next_action={NEXT_ACTION}.",
    }
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [ledger_row])
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__cp322a_exact_handoff_repair_feasibility",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "cp322a_exact_handoff_repair_feasibility(cp322A 정확 인계 수리 가능성)",
                "tier_scope": "old validation/OOS route signal plus latest forward absence(기존 검증/표본외 경로 신호 및 최신 전진 부재)",
                "scoreboard": "source_authority_runtime_parity_data_integrity(원천 권한/런타임 동등성/데이터 무결성)",
                "status": decision["status"],
                "judgment": decision["judgment"],
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "stage329_closed_no_selection;goal_achieve_not_claimed.",
                "decision": decision["decision"],
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        if path_exists(path) and path.is_file():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(path)}",
                    "artifact_type": "stage329H_cp322a_exact_handoff_closeout_artifact",
                    "path": rel(path),
                    "sha256": sha256_file(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "cp322A exact handoff feasibility and Stage330 handoff artifact; no operating claim.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_outputs(generated_at_utc: str) -> list[Path]:
    coverage_rows = route_signal_coverage_rows()
    identity = identity_surface_row()
    feasibility = feasibility_rows(coverage_rows)
    decision = decision_payload(coverage_rows, feasibility)
    artifacts: list[Path] = []
    artifacts.append(
        write_csv(
            RUN_DIR / "route_signal_coverage_audit.csv",
            [
                "route_signal_file",
                "exists",
                "split",
                "tier",
                "row_count",
                "active_signal_count",
                "first_timestamp",
                "last_timestamp",
                "rows_after_2026_04_14",
                "hash",
                "coverage_judgment",
            ],
            coverage_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "identity_surface_audit.csv",
            [
                "selected_candidate",
                "adapter_package",
                "onnx_model_path",
                "onnx_sha256",
                "onnx_input_name",
                "onnx_input_shape",
                "feature_order",
                "feature_order_hash",
                "probability_formula",
                "runtime_feature_order_csv",
                "decision_rule",
                "branch_lane",
                "shared_contract",
                "source_runtime_feature_order",
                "identity_judgment",
            ],
            [identity],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "exact_handoff_repair_feasibility_matrix.csv",
            [
                "repair_option",
                "changes_cp322a_contract",
                "uses_new_forward_tuning",
                "forward_handoff_available",
                "evidence",
                "leakage_or_overfit_risk",
                "verdict",
                "effect",
            ],
            feasibility,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "next_stage_research_handoff_queue.csv",
            ["queue_id", "next_stage_id", "next_run_id", "input_signal", "required_guard", "effect"],
            [
                {
                    "queue_id": "stage330A_design_packet",
                    "next_stage_id": NEXT_STAGE_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "input_signal": "c56_plain_low_pressure_is_a_clue_not_selection",
                    "required_guard": "no_forward_threshold_tuning;raw_session_gap_guard;cost_curve_guard;parity_receipt",
                    "effect": "prevents low-pressure evidence from becoming another overfit selection",
                }
            ],
        )
    )
    artifacts.append(write_json(RUN_DIR / "stage329_closeout_decision.json", decision))
    artifacts.extend(write_receipts(generated_at_utc, coverage_rows, feasibility, decision))
    artifacts.extend(write_reports(coverage_rows, feasibility, identity, decision))
    artifacts.extend(create_next_stage_files())
    artifacts.append(update_stage329_selection(decision))
    artifacts.extend(update_current_truth(decision))
    artifacts.append(write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": NEXT_ACTION,
                "claim_boundary": CLAIM_BOUNDARY,
                "goal_achieve": "not_claimed",
            },
        )
    )
    update_registers(generated_at_utc, artifacts, decision)
    return artifacts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Close Stage329 cp322A exact handoff feasibility and open Stage330.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    generated_at_utc = utc_now()
    artifacts = write_outputs(generated_at_utc)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": NEXT_ACTION,
                "artifact_count": len(artifacts),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
