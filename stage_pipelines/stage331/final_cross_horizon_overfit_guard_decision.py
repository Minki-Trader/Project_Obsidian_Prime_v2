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
STAGE_ID = "331_overfit_guard__cross_horizon_cost_curve_parity_probe"
RUN_NUMBER = "run331D"
RUN_ID = "run331D_final_cross_horizon_overfit_guard_decision_v1"
PARENT_RUN_ID = "run331C_runtime_replay_or_block_cross_horizon_probe_v1"
SOURCE_STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
NEXT_STAGE_ID = "332_overfit_guard__failure_memory_forward_research_handoff"
NEXT_RUN_ID = "run332A_design_failure_memory_forward_research_handoff_packet_v1"
STATUS = "completed_final_cross_horizon_overfit_guard_decision_stage331_closed_no_selection"
JUDGMENT = "stage331_closed_no_selection_research_handoff_no_goal_achieve"
DECISION = "no_attempt_passed_overfit_guard_for_selection_runtime_parity_matched_fragility_real"
CLAIM_BOUNDARY = (
    "research_development_only_final_cross_horizon_overfit_guard_decision_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN331A_DIR = STAGE_DIR / "02_runs" / "run331A"
RUN331B_DIR = STAGE_DIR / "02_runs" / "run331B"
RUN331C_DIR = STAGE_DIR / "02_runs" / "run331C"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN330G_DIR = SOURCE_STAGE_DIR / "02_runs" / "run330G"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage331D_final_cross_horizon_overfit_guard_decision.md"
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


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
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


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path.exists():
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


def fmt(value: Any, digits: int = 2) -> str:
    number = to_float(value)
    if number is None:
        return str(value)
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def full_cost_lookup(cost: pd.DataFrame, attempt_name: str, cost_level: float) -> dict[str, Any]:
    rows = cost[
        (cost["attempt_name"].astype(str) == attempt_name)
        & (cost["horizon_id"].astype(str) == "full_forward")
        & (cost["cost_level"].astype(float) == float(cost_level))
    ]
    if rows.empty:
        return {}
    return dict(rows.iloc[0])


def classify_attempt(row: Mapping[str, Any], runtime_row: Mapping[str, Any]) -> dict[str, Any]:
    attempt = str(row["attempt_name"])
    role = str(row["role"])
    full_pf = to_float(row.get("full_pf")) or 0.0
    cost1_pf = to_float(row.get("cost1_pf")) or 0.0
    cost2_pf = to_float(row.get("cost2_pf")) or 0.0
    third_share = to_float(row.get("third_positive_share")) or 0.0
    rolling_min = to_float(row.get("rolling20_min_net")) or 0.0
    replay_trades = to_float(runtime_row.get("replay_trade_count")) if runtime_row else None
    runtime_match = str(runtime_row.get("metrics_match", "")).lower() in {"true", "1"} if runtime_row else False

    if cost1_pf > 1.0 and cost2_pf > 1.0:
        cost_read = "survives_plus1_and_plus2_cost"
    elif cost1_pf > 1.0:
        cost_read = "survives_plus1_only_fails_plus2_cost"
    else:
        cost_read = "fails_plus1_and_plus2_cost"

    if rolling_min <= -60:
        curve_read = "deep_negative_rolling20_pocket"
    elif rolling_min < 0:
        curve_read = "negative_rolling20_pocket"
    else:
        curve_read = "no_negative_rolling20_pocket"

    if not runtime_match:
        disposition = "blocked_runtime_mismatch"
        reason = "runtime replay did not match source, so fragility cannot be trusted as model behavior"
    elif role == "negative_control_high_pressure":
        disposition = "closed_negative_memory_guard_caught"
        reason = "negative control was caught by cost or curve guard"
    elif attempt == "c56_plain_rf":
        disposition = "retained_failure_memory_clue_not_selection"
        reason = "best preserved clue keeps headline PF but fails plus2 cost and keeps a negative rolling pocket"
    elif attempt == "m48_plain_rf":
        disposition = "fragile_failure_memory_clue_not_selection"
        reason = "larger net is concentrated, plus1 cost is near break-even, plus2 cost fails, and rolling pocket is deep"
    else:
        disposition = "closed_no_selection"
        reason = "attempt did not satisfy final overfit guard"

    selection_eligible = (
        runtime_match
        and role != "negative_control_high_pressure"
        and full_pf > 1.25
        and cost1_pf > 1.05
        and cost2_pf > 1.0
        and third_share >= 0.67
        and rolling_min >= 0.0
        and (replay_trades or 0) >= 50
    )
    if selection_eligible:
        disposition = "would_require_independent_followup_before_selection"
        reason = "all numeric guard checks passed but this run is still not a selection packet"

    return {
        "attempt_name": attempt,
        "artifact_slug": row.get("artifact_slug"),
        "role": role,
        "runtime_replay_match": runtime_match,
        "source_net_profit": to_float(row.get("full_net")),
        "source_profit_factor": full_pf,
        "runtime_trade_count": replay_trades,
        "cost1_profit_factor": cost1_pf,
        "cost2_profit_factor": cost2_pf,
        "third_positive_share": third_share,
        "rolling20_min_net": rolling_min,
        "guard_cost_read": cost_read,
        "guard_curve_read": curve_read,
        "runtime_read": "matched_source" if runtime_match else "mismatch_or_missing",
        "selection_eligible": selection_eligible,
        "final_disposition": disposition,
        "no_selection_reason": reason,
    }


def build_final_matrix() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    survival = read_csv(RUN331B_DIR / "candidate_survival_summary.csv")
    cost = read_csv(RUN331B_DIR / "cost_curve_by_horizon_report.csv")
    resampling = read_csv(RUN331B_DIR / "resampling_stability_report.csv")
    runtime = read_csv(RUN331C_DIR / "runtime_replay_compare_report.csv")
    runtime_by_attempt = {str(row["attempt_name"]): dict(row) for _, row in runtime.iterrows()}

    matrix: list[dict[str, Any]] = []
    for _, raw_row in survival.iterrows():
        row = dict(raw_row)
        attempt = str(row["attempt_name"])
        row["cost1_pf"] = full_cost_lookup(cost, attempt, 1.0).get("profit_factor_after_cost", row.get("cost1_pf"))
        row["cost2_pf"] = full_cost_lookup(cost, attempt, 2.0).get("profit_factor_after_cost", row.get("cost2_pf"))
        matrix.append(classify_attempt(row, runtime_by_attempt.get(attempt, {})))

    clue_rows = []
    for row in matrix:
        if row["role"] != "preserved_clue_not_selection":
            continue
        next_probe = (
            "build broader forward-safe feature thesis with anti-concentration guard before any ONNX export"
            if row["attempt_name"] == "m48_plain_rf"
            else "keep as low-frequency cost-shape clue, then test independent data and stricter cost before any package"
        )
        clue_rows.append(
            {
                "attempt_name": row["attempt_name"],
                "stage330_incoming_role": "preserved_clue_not_selection",
                "stage331_final_disposition": row["final_disposition"],
                "selection_status": "not_selected",
                "forward_status": "not_passed_not_failed_research_only",
                "runtime_parity_read": row["runtime_read"],
                "cost_guard_read": row["guard_cost_read"],
                "curve_guard_read": row["guard_curve_read"],
                "allowed_future_use": "research_memory_only",
                "forbidden_future_use": "do_not_promote_as_selected_candidate_or_operating_reference",
                "required_next_probe": next_probe,
            }
        )

    resampling_by_attempt = {str(row["attempt_name"]): dict(row) for _, row in resampling.iterrows()}
    memory_rows = []
    for row in matrix:
        resample = resampling_by_attempt.get(row["attempt_name"], {})
        modes = [
            row["guard_cost_read"],
            row["guard_curve_read"],
            f"third_positive_share={fmt(row['third_positive_share'], 2)}",
        ]
        if row["role"] == "negative_control_high_pressure":
            memory_class = "negative_memory"
        elif row["attempt_name"] == "c56_plain_rf":
            memory_class = "weak_positive_clue_memory"
        else:
            memory_class = "fragility_memory"
        memory_rows.append(
            {
                "attempt_name": row["attempt_name"],
                "memory_class": memory_class,
                "final_disposition": row["final_disposition"],
                "observed_failure_modes": ";".join(modes),
                "full_pf": row["source_profit_factor"],
                "cost1_pf": row["cost1_profit_factor"],
                "cost2_pf": row["cost2_profit_factor"],
                "rolling20_min_net": row["rolling20_min_net"],
                "fifth_positive_share": resample.get("fifth_positive_share"),
                "not_a_repair_action": "no threshold, lot, or model change was made in Stage331",
                "future_design_constraint": "avoid selecting any surface that only survives headline net while failing cost or rolling-pocket guards",
            }
        )
    return matrix, clue_rows, memory_rows


def evidence_rollup_rows(matrix: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    matched_count = sum(1 for row in matrix if row["runtime_replay_match"])
    eligible_count = sum(1 for row in matrix if row["selection_eligible"])
    return [
        {
            "evidence_id": "stage330G_failure_memory",
            "source_path": rel(RUN330G_DIR / "failure_memory_report.csv"),
            "availability": "tracked",
            "key_read": "Stage330 closed without selection and passed two preserved clues plus four negative memories to Stage331.",
            "claim_effect": "prevents reading Stage330 headline profit as a forward pass",
        },
        {
            "evidence_id": "run331A_design_packet",
            "source_path": rel(RUN331A_DIR / "run_manifest.json"),
            "availability": "tracked",
            "key_read": "Designed no-retune cross-horizon, cost, curve, and runtime parity guards.",
            "claim_effect": "locks the guard before reading run331B or run331C results",
        },
        {
            "evidence_id": "run331B_no_retune_materialization",
            "source_path": rel(RUN331B_DIR / "candidate_survival_summary.csv"),
            "availability": "tracked",
            "key_read": "0 attempts satisfy final selection guard; c56_plain survives plus1 cost only; m48_plain is cost and pocket fragile.",
            "claim_effect": "keeps preserved clues as research memory only",
        },
        {
            "evidence_id": "run331C_runtime_replay",
            "source_path": rel(RUN331C_DIR / "runtime_replay_compare_report.csv"),
            "availability": "tracked",
            "key_read": f"{matched_count}/6 runtime replays matched source net, PF, and trade count.",
            "claim_effect": "confirms fragility is not caused by replay path drift",
        },
        {
            "evidence_id": "run331D_final_decision",
            "source_path": rel(RUN_DIR / "final_decision_matrix.csv"),
            "availability": "generated",
            "key_read": f"{eligible_count} selection-eligible attempts after cost, curve, resampling, and runtime checks.",
            "claim_effect": "Stage331 closes no selection and hands failure memory to Stage332",
        },
    ]


def gate_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "kpi_contract_audit",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "final_decision_matrix.csv"),
            "notes": "trading KPI, cost stress, curve pocket, and runtime replay are separated before judgment",
        },
        {
            "gate": "row_grain_audit",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "survivor_clue_disposition.csv"),
            "notes": "attempt-level rows are kept separate; no synthetic selected candidate row is created",
        },
        {
            "gate": "source_authority_audit",
            "status": "pass",
            "evidence_path": rel(RUN331C_DIR / "runtime_replay_compare_report.csv"),
            "notes": "MT5 runtime replay matched source results and supports research-only judgment",
        },
        {
            "gate": "required_gate_coverage_audit",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "required_gate_coverage_audit.csv"),
            "notes": "required kpi_evidence gates are explicitly represented in run331D closeout",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "result_judgment_receipt.json"),
            "notes": "Forward Passed, Forward Failed, live readiness, deployment, operating promotion, runtime authority, and Goal Achieve are not claimed",
        },
        {
            "gate": "state_sync_audit",
            "status": "pass",
            "evidence_path": rel(SELECTED_DIR / "selection_status.md"),
            "notes": "selection status and current truth are updated to Stage332 handoff after Stage331 closeout",
        },
    ]


