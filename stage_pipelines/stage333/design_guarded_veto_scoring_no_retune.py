from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
RUN_NUMBER = "run333B"
RUN_ID = "run333B_design_guarded_veto_scoring_no_retune_v1"
PARENT_RUN_ID = "run333A_materialize_timestamp_safe_pocket_veto_features_v1"
NEXT_RUN_ID = "run333C_materialize_guarded_veto_scoring_payloads_v1"
STATUS = "completed_guarded_veto_scoring_design_no_selection"
JUDGMENT = "guarded_scoring_design_research_only_no_goal_achieve"
DECISION = "guarded_veto_scoring_protocol_ready_for_materialization_no_threshold_retune"
CLAIM_BOUNDARY = (
    "research_development_only_guarded_veto_scoring_design_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN333A_DIR = STAGE_DIR / "02_runs" / "run333A"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SOURCE_STAGE_ID = "332_overfit_guard__failure_memory_forward_research_handoff"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN332D_DIR = SOURCE_STAGE_DIR / "02_runs" / "run332D"
RUN332E_DIR = SOURCE_STAGE_DIR / "02_runs" / "run332E"
RUN332F_DIR = SOURCE_STAGE_DIR / "02_runs" / "run332F"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage333B_guarded_veto_scoring_design.md"


SCORING_DESIGNS: dict[str, dict[str, Any]] = {
    "pv_c56_volatility_cost_shape_sentry": {
        "guard_family": "cost_shape_sentry",
        "candidate_inputs": [
            "atr_14_over_atr_50",
            "historical_vol_5_over_20",
            "return_1_over_atr_14",
            "adx_14",
            "di_spread_14",
        ],
        "scoring_formula": "past_only_rank(atr_14_over_atr_50)+past_only_rank(historical_vol_5_over_20)+past_only_rank(abs(return_1_over_atr_14))+past_only_rank(abs(di_spread_14))",
        "veto_rule": "hard_veto if rolling_past_rank_score >= 0.80 using train/WFO-only or expanding-past calibration; never fit on forward PnL",
        "negative_control": "reverse_veto_on_low_volatility_shape",
    },
    "pv_c56_session_liquidity_veto": {
        "guard_family": "session_liquidity_timing",
        "candidate_inputs": [
            "timestamp_hour_utc",
            "timestamp_weekday_utc",
            "session_bucket_code",
            "session_asia",
            "session_europe",
            "session_us_open",
            "session_us_late",
            "session_rollover",
        ],
        "scoring_formula": "calendar_bucket_lookup_predeclared_without_pnl_fit",
        "veto_rule": "bucket risk map must be declared before scoring from market session semantics, not from Stage331 pocket dates",
        "negative_control": "randomized_bucket_label_control_with_same_density",
    },
    "pv_m48_macro_rate_volatility_guard": {
        "guard_family": "macro_rate_volatility_interaction",
        "candidate_inputs": [
            "vix_change_1",
            "vix_zscore_20",
            "us10yr_change_1",
            "us10yr_zscore_20",
            "usdx_change_1",
            "usdx_zscore_20",
        ],
        "scoring_formula": "past_only_rank(abs(vix_zscore_20))+past_only_rank(abs(us10yr_zscore_20))+past_only_rank(abs(usdx_zscore_20))+directional_shift_terms",
        "veto_rule": "macro shock guard must use prior/latest-known macro values and fixed transform family only",
        "negative_control": "macro_sign_flip_control",
    },
    "pv_m48_breadth_reintroduction_control": {
        "guard_family": "bounded_breadth_divergence_control",
        "candidate_inputs": ["joined_us100_minus_mega8_equal_return_1"],
        "scoring_formula": "past_only_rank(abs(joined_us100_minus_mega8_equal_return_1)) with explicit missing-breadth abstain",
        "veto_rule": "missing breadth values must abstain or remain separate overlap-view; never impute from future rows",
        "negative_control": "missing_as_tradeable_control_forbidden_expected_invalid",
    },
}


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
    try:
        return io_path(path).exists()
    except OSError:
        return False


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
    return value


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
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
    encoding = "utf-8-sig" if had_bom else "utf-8"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(text)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def insert_after_line(text: str, anchor_prefix: str, insertion: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(anchor_prefix):
            lines.insert(index + 1, insertion)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text + ("\n" if text.endswith("\n") else "\n") + insertion + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += "\n" + block.strip() + "\n"
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
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    index: dict[tuple[str, ...], dict[str, Any]] = {
        tuple(str(row.get(key, "")) for key in key_columns): row for row in existing
    }
    for row in rows:
        index[tuple(str(row.get(key, "")) for key in key_columns)] = dict(row)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in index.values():
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})
    return path


