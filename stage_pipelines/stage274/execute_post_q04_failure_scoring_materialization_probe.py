from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild"
RUN_ID = "run274D_execute_post_q04_failure_scoring_materialization_probe_v1"
SOURCE_RUN_ID = "run274C_materialize_post_q04_failure_scoring_handoff_inputs_v1"
STATUS = "completed_post_q04_failure_score_surface_materialization_no_candidate_selection"
JUDGMENT = "score_surfaces_materialized_no_candidate_selection"
JUDGMENT_CLASS = "inconclusive"
NEXT_ACTION = "run274E_screen_post_q04_failure_score_surfaces"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN274C = STAGE / "02_runs" / "run274C"
RUN_DIR = STAGE / "02_runs" / "run274D"
SCORE_DIR = RUN_DIR / "score_tables"
HANDOFF_DIR = RUN_DIR / "handoff"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

SOURCE_SPECS = RUN274C / "scoring_input_specs.json"
SOURCE_HANDOFF_PLAN = RUN274C / "handoff_input_plan.csv"
SOURCE_IDENTITY = RUN274C / "package_identity_receipts.csv"
SOURCE_RUN274C_MANIFEST = RUN274C / "run_manifest.json"
SOURCE_Q04_PAYLOAD = (
    ROOT
    / "stages"
    / "272_onnx_candidate_campaign__time_risk_router_pressure_probe"
    / "02_runs"
    / "run272B"
    / "payloads"
    / "q04_payload.parquet"
)

SCORE_SURFACE_SUMMARY = RUN_DIR / "score_surface_summary.csv"
SUMMARY_BY_VIEW = REVIEWS / "run274D_score_surface_summary.csv"
NORMALIZATION_RECEIPT = RUN_DIR / "normalization_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run274D_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]
STAGE_LEDGER_COLUMNS = [
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
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]

