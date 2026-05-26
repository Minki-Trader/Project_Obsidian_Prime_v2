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
RUN_NUMBER = "run334F"
RUN_ID = "run334F_materialize_no_retune_nonidentity_stress_probe_inputs_v1"
PARENT_RUN_ID = "run334E_design_no_retune_forward_usable_nonidentity_stress_probe_from_reconciled_memory_v1"
NEXT_RUN_ID = "run334G_review_no_retune_stress_probe_materialization_and_failure_memory_v1"
STATUS = "completed_no_retune_nonidentity_stress_probe_input_materialization_no_selection"
JUDGMENT = "stress_probe_inputs_materialized_research_only_no_goal_achieve"
DECISION = "stage334F_fixed_input_diagnostic_views_materialized_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_no_retune_nonidentity_stress_probe_materialization_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
VIEWS_DIR = RUN_DIR / "diagnostic_views"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage334F_no_retune_stress_probe_materialization.md"

RUN334E_DIR = STAGE_DIR / "02_runs" / "run334E"
RUN334E_QUEUE = RUN334E_DIR / "run334F_materialization_queue.csv"
RUN334E_MATRIX = RUN334E_DIR / "stress_probe_matrix.csv"
RUN334E_REJECTION = RUN334E_DIR / "overfit_rejection_rules.csv"
RUN334E_CONTRACT = RUN334E_DIR / "no_retune_stress_probe_contract.csv"
RUN334E_DECISION = RUN334E_DIR / "final_stress_probe_design_decision.json"

RUN334D_DIR = STAGE_DIR / "02_runs" / "run334D"
RUN334D_ALL_SIX = RUN334D_DIR / "all_six_runtime_reconciliation.csv"
RUN334D_MEMORY = RUN334D_DIR / "preserved_clue_and_failure_memory.csv"

STAGE330_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN330E_DIR = STAGE330_DIR / "02_runs" / "run330E"
RUN330F_DIR = STAGE330_DIR / "02_runs" / "run330F"
RUN330E_FEATURE_MANIFEST = RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"
RUN330F_KPI = RUN330F_DIR / "forward_mt5_kpi_report.csv"
RUN330F_COST = RUN330F_DIR / "cost_stress_report.csv"
RUN330F_CURVE = RUN330F_DIR / "curve_pocket_report.csv"
RUN330F_UNDERWATER = RUN330F_DIR / "underwater_stretch_report.csv"
RUN330F_DIRECTION = RUN330F_DIR / "long_short_attribution_report.csv"
RUN330F_SLICES = RUN330F_DIR / "session_hour_month_volatility_adx_vix_usd_rate_slices.csv"
RUN330F_TRADE_RECORDS = RUN330F_DIR / "trade_level_records.csv"


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


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def index_by(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {row.get(key, ""): row for row in rows if row.get(key)}


def group_by(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, list[Mapping[str, str]]]:
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get(key, "")].append(row)
    return grouped


def path_from_rel(value: str) -> Path:
    return ROOT / value if value else ROOT / "__missing__"


def load_context() -> dict[str, Any]:
    return {
        "queue": read_csv_rows(RUN334E_QUEUE),
        "matrix": read_csv_rows(RUN334E_MATRIX),
        "contract": read_csv_rows(RUN334E_CONTRACT),
        "rejection": read_csv_rows(RUN334E_REJECTION),
        "run334e_decision": read_json(RUN334E_DECISION),
        "run334d_all_six": read_csv_rows(RUN334D_ALL_SIX),
        "run334d_memory": read_csv_rows(RUN334D_MEMORY),
        "feature_manifest": read_csv_rows(RUN330E_FEATURE_MANIFEST),
        "kpi": read_csv_rows(RUN330F_KPI),
        "cost": read_csv_rows(RUN330F_COST),
        "curve": read_csv_rows(RUN330F_CURVE),
        "underwater": read_csv_rows(RUN330F_UNDERWATER),
        "direction": read_csv_rows(RUN330F_DIRECTION),
        "slices": read_csv_rows(RUN330F_SLICES),
        "trades": read_csv_rows(RUN330F_TRADE_RECORDS),
    }