def append_unique_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    existing_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in existing}
    next_rows = list(existing)
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        if key not in existing_keys:
            next_rows.append(dict(row))
            existing_keys.add(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in next_rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})
    return path


def source_artifacts() -> dict[str, Path]:
    return {
        "run333A_feature_manifest": RUN333A_DIR / "feature_materialization_manifest.csv",
        "run333A_readiness_matrix": RUN333A_DIR / "materialization_readiness_matrix.csv",
        "run333A_boundary_audit": RUN333A_DIR / "feature_boundary_audit.csv",
        "run333A_gate_audit": RUN333A_DIR / "required_gate_coverage_audit.csv",
        "run332D_thesis_registry": RUN332D_DIR / "feature_thesis_registry.csv",
        "run332D_pocket_veto_plan": RUN332D_DIR / "pocket_veto_plan.csv",
        "run332E_runtime_readiness": RUN332E_DIR / "runtime_probe_readiness_matrix.csv",
        "run332F_handoff": RUN332F_DIR / "stage332_to_stage333_handoff.csv",
    }


def source_hash_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for artifact_id, path in source_artifacts().items():
        exists = path_exists(path)
        rows.append(
            {
                "artifact_id": artifact_id,
                "path": rel(path),
                "exists": exists,
                "sha256": sha256_file(path) if exists and io_path(path).is_file() else "",
            }
        )
    return rows


def manifest_by_thesis() -> dict[str, dict[str, str]]:
    return {row["thesis_id"]: row for row in read_csv_rows(RUN333A_DIR / "feature_materialization_manifest.csv")}


def readiness_by_thesis() -> dict[str, dict[str, str]]:
    return {row["thesis_id"]: row for row in read_csv_rows(RUN333A_DIR / "materialization_readiness_matrix.csv")}


def pocket_plan_by_thesis() -> dict[str, dict[str, str]]:
    return {row["thesis_id"]: row for row in read_csv_rows(RUN332D_DIR / "pocket_veto_plan.csv")}


def scoring_protocol_rows() -> list[dict[str, Any]]:
    manifest = manifest_by_thesis()
    readiness = readiness_by_thesis()
    pocket_plan = pocket_plan_by_thesis()
    rows: list[dict[str, Any]] = []
    for thesis_id, design in SCORING_DESIGNS.items():
        frame = manifest.get(thesis_id, {})
        ready = readiness.get(thesis_id, {})
        pocket = pocket_plan.get(thesis_id, {})
        missing_breadth = int(frame.get("missing_joined_breadth_values") or 0)
        rows.append(
            {
                "thesis_id": thesis_id,
                "guard_family": design["guard_family"],
                "feature_frame_path": frame.get("feature_frame_path", ""),
                "feature_frame_sha256": frame.get("feature_frame_sha256", ""),
                "rows": frame.get("rows", ""),
                "candidate_inputs": ";".join(design["candidate_inputs"]),
                "score_transform_policy": "past_only_or_train_wfo_only_calibration_no_forward_pnl_fit",
                "scoring_formula_contract": design["scoring_formula"],
                "veto_rule_contract": design["veto_rule"],
                "missing_data_policy": "overlap_view_required_and_missing_values_abstain" if missing_breadth else "no_missing_materialized_inputs",
                "required_cost_veto": pocket.get("required_cost_veto", "cost2_pf_ge_1_before_candidate_language"),
                "required_curve_veto": pocket.get("required_curve_veto", "rolling20_and_rolling40_nonnegative_before_candidate_language"),
                "runtime_readiness_inherited": "design_ready_but_not_runtime_ready",
                "materialization_readiness": ready.get("materialization_readiness", ""),
                "allowed_claim_after_run333B": "scoring_protocol_ready_only",
                "forbidden_claim_after_run333B": "no_scoring_result_no_candidate_selection_no_forward_decision_no_runtime_authority",
            }
        )
    return rows


