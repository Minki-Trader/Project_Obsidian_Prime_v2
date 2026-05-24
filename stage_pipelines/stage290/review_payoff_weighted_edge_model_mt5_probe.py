from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from stage_pipelines.stage280.validate_directional_mapping_stability import safe_float, trade_frame  # noqa: E402


STAGE290_ID = "290_onnx_candidate_campaign__payoff_weighted_edge_model_rebuild"
STAGE291_FAILURE_ID = "291_onnx_candidate_campaign__walk_forward_payoff_generalization_rebuild"
STAGE291_ADAPTER_ID = "291_onnx_candidate_campaign__adapter_package_for_stage290_survivor"
RUN_ID = "run290C_review_payoff_weighted_edge_model_mt5_probe_v1"
RUN_NUMBER = "run290C"
SOURCE_RUN_ID = "run290B_payoff_weighted_edge_model_mt5_probe_v1"
STATUS_NO_CANDIDATE = "completed_payoff_weighted_edge_review_no_candidate_stage291_opened"
STATUS_SELECTED = "completed_payoff_weighted_edge_review_candidate_selected_stage291_adapter_opened"
JUDGMENT_NO_CANDIDATE = "payoff_weighted_edge_model_did_not_meet_onnx_worthy_gate_no_adapter_no_onnx"
JUDGMENT_SELECTED = "payoff_weighted_edge_model_candidate_selected_for_adapter_package_no_onnx_yet"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE290 = ROOT / "stages" / STAGE290_ID
RUN290A = STAGE290 / "02_runs" / "run290A"
RUN290B = STAGE290 / "02_runs" / "run290B"
RUN_DIR = STAGE290 / "02_runs" / RUN_NUMBER
REVIEWS290 = STAGE290 / "03_reviews"
SELECTED290 = STAGE290 / "04_selected" / "selection_status.md"
REVIEW_INDEX290 = REVIEWS290 / "review_index.md"
STAGE_LEDGER290 = REVIEWS290 / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN290A / "candidate_payload_manifest.csv"
SOURCE_MODEL_SCOREBOARD = RUN290A / "model_scout_scoreboard.csv"
SOURCE_MODEL_MANIFEST = RUN290A / "model_artifact_manifest.csv"
SOURCE_KPI = RUN290B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN290B / "execution_result.json"
SOURCE_RUN_MANIFEST = RUN290B / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage290/review_payoff_weighted_edge_model_mt5_probe.py")

SCOREBOARD = RUN_DIR / "payoff_weighted_edge_scoreboard.csv"
MONTHLY = RUN_DIR / "monthly_attribution.csv"
SESSION = RUN_DIR / "session_attribution.csv"
LOCAL_POCKETS = RUN_DIR / "local_curve_pocket_diagnostics.csv"
CURVE = RUN_DIR / "curve_stability_summary.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
SURVIVOR_QUEUE = RUN_DIR / "stage291_survivor_or_rebuild_queue.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS290 / "run290C_payoff_weighted_edge_review_stage291_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage290_payoff_weighted_edge_review_stage291_open.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "model_family",
    "validation_net_profit",
    "validation_pf",
    "validation_trade_count",
    "validation_trades_per_day",
    "validation_dd",
    "validation_recovery",
    "validation_expectancy",
    "validation_positive_month_share",
    "validation_worst_month_net",
    "validation_worst_session_net",
    "validation_worst_rolling_20_net",
    "validation_worst_rolling_50_net",
    "validation_underwater_ratio",
    "oos_net_profit",
    "oos_pf",
    "oos_trade_count",
    "oos_trades_per_day",
    "oos_dd",
    "oos_recovery",
    "oos_expectancy",
    "oos_positive_month_share",
    "oos_worst_month_net",
    "oos_worst_session_net",
    "oos_worst_rolling_20_net",
    "oos_worst_rolling_50_net",
    "oos_underwater_ratio",
    "density_gate",
    "profit_scale_gate",
    "efficiency_gate",
    "curve_quality_gate",
    "review_label",
    "failure_reasons",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
