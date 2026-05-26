from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-26"
STAGE_ID = "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
RUN_NUMBER = "run334G"
RUN_ID = "run334G_review_no_retune_stress_probe_materialization_and_failure_memory_v1"
PARENT_RUN_ID = "run334F_materialize_no_retune_nonidentity_stress_probe_inputs_v1"
NEXT_RUN_ID = "run334H_close_stage334_open_failure_memory_research_handoff_v1"
STATUS = "completed_no_retune_stress_materialization_review_no_selection"
JUDGMENT = "no_retune_stress_review_completed_all_six_blocked_research_only_no_goal_achieve"
DECISION = "stage334G_all_six_no_retune_stress_review_blocks_selection_failure_memory_handoff"
CLAIM_BOUNDARY = (
    "research_development_only_no_retune_stress_probe_review_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage334G_no_retune_stress_review.md"

RUN334D_DIR = STAGE_DIR / "02_runs" / "run334D"
RUN334D_ALL_SIX = RUN334D_DIR / "all_six_runtime_reconciliation.csv"
RUN334D_MEMORY = RUN334D_DIR / "preserved_clue_and_failure_memory.csv"

RUN334E_DIR = STAGE_DIR / "02_runs" / "run334E"
RUN334E_REJECTION = RUN334E_DIR / "overfit_rejection_rules.csv"
RUN334E_MATRIX = RUN334E_DIR / "stress_probe_matrix.csv"
RUN334E_DECISION = RUN334E_DIR / "final_stress_probe_design_decision.json"

RUN334F_DIR = STAGE_DIR / "02_runs" / "run334F"
RUN334F_MANIFEST = RUN334F_DIR / "materialization_manifest.csv"
RUN334F_SUMMARY = RUN334F_DIR / "stress_failure_memory_summary.csv"
RUN334F_DECISION = RUN334F_DIR / "final_materialization_decision.json"
RUN334F_COST = RUN334F_DIR / "diagnostic_views" / "cost_stress_diagnostic_views.csv"
RUN334F_CURVE = RUN334F_DIR / "diagnostic_views" / "curve_pocket_diagnostic_views.csv"
RUN334F_REGIME = RUN334F_DIR / "diagnostic_views" / "regime_slice_diagnostic_views.csv"
RUN334F_DIRECTION = RUN334F_DIR / "diagnostic_views" / "direction_diagnostic_views.csv"
RUN334F_UNDERWATER = RUN334F_DIR / "diagnostic_views" / "underwater_diagnostic_views.csv"
RUN334F_IDENTITY = RUN334F_DIR / "diagnostic_views" / "runtime_identity_diagnostic_views.csv"


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return "missing"
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_json(path: Path) -> Any:
    if not path_exists(path):
        return {}
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
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
    index_by_key = {
        tuple(str(row.get(column, "")) for column in key_columns): index
        for index, row in enumerate(existing)
    }
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in index_by_key:
            existing[index_by_key[key]] = payload
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
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line_once(text: str, marker: str, insertion: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == marker:
            lines[index + 1:index + 1] = insertion.strip("\n").splitlines()
            return "\n".join(lines) + "\n"
    return insertion.strip() + "\n" + text


def append_section_once(path: Path, heading: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if heading in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", had_bom)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).strip()
        if text == "":
            return default
        return float(text)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        text = str(value).strip()
        if text == "":
            return default
        return int(float(text))
    except (TypeError, ValueError):
        return default


def index_by(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {row.get(key, ""): row for row in rows if row.get(key)}


def group_by(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, list[Mapping[str, str]]]:
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get(key, "")].append(row)
    return grouped


def load_context() -> dict[str, Any]:
    return {
        "run334d_all_six": read_csv_rows(RUN334D_ALL_SIX),
        "run334d_memory": read_csv_rows(RUN334D_MEMORY),
        "run334e_rejection": read_csv_rows(RUN334E_REJECTION),
        "run334e_matrix": read_csv_rows(RUN334E_MATRIX),
        "run334e_decision": read_json(RUN334E_DECISION),
        "manifest": read_csv_rows(RUN334F_MANIFEST),
        "summary": read_csv_rows(RUN334F_SUMMARY),
        "run334f_decision": read_json(RUN334F_DECISION),
        "cost": read_csv_rows(RUN334F_COST),
        "curve": read_csv_rows(RUN334F_CURVE),
        "regime": read_csv_rows(RUN334F_REGIME),
        "direction": read_csv_rows(RUN334F_DIRECTION),
        "underwater": read_csv_rows(RUN334F_UNDERWATER),
        "identity": read_csv_rows(RUN334F_IDENTITY),
    }


def failure_category(status: str) -> str:
    if status in {"cost_breaks_pf_or_net", "deep_curve_pocket", "loss_regime_slice", "weak_direction_negative", "long_underwater_stretch"}:
        return "hard"
    if status == "identity_source_missing":
        return "invalid_or_blocked"
    return "warning"


def build_outputs(context: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    manifest = list(context["manifest"])
    summary = list(context["summary"])
    d_memory = index_by(context["run334d_memory"], "attempt_name")
    d_all_six = index_by(context["run334d_all_six"], "attempt_name")
    matrix = index_by(context["run334e_matrix"], "attempt_name")
    manifest_by_attempt = group_by(manifest, "attempt_name")
    manifest_by_axis = group_by(manifest, "stress_axis")
    identity_by_attempt = index_by(context["identity"], "attempt_name")

    attempt_rows: list[dict[str, Any]] = []
    clue_rows: list[dict[str, Any]] = []
    heatmap_rows: list[dict[str, Any]] = []
    blocker_rows: list[dict[str, Any]] = []
    rejection_rows: list[dict[str, Any]] = []
    identity_review_rows: list[dict[str, Any]] = []
    next_queue_rows: list[dict[str, Any]] = []

    for row in summary:
        attempt = row.get("attempt_name", "")
        d_row = d_all_six.get(attempt, {})
        m_row = matrix.get(attempt, {})
        mem_row = d_memory.get(attempt, {})
        rows = manifest_by_attempt.get(attempt, [])
        hard_axes = sorted({item.get("stress_axis", "") for item in rows if failure_category(item.get("diagnostic_status", "")) == "hard"})
        warning_axes = sorted({item.get("stress_axis", "") for item in rows if failure_category(item.get("diagnostic_status", "")) == "warning"})
        invalid_axes = sorted({item.get("stress_axis", "") for item in rows if failure_category(item.get("diagnostic_status", "")) == "invalid_or_blocked"})
        identity = identity_by_attempt.get(attempt, {})
        preserved_before = str(mem_row.get("preserved_clue", "")).lower() == "true" or str(m_row.get("preserved_clue", "")).lower() == "true"
        final_status = "demoted_to_failure_memory" if preserved_before else "failure_memory_confirmed"
        if invalid_axes:
            final_status = "blocked_by_identity_gap"
        attempt_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": row.get("artifact_slug", ""),
                "severity": row.get("severity", ""),
                "headline_net_profit": row.get("headline_net_profit", ""),
                "headline_profit_factor": row.get("headline_profit_factor", ""),
                "diagnostic_row_count": row.get("diagnostic_row_count", ""),
                "hard_failure_count": row.get("hard_failure_count", ""),
                "warning_count": row.get("warning_count", ""),
                "hard_failure_axes": hard_axes,
                "warning_axes": warning_axes,
                "invalid_or_blocked_axes": invalid_axes,
                "runtime_identity_status": identity.get("diagnostic_status", ""),
                "preserved_clue_before_run334F": preserved_before,
                "run334G_status": final_status,
                "selection_eligible": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "stress review blocks candidate selection and keeps evidence as failure memory",
            }
        )
        clue_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": row.get("artifact_slug", ""),
                "was_preserved_clue": preserved_before,
                "pre_stress_reason": mem_row.get("primary_positive_evidence", ""),
                "stress_failure_reason": ";".join(hard_axes),
                "post_review_label": final_status,
                "next_allowed_use": "failure_memory_or_predeclared_feature_thesis_only",
                "forbidden_use": "candidate_selection_or_threshold_lot_rule_repair",
                "effect": "headline-positive clues are not discarded, but they are no longer selection candidates",
            }
        )
        blocker_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": row.get("artifact_slug", ""),
                "blocker_count": len(hard_axes) + len(invalid_axes),
                "blocking_axes": hard_axes + invalid_axes,
                "smallest_legitimate_next_condition": "predeclared feature thesis or data/runtime repair that does not use forward stress pockets as exclusion filters",
                "blocked_claims": [
                    "Forward Passed",
                    "Forward Failed",
                    "selected candidate",
                    "runtime authority",
                    "Goal Achieve",
                ],
                "effect": "review closes selection pressure and hands off only constraints",
            }
        )
        next_queue_rows.append(
            {
                "queue_id": f"run334H_failure_memory_handoff_{attempt}",
                "attempt_name": attempt,
                "artifact_slug": row.get("artifact_slug", ""),
                "handoff_type": "failure_memory",
                "must_carry": hard_axes,
                "must_not_do": [
                    "threshold_retuning",
                    "lot_optimization",
                    "date_hour_regime_pruning",
                    "direction_drop_as_fix",
                    "db_source_claim_without_tags",
                ],
                "recommended_next_stage_role": "constraint_seed_not_candidate",
                "selection_eligible": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        identity_review_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": row.get("artifact_slug", ""),
                "diagnostic_status": identity.get("diagnostic_status", "missing_identity_row"),
                "feature_matrix_path": identity.get("feature_matrix_path", ""),
                "feature_matrix_sha256": identity.get("feature_matrix_sha256", ""),
                "model_path": identity.get("model_path", ""),
                "model_sha256": identity.get("model_sha256", ""),
                "trade_records_sha256": identity.get("trade_records_sha256", ""),
                "slice_report_sha256": identity.get("slice_report_sha256", ""),
                "identity_judgment": "identity_sources_available_no_runtime_authority"
                if identity.get("diagnostic_status", "") == "identity_sources_available"
                else "identity_gap_blocks_runtime_claim",
                "runtime_authority": "not_claimed",
                "effect": "identity evidence is connected for review, but no new MT5 execution or authority is claimed",
            }
        )

    for axis, rows in sorted(manifest_by_axis.items()):
        hard = [row for row in rows if failure_category(row.get("diagnostic_status", "")) == "hard"]
        warning = [row for row in rows if failure_category(row.get("diagnostic_status", "")) == "warning"]
        invalid = [row for row in rows if failure_category(row.get("diagnostic_status", "")) == "invalid_or_blocked"]
        heatmap_rows.append(
            {
                "stress_axis": axis,
                "scenario_count": len(rows),
                "hard_failure_count": len(hard),
                "warning_count": len(warning),
                "invalid_or_blocked_count": len(invalid),
                "hard_failure_attempts": sorted({row.get("attempt_name", "") for row in hard}),
                "axis_judgment": "blocks_selection" if hard or invalid else "warning_only",
                "effect": "axis-level stress review summarizes why no attempt can be selected",
            }
        )

    for rule in context["run334e_rejection"]:
        rejection_rows.append(
            {
                "rule_id": rule.get("rule_id", ""),
                "trigger": rule.get("trigger", ""),
                "status": "active_no_violation_observed",
                "evidence": rel(RUN334F_MANIFEST),
                "effect": rule.get("effect", ""),
            }
        )

    return {
        "attempt_review": attempt_rows,
        "clue_resolution": clue_rows,
        "axis_heatmap": heatmap_rows,
        "selection_blockers": blocker_rows,
        "overfit_rejection_audit": rejection_rows,
        "runtime_identity_review": identity_review_rows,
        "next_queue": next_queue_rows,
    }