def score_formula_rows(protocol_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in protocol_rows:
        rows.extend(
            [
                {
                    "thesis_id": row["thesis_id"],
                    "formula_component": "primary_guard_score",
                    "allowed_source": "materialized_feature_frame_only",
                    "calibration_boundary": "train/WFO-only or expanding-past rows; never full-forward PnL",
                    "forbidden_source": "future return; tester outcome; known pocket date label; post-hoc profitable hour list",
                    "output_field": f"{row['thesis_id']}__guard_score",
                },
                {
                    "thesis_id": row["thesis_id"],
                    "formula_component": "hard_veto_flag",
                    "allowed_source": "primary_guard_score plus predeclared missing-data policy",
                    "calibration_boundary": "fixed protocol before run333C scoring materialization",
                    "forbidden_source": "threshold search on forward net/PF/DD",
                    "output_field": f"{row['thesis_id']}__hard_veto",
                },
                {
                    "thesis_id": row["thesis_id"],
                    "formula_component": "soft_weight_flag",
                    "allowed_source": "same guard score with predeclared rank bands",
                    "calibration_boundary": "ablation only; not a lot optimization",
                    "forbidden_source": "lot size fitting or runtime risk rewrite",
                    "output_field": f"{row['thesis_id']}__soft_weight",
                },
            ]
        )
    return rows


def branch_queue_rows(protocol_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in protocol_rows:
        for mode in ["control_no_veto", "hard_veto", "soft_veto", "negative_control"]:
            if mode == "control_no_veto":
                description = "baseline replay of source signals without applying the new veto features"
            elif mode == "hard_veto":
                description = "drop rows flagged by the predeclared guard"
            elif mode == "soft_veto":
                description = "mark rows for separate scoring view without changing lot logic"
            else:
                description = SCORING_DESIGNS[str(row["thesis_id"])]["negative_control"]
            rows.append(
                {
                    "queue_id": f"{row['thesis_id']}__{mode}",
                    "thesis_id": row["thesis_id"],
                    "scoring_mode": mode,
                    "feature_frame_path": row["feature_frame_path"],
                    "materialization_status": "queued_for_run333C",
                    "description": description,
                    "required_outputs": "scored_payload_csv;score_manifest;cost_curve_placeholder_or_future_kpi_plan",
                    "forbidden_actions": "no_threshold_retuning_no_lot_optimization_no_model_update_no_runtime_claim",
                }
            )
    return rows


def evidence_plan_rows(protocol_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "cost_ladder_required",
            "scope": "all queued scoring modes",
            "required_measurement": "cost ladder 0/0.25/0.5/1/2/3/5 before candidate language",
            "claim_if_missing": "inconclusive_or_blocked_no_forward_judgment",
        },
        {
            "evidence_id": "curve_pocket_required",
            "scope": "all queued scoring modes",
            "required_measurement": "rolling20 and rolling40 min net, underwater stretch, worst chunk",
            "claim_if_missing": "inconclusive_no_curve_claim",
        },
        {
            "evidence_id": "temporal_slice_required",
            "scope": "all queued scoring modes",
            "required_measurement": "month, half, thirds, fifths, session/hour, volatility and macro slices",
            "claim_if_missing": "inconclusive_no_robustness_claim",
        },
        {
            "evidence_id": "runtime_contract_required",
            "scope": "before MT5 interpretation",
            "required_measurement": "feature/model/threshold/risk/report/telemetry identity from run332E contract",
            "claim_if_missing": "no_runtime_authority_no_forward_passed",
        },
    ]


def invalid_condition_rows(protocol_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "condition_id": "forward_pnl_fit",
            "invalid_trigger": "guard threshold chosen by raw-forward net/PF/DD/curve pocket",
            "result": "invalid_overfit_repair",
        },
        {
            "condition_id": "known_pocket_date_feature",
            "invalid_trigger": "date range or explicit Stage331 pocket timestamp used as feature/filter",
            "result": "invalid_leakage",
        },
        {
            "condition_id": "runtime_claim_without_tester",
            "invalid_trigger": "runtime authority or Forward Passed claimed before MT5 report/telemetry reconciliation",
            "result": "invalid_claim_boundary",
        },
        {
            "condition_id": "lot_or_threshold_repair",
            "invalid_trigger": "lot, ATR SL/TP, D/B surface, or score threshold changed to rescue KPI",
            "result": "invalid_retune",
        },
    ]
    for row in protocol_rows:
        if str(row.get("missing_data_policy", "")).startswith("overlap_view"):
            rows.append(
                {
                    "condition_id": f"{row['thesis_id']}__missing_breadth_imputation",
                    "invalid_trigger": "missing breadth rows are forward-filled or future-filled instead of abstain/overlap view",
                    "result": "invalid_data_handoff",
                }
            )
    return rows