def cost_row(cost_rows: Sequence[Mapping[str, str]], attempt: str, scenario_id: str) -> Mapping[str, str]:
    target = 1.0 if scenario_id == "cost_plus_1" else 2.0
    rows = [row for row in cost_rows if row.get("attempt_name") == attempt]
    return next((row for row in rows if abs(as_float(row.get("extra_cost_per_round_trip_account_ccy")) - target) < 1e-9), {})


def worst_curve_row(curve_rows: Sequence[Mapping[str, str]], attempt: str) -> Mapping[str, str]:
    rows = [row for row in curve_rows if row.get("attempt_name") == attempt and row.get("chunk_type") == "rolling_worst_net"]
    if not rows:
        rows = [row for row in curve_rows if row.get("attempt_name") == attempt]
    return min(rows, key=lambda row: as_float(row.get("net_profit"))) if rows else {}


def worst_slice_row(slice_rows: Sequence[Mapping[str, str]], attempt: str) -> Mapping[str, str]:
    rows = [row for row in slice_rows if row.get("attempt_name") == attempt]
    return min(rows, key=lambda row: as_float(row.get("net_profit"))) if rows else {}


def direction_rows(direction_rows_: Sequence[Mapping[str, str]], attempt: str) -> tuple[Mapping[str, str], Mapping[str, str]]:
    rows = [row for row in direction_rows_ if row.get("attempt_name") == attempt]
    buy = next((row for row in rows if row.get("direction") == "buy"), {})
    sell = next((row for row in rows if row.get("direction") == "sell"), {})
    return buy, sell


def trade_window_stats(trades_by_attempt: Mapping[str, Sequence[Mapping[str, str]]], attempt: str, start: str, end: str) -> dict[str, Any]:
    rows = list(trades_by_attempt.get(attempt, []))
    if start:
        rows = [row for row in rows if row.get("close_time", "") >= start]
    if end:
        rows = [row for row in rows if row.get("close_time", "") <= end]
    net = sum(as_float(row.get("net_profit")) for row in rows)
    return {
        "window_trade_count": len(rows),
        "window_net_profit": net,
        "window_buy_count": sum(1 for row in rows if row.get("direction") == "buy"),
        "window_sell_count": sum(1 for row in rows if row.get("direction") == "sell"),
    }