ATTRIBUTION_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "split",
    "bucket_type",
    "bucket",
    "trade_count",
    "net_profit",
    "profit_factor",
    "positive_bucket",
    "source_report_path",
)
CURVE_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "split",
    "trade_count",
    "final_net",
    "max_equity_peak",
    "min_equity",
    "underwater_ratio",
    "source_report_path",
)
POCKET_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "split",
    "rolling_window",
    "worst_rolling_net",
    "pocket_threshold",
    "pocket_label",
    "source_report_path",
)
FAILURE_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "failure_type",
    "failure_reasons",
    "salvage_value",
    "reopen_condition",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "seed_id",
    "source_materialized_branch_id",
    "source_package_id",
    "seed_role",
    "fresh_stage291_question",
    "required_change",
    "forbidden_repair_loop",
    "prior_stage_refs",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
STAGE_LEDGER_COLUMNS = (
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
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    upsert_csv_rows(path, columns, rows, key=key)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def parse_obj(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    text = str(value or "").strip()
    if not text:
        return {}
    return dict(ast.literal_eval(text))


def manifest_by_id() -> dict[str, dict[str, str]]:
    return {row["materialized_branch_id"]: row for row in read_csv_dicts(SOURCE_MANIFEST)}


def model_family_by_id() -> dict[str, str]:
    rows = read_csv_dicts(SOURCE_MODEL_MANIFEST)
    return {row["materialized_branch_id"]: row.get("model_family", "") for row in rows}


def safe_name(value: str, limit: int = 80) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def stage290_variant_token(row: Mapping[str, str], limit: int = 44) -> str:
    text = str(row.get("materialized_branch_id") or row.get("queue_id") or "unknown")
    text = text.replace("run279B_", "").replace("run279C_", "")
    return safe_name(text, limit)


def parse_records() -> dict[tuple[str, str], dict[str, Any]]:
    records: dict[tuple[str, str], dict[str, Any]] = {}
    manifest = manifest_by_id()
    known_ids = sorted(manifest, key=len, reverse=True)
    token_to_id = {stage290_variant_token(row): materialized_id for materialized_id, row in manifest.items()}
    known_tokens = sorted((token for token in token_to_id if token), key=len, reverse=True)
    for row in read_csv_dicts(SOURCE_KPI):
        if row.get("route_role") != "actual_routed_total":
            continue
        metrics = parse_obj(row.get("metrics"))
        report = parse_obj(row.get("report"))
        attempt_name = str(report.get("attempt_name") or "")
        record_view = str(row.get("record_view") or "")
        attempt_text = " ".join([attempt_name, record_view])
        materialized_id = next((item for item in known_ids if item in attempt_name), "")
        if not materialized_id:
            materialized_id = next((token_to_id[token] for token in known_tokens if token in attempt_text), "")
        if not materialized_id:
            continue
        report_path_text = str(metrics.get("report_path") or report.get("html_report") or "").strip()
        records[(materialized_id, str(row.get("split", "")))] = {
            "metrics": metrics,
            "report_path": Path(report_path_text) if report_path_text else None,
        }
    return records


def profit_factor(values: Sequence[float]) -> float:
    gross_profit = sum(value for value in values if value > 0)
    gross_loss = sum(value for value in values if value < 0)
    return gross_profit / abs(gross_loss) if gross_loss < 0 else 0.0


def rolling_min(values: Sequence[float], window: int) -> float:
    if len(values) < window:
        return 0.0
    return float(pd.Series([float(value) for value in values]).rolling(window).sum().min())


def split_days(split: str) -> int:
    return 183 if split == "validation_is" else 131


def attribution_rows(frame: pd.DataFrame, materialized_id: str, package_id: str, split: str, bucket_type: str, bucket_column: str, report_path: Path) -> list[dict[str, Any]]:
    if frame.empty or bucket_column not in frame.columns:
        return []
    rows: list[dict[str, Any]] = []
    for bucket, group in frame.groupby(bucket_column, sort=True):
        profits = [float(value) for value in group["net_profit"].tolist()]
        net = sum(profits)
        rows.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "split": split,
                "bucket_type": bucket_type,
                "bucket": str(bucket),
                "trade_count": len(profits),
                "net_profit": net,
                "profit_factor": profit_factor(profits),
                "positive_bucket": "yes" if net > 0 else "no",
                "source_report_path": report_path.as_posix(),
            }
        )
    return rows