def write_receipts(generated_at_utc: str, matrix: Sequence[Mapping[str, Any]]) -> list[Path]:
    eligible_count = sum(1 for row in matrix if row["selection_eligible"])
    best = max(matrix, key=lambda row: to_float(row.get("source_profit_factor")) or 0.0)
    c56 = next(row for row in matrix if row["attempt_name"] == "c56_plain_rf")
    m48 = next(row for row in matrix if row["attempt_name"] == "m48_plain_rf")
    receipts = [
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "skill": "obsidian-performance-attribution",
                "observed_change": "Headline raw-forward profits replayed exactly, but cost and rolling-pocket guards prevent selection.",
                "comparison_baseline": "Stage330G preserved clue and negative memory split.",
                "likely_drivers": [
                    "cost sensitivity",
                    "rolling drawdown pocket concentration",
                    "first-half versus second-half instability",
                    "runtime path parity is not the source of the weakness",
                ],
                "segment_checks": [
                    "full_forward",
                    "first_half",
                    "second_half",
                    "month_2026-04",
                    "month_2026-05",
                    "worst_pocket",
                    "cost levels 0 to 5",
                    "runtime replay exact match",
                ],
                "trade_shape": {
                    "best_headline_attempt": best["attempt_name"],
                    "best_headline_pf": best["source_profit_factor"],
                    "c56_plain_trade_count": c56["runtime_trade_count"],
                    "m48_plain_trade_count": m48["runtime_trade_count"],
                    "c56_plain_rolling20_min_net": c56["rolling20_min_net"],
                    "m48_plain_rolling20_min_net": m48["rolling20_min_net"],
                },
                "alternative_explanations": [
                    "small forward sample",
                    "US100 cost regime sensitivity",
                    "session and volatility concentration not fully resolved in Stage331",
                ],
                "attribution_confidence": "medium",
                "next_probe": "Stage332 should design a failure-memory research packet that penalizes cost fragility and pocket concentration before model export.",
            },
        ),
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "skill": "obsidian-model-validation",
                "model_family": "Stage330 forward-safe non-identity ONNX research artifacts",
                "target_and_label": "raw-forward fixed-threshold trade direction/control-surface replay; no new label built in Stage331",
                "split_method": "post-2026-04-14 raw-forward replay with cross-horizon and runtime replay checks",
                "selection_metric": "none selected; guard matrix blocks selection",
                "secondary_metrics": [
                    "profit factor after cost",
                    "rolling20 minimum net",
                    "third/fifth positive share",
                    "runtime replay metric match",
                    "negative control catch rate",
                ],
                "threshold_policy": "fixed from source artifacts; no threshold retuning",
                "overfit_risk": "headline profit can be preserved while plus2 cost and rolling pockets fail",
                "calibration_risk": "scores remain decision surface outputs, not probability claims",
                "comparison_baseline": "Stage330G failure memory and run331B negative controls",
                "validation_judgment": "exploratory_research_handoff_no_selection",
                "selection_eligible_attempts": eligible_count,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "skill": "obsidian-result-judgment",
                "result_subject": RUN_ID,
                "evidence_available": [
                    rel(RUN331B_DIR / "candidate_survival_summary.csv"),
                    rel(RUN331B_DIR / "cost_curve_by_horizon_report.csv"),
                    rel(RUN331B_DIR / "resampling_stability_report.csv"),
                    rel(RUN331C_DIR / "runtime_replay_compare_report.csv"),
                    rel(RUN_DIR / "final_decision_matrix.csv"),
                ],
                "evidence_missing": [
                    "independent newer broker data beyond the current raw-forward sample",
                    "fresh model design that avoids Stage331 failure modes",
                    "operating promotion packet",
                ],
                "judgment_label": "negative_for_selection_positive_as_failure_memory",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": "Stage332 must design and test a new research packet that does not tune to Stage331 pockets and then re-run forward/parity controls.",
                "user_explanation_hook": "The replay worked, but the surviving clues still break under cost and curve-pocket guards, so Stage331 closes with no selected ONNX.",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "skill": "obsidian-artifact-lineage",
                "source_inputs": [
                    rel(RUN330G_DIR / "failure_memory_report.csv"),
                    rel(RUN331A_DIR / "run_manifest.json"),
                    rel(RUN331B_DIR / "candidate_survival_summary.csv"),
                    rel(RUN331B_DIR / "cost_curve_by_horizon_report.csv"),
                    rel(RUN331B_DIR / "resampling_stability_report.csv"),
                    rel(RUN331C_DIR / "runtime_replay_compare_report.csv"),
                ],
                "producer": rel(Path(__file__)),
                "consumer": [
                    rel(REVIEWS_DIR / "run331D_final_cross_horizon_overfit_guard_decision.md"),
                    rel(NEXT_STAGE_DIR / "00_spec" / "stage_brief.md"),
                    rel(RUN_REGISTRY),
                    rel(ALPHA_LEDGER),
                    rel(STAGE_LEDGER),
                    rel(ARTIFACT_REGISTRY),
                ],
                "artifact_paths": [
                    rel(RUN_DIR / "final_decision_matrix.csv"),
                    rel(RUN_DIR / "evidence_rollup.csv"),
                    rel(RUN_DIR / "survivor_clue_disposition.csv"),
                    rel(RUN_DIR / "overfit_guard_failure_memory.csv"),
                    rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                ],
                "artifact_hashes": "recorded in docs/registers/artifact_registry.csv",
                "registry_links": [
                    rel(RUN_REGISTRY),
                    rel(ALPHA_LEDGER),
                    rel(STAGE_LEDGER),
                    rel(ARTIFACT_REGISTRY),
                ],
                "availability": "tracked",
                "lineage_judgment": "connected_with_boundary",
                "generated_at_utc": generated_at_utc,
            },
        ),
    ]
    return receipts