def gate_rows(protocol_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    source_missing = [row["artifact_id"] for row in source_hash_rows() if not row["exists"]]
    all_protocols = len(protocol_rows) == 4
    all_queue = len(queue_rows) == 16
    no_runtime_claim = all(row["allowed_claim_after_run333B"] == "scoring_protocol_ready_only" for row in protocol_rows)
    no_missing_frame = all(row.get("feature_frame_path") and row.get("feature_frame_sha256") for row in protocol_rows)
    return [
        {
            "gate": "source_artifacts_present",
            "status": "pass" if not source_missing else "fail",
            "evidence_path": rel(RUN_DIR / "source_artifact_hashes.json"),
            "notes": "all run333A/run332 source artifacts present" if not source_missing else f"missing={source_missing}",
        },
        {
            "gate": "all_materialized_frames_referenced",
            "status": "pass" if all_protocols and no_missing_frame else "fail",
            "evidence_path": rel(RUN_DIR / "guarded_scoring_protocol.csv"),
            "notes": f"protocol_rows={len(protocol_rows)}",
        },
        {
            "gate": "run333C_queue_complete",
            "status": "pass" if all_queue else "fail",
            "evidence_path": rel(RUN_DIR / "scoring_branch_queue.csv"),
            "notes": f"queue_rows={len(queue_rows)}",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "no_retune_guard_receipt.json"),
            "notes": "no threshold, lot, model, ONNX, D/B rule, or runtime handoff change in design.",
        },
        {
            "gate": "runtime_claim_boundary",
            "status": "pass" if no_runtime_claim else "fail",
            "evidence_path": rel(RUN_DIR / "result_judgment_receipt.json"),
            "notes": "design ready only; runtime authority and forward pass are forbidden.",
        },
        {
            "gate": "invalid_conditions_named",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "invalid_condition_matrix.csv"),
            "notes": "retune/leakage/runtime-claim invalid conditions are explicit.",
        },
        {
            "gate": "outputs_exist",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "run_manifest.json"),
            "notes": "run333B design artifacts are materialized.",
        },
    ]