def curve_outputs(report_path: Path | None, materialized_id: str, package_id: str, split: str) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    frame = trade_frame(report_path) if report_path and path_exists(report_path) else pd.DataFrame()
    profits = [float(value) for value in frame["net_profit"].tolist()] if not frame.empty else []
    source_report_path = report_path.as_posix() if report_path else ""
    balance = 0.0
    peak = 0.0
    min_equity = 0.0
    underwater = 0
    for profit in profits:
        balance += profit
        peak = max(peak, balance)
        min_equity = min(min_equity, balance)
        if balance < peak:
            underwater += 1
    curve = {
        "materialized_branch_id": materialized_id,
        "package_id": package_id,
        "split": split,
        "trade_count": len(profits),
        "final_net": balance,
        "max_equity_peak": peak,
        "min_equity": min_equity,
        "underwater_ratio": underwater / len(profits) if profits else 0.0,
        "source_report_path": source_report_path,
    }
    pockets = []
    for window, threshold in ((20, -120.0), (50, -150.0)):
        worst = rolling_min(profits, window)
        pockets.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "split": split,
                "rolling_window": window,
                "worst_rolling_net": worst,
                "pocket_threshold": threshold,
                "pocket_label": "deep_local_pocket" if worst < threshold else "tolerable",
                "source_report_path": source_report_path,
            }
        )
    monthly = attribution_rows(frame, materialized_id, package_id, split, "month", "month", report_path) if report_path else []
    session = attribution_rows(frame, materialized_id, package_id, split, "session", "session", report_path) if report_path else []
    return curve, pockets, monthly, session


def positive_share(rows: Sequence[Mapping[str, Any]]) -> float:
    if not rows:
        return 0.0
    return sum(1 for row in rows if float(row["net_profit"]) > 0) / len(rows)


def min_net(rows: Sequence[Mapping[str, Any]]) -> float:
    if not rows:
        return 0.0
    return min(float(row["net_profit"]) for row in rows)