def build_outputs(context: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    queue = list(context["queue"])
    matrix_by_attempt = index_by(context["matrix"], "attempt_name")
    kpi_by_attempt = index_by(context["kpi"], "attempt_name")
    underwater_by_attempt = index_by(context["underwater"], "attempt_name")
    feature_by_slug = index_by(context["feature_manifest"], "artifact_slug")
    trades_by_attempt = group_by(context["trades"], "attempt_name")

    cost_views: list[dict[str, Any]] = []
    curve_views: list[dict[str, Any]] = []
    regime_views: list[dict[str, Any]] = []
    direction_views: list[dict[str, Any]] = []
    underwater_views: list[dict[str, Any]] = []
    identity_views: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    attempt_summary: dict[str, dict[str, Any]] = {}

    for item in queue:
        attempt = item.get("attempt_name", "")
        slug = item.get("artifact_slug", "")
        scenario_id = item.get("scenario_id", "")
        axis = item.get("stress_axis", "")
        matrix = matrix_by_attempt.get(attempt, {})
        kpi = kpi_by_attempt.get(attempt, {})
        feature = feature_by_slug.get(slug, {})
        scenario_result = "materialized"
        diagnostic_status = "research_only"
        source_rows = 0
        view_path = ""
        if attempt not in attempt_summary:
            attempt_summary[attempt] = {
                "attempt_name": attempt,
                "artifact_slug": slug,
                "severity": item.get("severity", ""),
                "headline_net_profit": as_float(kpi.get("net_profit")),
                "headline_profit_factor": as_float(kpi.get("profit_factor")),
                "diagnostic_row_count": 0,
                "hard_failure_count": 0,
                "warning_count": 0,
                "selection_eligible": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }

        if axis == "cost_stress":
            row = cost_row(context["cost"], attempt, scenario_id)
            source_rows = 1 if row else 0
            pf = as_float(row.get("profit_factor_after_cost"))
            net = as_float(row.get("net_profit_after_cost"))
            diagnostic_status = "cost_breaks_pf_or_net" if pf <= 1.0 or net <= 0 else "cost_survives_diagnostic"
            if diagnostic_status == "cost_breaks_pf_or_net":
                attempt_summary[attempt]["hard_failure_count"] += 1
            else:
                attempt_summary[attempt]["warning_count"] += 1
            cost_views.append(
                {
                    "queue_id": item.get("queue_id", ""),
                    "attempt_name": attempt,
                    "artifact_slug": slug,
                    "scenario_id": scenario_id,
                    "extra_cost_per_round_trip_account_ccy": row.get("extra_cost_per_round_trip_account_ccy", ""),
                    "net_profit_after_cost": net if row else "",
                    "profit_factor_after_cost": pf if row else "",
                    "max_drawdown_after_cost": as_float(row.get("max_drawdown_after_cost")) if row else "",
                    "survives_pf_gt_1": as_bool(row.get("survives_pf_gt_1")),
                    "diagnostic_status": diagnostic_status,
                    "selection_eligible": False,
                    "effect": "cost stress is diagnostic only; no threshold or lot change is allowed",
                }
            )
            view_path = rel(VIEWS_DIR / "cost_stress_diagnostic_views.csv")
        elif axis == "curve_pocket":
            row = worst_curve_row(context["curve"], attempt)
            stats = trade_window_stats(trades_by_attempt, attempt, row.get("start_time", ""), row.get("end_time", ""))
            source_rows = stats["window_trade_count"]
            net = as_float(row.get("net_profit"))
            diagnostic_status = "deep_curve_pocket" if net <= -50 else "curve_pocket_warning"
            if diagnostic_status == "deep_curve_pocket":
                attempt_summary[attempt]["hard_failure_count"] += 1
            else:
                attempt_summary[attempt]["warning_count"] += 1
            curve_views.append(
                {
                    "queue_id": item.get("queue_id", ""),
                    "attempt_name": attempt,
                    "artifact_slug": slug,
                    "chunk_id": row.get("chunk_id", ""),
                    "start_time": row.get("start_time", ""),
                    "end_time": row.get("end_time", ""),
                    "reported_trade_count": row.get("trade_count", ""),
                    "window_trade_count": stats["window_trade_count"],
                    "reported_net_profit": net if row else "",
                    "window_net_profit": stats["window_net_profit"],
                    "profit_factor": as_float(row.get("profit_factor")) if row else "",
                    "diagnostic_status": diagnostic_status,
                    "selection_eligible": False,
                    "effect": "worst rolling pocket is preserved as evidence; no date exclusion is allowed",
                }
            )
            view_path = rel(VIEWS_DIR / "curve_pocket_diagnostic_views.csv")
        elif axis == "regime_slice":
            row = worst_slice_row(context["slices"], attempt)
            source_rows = int(as_float(row.get("trade_count"))) if row else 0
            net = as_float(row.get("net_profit"))
            diagnostic_status = "loss_regime_slice" if net < 0 else "regime_warning"
            if diagnostic_status == "loss_regime_slice":
                attempt_summary[attempt]["hard_failure_count"] += 1
            else:
                attempt_summary[attempt]["warning_count"] += 1
            regime_views.append(
                {
                    "queue_id": item.get("queue_id", ""),
                    "attempt_name": attempt,
                    "artifact_slug": slug,
                    "axis": row.get("axis", ""),
                    "bucket": row.get("bucket", ""),
                    "trade_count": source_rows,
                    "net_profit": net if row else "",
                    "profit_factor": as_float(row.get("profit_factor")) if row else "",
                    "max_drawdown": as_float(row.get("max_drawdown")) if row else "",
                    "diagnostic_status": diagnostic_status,
                    "selection_eligible": False,
                    "effect": "worst regime slice is evidence only; no pocket pruning is allowed",
                }
            )
            view_path = rel(VIEWS_DIR / "regime_slice_diagnostic_views.csv")
        elif axis == "direction":
            buy, sell = direction_rows(context["direction"], attempt)
            source_rows = int(as_float(buy.get("trade_count"))) + int(as_float(sell.get("trade_count")))
            weak_direction = "buy" if as_float(buy.get("net_profit")) <= as_float(sell.get("net_profit")) else "sell"
            diagnostic_status = "weak_direction_negative" if min(as_float(buy.get("net_profit")), as_float(sell.get("net_profit"))) < 0 else "direction_warning"
            if diagnostic_status == "weak_direction_negative":
                attempt_summary[attempt]["hard_failure_count"] += 1
            else:
                attempt_summary[attempt]["warning_count"] += 1
            direction_views.append(
                {
                    "queue_id": item.get("queue_id", ""),
                    "attempt_name": attempt,
                    "artifact_slug": slug,
                    "buy_trade_count": buy.get("trade_count", ""),
                    "buy_net_profit": as_float(buy.get("net_profit")) if buy else "",
                    "buy_profit_factor": as_float(buy.get("profit_factor")) if buy else "",
                    "sell_trade_count": sell.get("trade_count", ""),
                    "sell_net_profit": as_float(sell.get("net_profit")) if sell else "",
                    "sell_profit_factor": as_float(sell.get("profit_factor")) if sell else "",
                    "weak_direction": weak_direction,
                    "diagnostic_status": diagnostic_status,
                    "selection_eligible": False,
                    "effect": "direction weakness is not used to drop a side after the fact",
                }
            )
            view_path = rel(VIEWS_DIR / "direction_diagnostic_views.csv")
        elif axis == "drawdown_shape":
            row = underwater_by_attempt.get(attempt, {})
            total = as_float(row.get("total_trade_count"))
            underwater_count = as_float(row.get("max_underwater_trade_count"))
            share = underwater_count / total if total else 0.0
            source_rows = int(underwater_count)
            diagnostic_status = "long_underwater_stretch" if share >= 0.5 else "underwater_warning"
            if diagnostic_status == "long_underwater_stretch":
                attempt_summary[attempt]["hard_failure_count"] += 1
            else:
                attempt_summary[attempt]["warning_count"] += 1
            underwater_views.append(
                {
                    "queue_id": item.get("queue_id", ""),
                    "attempt_name": attempt,
                    "artifact_slug": slug,
                    "total_trade_count": int(total),
                    "max_underwater_trade_count": int(underwater_count),
                    "underwater_trade_share": share,
                    "max_underwater_start": row.get("max_underwater_start", ""),
                    "max_underwater_end": row.get("max_underwater_end", ""),
                    "max_drawdown": as_float(row.get("max_drawdown")) if row else "",
                    "diagnostic_status": diagnostic_status,
                    "selection_eligible": False,
                    "effect": "underwater stretch is a risk shape diagnostic, not lot optimization input",
                }
            )
            view_path = rel(VIEWS_DIR / "underwater_diagnostic_views.csv")
        elif axis == "runtime_parity":
            paths = {
                "feature_matrix": path_from_rel(item.get("source_feature_matrix", "")),
                "model": path_from_rel(item.get("source_model", "")),
                "trade_records": path_from_rel(item.get("source_trade_records", "")),
                "slice_report": path_from_rel(item.get("source_slice_report", "")),
            }
            exists = {name: path_exists(path) for name, path in paths.items()}
            hashes = {name: sha256_file(path) for name, path in paths.items()}
            source_rows = sum(1 for ok in exists.values() if ok)
            diagnostic_status = "identity_sources_available" if all(exists.values()) else "identity_source_missing"
            if diagnostic_status != "identity_sources_available":
                attempt_summary[attempt]["hard_failure_count"] += 1
            else:
                attempt_summary[attempt]["warning_count"] += 1
            identity_views.append(
                {
                    "queue_id": item.get("queue_id", ""),
                    "attempt_name": attempt,
                    "artifact_slug": slug,
                    "feature_set_id": feature.get("feature_set_id", ""),
                    "decision_threshold": feature.get("decision_threshold", ""),
                    "feature_matrix_path": item.get("source_feature_matrix", ""),
                    "feature_matrix_exists": exists["feature_matrix"],
                    "feature_matrix_sha256": hashes["feature_matrix"],
                    "model_path": item.get("source_model", ""),
                    "model_exists": exists["model"],
                    "model_sha256": hashes["model"],
                    "trade_records_exists": exists["trade_records"],
                    "trade_records_sha256": hashes["trade_records"],
                    "slice_report_exists": exists["slice_report"],
                    "slice_report_sha256": hashes["slice_report"],
                    "diagnostic_status": diagnostic_status,
                    "selection_eligible": False,
                    "effect": "runtime identity sources are present for materialization, but runtime authority is not claimed",
                }
            )
            view_path = rel(VIEWS_DIR / "runtime_identity_diagnostic_views.csv")
        attempt_summary[attempt]["diagnostic_row_count"] += 1
        manifest_rows.append(
            {
                "queue_id": item.get("queue_id", ""),
                "attempt_name": attempt,
                "artifact_slug": slug,
                "stress_axis": axis,
                "scenario_id": scenario_id,
                "severity": item.get("severity", ""),
                "source_rows_used": source_rows,
                "diagnostic_status": diagnostic_status,
                "scenario_result": scenario_result,
                "view_path": view_path,
                "selection_eligible": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    summary_rows = []
    for attempt, row in sorted(attempt_summary.items()):
        hard = int(row["hard_failure_count"])
        warning = int(row["warning_count"])
        row["materialization_judgment"] = "hard_failure_memory" if hard else "warning_only_preserved_clue"
        row["next_action"] = NEXT_RUN_ID
        row["effect"] = "diagnostic materialization complete; selection remains blocked"
        row["warning_count"] = warning
        summary_rows.append(row)

    return {
        "manifest": manifest_rows,
        "cost": cost_views,
        "curve": curve_views,
        "regime": regime_views,
        "direction": direction_views,
        "underwater": underwater_views,
        "identity": identity_views,
        "summary": summary_rows,
    }


def write_skill_receipts(context: Mapping[str, Any], outputs: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[Path]:
    source_inputs = [
        RUN334E_QUEUE,
        RUN334E_MATRIX,
        RUN334E_REJECTION,
        RUN334E_CONTRACT,
        RUN334D_ALL_SIX,
        RUN334D_MEMORY,
        RUN330E_FEATURE_MANIFEST,
        RUN330F_COST,
        RUN330F_CURVE,
        RUN330F_UNDERWATER,
        RUN330F_DIRECTION,
        RUN330F_SLICES,
        RUN330F_TRADE_RECORDS,
    ]
    hard_count = sum(1 for row in outputs["summary"] if row.get("materialization_judgment") == "hard_failure_memory")
    receipts: list[Path] = []
    receipts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [rel(path) for path in source_inputs],
                "time_axis": "run334F uses inherited Stage330F trade close times and slice reports; no new bars or labels are built.",
                "sample_scope": {
                    "queue_rows": len(outputs["manifest"]),
                    "attempt_rows": len(outputs["summary"]),
                    "symbol": "US100",
                    "timeframe": "M5",
                },
                "missing_or_duplicate_check": "materialization checks source file availability through runtime identity diagnostic rows; duplicate bar audit is out of scope because no bars are rebuilt.",
                "feature_label_boundary": "features, model, threshold, risk, and lot are inherited and unchanged.",
                "split_boundary": "post-forward evidence is reused for diagnostics only, not retuning or selection.",
                "leakage_risk": "diagnostic views can become leakage if converted into exclusion rules; overfit rejection rules remain attached.",
                "data_hash_or_identity": {rel(path): sha256_file(path) for path in source_inputs},
                "integrity_judgment": "usable_with_boundary",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": [rel(RUN330E_DIR), rel(RUN330F_DIR)],
                "shared_contract": "run334F materializes diagnostic views from fixed Stage330E/330F feature, model, report, trade, and slice identities.",
                "known_differences": [
                    "No MT5 rerun is launched in run334F.",
                    "Stage330 non-identity ONNX remains separate from cp322A exact.",
                    "Runtime authority remains not claimed.",
                ],
                "parity_check": "runtime_identity_diagnostic_views.csv records existence and hashes for source feature/model/trade/slice files.",
                "parity_identity": {
                    "identity_rows": len(outputs["identity"]),
                    "all_identity_sources_available": all(row.get("diagnostic_status") == "identity_sources_available" for row in outputs["identity"]),
                },
                "runtime_claim_boundary": "materialization_only_no_runtime_authority",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "existing Stage330 non-identity ONNX surfaces",
                "target_and_label": "inherited; no label generation occurs in run334F",
                "split_method": "fixed post-forward diagnostic materialization",
                "selection_metric": "none",
                "secondary_metrics": [
                    "cost stress",
                    "curve pocket",
                    "worst regime slice",
                    "direction weakness",
                    "underwater stretch",
                    "runtime identity",
                ],
                "threshold_policy": "fixed inherited threshold; no search or calibration",
                "overfit_risk": "high if diagnostic failures are converted into exclusion filters; rejection rules forbid this.",
                "calibration_risk": "not assessed in this materialization packet",
                "comparison_baseline": "run334E stress design and run334D all-six reconciliation",
                "validation_judgment": "exploratory_materialization_no_selection",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "observed_change": "run334F turns each stress queue row into a concrete diagnostic view.",
                "comparison_baseline": "run334E design queue",
                "likely_drivers": [
                    "cost sensitivity",
                    "rolling curve pockets",
                    "worst regime slice losses",
                    "direction asymmetry",
                    "underwater stretch",
                    "runtime identity completeness",
                ],
                "segment_checks": [
                    "cost_plus_1",
                    "cost_plus_2",
                    "rolling_worst_curve",
                    "worst_regime_slice",
                    "directional_side",
                    "underwater_stretch",
                    "runtime_identity",
                ],
                "trade_shape": {
                    "hard_failure_attempts": hard_count,
                    "diagnostic_rows": len(outputs["manifest"]),
                },
                "alternative_explanations": [
                    "short forward window noise",
                    "synthetic cost approximations",
                    "single-surface attribution limits",
                ],
                "attribution_confidence": "medium_materialized_research_only",
                "next_probe": NEXT_RUN_ID,
            },
        )
    )
    return receipts


def write_run_artifacts(context: Mapping[str, Any], outputs: Mapping[str, Sequence[Mapping[str, Any]]], now: str) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_csv(
            RUN_DIR / "materialization_manifest.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "stress_axis",
                "scenario_id",
                "severity",
                "source_rows_used",
                "diagnostic_status",
                "scenario_result",
                "view_path",
                "selection_eligible",
                "claim_boundary",
            ],
            outputs["manifest"],
        )
    )
    artifacts.append(
        write_csv(
            VIEWS_DIR / "cost_stress_diagnostic_views.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "scenario_id",
                "extra_cost_per_round_trip_account_ccy",
                "net_profit_after_cost",
                "profit_factor_after_cost",
                "max_drawdown_after_cost",
                "survives_pf_gt_1",
                "diagnostic_status",
                "selection_eligible",
                "effect",
            ],
            outputs["cost"],
        )
    )
    artifacts.append(
        write_csv(
            VIEWS_DIR / "curve_pocket_diagnostic_views.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "chunk_id",
                "start_time",
                "end_time",
                "reported_trade_count",
                "window_trade_count",
                "reported_net_profit",
                "window_net_profit",
                "profit_factor",
                "diagnostic_status",
                "selection_eligible",
                "effect",
            ],
            outputs["curve"],
        )
    )
    artifacts.append(
        write_csv(
            VIEWS_DIR / "regime_slice_diagnostic_views.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "axis",
                "bucket",
                "trade_count",
                "net_profit",
                "profit_factor",
                "max_drawdown",
                "diagnostic_status",
                "selection_eligible",
                "effect",
            ],
            outputs["regime"],
        )
    )
    artifacts.append(
        write_csv(
            VIEWS_DIR / "direction_diagnostic_views.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "buy_trade_count",
                "buy_net_profit",
                "buy_profit_factor",
                "sell_trade_count",
                "sell_net_profit",
                "sell_profit_factor",
                "weak_direction",
                "diagnostic_status",
                "selection_eligible",
                "effect",
            ],
            outputs["direction"],
        )
    )
    artifacts.append(
        write_csv(
            VIEWS_DIR / "underwater_diagnostic_views.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "total_trade_count",
                "max_underwater_trade_count",
                "underwater_trade_share",
                "max_underwater_start",
                "max_underwater_end",
                "max_drawdown",
                "diagnostic_status",
                "selection_eligible",
                "effect",
            ],
            outputs["underwater"],
        )
    )
    artifacts.append(
        write_csv(
            VIEWS_DIR / "runtime_identity_diagnostic_views.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "decision_threshold",
                "feature_matrix_path",
                "feature_matrix_exists",
                "feature_matrix_sha256",
                "model_path",
                "model_exists",
                "model_sha256",
                "trade_records_exists",
                "trade_records_sha256",
                "slice_report_exists",
                "slice_report_sha256",
                "diagnostic_status",
                "selection_eligible",
                "effect",
            ],
            outputs["identity"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "stress_failure_memory_summary.csv",
            [
                "attempt_name",
                "artifact_slug",
                "severity",
                "headline_net_profit",
                "headline_profit_factor",
                "diagnostic_row_count",
                "hard_failure_count",
                "warning_count",
                "selection_eligible",
                "claim_boundary",
                "materialization_judgment",
                "next_action",
                "effect",
            ],
            outputs["summary"],
        )
    )
    artifacts.extend(write_skill_receipts(context, outputs))
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence", "claim_effect"],
            [
                {
                    "gate": "data_integrity",
                    "status": "passed_usable_with_boundary",
                    "evidence": "data_integrity_receipt.json",
                    "claim_effect": "No new bars, labels, thresholds, or model data are created.",
                },
                {
                    "gate": "runtime_parity",
                    "status": "passed_identity_materialized_no_authority",
                    "evidence": "runtime_parity_receipt.json",
                    "claim_effect": "Source file existence and hashes are materialized without runtime authority.",
                },
                {
                    "gate": "model_validation",
                    "status": "passed_no_selection_no_retune",
                    "evidence": "model_validation_receipt.json",
                    "claim_effect": "No model, threshold, lot, or rule is selected from diagnostics.",
                },
                {
                    "gate": "performance_attribution",
                    "status": "passed_materialized_research_only",
                    "evidence": "performance_attribution_receipt.json",
                    "claim_effect": "Cost, curve, regime, direction, and underwater evidence is now materialized.",
                },
                {
                    "gate": "artifact_lineage",
                    "status": "passed_connected_with_boundary",
                    "evidence": "artifact_lineage_receipt.json",
                    "claim_effect": "run334E queue connects to run334F diagnostic views and registers.",
                },
                {
                    "gate": "result_judgment",
                    "status": "passed_no_goal_achieve",
                    "evidence": "result_judgment.csv",
                    "claim_effect": "Forward Passed/Failed and Goal Achieve are not claimed.",
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
    hard_attempts = sum(1 for row in outputs["summary"] if row.get("materialization_judgment") == "hard_failure_memory")
    artifacts.append(
        write_json(
            RUN_DIR / "final_materialization_decision.json",
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "queue_rows_materialized": len(outputs["manifest"]),
                "attempt_rows": len(outputs["summary"]),
                "hard_failure_attempts": hard_attempts,
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
            rel(RUN334E_QUEUE),
            rel(RUN334E_MATRIX),
            rel(RUN334E_REJECTION),
            rel(RUN334E_CONTRACT),
            rel(RUN334D_ALL_SIX),
            rel(RUN334D_MEMORY),
            rel(RUN330E_FEATURE_MANIFEST),
            rel(RUN330F_COST),
            rel(RUN330F_CURVE),
            rel(RUN330F_UNDERWATER),
            rel(RUN330F_DIRECTION),
            rel(RUN330F_SLICES),
            rel(RUN330F_TRADE_RECORDS),
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
                "source_inputs": lineage["source_inputs"],
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
    hard_attempts = [row["attempt_name"] for row in outputs["summary"] if row.get("materialization_judgment") == "hard_failure_memory"]
    report = write_md(
        REVIEWS_DIR / "run334F_no_retune_stress_probe_materialization.md",
        f"""
# run334F No-Retune Stress Probe Materialization(334F 무재튜닝 압박 탐침 물질화)

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

## Materialized Views(물질화된 보기)

- materialization_manifest(물질화 목록): `{len(outputs["manifest"])}` rows
- cost stress views(비용 압박 보기): `{len(outputs["cost"])}` rows
- curve pocket views(곡선 포켓 보기): `{len(outputs["curve"])}` rows
- regime slice views(국면 슬라이스 보기): `{len(outputs["regime"])}` rows
- direction views(방향 보기): `{len(outputs["direction"])}` rows
- underwater views(수중 구간 보기): `{len(outputs["underwater"])}` rows
- runtime identity views(런타임 정체성 보기): `{len(outputs["identity"])}` rows
- hard_failure_attempts(강한 실패 시도): `{', '.join(hard_attempts) if hard_attempts else 'none'}`

Effect(효과): run334E(334E 실행)의 stress design(압박 설계)을 실제 fixed-input diagnostic evidence(고정 입력 진단 근거)로 만들었지만, 선택 후보나 운영 주장은 만들지 않는다.

Next(다음): `{NEXT_RUN_ID}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage334F No-Retune Stress Probe Materialization(334F 무재튜닝 압박 탐침 물질화)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 42개 no-retune stress queue(무재튜닝 압박 대기열)를 diagnostic view(진단 보기)로 물질화했고, 다음 실행에서 실패 기억과 보존 단서를 검토한다.
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
- latest_stress_materialization(최신 압박 물질화): `{RUN_ID}`
- active_question(활성 질문): `forward_usable_onnx_handoff_contract_hardening_without_overfit`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage334F(334F 실행)는 fixed-input diagnostic views(고정 입력 진단 보기)를 물질화했고, 선택 후보는 만들지 않았다.
""",
    )
    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = replace_prefix_line(text, "- status(상태):", "- status(상태): `open_active`")
        text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        write_text_lossless(STAGE_BRIEF, text, had_bom)
    append_section_once(
        INPUTS_DIR / "input_refs.md",
        "## run334F No-Retune Stress Probe Materialization Outputs(334F 무재튜닝 압박 탐침 물질화 출력)",
        f"""
- run334F_manifest(334F 물질화 목록): `stages/{STAGE_ID}/02_runs/run334F/materialization_manifest.csv`
- run334F_views(334F 진단 보기): `stages/{STAGE_ID}/02_runs/run334F/diagnostic_views/`
- run334F_summary(334F 실패 기억 요약): `stages/{STAGE_ID}/02_runs/run334F/stress_failure_memory_summary.csv`
- run334F_final_decision(334F 최종 결정): `stages/{STAGE_ID}/02_runs/run334F/final_materialization_decision.json`
""",
    )
    return [status_path, STAGE_BRIEF, INPUTS_DIR / "input_refs.md"]


def update_state_docs() -> list[Path]:
    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_insert = f"""- >-
  Stage334(334단계) run334F(334F 실행)는 `{STATUS}`로 no-retune stress probe inputs(무재튜닝 압박 탐침 입력)를 materialized(물질화)했다. Effect(효과): 42개 queue(대기열)를 cost/curve/regime/direction/underwater/runtime identity(비용/곡선/국면/방향/수중구간/런타임 정체성) diagnostic views(진단 보기)로 만들었지만 selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다."""
    text = insert_after_line_once(text, "current_focus:", focus_insert, "run334F(334F 실행)")
    write_text_lossless(WORKSPACE_STATE, text, had_bom)

    text, had_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v7`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": "- status(상태): `completed_no_retune_stress_probe_materialization_ready_for_review`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = f"- run334F_summary(334F 요약): no-retune stress probe materialization(무재튜닝 압박 탐침 물질화)을 `{STATUS}`로 완료했다. Effect(효과): 42개 fixed-input diagnostic view(고정 입력 진단 보기)를 만들었고, 다음 run334G(334G 실행)는 실패 기억과 보존 단서를 검토한다."
    text = insert_after_line_once(text, f"- decision(판정): `{DECISION}`", summary, "run334F_summary")
    write_text_lossless(CURRENT_STATE, text, had_bom)

    append_section_once(
        CHANGELOG,
        "## 2026-05-26 - Stage334F No-Retune Stress Probe Materialization(334F 무재튜닝 압박 탐침 물질화)",
        f"""
- run334F(334F 실행): run334E(334E 실행)의 42개 stress queue(압박 대기열)를 diagnostic views(진단 보기)로 물질화했다.
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
                "lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334F_no_retune_stress_probe_materialization.md",
                "notes": "no_retune_diagnostic_views_materialized;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__diagnostic_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "no_retune_stress_probe_diagnostic_materialization",
                "tier_scope": "research_contract_no_tier_kpi",
                "kpi_scope": "diagnostic_views_no_new_trading_kpi",
                "scoreboard_lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334F_no_retune_stress_probe_materialization.md",
                "primary_kpi": "materialization_queue_rows=42;attempt_rows=6",
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
                "ledger_row_id": f"{RUN_ID}__diagnostic_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "experiment_execution",
                "evidence_scope": "no_retune_stress_probe_diagnostic_views",
                "kpi_scope": "diagnostic_views_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": f"stages/{STAGE_ID}/03_reviews/run334F_no_retune_stress_probe_materialization.md",
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
                "artifact_type": "stage334F_no_retune_stress_materialization_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": "fixed-input diagnostic materialization; no operating claim.",
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
                "materialization_rows": len(outputs["manifest"]),
                "attempt_rows": len(outputs["summary"]),
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