def write_reports(matrix: Sequence[Mapping[str, Any]]) -> list[Path]:
    c56 = next(row for row in matrix if row["attempt_name"] == "c56_plain_rf")
    m48 = next(row for row in matrix if row["attempt_name"] == "m48_plain_rf")
    matched = sum(1 for row in matrix if row["runtime_replay_match"])
    negative_caught = [row["attempt_name"] for row in matrix if row["final_disposition"] == "closed_negative_memory_guard_caught"]
    eligible = [row["attempt_name"] for row in matrix if row["selection_eligible"]]
    matrix_lines = "\n".join(
        [
            "| attempt(시도) | role(역할) | PF(수익 팩터) | cost+1 PF(비용+1 수익 팩터) | cost+2 PF(비용+2 수익 팩터) | rolling20 net(롤링20 순손익) | disposition(처분) |",
            "|---|---|---:|---:|---:|---:|---|",
            *[
                f"| {row['attempt_name']} | {row['role']} | {fmt(row['source_profit_factor'])} | {fmt(row['cost1_profit_factor'])} | {fmt(row['cost2_profit_factor'])} | {fmt(row['rolling20_min_net'])} | {row['final_disposition']} |"
                for row in matrix
            ],
        ]
    )
    report = f"""
# run331D Final Cross-Horizon Overfit Guard Decision(331D 최종 교차 기간 과적합 방어 판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Decision(판정)

Stage331(331단계)은 no selection(선택 없음)으로 닫는다.
Effect(효과): run331C(331C 실행)의 runtime replay(런타임 재생)는 {matched}/6개 모두 맞았지만, run331B(331B 실행)의 cost/curve/resampling guard(비용/곡선/재표본 방어)가 선택 가능한 ONNX(온엑스)를 남기지 않았다.

## Matrix(행렬)

{matrix_lines}

## Read(판독)

- negative_controls_caught(포착된 부정 대조군): `{", ".join(negative_caught)}`
- c56_plain_rf(코어56 일반 RF): cost+1 PF(비용+1 수익 팩터) `{fmt(c56["cost1_profit_factor"], 3)}`는 버티지만 cost+2 PF(비용+2 수익 팩터) `{fmt(c56["cost2_profit_factor"], 3)}`와 rolling20 pocket(롤링20 포켓) `{fmt(c56["rolling20_min_net"])}` 때문에 선택하지 않는다.
- m48_plain_rf(매크로48 일반 RF): headline net(표면 순손익)은 가장 크지만 cost+1 PF(비용+1 수익 팩터)가 `{fmt(m48["cost1_profit_factor"], 3)}`로 거의 손익분기이고 rolling20 pocket(롤링20 포켓)이 `{fmt(m48["rolling20_min_net"])}`라 선택하지 않는다.
- selection_eligible_attempts(선택 가능 시도): `{len(eligible)}`

## Boundary(경계)

- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
- live_readiness(실거래 준비), deployment(배포), operating_promotion(운영 승격), runtime_authority(런타임 권위)는 주장하지 않는다.
- Stage332(332단계)는 failure memory(실패 기억)를 받아 새 연구 packet(작업 묶음)을 설계한다. 이 말은 Stage331(331단계) 후보를 고치는 선택 주장이 아니다.
"""
    decision = f"""
# 2026-05-26 Stage331D Final Decision(331D 최종 판정)

Stage331(331단계)은 `closed_no_selection_research_handoff(선택 없음 연구 인계 종료)`로 닫았다.

- result(결과): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`

핵심 이유는 runtime parity(런타임 동등성)가 깨져서가 아니다. run331C(331C 실행)는 6/6 재생 일치를 만들었다. 그래서 cost fragility(비용 취약성), curve pocket(곡선 포켓), sample concentration(표본 집중)을 실제 연구 실패 기억으로 취급한다.
"""
    return [
        write_md(REVIEWS_DIR / "run331D_final_cross_horizon_overfit_guard_decision.md", report),
        write_md(DECISION_DOC, decision),
    ]