def salvage_value(materialized_id: str, scoreboard: Mapping[str, Any]) -> str:
    if float(scoreboard["oos_net_profit"]) > 0 and float(scoreboard["validation_net_profit"]) <= 0:
        return "OOS upside clue(표본외 상방 단서) but validation failed(검증 실패)"
    if float(scoreboard["validation_net_profit"]) > 0 and float(scoreboard["oos_net_profit"]) <= 0:
        return "validation payoff fit clue(검증 손익 적합 단서) but OOS generalization failed(표본외 일반화 실패)"
    if scoreboard["density_gate"] == "passed":
        return "density construction clue(밀도 구성 단서) only"
    return "failure memory(실패 기억)"


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str, str, str]:
    manifest = manifest_by_id()
    model_families = model_family_by_id()
    records = parse_records()
    if not records:
        raise RuntimeError(f"No actual routed total KPI records found in {SOURCE_KPI}")
    scoreboard_rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for materialized_id, manifest_row in manifest.items():
        package_id = manifest_row["package_id"]
        data: dict[str, dict[str, Any]] = {}
        for split in ("validation_is", "oos"):
            entry = records.get((materialized_id, split), {})
            metrics = entry.get("metrics", {})
            report_path = entry.get("report_path")
            curve, pockets, monthly, session = curve_outputs(report_path, materialized_id, package_id, split)
            monthly_rows.extend(monthly)
            session_rows.extend(session)
            curve_rows.append(curve)
            pocket_rows.extend(pockets)
            data[split] = {
                "net": safe_float(metrics.get("net_profit")),
                "pf": safe_float(metrics.get("profit_factor")),
                "trades": safe_float(metrics.get("trade_count")),
                "tpd": safe_float(metrics.get("trade_count")) / split_days(split),
                "dd": safe_float(metrics.get("max_drawdown_amount")),
                "recovery": safe_float(metrics.get("recovery_factor")),
                "expectancy": safe_float(metrics.get("expectancy")),
                "positive_month_share": positive_share(monthly),
                "worst_month_net": min_net(monthly),
                "worst_session_net": min_net(session),
                "r20": next(row["worst_rolling_net"] for row in pockets if row["rolling_window"] == 20),
                "r50": next(row["worst_rolling_net"] for row in pockets if row["rolling_window"] == 50),
                "underwater_ratio": curve["underwater_ratio"],
            }
        density_ok = 4.0 <= data["validation_is"]["tpd"] <= 10.0 and 4.0 <= data["oos"]["tpd"] <= 10.0
        profit_ok = data["validation_is"]["net"] > 150.0 and data["oos"]["net"] > 250.0
        efficiency_ok = (
            data["validation_is"]["pf"] >= 1.10
            and data["oos"]["pf"] >= 1.10
            and data["validation_is"]["recovery"] >= 1.0
            and data["oos"]["recovery"] >= 1.0
            and data["validation_is"]["expectancy"] > 0.0
            and data["oos"]["expectancy"] > 0.0
        )
        curve_ok = (
            data["validation_is"]["positive_month_share"] >= 0.60
            and data["oos"]["positive_month_share"] >= 0.60
            and data["validation_is"]["worst_month_net"] >= -90.0
            and data["oos"]["worst_month_net"] >= -90.0
            and data["validation_is"]["worst_session_net"] >= -120.0
            and data["oos"]["worst_session_net"] >= -120.0
            and data["validation_is"]["r20"] >= -120.0
            and data["oos"]["r20"] >= -120.0
            and data["validation_is"]["r50"] >= -150.0
            and data["oos"]["r50"] >= -150.0
            and data["validation_is"]["underwater_ratio"] <= 0.90
            and data["oos"]["underwater_ratio"] <= 0.90
        )
        reasons: list[str] = []
        if not density_ok:
            reasons.append("trade_density_outside_4_10")
        if not profit_ok:
            reasons.append("profit_scale_not_both_splits")
        if not efficiency_ok:
            reasons.append("efficiency_pf_recovery_expectancy_not_jointly_credible")
        if not curve_ok:
            reasons.append("curve_quality_month_session_or_local_pocket_fail")
        label = "adapter_candidate_ready" if not reasons else "payoff_weighted_edge_negative"
        scoreboard = {
            "materialized_branch_id": materialized_id,
            "package_id": package_id,
            "model_family": model_families.get(materialized_id, ""),
            "validation_net_profit": data["validation_is"]["net"],
            "validation_pf": data["validation_is"]["pf"],
            "validation_trade_count": data["validation_is"]["trades"],
            "validation_trades_per_day": data["validation_is"]["tpd"],
            "validation_dd": data["validation_is"]["dd"],
            "validation_recovery": data["validation_is"]["recovery"],
            "validation_expectancy": data["validation_is"]["expectancy"],
            "validation_positive_month_share": data["validation_is"]["positive_month_share"],
            "validation_worst_month_net": data["validation_is"]["worst_month_net"],
            "validation_worst_session_net": data["validation_is"]["worst_session_net"],
            "validation_worst_rolling_20_net": data["validation_is"]["r20"],
            "validation_worst_rolling_50_net": data["validation_is"]["r50"],
            "validation_underwater_ratio": data["validation_is"]["underwater_ratio"],
            "oos_net_profit": data["oos"]["net"],
            "oos_pf": data["oos"]["pf"],
            "oos_trade_count": data["oos"]["trades"],
            "oos_trades_per_day": data["oos"]["tpd"],
            "oos_dd": data["oos"]["dd"],
            "oos_recovery": data["oos"]["recovery"],
            "oos_expectancy": data["oos"]["expectancy"],
            "oos_positive_month_share": data["oos"]["positive_month_share"],
            "oos_worst_month_net": data["oos"]["worst_month_net"],
            "oos_worst_session_net": data["oos"]["worst_session_net"],
            "oos_worst_rolling_20_net": data["oos"]["r20"],
            "oos_worst_rolling_50_net": data["oos"]["r50"],
            "oos_underwater_ratio": data["oos"]["underwater_ratio"],
            "density_gate": "passed" if density_ok else "failed",
            "profit_scale_gate": "passed" if profit_ok else "failed",
            "efficiency_gate": "passed" if efficiency_ok else "failed",
            "curve_quality_gate": "passed" if curve_ok else "failed",
            "review_label": label,
            "failure_reasons": "|".join(reasons) if reasons else "none",
            "selected_candidate": "none" if reasons else package_id,
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        scoreboard_rows.append(scoreboard)
        if reasons:
            failure_rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "package_id": package_id,
                    "failure_type": label,
                    "failure_reasons": "|".join(reasons),
                    "salvage_value": salvage_value(materialized_id, scoreboard),
                    "reopen_condition": "Only reopen through walk-forward payoff generalization or a new label/risk objective, not threshold repair.",
                    "claim_boundary": BOUNDARY,
                }
            )
    survivors = [row for row in scoreboard_rows if row["review_label"] == "adapter_candidate_ready"]
    if survivors:
        best = sorted(survivors, key=lambda row: (float(row["validation_net_profit"]) + float(row["oos_net_profit"])), reverse=True)[0]
        target_stage = STAGE291_ADAPTER_ID
        status = STATUS_SELECTED
        judgment = JUDGMENT_SELECTED
        next_action = "run291A_build_adapter_package_for_stage290_survivor"
        queue_rows = [
            {
                "seed_id": "stage291_adapter_package_for_stage290_survivor",
                "source_materialized_branch_id": best["materialized_branch_id"],
                "source_package_id": best["package_id"],
                "seed_role": "selected_candidate_for_adapter_package",
                "fresh_stage291_question": "Can the selected payoff-weighted survivor be represented as an Adapter package with traceable feature order and runtime handoff?",
                "required_change": "build Adapter package and freeze model/feature/decision/risk identity",
                "forbidden_repair_loop": "Do not change the selected decision surface inside Adapter packaging.",
                "prior_stage_refs": rel(SCOREBOARD),
                "claim_boundary": BOUNDARY,
            }
        ]
    else:
        target_stage = STAGE291_FAILURE_ID
        status = STATUS_NO_CANDIDATE
        judgment = JUDGMENT_NO_CANDIDATE
        next_action = "run291A_design_walk_forward_payoff_generalization_rebuild_packet"
        prior_refs = "|".join([rel(SCOREBOARD), rel(LOCAL_POCKETS), rel(FAILURE_MEMORY), rel(SOURCE_MODEL_SCOREBOARD)])
        queue_rows = [
            {
                "seed_id": "stage291_wfo_payoff_generalization",
                "source_materialized_branch_id": "stage290_all_branches",
                "source_package_id": "none",
                "seed_role": "validation_fit_or_oos_collapse_memory",
                "fresh_stage291_question": "Can walk-forward anchored payoff modeling avoid validation-fit and OOS collapse while preserving 4-10 trades/day?",
                "required_change": "walk-forward threshold/model selection with OOS-like holdout inside construction",
                "forbidden_repair_loop": "Do not retune the same Stage290 thresholds on the same validation window.",
                "prior_stage_refs": prior_refs,
                "claim_boundary": BOUNDARY,
            },
            {
                "seed_id": "stage291_direction_side_relabel",
                "source_materialized_branch_id": "stage290_inverse_orientation_commonality",
                "source_package_id": "none",
                "seed_role": "all_stage290_models_chose_inverse_orientation",
                "fresh_stage291_question": "Does the universal inverse orientation mean the label horizon or side payoff label is misaligned?",
                "required_change": "direction-specific payoff labels or side-separated model objective",
                "forbidden_repair_loop": "Do not just invert every model and lower thresholds.",
                "prior_stage_refs": prior_refs,
                "claim_boundary": BOUNDARY,
            },
            {
                "seed_id": "stage291_cost_curve_native_objective",
                "source_materialized_branch_id": "stage290_curve_pocket_failures",
                "source_package_id": "none",
                "seed_role": "curve_smoothness_not_solved_by_posthoc_threshold",
                "fresh_stage291_question": "Can cost and rolling-pocket penalties be native to the objective before signal materialization?",
                "required_change": "native cost/curve objective or trade-level simulator in candidate construction",
                "forbidden_repair_loop": "Do not rely on post-hoc curve rejection after MT5 only.",
                "prior_stage_refs": prior_refs,
                "claim_boundary": BOUNDARY,
            },
        ]
    return scoreboard_rows, monthly_rows, session_rows, curve_rows, pocket_rows, failure_rows, queue_rows, target_stage, status, judgment, next_action