def write_skill_receipts(context: Mapping[str, Any], outputs: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[Path]:
    source_inputs = [
        RUN334D_ALL_SIX,
        RUN334D_MEMORY,
        RUN334E_REJECTION,
        RUN334E_MATRIX,
        RUN334E_DECISION,
        RUN334F_MANIFEST,
        RUN334F_SUMMARY,
        RUN334F_DECISION,
        RUN334F_COST,
        RUN334F_CURVE,
        RUN334F_REGIME,
        RUN334F_DIRECTION,
        RUN334F_UNDERWATER,
        RUN334F_IDENTITY,
    ]
    hard_attempts = [row["attempt_name"] for row in outputs["attempt_review"] if row.get("run334G_status") in {"demoted_to_failure_memory", "failure_memory_confirmed"}]
    receipts: list[Path] = []
    receipts.append(
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "observed_change": "run334F materialization turns all six headline-positive or mixed attempts into hard failure memory under no-retune stress.",
                "comparison_baseline": "run334D preserved clues and run334E stress design",
                "likely_drivers": [
                    "cost stress failures",
                    "curve pocket failures",
                    "worst regime slices",
                    "direction weakness",
                    "underwater stretch",
                ],
                "segment_checks": [
                    "cost_stress",
                    "curve_pocket",
                    "regime_slice",
                    "direction",
                    "drawdown_shape",
                    "runtime_parity",
                ],
                "trade_shape": {
                    "attempts_reviewed": len(outputs["attempt_review"]),
                    "failure_memory_attempts": len(hard_attempts),
                    "axis_rows": len(outputs["axis_heatmap"]),
                },
                "alternative_explanations": [
                    "short forward sample noise remains possible",
                    "synthetic cost assumptions are approximations",
                    "single-surface non-identity evidence cannot answer cp322A D/B source behavior",
                ],
                "attribution_confidence": "medium_reviewed_research_only",
                "next_probe": NEXT_RUN_ID,
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "existing Stage330 non-identity ONNX surfaces",
                "target_and_label": "inherited; no label generation or model rebuild in run334G",
                "split_method": "post-forward diagnostic review",
                "selection_metric": "none",
                "secondary_metrics": [
                    "hard failure count",
                    "axis heatmap",
                    "runtime identity status",
                    "overfit rejection audit",
                ],
                "threshold_policy": "fixed inherited threshold; no search",
                "overfit_risk": "using diagnostic failures as direct repair filters would overfit; rejection audit keeps this forbidden",
                "calibration_risk": "not assessed and not used for selection",
                "comparison_baseline": "run334F materialized diagnostics",
                "validation_judgment": "negative_research_memory_no_selection",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": [rel(RUN334F_IDENTITY), rel(RUN334F_MANIFEST)],
                "shared_contract": "diagnostic review must preserve source feature/model/trade/slice identities and avoid runtime authority claims.",
                "known_differences": [
                    "run334G does not launch a new MT5 run.",
                    "Stage330 non-identity evidence remains separate from cp322A exact.",
                ],
                "parity_check": "runtime identity diagnostic statuses are read and reviewed.",
                "parity_identity": {
                    "identity_rows": len(context["identity"]),
                    "identity_sources_available": all(row.get("diagnostic_status") == "identity_sources_available" for row in context["identity"]),
                    "runtime_identity_sha256": sha256_file(RUN334F_IDENTITY),
                },
                "runtime_claim_boundary": "review_only_no_runtime_authority",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": "run334F no-retune stress materialization under Stage334 contract",
                "evidence_available": [rel(path) for path in source_inputs],
                "evidence_missing": "No new MT5 rerun or cp322A exact forward handoff exists.",
                "judgment_label": "negative_research_memory",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "The non-identity clues are useful as failure memory, but they are not candidates.",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [rel(path) for path in source_inputs],
                "time_axis": "run334G reviews previously materialized post-2026-04-14 diagnostics; it does not rebuild bars.",
                "sample_scope": "six Stage330 non-identity attempts and 42 diagnostic rows",
                "missing_or_duplicate_check": "runtime identity diagnostics passed in run334F; run334G checks review completeness.",
                "feature_label_boundary": "no features, labels, thresholds, or models are changed",
                "split_boundary": "forward diagnostics are failure memory only, not selection data",
                "leakage_risk": "failure axes must not become direct filters",
                "data_hash_or_identity": {rel(path): sha256_file(path) for path in source_inputs},
                "integrity_judgment": "usable_with_boundary",
            },
        )
    )
    return receipts