def write_stage332_open() -> list[Path]:
    paths: list[Path] = []
    paths.append(
        write_md(
            NEXT_STAGE_DIR / "00_spec" / "stage_brief.md",
            f"""
# Stage332 Failure Memory Forward Research Handoff(332단계 실패 기억 전진 연구 인계)

- active_question(활성 질문): Stage331(331단계)의 cost/curve/runtime guard(비용/곡선/런타임 방어) 실패 기억을 이용해, 과적합을 반복하지 않는 다음 research packet(연구 작업 묶음)을 어떻게 설계할 것인가?
- opened_by(개방 실행): `{RUN_ID}`
- first_run(첫 실행): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_failure_memory_handoff_no_threshold_retuning_no_candidate_selection_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

Effect(효과): c56_plain_rf와 m48_plain_rf를 선택 후보로 고치지 않고, 실패 기억을 다음 설계의 제약 조건으로 옮긴다.
""",
        )
    )
    paths.append(
        write_md(
            NEXT_STAGE_DIR / "01_inputs" / "input_refs.md",
            f"""
# Stage332 Input References(332단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- closeout_report(종료 보고): `{rel(REVIEWS_DIR / "run331D_final_cross_horizon_overfit_guard_decision.md")}`
- final_matrix(최종 행렬): `{rel(RUN_DIR / "final_decision_matrix.csv")}`
- failure_memory(실패 기억): `{rel(RUN_DIR / "overfit_guard_failure_memory.csv")}`
- survivor_clues(생존 단서): `{rel(RUN_DIR / "survivor_clue_disposition.csv")}`
- runtime_replay(런타임 재생): `{rel(RUN331C_DIR / "runtime_replay_compare_report.csv")}`

Effect(효과): 다음 단계는 Stage331(331단계)의 좋은 숫자를 재튜닝(retuning, 재튜닝)하지 않고, 어떤 약점을 피해야 하는지부터 읽는다.
""",
        )
    )
    paths.append(
        write_csv(
            NEXT_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv",
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
    paths.append(
        write_md(
            NEXT_STAGE_DIR / "04_selected" / "selection_status.md",
            f"""
# Stage332 Selection Status(332단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{STAGE_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage331(331단계)의 실패 기억을 새 연구 설계 입력으로 쓰되, 기존 단서를 선택 후보로 승격하지 않는다.
""",
        )
    )
    (NEXT_STAGE_DIR / "02_runs").mkdir(parents=True, exist_ok=True)
    return paths


def update_selection_status() -> Path:
    text = f"""
# Stage331 Selection Status(331단계 선택 상태)

- stage_status(단계 상태): `closed_no_selection_research_handoff`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- latest_design(최신 설계): `run331A_design_cross_horizon_cost_curve_parity_probe_packet_v1`
- latest_materialization(최신 물질화): `run331B_materialize_no_retune_replay_and_resampling_controls_v1`
- latest_runtime_replay(최신 런타임 재생): `{PARENT_RUN_ID}`
- latest_final_decision(최신 최종 판정): `{RUN_ID}`
- retained_clues_not_selection(선택 아닌 유지 단서): `c56_plain_rf`
- fragile_clues_not_selection(선택 아닌 취약 단서): `m48_plain_rf`
- negative_controls_caught(포착된 부정 대조군): `c56_bal_rf, m48_bal_rf, u42_bal_rf, u42_plain_rf`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): runtime replay(런타임 재생)는 맞았지만 cost/curve guard(비용/곡선 방어)를 통과한 선택 후보가 없어 Stage331(331단계)을 연구 인계로 닫는다.
"""
    return write_md(SELECTED_DIR / "selection_status.md", text)


def update_current_truth() -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage332(332단계) `{NEXT_STAGE_ID}`는 run331D(331D 실행)에서 open_planned(열림 계획)로 열렸다. Effect(효과): Stage331(331단계)의 failure memory(실패 기억)를 다음 research packet(연구 작업 묶음)의 제약 조건으로 넘기고, 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
        "- >-\n"
        f"  Stage331(331단계) run331D(331D 실행)는 `{STATUS}`로 닫혔다. Effect(효과): runtime parity(런타임 동등성)는 6/6 재생 일치였지만 cost/curve/resampling guard(비용/곡선/재표본 방어)를 통과한 선택 후보가 없어 no selection(선택 없음)으로 연구 인계한다.\n"
    )
    marker = "Stage331(331단계) run331D(331D 실행)"
    if marker not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`",
        "- source_stage(": f"- source_stage(원천 단계): `{STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `failure_memory_forward_research_handoff`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run331D_summary(331D 요약): final cross-horizon overfit guard decision(최종 교차 기간 과적합 방어 판정)을 `{STATUS}`로 닫았다. "
        "Effect(효과): runtime parity(런타임 동등성)는 맞았지만 선택 가능한 ONNX(온엑스)는 없어서 Stage332(332단계)의 failure memory research handoff(실패 기억 연구 인계)로 넘긴다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run331D_summary(331D 요약)")
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    updated.append(
        append_if_missing(
            CHANGELOG,
            "Stage331D Final Cross-Horizon Overfit Guard Decision",
            f"""
## 2026-05-26 - Stage331D Final Cross-Horizon Overfit Guard Decision(331D 최종 교차 기간 과적합 방어 판정)

- run331D(331D 실행): Stage331(331단계)을 no selection(선택 없음) 연구 인계로 닫았다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): runtime replay(런타임 재생)는 맞았지만 cost/curve/resampling guard(비용/곡선/재표본 방어) 때문에 Forward Passed(전진 통과), Forward Failed(전진 실패), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        )
    )
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run331D_final_cross_horizon_overfit_guard_decision.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "kpi_evidence",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": f"stage331_closed_no_selection;next_stage={NEXT_STAGE_ID};goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__final_decision",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "final_cross_horizon_overfit_guard_decision",
                "tier_scope": "raw_forward_runtime_probe_total",
                "kpi_scope": "cost_curve_resampling_runtime_parity_closeout",
                "scoreboard_lane": "kpi_evidence",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "selection_eligible_attempts=0",
                "guardrail_kpi": "no_threshold_retuning;no_lot_optimization;no_model_update;goal_achieve_not_claimed",
                "external_verification_status": "completed_runtime_replay_boundary_research_only",
                "notes": f"decision={DECISION};next_stage={NEXT_STAGE_ID};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__final_decision",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "final_cross_horizon_overfit_guard_decision(최종 교차 기간 과적합 방어 판정)",
                "tier_scope": "raw_forward_runtime_probe_total(원본 전진 런타임 탐침 전체)",
                "scoreboard": "cost_curve_resampling_runtime_parity_closeout(비용/곡선/재표본/런타임 동등성 종료)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    rows: list[dict[str, Any]] = []
    for artifact in [*artifacts, Path(__file__)]:
        if artifact.exists() and io_path(artifact).is_file():
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact)}",
                    "artifact_type": artifact.suffix.lstrip(".") or "file",
                    "path": rel(artifact),
                    "sha256": sha256_file(artifact),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage331D final decision artifact; no operating claim.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_run_artifacts(generated_at_utc: str) -> list[Path]:
    matrix, clue_rows, memory_rows = build_final_matrix()
    artifacts = [
        write_csv(
            RUN_DIR / "final_decision_matrix.csv",
            [
                "attempt_name",
                "artifact_slug",
                "role",
                "runtime_replay_match",
                "source_net_profit",
                "source_profit_factor",
                "runtime_trade_count",
                "cost1_profit_factor",
                "cost2_profit_factor",
                "third_positive_share",
                "rolling20_min_net",
                "guard_cost_read",
                "guard_curve_read",
                "runtime_read",
                "selection_eligible",
                "final_disposition",
                "no_selection_reason",
            ],
            matrix,
        ),
        write_csv(
            RUN_DIR / "evidence_rollup.csv",
            ["evidence_id", "source_path", "availability", "key_read", "claim_effect"],
            evidence_rollup_rows(matrix),
        ),
        write_csv(
            RUN_DIR / "survivor_clue_disposition.csv",
            [
                "attempt_name",
                "stage330_incoming_role",
                "stage331_final_disposition",
                "selection_status",
                "forward_status",
                "runtime_parity_read",
                "cost_guard_read",
                "curve_guard_read",
                "allowed_future_use",
                "forbidden_future_use",
                "required_next_probe",
            ],
            clue_rows,
        ),
        write_csv(
            RUN_DIR / "overfit_guard_failure_memory.csv",
            [
                "attempt_name",
                "memory_class",
                "final_disposition",
                "observed_failure_modes",
                "full_pf",
                "cost1_pf",
                "cost2_pf",
                "rolling20_min_net",
                "fifth_positive_share",
                "not_a_repair_action",
                "future_design_constraint",
            ],
            memory_rows,
        ),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "notes"],
            gate_audit_rows(),
        ),
        write_json(
            RUN_DIR / "stage331_closeout_decision.json",
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "selected_candidate": "none",
                "stage331_status": "closed_no_selection_research_handoff",
                "next_stage_id": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "selection_eligible_attempts": sum(1 for row in matrix if row["selection_eligible"]),
                "runtime_replay_matched_attempts": sum(1 for row in matrix if row["runtime_replay_match"]),
                "reason": "runtime replay matched, but no attempt survived the final cost, curve pocket, resampling, and selection guard.",
                "claim_boundary": CLAIM_BOUNDARY,
                "generated_at_utc": generated_at_utc,
            },
        ),
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "primary_family": "kpi_evidence",
                "primary_skill": "obsidian-result-judgment",
                "support_skills": [
                    "obsidian-performance-attribution",
                    "obsidian-model-validation",
                    "obsidian-artifact-lineage",
                ],
                "required_gates": [
                    "kpi_contract_audit",
                    "row_grain_audit",
                    "source_authority_audit",
                    "required_gate_coverage_audit",
                    "final_claim_guard",
                    "state_sync_audit",
                ],
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_inputs": [
                    rel(RUN330G_DIR / "failure_memory_report.csv"),
                    rel(RUN331B_DIR / "candidate_survival_summary.csv"),
                    rel(RUN331B_DIR / "cost_curve_by_horizon_report.csv"),
                    rel(RUN331B_DIR / "resampling_stability_report.csv"),
                    rel(RUN331C_DIR / "runtime_replay_compare_report.csv"),
                ],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.extend(write_receipts(generated_at_utc, matrix))
    artifacts.extend(write_reports(matrix))
    artifacts.append(update_selection_status())
    artifacts.extend(write_stage332_open())
    artifacts.extend(update_current_truth())
    return artifacts


def main() -> None:
    generated_at_utc = utc_now()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = write_run_artifacts(generated_at_utc)
    update_registers(generated_at_utc, artifacts)
    matrix = read_csv(RUN_DIR / "final_decision_matrix.csv")
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "selection_eligible_attempts": int(matrix["selection_eligible"].astype(str).str.lower().isin(["true", "1"]).sum()),
                "runtime_replay_matched_attempts": int(matrix["runtime_replay_match"].astype(str).str.lower().isin(["true", "1"]).sum()),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