def ensure_stage291(target_stage: str, status: str, queue_rows: Sequence[Mapping[str, Any]]) -> None:
    stage = ROOT / "stages" / target_stage
    for sub in ("00_spec", "01_inputs", "03_reviews", "04_selected"):
        io_path(stage / sub).mkdir(parents=True, exist_ok=True)
    if target_stage == STAGE291_ADAPTER_ID:
        big_question = "Can the Stage290 survivor be converted into a traceable Adapter package without changing its decision surface?"
        next_action = "run291A_build_adapter_package_for_stage290_survivor"
        stage_status = "opened_adapter_package_for_stage290_survivor"
    else:
        big_question = "Can walk-forward payoff generalization, side relabeling, or native cost/curve objectives create a stronger ONNX-worthy candidate seed?"
        next_action = "run291A_design_walk_forward_payoff_generalization_rebuild_packet"
        stage_status = "opened_walk_forward_payoff_generalization_rebuild"
    write_md(
        stage / "00_spec" / "stage_brief.md",
        f"""# Stage291 {target_stage.split('__', 1)[1].replace('_', ' ').title()}(291단계)

- canonical_stage_id(정식 단계 ID): `{target_stage}`
- big_question(큰 질문): {big_question}
- source_stage(원천 단계): `{STAGE290_ID}`
- seed_count(씨앗 수): `{len(queue_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): Stage290(290단계)의 결과를 같은 threshold repair(임계값 수선)로 늘리지 않고 새 질문으로 넘긴다.
""",
    )
    write_csv(stage / "01_inputs" / "stage291_seed_queue.csv", QUEUE_COLUMNS, queue_rows)
    write_md(
        stage / "01_inputs" / "input_refs.md",
        f"""# Stage291 Input Refs(291단계 입력 참조)

- `{rel(SCOREBOARD)}`
- `{rel(FAILURE_MEMORY)}`
- `{rel(LOCAL_POCKETS)}`
- `{rel(SOURCE_MODEL_SCOREBOARD)}`

Effect(효과): Stage291(291단계)은 Stage290(290단계)의 MT5 evidence(MT5 근거)를 새 질문의 입력으로만 쓴다.
""",
    )
    write_md(stage / "03_reviews" / "review_index.md", "# Stage291 Review Index(291단계 검토 색인)\n")
    write_csv(
        stage / "03_reviews" / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage291_opened_from_run290C",
                "stage_id": target_stage,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage291_seed_queue",
                "status": stage_status,
                "judgment": "stage_opened_from_stage290_review",
                "evidence_boundary": "planning_from_stage290_evidence",
                "report_path": rel(REPORT),
                "notes": f"seed_count={len(queue_rows)};next_action={next_action}",
            }
        ],
    )
    write_md(
        stage / "04_selected" / "selection_status.md",
        f"""# Stage291 Selection Status(291단계 선택 상태)

- stage_status(단계 상태): `{stage_status}`
- current_packet(현재 작업 묶음): `{target_stage}_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE290_ID}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- input_refs(입력 참조): `{rel(stage / "01_inputs" / "input_refs.md")}`
""",
    )


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], status: str, judgment: str, next_action: str) -> str:
    lines = []
    for row in scoreboard_rows:
        lines.append(
            f"- `{row['package_id']}`: validation(검증) net `{float(row['validation_net_profit']):.2f}`, PF `{float(row['validation_pf']):.2f}`, "
            f"`{float(row['validation_trades_per_day']):.2f}` trades/day(일 거래); OOS(표본외) net `{float(row['oos_net_profit']):.2f}`, "
            f"PF `{float(row['oos_pf']):.2f}`, `{float(row['oos_trades_per_day']):.2f}` trades/day(일 거래); "
            f"gates(게이트) `{row['density_gate']}/{row['profit_scale_gate']}/{row['efficiency_gate']}/{row['curve_quality_gate']}`."
        )
    return f"""# run290C Payoff Weighted Edge Review(290C 손익가중 엣지 검토)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- selected_candidate(선택 후보): `{next((row['package_id'] for row in scoreboard_rows if row['review_label'] == 'adapter_candidate_ready'), 'none')}`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- stage291_seed_count(291단계 씨앗 수): `{len(queue_rows)}`
- next_action(다음 행동): `{next_action}`

## Scoreboard(점수판)

{chr(10).join(lines)}

## Decision(결정)

Stage290(290단계)는 MT5 runtime probe(MT5 런타임 탐침)와 curve/time-slice/trade-quality(곡선/시간구간/거래품질) 검토 전에는 후보를 부르지 않았다. 위 gate(게이트)를 모두 통과한 경우에만 Adapter(어댑터) 단계로 넘긴다.

## Boundary(경계)

`{BOUNDARY}`
"""