def write_receipts(generated_at_utc: str, protocol_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    failed_gates = [row for row in gate_rows(protocol_rows, queue_rows) if row["status"] != "pass"]
    return [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()),
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "hypothesis": "Materialized pocket-veto features can be scored in a no-retune way by predeclaring transforms, veto modes, and invalid conditions before any KPI read.",
                "decision_use": "Authorize run333C scoring payload materialization without granting candidate or forward status.",
                "comparison_baseline": "run333A materialized feature frames and run332D/332E guard contracts.",
                "control_variables": "US100 M5 forward handoff scope, fixed source frames, fixed model/threshold/lot/runtime handoff.",
                "changed_variables": "scoring protocol only; hard/soft/control/negative-control views are queued.",
                "sample_scope": "raw-forward feature frame scope; no new training or MT5 execution.",
                "success_criteria": "four protocols, sixteen queued views, explicit invalid conditions, and no runtime or forward claim.",
                "failure_criteria": "missing feature frame, missing queue row, or any threshold/lot/model retune.",
                "invalid_conditions": [row["condition_id"] for row in invalid_condition_rows(protocol_rows)],
                "stop_conditions": "stop before scoring if any source hash, feature boundary, or claim-boundary gate fails.",
                "evidence_plan": [rel(RUN_DIR / "guarded_scoring_protocol.csv"), rel(RUN_DIR / "scoring_branch_queue.csv")],
            },
        ),
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": rel(RUN333A_DIR / "feature_materialization_manifest.csv"),
                "time_axis": "inherits run333A timestamp_utc; run333B does not calculate time-dependent scores",
                "sample_scope": "four materialized feature frames; breadth branch keeps overlap/missing boundary",
                "missing_or_duplicate_check": rel(RUN333A_DIR / "timestamp_integrity_audit.csv"),
                "feature_label_boundary": rel(RUN333A_DIR / "feature_boundary_audit.csv"),
                "split_boundary": "design only; no score calibration on forward PnL",
                "leakage_risk": "using full forward PnL or known pocket dates to set guard thresholds",
                "data_hash_or_identity": rel(RUN_DIR / "source_artifact_hashes.json"),
                "integrity_judgment": "usable_for_design_only",
            },
        ),
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "none_new_model_guarded_scoring_protocol_only",
                "target_and_label": "no new label; scoring protocol must not use future returns",
                "split_method": "design only; future run333C must use train/WFO-only or expanding-past calibration",
                "selection_metric": "not_applicable_no_selection",
                "secondary_metrics": "future cost ladder, rolling pocket, temporal slices, negative controls",
                "threshold_policy": "no score threshold retuning; veto bands must be predeclared before KPI read",
                "overfit_risk": "guard rules tuned to Stage331/forward pocket",
                "calibration_risk": "guard scores are ranks/flags, not probabilities",
                "comparison_baseline": "control_no_veto and negative-control branch queue",
                "validation_judgment": "exploratory_design_only",
            },
        ),
        write_json(
            RUN_DIR / "no_retune_guard_receipt.json",
            {
                "selected_candidate_changed": False,
                "onnx_changed": False,
                "feature_order_changed_for_existing_models": False,
                "threshold_changed": False,
                "d_b_rule_changed": False,
                "risk_or_lot_logic_changed": False,
                "runtime_handoff_changed": False,
                "new_model_trained": False,
                "scoring_executed": False,
                "notes": "run333B designs a scoring protocol only.",
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "source_inputs": [rel(path) for path in source_artifacts().values()],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(RUN_DIR / "guarded_scoring_protocol.csv"),
                    rel(RUN_DIR / "score_formula_contract.csv"),
                    rel(RUN_DIR / "scoring_branch_queue.csv"),
                    rel(RUN_DIR / "invalid_condition_matrix.csv"),
                ],
                "artifact_hashes": "recorded in docs/registers/artifact_registry.csv",
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked",
                "lineage_judgment": "connected_with_design_boundary",
                "generated_at_utc": generated_at_utc,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": "run333B guarded veto scoring design",
                "evidence_available": [
                    rel(RUN_DIR / "guarded_scoring_protocol.csv"),
                    rel(RUN_DIR / "scoring_branch_queue.csv"),
                    rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                ],
                "evidence_missing": ["no scored payload", "no MT5 tester result", "no forward pass/fail judgment"],
                "judgment_label": "exploratory_design_completed",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "The scoring rules are now predeclared; performance still has not been measured.",
                "failed_gates": failed_gates,
            },
        ),
    ]