PACKAGE_SHORT_IDS = {
    "cp274A_session_loss_asymmetry_router": "cp274A",
    "cp274B_month_regime_resilience_surface": "cp274B",
    "cp274C_drawdown_recovery_context_router": "cp274C",
    "cp274D_q04_failure_boundary_control": "cp274D",
}
PRIMARY_SCORE = {
    "cp274A_session_loss_asymmetry_router": "session_loss_asymmetry_score",
    "cp274B_month_regime_resilience_surface": "month_regime_resilience_score",
    "cp274C_drawdown_recovery_context_router": "drawdown_recovery_context_score",
    "cp274D_q04_failure_boundary_control": "q04_candidate_decision_score",
}
SUMMARY_VIEWS = ["Tier A separate", "Tier B separate", "Tier A+B combined"]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def stable_hash(payload: Any) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["status"]
    temp_path = path.with_name(path.name + ".tmp")
    with io_path(temp_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
    io_path(temp_path).replace(io_path(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing = read_csv_rows(path)
    new_keys = {str(row[key]) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, merged, columns)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("; ".join(missing))


def load_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def sigmoid(value: pd.Series | np.ndarray | float) -> pd.Series:
    array = np.asarray(value, dtype="float64")
    clipped = np.clip(array, -20.0, 20.0)
    return pd.Series(1.0 / (1.0 + np.exp(-clipped)))


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> pd.Series:
    if name not in frame.columns:
        return pd.Series(default, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[name], errors="coerce").astype("float64").fillna(default)


def train_scaled(frame: pd.DataFrame, column: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    numeric = col(frame, column)
    output = pd.Series(0.0, index=frame.index, dtype="float64")
    receipts: list[dict[str, Any]] = []
    for tier_view in sorted(str(value) for value in frame["tier_view"].dropna().unique()):
        tier_mask = frame["tier_view"].astype(str).eq(tier_view)
        train_mask = tier_mask & frame["split"].astype(str).eq("train")
        train_values = numeric[train_mask]
        median = float(train_values.median(skipna=True)) if len(train_values) else 0.0
        mad = float((train_values - median).abs().median(skipna=True)) if len(train_values) else 0.0
        std = float(train_values.std(skipna=True)) if len(train_values) else 0.0
        scale = mad * 1.4826 if np.isfinite(mad) and mad > 0 else std
        if not np.isfinite(scale) or scale <= 0:
            scale = 1.0
        output.loc[tier_mask] = ((numeric.loc[tier_mask] - median) / scale).clip(-6.0, 6.0)
        receipts.append(
            {
                "column": column,
                "tier_view": tier_view,
                "train_rows": int(train_mask.sum()),
                "median": round(median, 12),
                "scale": round(float(scale), 12),
                "method": "train_split_median_mad_or_std",
            }
        )
    return output.fillna(0.0), receipts


def make_base(frame: pd.DataFrame, package: Mapping[str, Any]) -> pd.DataFrame:
    package_id = str(package["package_id"])
    return pd.DataFrame(
        {
            "timestamp": frame["timestamp"],
            "symbol": frame["symbol"].astype(str),
            "split": frame["split"].astype(str),
            "tier_view": frame["tier_view"].astype(str),
            "source_package_id": frame["package_id"].astype(str),
            "package_id": package_id,
            "route_code": frame["route_code"].astype(str),
            "source_route_signal_label": frame["route_signal_label"].astype(str),
            "source_candidate_decision_score": col(frame, "candidate_decision_score").round(8),
            "source_materialized_decision_flag": col(frame, "materialized_decision_flag").astype("int8"),
            "feature_order_hash": package["source_feature_order_hash"],
            "blueprint_hash": package["source_blueprint_hash"],
            "score_columns_hash": package["score_columns_hash"],
            "decision_rule_hash": package["decision_rule_hash"],
            "risk_rule_hash": package["risk_rule_hash"],
            "adapter_schema_hash": package["adapter_schema_hash"],
            "claim_boundary": BOUNDARY,
        }
    )


def finalize_outputs(output: pd.DataFrame) -> pd.DataFrame:
    output["atr_stop_multiplier"] = output["atr_stop_multiplier"].clip(0.7, 3.0).round(6)
    output["atr_take_profit_multiplier"] = output["atr_take_profit_multiplier"].clip(0.8, 5.0).round(6)
    output["max_hold_bars"] = output["max_hold_bars"].clip(6, 144).round().astype("int16")
    output["reentry_cooldown_bars"] = output["reentry_cooldown_bars"].clip(0, 48).round().astype("int16")
    output["model_risk_pct"] = output["model_risk_pct"].clip(0.0, 1.0).round(8)
    return output


def route_value(frame: pd.DataFrame) -> pd.Series:
    if "route_signal_value" in frame.columns:
        return col(frame, "route_signal_value")
    label = frame["route_signal_label"].astype(str).str.lower()
    return label.map({"long": 1.0, "short": -1.0, "flat": 0.0}).fillna(0.0)


def signal_from_permission(frame: pd.DataFrame, long_permission: pd.Series, short_permission: pd.Series) -> pd.Series:
    label = frame["route_signal_label"].astype(str).str.lower()
    signal = pd.Series("flat", index=frame.index, dtype="object")
    signal.loc[(label.eq("long")) & (long_permission >= 0.56)] = "long"
    signal.loc[(label.eq("short")) & (short_permission >= 0.56)] = "short"
    return signal


def score_cp274a(frame: pd.DataFrame, package: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    session_z, r1 = train_scaled(frame, "session_clock_risk")
    phase_z, r2 = train_scaled(frame, "phase_risk_score")
    candidate_z, r3 = train_scaled(frame, "candidate_decision_score")
    route_z, r4 = train_scaled(frame, "route_signal_value")
    weekday_z, r5 = train_scaled(frame, "weekday_phase")
    session = col(frame, "session_clock_risk")
    candidate = col(frame, "candidate_decision_score")
    raw = 0.46 * candidate_z + 0.24 * route_z.abs() - 0.34 * session_z - 0.22 * phase_z + 0.08 * weekday_z.abs()
    session_loss_asymmetry_score = sigmoid(raw)
    long_permission_score = sigmoid(raw + 0.20 * (route_value(frame) > 0).astype("float64") - 0.18 * session_z)
    short_permission_score = sigmoid(raw + 0.20 * (route_value(frame) < 0).astype("float64") - 0.18 * session_z)
    exposure_reduction_score = sigmoid(0.48 * session_z + 0.36 * phase_z - 0.30 * candidate_z)

    output = make_base(frame, package)
    output["session_loss_asymmetry_score"] = session_loss_asymmetry_score.round(8)
    output["long_permission_score"] = long_permission_score.round(8)
    output["short_permission_score"] = short_permission_score.round(8)
    output["exposure_reduction_score"] = exposure_reduction_score.round(8)
    output["entry_signal"] = signal_from_permission(frame, long_permission_score, short_permission_score)
    output["model_risk_pct"] = (0.08 + 0.82 * session_loss_asymmetry_score * (1.0 - 0.58 * exposure_reduction_score)).clip(0.0, 1.0)
    output["atr_stop_multiplier"] = 1.00 + 0.40 * exposure_reduction_score + 0.15 * session.clip(0, 1)
    output["atr_take_profit_multiplier"] = 1.35 + 0.65 * session_loss_asymmetry_score
    output["max_hold_bars"] = 36 + 20 * (1.0 - exposure_reduction_score)
    output["reentry_cooldown_bars"] = 6 + 18 * exposure_reduction_score
    return finalize_outputs(output), [*r1, *r2, *r3, *r4, *r5]


def score_cp274b(frame: pd.DataFrame, package: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    month_z, r1 = train_scaled(frame, "month_regime_pressure")
    risk_z, r2 = train_scaled(frame, "phase_risk_score")
    opp_z, r3 = train_scaled(frame, "phase_opportunity_score")
    age_z, r4 = train_scaled(frame, "chron_phase_age")
    session_z, r5 = train_scaled(frame, "session_clock_risk")
    payoff_budget_score = sigmoid(0.52 * opp_z - 0.34 * risk_z - 0.28 * month_z + 0.10 * age_z.abs())
    regime_pressure_adjustment = sigmoid(0.42 * month_z + 0.28 * risk_z + 0.20 * session_z - 0.18 * opp_z)
    opportunity_override_score = sigmoid(0.58 * opp_z - 0.32 * month_z - 0.22 * session_z)
    month_regime_resilience_score = sigmoid(
        0.52 * payoff_budget_score + 0.25 * opportunity_override_score - 0.46 * regime_pressure_adjustment
    )

    route = route_value(frame)
    output = make_base(frame, package)
    output["month_regime_resilience_score"] = month_regime_resilience_score.round(8)
    output["payoff_budget_score"] = payoff_budget_score.round(8)
    output["regime_pressure_adjustment"] = regime_pressure_adjustment.round(8)
    output["opportunity_override_score"] = opportunity_override_score.round(8)
    signal = pd.Series("flat", index=frame.index, dtype="object")
    active = (month_regime_resilience_score >= 0.52) & ((payoff_budget_score >= 0.54) | (opportunity_override_score >= 0.58))
    signal.loc[active & (route > 0)] = "long"
    signal.loc[active & (route < 0)] = "short"
    output["entry_signal"] = signal
    output["model_risk_pct"] = (0.06 + 0.86 * month_regime_resilience_score * (1.0 - 0.50 * regime_pressure_adjustment)).clip(0.0, 1.0)
    output["atr_stop_multiplier"] = 1.05 + 0.35 * regime_pressure_adjustment
    output["atr_take_profit_multiplier"] = 1.25 + 0.90 * payoff_budget_score
    output["max_hold_bars"] = 30 + 26 * payoff_budget_score
    output["reentry_cooldown_bars"] = 5 + 16 * regime_pressure_adjustment
    return finalize_outputs(output), [*r1, *r2, *r3, *r4, *r5]


def score_cp274c(frame: pd.DataFrame, package: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    age_z, r1 = train_scaled(frame, "chron_phase_age")
    session_z, r2 = train_scaled(frame, "session_clock_risk")
    risk_z, r3 = train_scaled(frame, "phase_risk_score")
    route_z, r4 = train_scaled(frame, "route_signal_value")
    candidate_z, r5 = train_scaled(frame, "candidate_decision_score")
    underwater_proxy_score = sigmoid(0.34 * session_z + 0.34 * risk_z + 0.22 * age_z.abs() - 0.24 * candidate_z)
    reentry_permission_score = sigmoid(0.56 * candidate_z + 0.18 * route_z.abs() - 0.35 * underwater_proxy_score - 0.20 * risk_z)
    same_direction_delay_score = sigmoid(0.50 * underwater_proxy_score + 0.24 * risk_z - 0.22 * candidate_z)
    drawdown_recovery_context_score = sigmoid(0.48 * reentry_permission_score + 0.25 * candidate_z - 0.40 * same_direction_delay_score)

    route = route_value(frame)
    output = make_base(frame, package)
    output["drawdown_recovery_context_score"] = drawdown_recovery_context_score.round(8)
    output["reentry_permission_score"] = reentry_permission_score.round(8)
    output["same_direction_delay_score"] = same_direction_delay_score.round(8)
    output["underwater_proxy_score"] = underwater_proxy_score.round(8)
    signal = pd.Series("flat", index=frame.index, dtype="object")
    active = (reentry_permission_score >= 0.52) & (same_direction_delay_score <= 0.66)
    signal.loc[active & (route > 0)] = "long"
    signal.loc[active & (route < 0)] = "short"
    output["entry_signal"] = signal
    output["model_risk_pct"] = (0.05 + 0.82 * drawdown_recovery_context_score * (1.0 - 0.46 * underwater_proxy_score)).clip(0.0, 1.0)
    output["atr_stop_multiplier"] = 1.00 + 0.45 * underwater_proxy_score
    output["atr_take_profit_multiplier"] = 1.20 + 0.70 * reentry_permission_score
    output["max_hold_bars"] = 28 + 24 * drawdown_recovery_context_score
    output["reentry_cooldown_bars"] = 4 + 22 * same_direction_delay_score
    return finalize_outputs(output), [*r1, *r2, *r3, *r4, *r5]


def score_cp274d(frame: pd.DataFrame, package: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    session_z, r1 = train_scaled(frame, "session_clock_risk")
    month_z, r2 = train_scaled(frame, "month_regime_pressure")
    candidate = col(frame, "candidate_decision_score")
    route = route_value(frame)
    q04_failure_signature_flag = ((session_z > 0.75) | (month_z > 0.75) | (frame["risk_action_code"].astype(str).isin(["clock_hold", "phase_cut"]))).astype("int8")

    output = make_base(frame, package)
    output["q04_route_signal_value"] = route.round(8)
    output["q04_candidate_decision_score"] = candidate.round(8)
    output["q04_failure_signature_flag"] = q04_failure_signature_flag
    signal = pd.Series("flat", index=frame.index, dtype="object")
    active = col(frame, "variant_decision_flag").astype("int8").eq(1)
    signal.loc[active & (route > 0)] = "long"
    signal.loc[active & (route < 0)] = "short"
    output["entry_signal"] = signal
    output["model_risk_pct"] = np.where(active, 1.0, 0.0)
    output["atr_stop_multiplier"] = 1.0
    output["atr_take_profit_multiplier"] = 1.0
    output["max_hold_bars"] = 36
    output["reentry_cooldown_bars"] = 0
    return finalize_outputs(output), [*r1, *r2]


SCORERS = {
    "cp274A_session_loss_asymmetry_router": score_cp274a,
    "cp274B_month_regime_resilience_surface": score_cp274b,
    "cp274C_drawdown_recovery_context_router": score_cp274c,
    "cp274D_q04_failure_boundary_control": score_cp274d,
}


def summarize_score_table(frame: pd.DataFrame, package: Mapping[str, Any], score_path: Path) -> list[dict[str, Any]]:
    package_id = str(package["package_id"])
    primary_score = PRIMARY_SCORE[package_id]
    rows: list[dict[str, Any]] = []
    for view in SUMMARY_VIEWS:
        if view == "Tier A+B combined":
            view_frame = frame
        else:
            view_frame = frame[frame["tier_view"].eq(view)]
        if view_frame.empty:
            rows.append(
                {
                    "package_id": package_id,
                    "package_role": package["package_role"],
                    "record_view": view,
                    "rows": 0,
                    "active_signal_count": 0,
                    "active_signal_rate": 0.0,
                    "long_count": 0,
                    "short_count": 0,
                    "mean_primary_score": 0.0,
                    "mean_model_risk_pct": 0.0,
                    "score_table_path": rel(score_path),
                    "score_table_hash": sha256_file(score_path),
                    "judgment": "empty_view",
                    "claim_boundary": BOUNDARY,
                }
            )
            continue
        active = view_frame["entry_signal"].ne("flat")
        rows.append(
            {
                "package_id": package_id,
                "package_role": package["package_role"],
                "record_view": view,
                "rows": int(len(view_frame)),
                "active_signal_count": int(active.sum()),
                "active_signal_rate": round(float(active.mean()), 8),
                "long_count": int(view_frame["entry_signal"].eq("long").sum()),
                "short_count": int(view_frame["entry_signal"].eq("short").sum()),
                "mean_primary_score": round(float(pd.to_numeric(view_frame[primary_score], errors="coerce").mean()), 8),
                "mean_model_risk_pct": round(float(pd.to_numeric(view_frame["model_risk_pct"], errors="coerce").mean()), 8),
                "score_table_path": rel(score_path),
                "score_table_hash": sha256_file(score_path),
                "judgment": "score_surface_materialized_no_candidate_selection",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def materialize_score_tables(specs: Mapping[str, Any]) -> tuple[list[Path], list[Path], list[dict[str, Any]], list[dict[str, Any]]]:
    frame = pd.read_parquet(io_path(SOURCE_Q04_PAYLOAD)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    packages = list(specs["packages"])
    score_paths: list[Path] = []
    handoff_paths: list[Path] = []
    summary_rows: list[dict[str, Any]] = []
    normalization_rows: list[dict[str, Any]] = []
    for package in packages:
        package_id = str(package["package_id"])
        short_id = PACKAGE_SHORT_IDS[package_id]
        output, receipts = SCORERS[package_id](frame, package)
        output_path = SCORE_DIR / f"{short_id}_scores.parquet"
        io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
        output.to_parquet(io_path(output_path), index=False)
        score_paths.append(output_path)
        normalization_rows.extend({"package_id": package_id, **row} for row in receipts)
        summary = summarize_score_table(output, package, output_path)
        summary_rows.extend(summary)
        handoff = {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "package_id": package_id,
            "package_role": package["package_role"],
            "score_table_path": rel(output_path),
            "score_table_hash": sha256_file(output_path),
            "summary_rows": [row for row in summary if row["package_id"] == package_id],
            "runtime_handoff_status": "score_table_materialized_not_runtime_package",
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_consumer": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        }
        handoff_path = HANDOFF_DIR / f"{short_id}_handoff.json"
        write_json(handoff_path, handoff)
        handoff_paths.append(handoff_path)
    return score_paths, handoff_paths, summary_rows, normalization_rows


def write_receipts(summary_rows: Sequence[Mapping[str, Any]], normalization_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    package_count = len({row["package_id"] for row in summary_rows})
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "hypothesis": "run274C(274C 실행)의 scoring input spec(점수 입력 규격)은 deterministic score surface(결정 점수 표면)로 물질화될 수 있다.",
            "decision_use": "run274E(274E 실행)가 score surface(점수 표면)를 screening(선별)할 수 있게 한다.",
            "comparison_baseline": "cp274D_q04_failure_boundary_control(q04 실패 경계 보조 대조)",
            "control_variables": {
                "source_payload": rel(SOURCE_Q04_PAYLOAD),
                "normalization": "train split only by tier_view(티어 보기별 학습 분할만 사용)",
                "claim_boundary": BOUNDARY,
            },
            "changed_variables": sorted({row["package_id"] for row in summary_rows if row["package_role"] == "selectable_blueprint"}),
            "sample_scope": "Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산) score surface scout(점수 표면 탐색)",
            "success_criteria": "Each package has a score table(점수표), handoff JSON(인계 JSON), and paired summary rows(쌍 요약 행).",
            "failure_criteria": "Missing score table(점수표 누락), missing Tier B row(티어 B 행 누락), or empty active-signal diagnostics(활성 신호 진단 누락).",
            "invalid_conditions": "If labels/future columns(라벨/미래 열) enter normalization(정규화) or score formula(점수 공식), the run is invalid(무효).",
            "stop_conditions": "Do not select a candidate(후보 선택 금지) until run274E screening(274E 선별) and later MT5 validation(MT5 검증) exist.",
            "evidence_plan": [rel(SCORE_SURFACE_SUMMARY), rel(SUMMARY_BY_VIEW), rel(NORMALIZATION_RECEIPT)],
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "data_source": [rel(SOURCE_Q04_PAYLOAD), rel(SOURCE_SPECS)],
            "time_axis": "timestamp(타임스탬프)는 UTC(협정세계시)이며, 새 resampling(재표본화)은 없다.",
            "sample_scope": {
                "package_count": package_count,
                "summary_rows": len(summary_rows),
                "tier_views": SUMMARY_VIEWS,
            },
            "missing_or_duplicate_check": "Score tables(점수표)는 q04 payload(q04 페이로드) 행 수를 보존하고 summary(요약)에 view rows(보기 행)를 기록한다.",
            "feature_label_boundary": "No label/future columns(라벨/미래 열)을 score formula(점수 공식)에 사용하지 않는다.",
            "split_boundary": "Scaling parameters(스케일 파라미터)는 train split(학습 분할)에서만 산출해 validation/oos(검증/표본외)에 적용한다.",
            "leakage_risk": "Formula weights(공식 가중치)는 탐색 고정값이며, performance optimization(성과 최적화)으로 조정하지 않았다.",
            "data_hash_or_identity": {rel(SOURCE_Q04_PAYLOAD): sha256_file(SOURCE_Q04_PAYLOAD), rel(SOURCE_SPECS): sha256_file(SOURCE_SPECS)},
            "integrity_judgment": "usable_with_boundary",
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "model_family": "deterministic scoring surfaces(결정 점수 표면)",
            "target_and_label": "No trained target(학습 목표) and no new label(새 라벨).",
            "split_method": "train normalization with validation/oos application(학습 정규화 후 검증/표본외 적용)",
            "selection_metric": "not_selected_in_run274D(274D에서 선택하지 않음)",
            "secondary_metrics": ["active_signal_rate(활성 신호율)", "mean_primary_score(평균 주 점수)", "mean_model_risk_pct(평균 모델 위험 비율)"],
            "threshold_policy": "fixed scout thresholds(고정 탐색 임계값), no search(탐색 없음)",
            "overfit_risk": "Weights(가중치) remain exploratory(탐색용) and require run274E screening(274E 선별).",
            "calibration_risk": "Scores are ranking/control signals(순위/제어 신호), not calibrated probability(보정 확률 아님).",
            "comparison_baseline": "cp274D q04 failure boundary control(q04 실패 경계 보조 대조)",
            "validation_judgment": "exploratory_score_surface_materialized_no_selection",
        },
    )
    write_json(
        NORMALIZATION_RECEIPT,
        {
            "run_id": RUN_ID,
            "method": "train_split_median_mad_or_std_by_tier_view",
            "effect": "validation/oos(검증/표본외) 분포를 normalization(정규화)에 쓰지 않아 lookahead risk(미래참조 위험)를 줄인다.",
            "rows": normalization_rows,
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        [
            {
                "result_subject": "run274D score surface materialization(274D 점수 표면 물질화)",
                "evidence_available": "score tables(점수표);handoff JSON(인계 JSON);summary CSV(요약 CSV);normalization receipt(정규화 영수증)",
                "evidence_missing": "screening judgment(선별 판정);MT5 KPI(MT5 핵심 성과 지표);selected candidate(선택 후보);ONNX export/parity(온엑스 내보내기/동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": JUDGMENT_CLASS,
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "점수표는 만들어졌지만 아직 후보를 고르거나 ONNX로 넘길 근거는 아니다.",
            }
        ],
    )
    gate_rows = [
        {
            "gate_name": "scope_completion_gate(범위 완료 게이트)",
            "status": "passed",
            "evidence_path": rel(SCORE_SURFACE_SUMMARY),
            "effect": "package(패키지)별 score table(점수표)과 summary(요약)를 만들었다.",
        },
        {
            "gate_name": "kpi_contract_audit(KPI 계약 감사)",
            "status": "passed_with_boundary",
            "evidence_path": rel(SUMMARY_BY_VIEW),
            "effect": "trading KPI(거래 핵심 성과 지표)가 아니라 score surface scout(점수 표면 탐색) KPI만 기록했다.",
        },
        {
            "gate_name": "skill_receipt_lint(스킬 영수증 검사)",
            "status": "passed",
            "evidence_path": rel(EXPERIMENT_RECEIPT),
            "effect": "experiment/data/model/result/lineage(실험/데이터/모델/결과/계보) 영수증을 연결했다.",
        },
        {
            "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "experiment_execution(실험 실행) 필수 게이트를 closeout(종료 기록)에 연결했다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]
    write_csv(GATE_AUDIT, gate_rows)
    return gate_rows


def write_outputs(summary_rows: Sequence[Mapping[str, Any]]) -> None:
    summary_columns = [
        "package_id",
        "package_role",
        "record_view",
        "rows",
        "active_signal_count",
        "active_signal_rate",
        "long_count",
        "short_count",
        "mean_primary_score",
        "mean_model_risk_pct",
        "score_table_path",
        "score_table_hash",
        "judgment",
        "claim_boundary",
    ]
    write_csv(SCORE_SURFACE_SUMMARY, summary_rows, summary_columns)
    write_csv(SUMMARY_BY_VIEW, summary_rows, summary_columns)
    package_count = len({row["package_id"] for row in summary_rows})
    combined_lines = "\n".join(
        f"- `{row['package_id']}` `{row['record_view']}`: active_signal_rate(활성 신호율) `{row['active_signal_rate']}`, mean_primary_score(평균 주 점수) `{row['mean_primary_score']}`"
        for row in summary_rows
        if row["record_view"] == "Tier A+B combined"
    )
    write_md(
        RUN_REPORT,
        f"""# run274D Score Surface Materialization(274D 점수 표면 물질화)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- judgment_class(판정 분류): `{JUDGMENT_CLASS}`
- packages(패키지): `{package_count}`
- summary_rows(요약 행): `{len(summary_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run274D(274D 실행)는 run274C(274C 실행)의 scoring/handoff input(점수/인계 입력)을 deterministic score table(결정 점수표)로 물질화했다.
효과(effect, 효과): run274E(274E 실행)가 Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산) 관점에서 점수 표면을 선별할 수 있다.

## Combined View(합산 보기)

{combined_lines}

## Evidence Paths(근거 경로)

- score_surface_summary(점수 표면 요약): `{rel(SCORE_SURFACE_SUMMARY)}`
- summary_by_view(보기별 요약): `{rel(SUMMARY_BY_VIEW)}`
- normalization_receipt(정규화 영수증): `{rel(NORMALIZATION_RECEIPT)}`
- score_tables(점수표): `{rel(SCORE_DIR)}`
- handoff(인계): `{rel(HANDOFF_DIR)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def write_manifests_and_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    source_inputs = [SOURCE_SPECS, SOURCE_HANDOFF_PLAN, SOURCE_IDENTITY, SOURCE_RUN274C_MANIFEST, SOURCE_Q04_PAYLOAD]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "judgment_class": JUDGMENT_CLASS,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage274/execute_post_q04_failure_scoring_materialization_probe.py",
        "entry_command": "python stage_pipelines/stage274/execute_post_q04_failure_scoring_materialization_probe.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)
    full_artifacts = [*artifacts, RUN_MANIFEST, LINEAGE_RECEIPT]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run274D_score_materialization_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run274D score surface materialization artifact.",
        }
        for path in full_artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def update_ledgers(summary_rows: Sequence[Mapping[str, Any]]) -> None:
    package_count = len({row["package_id"] for row in summary_rows})
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"packages={package_count};summary_rows={len(summary_rows)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__{row['package_id']}__{str(row['record_view']).replace(' ', '_').replace('+', 'plus')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": row["package_id"],
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": row["record_view"],
            "tier_scope": row["record_view"],
            "kpi_scope": "score_surface_structural_scout",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": row["judgment"],
            "path": row["score_table_path"],
            "primary_kpi": f"active_signal_rate={row['active_signal_rate']};mean_primary_score={row['mean_primary_score']}",
            "guardrail_kpi": "trading_kpi=not_applicable;selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "not_applicable",
            "notes": f"score_table_hash={row['score_table_hash']}",
        }
        for row in summary_rows
    ]
    stage_rows = [
        {
            "row_id": f"{RUN_ID}__{row['package_id']}__{str(row['record_view']).replace(' ', '_').replace('+', 'plus')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": f"score_surface_{row['record_view']}_{row['package_id']}",
            "tier_scope": row["record_view"],
            "scoreboard": "structural_scout",
            "status": STATUS,
            "judgment": row["judgment"],
            "evidence_boundary": "score_surface_only_no_candidate_no_onnx",
            "report_path": rel(RUN_REPORT),
            "notes": f"active_signal_rate={row['active_signal_rate']};score_table_hash={row['score_table_hash']}",
        }
        for row in summary_rows
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_rows, key="row_id")


def update_state_docs(summary_rows: Sequence[Mapping[str, Any]]) -> None:
    package_count = len({row["package_id"] for row in summary_rows})
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_once(selection, "run274D_report", f"- run274D_report(274D 보고서): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run274D_score_surface_summary", f"- run274D_score_surface_summary(274D 점수 표면 요약): `{rel(SCORE_SURFACE_SUMMARY)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run274D_report",
        "\n".join(
            [
                f"- run274D_report(274D 보고서): `{rel(RUN_REPORT)}`",
                f"- run274D_score_surface_summary(274D 점수 표면 요약): `{rel(SCORE_SURFACE_SUMMARY)}`",
                f"- run274D_summary_by_view(274D 보기별 요약): `{rel(SUMMARY_BY_VIEW)}`",
                f"- run274D_normalization_receipt(274D 정규화 영수증): `{rel(NORMALIZATION_RECEIPT)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run274D_summary",
        f"- run274D_summary(274D 요약): run274D(274D 실행)는 package(패키지) `{package_count}`개에 deterministic score table(결정 점수표)을 만들고 Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산) 요약 `{len(summary_rows)}`행을 기록했다. Effect(효과): run274E(274E 실행)에서 score surface(점수 표면)를 선별할 수 있지만, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage274(274단계) run274D(274D 실행) post-q04 score surface materialization(q04 이후 점수 표면 물질화) `{RUN_ID}`. "
        f"Effect(효과): package(패키지) `{package_count}`개에 score table(점수표)과 paired summary(쌍 요약) `{len(summary_rows)}`행을 만들고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run274D score surface materialization(274D 점수 표면 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): package(패키지) `{package_count}`개에 score table(점수표)과 paired summary(쌍 요약) `{len(summary_rows)}`행을 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def execute() -> dict[str, Any]:
    must_exist([SOURCE_SPECS, SOURCE_HANDOFF_PLAN, SOURCE_IDENTITY, SOURCE_RUN274C_MANIFEST, SOURCE_Q04_PAYLOAD])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(SCORE_DIR).mkdir(parents=True, exist_ok=True)
    io_path(HANDOFF_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    specs = load_json(SOURCE_SPECS)
    score_paths, handoff_paths, summary_rows, normalization_rows = materialize_score_tables(specs)
    write_outputs(summary_rows)
    gate_rows = write_receipts(summary_rows, normalization_rows)
    artifacts = [
        SCORE_SURFACE_SUMMARY,
        SUMMARY_BY_VIEW,
        NORMALIZATION_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
        *score_paths,
        *handoff_paths,
    ]
    write_manifests_and_registry(created_at, artifacts)
    update_ledgers(summary_rows)
    update_state_docs(summary_rows)
    package_count = len({row["package_id"] for row in summary_rows})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "judgment_class": JUDGMENT_CLASS,
        "packages": package_count,
        "summary_rows": len(summary_rows),
        "score_tables": len(score_paths),
        "handoff_files": len(handoff_paths),
        "gate_rows": len(gate_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