def write_outputs(
    scoreboard_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    pocket_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    target_stage: str,
    status: str,
    judgment: str,
    next_action: str,
    created_at: str,
) -> list[Path]:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(MONTHLY, ATTRIBUTION_COLUMNS, monthly_rows)
    write_csv(SESSION, ATTRIBUTION_COLUMNS, session_rows)
    write_csv(CURVE, CURVE_COLUMNS, curve_rows)
    write_csv(LOCAL_POCKETS, POCKET_COLUMNS, pocket_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv(SURVIVOR_QUEUE, QUEUE_COLUMNS, queue_rows)
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"scoreboard={rel(SCOREBOARD)};mt5_kpi={rel(SOURCE_KPI)};failure_rows={len(failure_rows)}",
                "evidence_missing": "Adapter package;ONNX parity;runtime reproduction",
                "judgment_label": judgment,
                "judgment_class": "candidate_selection_review",
                "claim_boundary": BOUNDARY,
                "next_condition": next_action,
                "user_explanation_hook": "MT5 실성능과 곡선까지 통과해야만 후보다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "mt5_external_evidence(외부 MT5 근거)",
                "status": "passed",
                "evidence_path": rel(SOURCE_KPI),
                "effect": "실제 Strategy Tester(전략 테스터) KPI로 검토했다.",
            },
            {
                "gate_name": "curve_trade_quality_review(곡선/거래품질 검토)",
                "status": "passed",
                "evidence_path": rel(SCOREBOARD),
                "effect": "수익, PF, DD, recovery(회복), expectancy(기대값), 월/세션/로컬 포켓을 같이 봤다.",
            },
            {
                "gate_name": "candidate_claim_boundary(후보 주장 경계)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "근거가 모자라면 Adapter/ONNX로 넘기지 않는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, queue_rows, status, judgment, next_action))
    write_md(
        DECISION,
        f"""# Stage290 Payoff Weighted Edge Review Decision(290단계 손익가중 엣지 검토 결정)

- source_run(원천 실행): `{SOURCE_RUN_ID}`
- review_run(검토 실행): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- target_stage(대상 단계): `{target_stage}`
- next_action(다음 행동): `{next_action}`

Effect(효과): Stage290(290단계)를 더 늘리지 않고, 후보가 있으면 Adapter(어댑터)로, 없으면 fresh thesis(새 논제) Stage291(291단계)로 넘긴다.
""",
    )
    final = [SCOREBOARD, MONTHLY, SESSION, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, SURVIVOR_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, DECISION]
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": PRODUCER.as_posix(),
            "source_artifacts": [rel(SOURCE_MANIFEST), rel(SOURCE_MODEL_SCOREBOARD), rel(SOURCE_KPI), rel(SOURCE_EXECUTION), rel(SOURCE_RUN_MANIFEST)],
            "produced_artifacts": [rel(path) for path in final if path_exists(path)],
            "claim_boundary": BOUNDARY,
        },
    )
    final.append(LINEAGE)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE290_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": status,
            "judgment": judgment,
            "created_at_utc": created_at,
            "scoreboard_rows": len(scoreboard_rows),
            "failure_rows": len(failure_rows),
            "target_stage": target_stage,
            "next_action": next_action,
            "selected_candidate": next((row["package_id"] for row in scoreboard_rows if row["review_label"] == "adapter_candidate_ready"), "none"),
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
            "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final if path_exists(path)},
        },
    )
    final.append(RUN_MANIFEST)
    return [path for path in final if path_exists(path)]