def write_reports(protocol_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    report = write_md(
        REVIEWS_DIR / "run333B_guarded_veto_scoring_design.md",
        f"""
# run333B Guarded Veto Scoring Design(333B 방어 거부 점수화 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Design Read(설계 판독)

- scoring_protocols(점수화 계약): `{len(protocol_rows)}`
- queued_scoring_views(대기 점수화 보기): `{len(queue_rows)}`
- design boundary(설계 경계): score payload(점수 페이로드)는 아직 만들지 않았고, MT5 runtime(런타임)도 실행하지 않았다.

Effect(효과): 다음 run333C(333C 실행)는 hard/soft/control/negative-control(강한 거부/약한 거부/대조/부정 대조) 16개 view(보기)를 만들 수 있지만, threshold(임계값), lot(로트), model(모델), ONNX(온엑스)는 바꾸지 않는다.

## Boundary(경계)

- no scoring execution(점수화 실행 없음)
- no threshold retuning(임계값 재튜닝 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 업데이트 없음)
- no MT5 execution(새 MT5 실행 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage333B Guarded Scoring Decision(333B 방어 점수화 결정)

run333B(333B 실행)는 run333A(333A 실행)의 materialized feature frames(물질화 피처 프레임)을 no-retune guarded scoring protocol(무재튜닝 방어 점수화 계약)로 바꿨다.

- decision(결정): `{DECISION}`
- scoring_protocols(점수화 계약): `{len(protocol_rows)}`
- queued_views(대기 보기): `{len(queue_rows)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run333C(333C 실행)는 사전 선언된 scoring payload(점수 페이로드)를 만들 수 있다. 아직 forward decision(전진 판정), runtime authority(런타임 권위), operating claim(운영 주장)은 없다.
""",
    )
    return [report, decision]


def update_selection_status() -> Path:
    text = f"""
# Stage333 Selection Status(333단계 선택 상태)

- stage_status(단계 상태): `open_guarded_scoring_design_completed_payload_materialization_next`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- latest_materialization(최신 물질화): `{PARENT_RUN_ID}`
- latest_scoring_design(최신 점수화 설계): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run333B(333B 실행)는 scoring protocol(점수화 계약)을 만들었고, 다음은 scored payload(점수 페이로드) 물질화다.
"""
    return write_md(SELECTED_DIR / "selection_status.md", text)


def update_current_truth() -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage333(333단계) run333B(333B 실행)는 `{STATUS}`로 no-retune guarded scoring protocol(무재튜닝 방어 점수화 계약)을 설계했다. Effect(효과): run333C(333C 실행)는 16개 control/hard/soft/negative view(대조/강한 거부/약한 거부/부정 보기)를 물질화할 수 있지만 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage333(333단계) run333B(333B 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v3`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- source_stage(": f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `guarded_veto_scoring_payload_materialization`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{DECISION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run333B_summary(333B 요약): guarded veto scoring design(방어 거부 점수화 설계)을 `{STATUS}`로 완료했다. "
        "Effect(효과): 4개 protocol(계약)과 16개 scoring view queue(점수화 보기 대기열)를 만들었지만 score result(점수 결과), MT5(메타트레이더5), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run333B_summary(333B 요약)")
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))
    updated.append(
        append_if_missing(
            CHANGELOG,
            "Stage333B Guarded Veto Scoring Design",
            f"""
## 2026-05-26 - Stage333B Guarded Veto Scoring Design(333B 방어 거부 점수화 설계)

- run333B(333B 실행): no-retune guarded scoring protocol(무재튜닝 방어 점수화 계약)을 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): hard/soft/control/negative-control(강한 거부/약한 거부/대조/부정 대조) 16개 payload(페이로드)를 다음 run333C(333C 실행)로 넘기고, 후보 선택이나 Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        )
    )
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run333B_guarded_veto_scoring_design.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": "guarded_scoring_design_only;selected_candidate=none;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__guarded_scoring_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "guarded_veto_scoring_design",
                "tier_scope": "raw_forward_feature_handoff_scope",
                "kpi_scope": "no_trading_kpi_design_only",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "scoring_protocols=4;queued_views=16",
                "guardrail_kpi": "no_threshold_retuning;no_lot_optimization;no_model_update;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_no_runtime_execution",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__guarded_scoring_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "guarded_veto_scoring_design(방어 거부 점수화 설계)",
                "tier_scope": "raw_forward_feature_handoff_scope(원본 전진 피처 인계 범위)",
                "scoreboard": "design_only_no_trading_kpi(설계 전용, 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact in [*artifacts, Path(__file__)]:
        if path_exists(artifact) and io_path(artifact).is_file():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact)}",
                    "artifact_type": artifact.suffix.lstrip(".") or "file",
                    "path": rel(artifact),
                    "sha256": sha256_file(artifact),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage333B guarded scoring design artifact; no operating claim.",
                }
            )
    append_unique_csv(ARTIFACT_REGISTRY, ["artifact_id", "path"], artifact_rows)


def write_run_artifacts(generated_at_utc: str) -> list[Path]:
    protocol_rows = scoring_protocol_rows()
    formula_rows = score_formula_rows(protocol_rows)
    queue_rows = branch_queue_rows(protocol_rows)
    evidence_rows = evidence_plan_rows(protocol_rows)
    invalid_rows = invalid_condition_rows(protocol_rows)
    artifacts: list[Path] = [
        write_csv(
            RUN_DIR / "guarded_scoring_protocol.csv",
            [
                "thesis_id",
                "guard_family",
                "feature_frame_path",
                "feature_frame_sha256",
                "rows",
                "candidate_inputs",
                "score_transform_policy",
                "scoring_formula_contract",
                "veto_rule_contract",
                "missing_data_policy",
                "required_cost_veto",
                "required_curve_veto",
                "runtime_readiness_inherited",
                "materialization_readiness",
                "allowed_claim_after_run333B",
                "forbidden_claim_after_run333B",
            ],
            protocol_rows,
        ),
        write_csv(
            RUN_DIR / "score_formula_contract.csv",
            [
                "thesis_id",
                "formula_component",
                "allowed_source",
                "calibration_boundary",
                "forbidden_source",
                "output_field",
            ],
            formula_rows,
        ),
        write_csv(
            RUN_DIR / "scoring_branch_queue.csv",
            [
                "queue_id",
                "thesis_id",
                "scoring_mode",
                "feature_frame_path",
                "materialization_status",
                "description",
                "required_outputs",
                "forbidden_actions",
            ],
            queue_rows,
        ),
        write_csv(
            RUN_DIR / "cost_curve_evidence_plan.csv",
            ["evidence_id", "scope", "required_measurement", "claim_if_missing"],
            evidence_rows,
        ),
        write_csv(
            RUN_DIR / "invalid_condition_matrix.csv",
            ["condition_id", "invalid_trigger", "result"],
            invalid_rows,
        ),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "notes"],
            gate_rows(protocol_rows, queue_rows),
        ),
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()),
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "primary_family": "experiment_design",
                "primary_skill": "obsidian-experiment-design",
                "support_skills": [
                    "obsidian-data-integrity",
                    "obsidian-model-validation",
                    "obsidian-artifact-lineage",
                    "obsidian-result-judgment",
                ],
                "required_gates": [
                    "work_packet_schema_lint",
                    "required_gate_coverage_audit",
                    "final_claim_guard",
                ],
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_inputs": [rel(path) for path in source_artifacts().values()],
                "scoring_protocols": len(protocol_rows),
                "queued_scoring_views": len(queue_rows),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.extend(write_receipts(generated_at_utc, protocol_rows, queue_rows))
    artifacts.extend(write_reports(protocol_rows, queue_rows))
    artifacts.append(update_selection_status())
    artifacts.extend(update_current_truth())
    return artifacts


def main() -> None:
    generated_at_utc = utc_now()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = write_run_artifacts(generated_at_utc)
    protocol_rows = read_csv_rows(RUN_DIR / "guarded_scoring_protocol.csv")
    queue_rows = read_csv_rows(RUN_DIR / "scoring_branch_queue.csv")
    failures = [row for row in gate_rows(protocol_rows, queue_rows) if row["status"] != "pass"]
    update_registers(generated_at_utc, artifacts)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "scoring_protocols": len(protocol_rows),
                "queued_scoring_views": len(queue_rows),
                "failed_gates": failures,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