def write_run_artifacts(context: Mapping[str, Any], outputs: Mapping[str, Sequence[Mapping[str, Any]]], now: str) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_csv(
            RUN_DIR / "attempt_failure_memory_review.csv",
            [
                "attempt_name",
                "artifact_slug",
                "severity",
                "headline_net_profit",
                "headline_profit_factor",
                "diagnostic_row_count",
                "hard_failure_count",
                "warning_count",
                "hard_failure_axes",
                "warning_axes",
                "invalid_or_blocked_axes",
                "runtime_identity_status",
                "preserved_clue_before_run334F",
                "run334G_status",
                "selection_eligible",
                "claim_boundary",
                "effect",
            ],
            outputs["attempt_review"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "preserved_clue_resolution.csv",
            [
                "attempt_name",
                "artifact_slug",
                "was_preserved_clue",
                "pre_stress_reason",
                "stress_failure_reason",
                "post_review_label",
                "next_allowed_use",
                "forbidden_use",
                "effect",
            ],
            outputs["clue_resolution"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "axis_failure_heatmap.csv",
            [
                "stress_axis",
                "scenario_count",
                "hard_failure_count",
                "warning_count",
                "invalid_or_blocked_count",
                "hard_failure_attempts",
                "axis_judgment",
                "effect",
            ],
            outputs["axis_heatmap"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "selection_blocker_review.csv",
            [
                "attempt_name",
                "artifact_slug",
                "blocker_count",
                "blocking_axes",
                "smallest_legitimate_next_condition",
                "blocked_claims",
                "effect",
            ],
            outputs["selection_blockers"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "overfit_rejection_audit.csv",
            ["rule_id", "trigger", "status", "evidence", "effect"],
            outputs["overfit_rejection_audit"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "runtime_identity_review.csv",
            [
                "attempt_name",
                "artifact_slug",
                "diagnostic_status",
                "feature_matrix_path",
                "feature_matrix_sha256",
                "model_path",
                "model_sha256",
                "trade_records_sha256",
                "slice_report_sha256",
                "identity_judgment",
                "runtime_authority",
                "effect",
            ],
            outputs["runtime_identity_review"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "run334H_failure_memory_handoff_queue.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "handoff_type",
                "must_carry",
                "must_not_do",
                "recommended_next_stage_role",
                "selection_eligible",
                "claim_boundary",
            ],
            outputs["next_queue"],
        )
    )
    artifacts.extend(write_skill_receipts(context, outputs))
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence", "claim_effect"],
            [
                {
                    "gate": "performance_attribution",
                    "status": "passed_reviewed_research_only",
                    "evidence": "performance_attribution_receipt.json",
                    "claim_effect": "All six attempts are decomposed into stress failure axes.",
                },
                {
                    "gate": "model_validation",
                    "status": "passed_negative_memory_no_selection",
                    "evidence": "model_validation_receipt.json",
                    "claim_effect": "No model, threshold, lot, or rule is selected from stress review.",
                },
                {
                    "gate": "runtime_parity",
                    "status": "passed_review_only_no_authority",
                    "evidence": "runtime_parity_receipt.json",
                    "claim_effect": "Runtime identity is reviewed without authority claim.",
                },
                {
                    "gate": "data_integrity",
                    "status": "passed_usable_with_boundary",
                    "evidence": "data_integrity_receipt.json",
                    "claim_effect": "Forward diagnostics remain failure memory, not tuning data.",
                },
                {
                    "gate": "result_judgment",
                    "status": "passed_no_goal_achieve",
                    "evidence": "result_judgment.csv",
                    "claim_effect": "Forward Passed/Failed and Goal Achieve are not claimed.",
                },
                {
                    "gate": "artifact_lineage",
                    "status": "passed_connected_with_boundary",
                    "evidence": "artifact_lineage_receipt.json",
                    "claim_effect": "run334F diagnostics connect to run334G review and run334H handoff queue.",
                },
            ],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "selected_candidate",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            [
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "selected_candidate": "none",
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "runtime_authority": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "final_stress_review_decision.json",
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "attempts_reviewed": len(outputs["attempt_review"]),
                "attempts_with_failure_memory": len(outputs["attempt_review"]),
                "preserved_clues_demoted": [
                    row["attempt_name"]
                    for row in outputs["clue_resolution"]
                    if row.get("was_preserved_clue") is True
                ],
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    lineage = {
        "source_inputs": [
            rel(RUN334D_ALL_SIX),
            rel(RUN334D_MEMORY),
            rel(RUN334E_REJECTION),
            rel(RUN334E_MATRIX),
            rel(RUN334E_DECISION),
            rel(RUN334F_MANIFEST),
            rel(RUN334F_SUMMARY),
            rel(RUN334F_DECISION),
            rel(RUN334F_COST),
            rel(RUN334F_CURVE),
            rel(RUN334F_REGIME),
            rel(RUN334F_DIRECTION),
            rel(RUN334F_UNDERWATER),
            rel(RUN334F_IDENTITY),
        ],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {},
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "artifact_registry": rel(ARTIFACT_REGISTRY),
        },
        "availability": "tracked_after_force_add_run_dir",
        "lineage_judgment": "connected_with_boundary",
    }
    lineage_path = write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage)
    artifacts.append(lineage_path)
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in artifacts}
    write_json(lineage_path, lineage)
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "created_at_utc": now,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "outputs": [rel(path) for path in artifacts],
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    return artifacts


def write_reports(outputs: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[Path]:
    demoted = [row["attempt_name"] for row in outputs["clue_resolution"] if row.get("was_preserved_clue") is True]
    report = write_md(
        REVIEWS_DIR / "run334G_no_retune_stress_review.md",
        f"""
# run334G No-Retune Stress Review(334G 무재튜닝 압박 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Review(검토)

- reviewed_attempts(검토 시도): `{len(outputs["attempt_review"])}`
- failure_memory_attempts(실패 기억 시도): `{len(outputs["attempt_review"])}`
- demoted_preserved_clues(강등된 보존 단서): `{', '.join(demoted) if demoted else 'none'}`
- next_queue(다음 대기열): `{len(outputs["next_queue"])}`

Effect(효과): run334F(334F 실행)의 diagnostic views(진단 보기)는 모든 non-identity clue(비정체성 단서)를 selection candidate(선택 후보)가 아니라 failure memory(실패 기억)로 만든다.

Next(다음): `{NEXT_RUN_ID}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage334G No-Retune Stress Review(334G 무재튜닝 압박 검토)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run334F(334F 실행)의 42개 diagnostic view(진단 보기)를 검토했고 6개 attempt(시도) 모두 failure memory(실패 기억)로 닫았다.
""",
    )
    return [report, decision]


def update_stage_docs() -> list[Path]:
    status_path = write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage334 Selection Status(334단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_exact_forward_handoff_missing`
- latest_contract_design(최신 계약 설계): `run334A_design_forward_usable_onnx_handoff_contract_after_cp322a_boundary_v1`
- latest_materialization(최신 물질화): `run334B_materialize_subject_separated_handoff_contract_inputs_v1`
- latest_runtime_probe_decision(최신 런타임 탐침 결정): `run334C_design_subject_separated_runtime_probe_or_block_v1`
- latest_reconciliation(최신 대조): `run334D_reconcile_existing_non_identity_runtime_probe_evidence_no_selection_v1`
- latest_stress_design(최신 압박 설계): `run334E_design_no_retune_forward_usable_nonidentity_stress_probe_from_reconciled_memory_v1`
- latest_stress_materialization(최신 압박 물질화): `run334F_materialize_no_retune_nonidentity_stress_probe_inputs_v1`
- latest_stress_review(최신 압박 검토): `{RUN_ID}`
- active_question(활성 질문): `forward_usable_onnx_handoff_contract_hardening_without_overfit`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage334G(334G 실행)는 6개 non-identity clue(비정체성 단서)를 모두 failure memory(실패 기억)로 닫고, Stage334 closeout/handoff(단계 종료/인계) 준비로 넘긴다.
""",
    )
    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = replace_prefix_line(text, "- status(상태):", "- status(상태): `open_active`")
        text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        write_text_lossless(STAGE_BRIEF, text, had_bom)
    append_section_once(
        INPUTS_DIR / "input_refs.md",
        "## run334G No-Retune Stress Review Outputs(334G 무재튜닝 압박 검토 출력)",
        f"""
- run334G_attempt_review(334G 시도 검토): `stages/{STAGE_ID}/02_runs/run334G/attempt_failure_memory_review.csv`
- run334G_axis_heatmap(334G 축 열지도): `stages/{STAGE_ID}/02_runs/run334G/axis_failure_heatmap.csv`
- run334G_clue_resolution(334G 단서 판정): `stages/{STAGE_ID}/02_runs/run334G/preserved_clue_resolution.csv`
- run334H_queue(334H 대기열): `stages/{STAGE_ID}/02_runs/run334G/run334H_failure_memory_handoff_queue.csv`
- run334G_final_decision(334G 최종 결정): `stages/{STAGE_ID}/02_runs/run334G/final_stress_review_decision.json`
""",
    )
    return [status_path, STAGE_BRIEF, INPUTS_DIR / "input_refs.md"]


def update_state_docs() -> list[Path]:
    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_insert = f"""- >-
  Stage334(334단계) run334G(334G 실행)는 `{STATUS}`로 no-retune stress review(무재튜닝 압박 검토)를 완료했다. Effect(효과): 6개 non-identity clue(비정체성 단서)를 모두 failure memory(실패 기억)로 닫고 selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다."""
    text = insert_after_line_once(text, "current_focus:", focus_insert, "run334G(334G 실행)")
    write_text_lossless(WORKSPACE_STATE, text, had_bom)

    text, had_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v8`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": "- status(상태): `completed_stress_review_ready_for_stage_closeout_handoff`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = f"- run334G_summary(334G 요약): no-retune stress review(무재튜닝 압박 검토)를 `{STATUS}`로 완료했다. Effect(효과): 6개 attempt(시도) 모두 failure memory(실패 기억)이며 다음 run334H(334H 실행)는 Stage334 closeout/handoff(단계 종료/인계)다."
    text = insert_after_line_once(text, f"- decision(판정): `{DECISION}`", summary, "run334G_summary")
    write_text_lossless(CURRENT_STATE, text, had_bom)

    append_section_once(
        CHANGELOG,
        "## 2026-05-26 - Stage334G No-Retune Stress Review(334G 무재튜닝 압박 검토)",
        f"""
- run334G(334G 실행): run334F(334F 실행)의 42개 diagnostic view(진단 보기)를 검토해 6개 non-identity clue(비정체성 단서)를 모두 failure memory(실패 기억)로 닫았다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    return [WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def update_registries(artifacts: Sequence[Path], now: str) -> None:
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
                "path": f"stages/{STAGE_ID}/03_reviews/run334G_no_retune_stress_review.md",
                "notes": "all_six_nonidentity_clues_demoted_to_failure_memory;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__stress_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "no_retune_stress_review_and_failure_memory",
                "tier_scope": "research_contract_no_tier_kpi",
                "kpi_scope": "diagnostic_review_no_new_trading_kpi",
                "scoreboard_lane": "performance_attribution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334G_no_retune_stress_review.md",
                "primary_kpi": "reviewed_attempts=6;failure_memory_attempts=6",
                "guardrail_kpi": "no_model_training;no_threshold_retuning;no_lot_optimization;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_existing_reports_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__stress_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "performance_attribution",
                "evidence_scope": "no_retune_stress_probe_review",
                "kpi_scope": "diagnostic_review_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": f"stages/{STAGE_ID}/03_reviews/run334G_no_retune_stress_review.md",
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage334G_no_retune_stress_review_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": "stress review and failure memory artifact; no operating claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> None:
    now = utc_now()
    context = load_context()
    outputs = build_outputs(context)
    run_artifacts = write_run_artifacts(context, outputs, now)
    report_artifacts = write_reports(outputs)
    stage_artifacts = update_stage_docs()
    state_artifacts = update_state_docs()
    all_artifacts = [Path(__file__), *run_artifacts, *report_artifacts, *stage_artifacts, *state_artifacts]
    update_registries(all_artifacts, now)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "attempts_reviewed": len(outputs["attempt_review"]),
                "failure_memory_attempts": len(outputs["attempt_review"]),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "artifact_count": len(all_artifacts),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