def update_docs(created_at: str, artifacts: Sequence[Path], scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], target_stage: str, status: str, judgment: str, next_action: str) -> None:
    selected_candidate = next((row["package_id"] for row in scoreboard_rows if row["review_label"] == "adapter_candidate_ready"), "none")
    upsert_csv(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE290_ID,
                "lane": "payoff_weighted_edge_model_review",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "notes": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};target_stage={target_stage};next_action={next_action}",
            }
        ],
        key="run_id",
    )
    upsert_csv(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE290_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "payoff_weighted_edge_model_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "candidate_selection_review",
                "scoreboard_lane": "payoff_weighted_edge_model",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)}",
                "guardrail_kpi": f"selected_candidate={selected_candidate};onnx_readiness=not_claimed",
                "external_verification_status": "completed_run290B_mt5_probe",
                "notes": f"target_stage={target_stage};next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv(
        STAGE_LEDGER290,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__review",
                "stage_id": STAGE290_ID,
                "run_id": RUN_ID,
                "view": "payoff_weighted_edge_model_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "payoff_weighted_edge_scoreboard",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "candidate_review_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"target_stage={target_stage};selected_candidate={selected_candidate}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage290_payoff_weighted_edge_review_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE290_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run290C payoff weighted edge review",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    ensure_stage291(target_stage, status, queue_rows)

    selected = io_path(SELECTED290).read_text(encoding="utf-8-sig") if path_exists(SELECTED290) else ""
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- selected_candidate(선택 후보):", f"- selected_candidate(선택 후보): `{selected_candidate}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selected = append_once(selected, "run290C_report", f"- run290C_report(290C 보고): `{rel(REPORT)}`")
    selected = append_once(selected, "run290C_scoreboard", f"- run290C_scoreboard(290C 점수판): `{rel(SCOREBOARD)}`")
    write_md(SELECTED290, selected)

    review_index = io_path(REVIEW_INDEX290).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX290) else "# Stage290 Review Index(290단계 검토 색인)\n"
    review_index = append_once(review_index, "run290C_report", f"- run290C_report(290C 보고): `{rel(REPORT)}`\n- run290C_scoreboard(290C 점수판): `{rel(SCOREBOARD)}`")
    write_md(REVIEW_INDEX290, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", f"- current_packet(현재 작업 묶음): `{target_stage}_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{target_stage}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE290_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", f"- target_surface(목표 표면): `{selected_candidate}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_once(
        current,
        "run290C_summary",
        f"- run290C_summary(290C 요약): Stage290(290단계) payoff-weighted edge model(손익가중 엣지 모델)을 MT5 KPI/곡선/월/세션으로 검토했다. Effect(효과): selected_candidate(선택 후보)는 `{selected_candidate}`이고, 다음 단계는 `{target_stage}`다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {target_stage}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage290(290단계) run290C(290C 실행) payoff-weighted edge review(손익가중 엣지 검토) `{RUN_ID}`. "
        f"Effect(효과): scoreboard(점수판) `{len(scoreboard_rows)}`행, failure memory(실패 기억) `{len(failure_rows)}`행을 만들고 selected candidate(선택 후보) `{selected_candidate}`로 `{target_stage}`를 열었다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run290C Payoff-weighted edge review(290C 손익가중 엣지 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        f"- effect(효과): Stage290(290단계)을 검토하고 `{target_stage}`를 열었다.\n"
        f"- selected_candidate(선택 후보): `{selected_candidate}`\n"
        f"- boundary(경계): ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    if "NEG-ST290-PAYOFF-WEIGHTED-EDGE" not in (io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "") and selected_candidate == "none":
        negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register\n"
        negative = negative.rstrip() + f"\n\n| `NEG-ST290-PAYOFF-WEIGHTED-EDGE` | `IDEA-ST290-PAYOFF-WEIGHTED-EDGE-MODEL` | payoff-weighted edge model(손익가중 엣지 모델)이 ONNX-worthy candidate(온엑스화 가치 후보)로 이어질 수 있다 | run290C(290C 실행)에서 MT5 KPI/곡선/거래품질 gate(게이트)를 통과한 candidate package(후보 패키지)가 없었다 | inverse orientation(역방향) 공통성과 density construction(밀도 구성)은 Stage291(291단계) seed clue(씨앗 단서)로 보존한다 | walk-forward payoff generalization(워크포워드 손익 일반화), side relabel(방향 재라벨), native cost/curve objective(비용/곡선 내장 목적함수)가 생길 때 |\n"
        write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    created_at = utc_now()
    outputs = build_outputs()
    scoreboard_rows, monthly_rows, session_rows, curve_rows, pocket_rows, failure_rows, queue_rows, target_stage, status, judgment, next_action = outputs
    artifacts = write_outputs(scoreboard_rows, monthly_rows, session_rows, curve_rows, pocket_rows, failure_rows, queue_rows, target_stage, status, judgment, next_action, created_at)
    update_docs(created_at, artifacts, scoreboard_rows, failure_rows, queue_rows, target_stage, status, judgment, next_action)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "scoreboard_rows": len(scoreboard_rows),
                "failure_rows": len(failure_rows),
                "selected_candidate": next((row["package_id"] for row in scoreboard_rows if row["review_label"] == "adapter_candidate_ready"), "none"),
                "target_stage": target_stage,
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": next_action,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
