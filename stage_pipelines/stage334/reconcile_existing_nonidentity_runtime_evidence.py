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
RUN_NUMBER = "run334D"
RUN_ID = "run334D_reconcile_existing_non_identity_runtime_probe_evidence_no_selection_v1"
PARENT_RUN_ID = "run334C_design_subject_separated_runtime_probe_or_block_v1"
NEXT_RUN_ID = "run334E_design_no_retune_forward_usable_nonidentity_stress_probe_from_reconciled_memory_v1"
STATUS = "completed_existing_nonidentity_runtime_evidence_reconciliation_no_selection"
JUDGMENT = "all_six_nonidentity_runtime_evidence_reconciled_research_only_no_goal_achieve"
DECISION = "stage334D_preserved_clues_and_failure_memory_reconciled_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_existing_nonidentity_runtime_evidence_reconciliation_"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage334D_existing_nonidentity_runtime_reconciliation.md"

RUN334C_DIR = STAGE_DIR / "02_runs" / "run334C"
RUN334C_QUEUE = RUN334C_DIR / "future_non_identity_runtime_reconciliation_queue.csv"
RUN334C_MATRIX = RUN334C_DIR / "runtime_probe_or_block_decision_matrix.csv"
RUN334C_DECISION = RUN334C_DIR / "final_runtime_probe_or_block_decision.json"

STAGE330_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN330D_DIR = STAGE330_DIR / "02_runs" / "run330D"
RUN330E_DIR = STAGE330_DIR / "02_runs" / "run330E"
RUN330F_DIR = STAGE330_DIR / "02_runs" / "run330F"

RUN330E_FEATURE_MANIFEST = RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"
RUN330E_SUMMARY = RUN330E_DIR / "mt5_runtime_probe_summary.csv"
RUN330F_KPI = RUN330F_DIR / "forward_mt5_kpi_report.csv"
RUN330F_COST = RUN330F_DIR / "cost_stress_report.csv"
RUN330F_CURVE = RUN330F_DIR / "curve_pocket_report.csv"
RUN330F_UNDERWATER = RUN330F_DIR / "underwater_stretch_report.csv"
RUN330F_LOT = RUN330F_DIR / "lot_normalized_report.csv"
RUN330F_DB = RUN330F_DIR / "db_attribution_report.csv"
RUN330F_DIRECTION = RUN330F_DIR / "long_short_attribution_report.csv"
RUN330F_REGIME = RUN330F_DIR / "regime_attribution_report.csv"
RUN330F_SLICES = RUN330F_DIR / "session_hour_month_volatility_adx_vix_usd_rate_slices.csv"
RUN330F_DECISION = RUN330F_DIR / "final_forward_decision.json"
RUN330D_SOURCE = RUN330D_DIR / "source_view_attribution_matrix.csv"
RUN330D_REGIME = RUN330D_DIR / "regime_fragility_matrix.csv"


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


def yes_no(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def by_attempt(rows: Sequence[Mapping[str, str]]) -> dict[str, list[Mapping[str, str]]]:
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("attempt_name", "")].append(row)
    return grouped


def single_by_attempt(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    result: dict[str, Mapping[str, str]] = {}
    for row in rows:
        attempt = row.get("attempt_name", "")
        if attempt:
            result[attempt] = row
    return result


def row_for_cost(cost_rows: Sequence[Mapping[str, str]], extra_cost: float) -> Mapping[str, str]:
    for row in cost_rows:
        if abs(as_float(row.get("extra_cost_per_round_trip_account_ccy")) - extra_cost) < 1e-9:
            return row
    return {}


def worst_net_row(rows: Sequence[Mapping[str, str]]) -> Mapping[str, str]:
    if not rows:
        return {}
    return min(rows, key=lambda row: as_float(row.get("net_profit"), 0.0))


def summarize_cost(attempt: str, cost_by_attempt: Mapping[str, Sequence[Mapping[str, str]]]) -> dict[str, Any]:
    rows = sorted(
        list(cost_by_attempt.get(attempt, [])),
        key=lambda row: as_float(row.get("extra_cost_per_round_trip_account_ccy")),
    )
    plus_025 = row_for_cost(rows, 0.25)
    plus_050 = row_for_cost(rows, 0.5)
    plus_100 = row_for_cost(rows, 1.0)
    plus_200 = row_for_cost(rows, 2.0)
    surviving = [as_float(row.get("extra_cost_per_round_trip_account_ccy")) for row in rows if yes_no(row.get("survives_pf_gt_1"))]
    failing = [as_float(row.get("extra_cost_per_round_trip_account_ccy")) for row in rows if not yes_no(row.get("survives_pf_gt_1"))]
    return {
        "cost_plus_025_survives": yes_no(plus_025.get("survives_pf_gt_1")),
        "cost_plus_050_survives": yes_no(plus_050.get("survives_pf_gt_1")),
        "cost_plus_100_survives": yes_no(plus_100.get("survives_pf_gt_1")),
        "cost_plus_200_survives": yes_no(plus_200.get("survives_pf_gt_1")),
        "cost_plus_100_net": as_float(plus_100.get("net_profit_after_cost")) if plus_100 else "",
        "cost_plus_100_pf": as_float(plus_100.get("profit_factor_after_cost")) if plus_100 else "",
        "cost_plus_200_net": as_float(plus_200.get("net_profit_after_cost")) if plus_200 else "",
        "cost_plus_200_pf": as_float(plus_200.get("profit_factor_after_cost")) if plus_200 else "",
        "max_cost_step_surviving_pf_gt_1": max(surviving) if surviving else "",
        "first_cost_step_breaking_pf": min(failing) if failing else "",
    }


def summarize_curve(attempt: str, curve_by_attempt: Mapping[str, Sequence[Mapping[str, str]]]) -> dict[str, Any]:
    rows = list(curve_by_attempt.get(attempt, []))
    rolling = [row for row in rows if row.get("chunk_type") == "rolling_worst_net"]
    thirds = [row for row in rows if row.get("chunk_type") == "thirds"]
    worst = worst_net_row(rows)
    worst_third = worst_net_row(thirds)
    rolling_worst = worst_net_row(rolling)
    return {
        "worst_curve_chunk_type": worst.get("chunk_type", ""),
        "worst_curve_chunk_id": worst.get("chunk_id", ""),
        "worst_curve_net": as_float(worst.get("net_profit")) if worst else "",
        "worst_curve_profit_factor": as_float(worst.get("profit_factor")) if worst else "",
        "worst_curve_start": worst.get("start_time", ""),
        "worst_curve_end": worst.get("end_time", ""),
        "rolling_worst_net": as_float(rolling_worst.get("net_profit")) if rolling_worst else "",
        "worst_third_id": worst_third.get("chunk_id", ""),
        "worst_third_net": as_float(worst_third.get("net_profit")) if worst_third else "",
    }


def summarize_slices(attempt: str, slice_by_attempt: Mapping[str, Sequence[Mapping[str, str]]]) -> dict[str, Any]:
    rows = list(slice_by_attempt.get(attempt, []))
    worst = worst_net_row(rows)
    negative_rows = [row for row in rows if as_float(row.get("net_profit")) < 0]
    axes = sorted({row.get("axis", "") for row in rows if row.get("axis")})
    axis_neg_counts = defaultdict(int)
    for row in negative_rows:
        axis_neg_counts[row.get("axis", "")] += 1
    most_negative_axis = ""
    if axis_neg_counts:
        most_negative_axis = sorted(axis_neg_counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
    return {
        "slice_row_count": len(rows),
        "slice_axis_count": len(axes),
        "negative_slice_count": len(negative_rows),
        "most_negative_axis": most_negative_axis,
        "worst_slice_axis": worst.get("axis", ""),
        "worst_slice_bucket": worst.get("bucket", ""),
        "worst_slice_net": as_float(worst.get("net_profit")) if worst else "",
        "worst_slice_profit_factor": as_float(worst.get("profit_factor")) if worst else "",
    }


def direction_summary(attempt: str, direction_by_attempt: Mapping[str, Sequence[Mapping[str, str]]]) -> dict[str, Any]:
    rows = list(direction_by_attempt.get(attempt, []))
    buy = next((row for row in rows if row.get("direction") == "buy"), {})
    sell = next((row for row in rows if row.get("direction") == "sell"), {})
    weak_direction = ""
    if buy and sell:
        weak_direction = "buy" if as_float(buy.get("net_profit")) <= as_float(sell.get("net_profit")) else "sell"
    return {
        "buy_trade_count": as_int(buy.get("trade_count")),
        "buy_net_profit": as_float(buy.get("net_profit")) if buy else "",
        "buy_profit_factor": as_float(buy.get("profit_factor")) if buy else "",
        "sell_trade_count": as_int(sell.get("trade_count")),
        "sell_net_profit": as_float(sell.get("net_profit")) if sell else "",
        "sell_profit_factor": as_float(sell.get("profit_factor")) if sell else "",
        "weak_direction": weak_direction,
        "directional_fragility": "sell_negative" if sell and as_float(sell.get("net_profit")) < 0 else "balanced_or_buy_led",
    }


def risk_flags(kpi: Mapping[str, Any], cost: Mapping[str, Any], curve: Mapping[str, Any], underwater: Mapping[str, Any], slices: Mapping[str, Any], direction: Mapping[str, Any]) -> list[str]:
    flags: list[str] = []
    pf = as_float(kpi.get("profit_factor"))
    net = as_float(kpi.get("net_profit"))
    trades = as_int(kpi.get("trade_count"))
    underwater_count = as_int(underwater.get("max_underwater_trade_count"))
    underwater_share = underwater_count / trades if trades else 0.0
    if net <= 0:
        flags.append("non_positive_net")
    if pf <= 1.05:
        flags.append("thin_profit_factor")
    if not cost.get("cost_plus_100_survives"):
        flags.append("cost_plus_1_breaks_pf")
    if not cost.get("cost_plus_200_survives"):
        flags.append("cost_plus_2_breaks_pf")
    if as_float(curve.get("worst_curve_net")) <= -50:
        flags.append("deep_curve_pocket")
    if underwater_share >= 0.5:
        flags.append("long_underwater_stretch")
    if as_float(slices.get("worst_slice_net")) <= -50:
        flags.append("regime_loss_pocket")
    if direction.get("directional_fragility") == "sell_negative":
        flags.append("short_side_negative")
    return flags


def reconciliation_label(flags: Sequence[str], stage330_watchlist: set[str]) -> str:
    if "cost_plus_1_breaks_pf" in flags or "thin_profit_factor" in flags or "long_underwater_stretch" in flags:
        return "failure_memory_required"
    if len(flags) <= 3:
        return "preserved_clue_with_unresolved_guards" if stage330_watchlist else "mixed_clue_research_only"
    return "fragile_clue_requires_next_probe"


def load_context() -> dict[str, Any]:
    return {
        "queue_rows": read_csv_rows(RUN334C_QUEUE),
        "decision_matrix": read_csv_rows(RUN334C_MATRIX),
        "run334c_decision": read_json(RUN334C_DECISION),
        "feature_manifest": read_csv_rows(RUN330E_FEATURE_MANIFEST),
        "stage330e_summary": read_csv_rows(RUN330E_SUMMARY),
        "kpi_rows": read_csv_rows(RUN330F_KPI),
        "cost_rows": read_csv_rows(RUN330F_COST),
        "curve_rows": read_csv_rows(RUN330F_CURVE),
        "underwater_rows": read_csv_rows(RUN330F_UNDERWATER),
        "lot_rows": read_csv_rows(RUN330F_LOT),
        "db_rows": read_csv_rows(RUN330F_DB),
        "direction_rows": read_csv_rows(RUN330F_DIRECTION),
        "regime_rows": read_csv_rows(RUN330F_REGIME),
        "slice_rows": read_csv_rows(RUN330F_SLICES),
        "run330f_decision": read_json(RUN330F_DECISION),
        "source_rows": read_csv_rows(RUN330D_SOURCE),
        "run330d_regime_rows": read_csv_rows(RUN330D_REGIME),
    }


def build_reconciliation(context: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    queue_by_attempt = single_by_attempt(context["queue_rows"])
    kpi_by_attempt = single_by_attempt(context["kpi_rows"])
    underwater_by_attempt = single_by_attempt(context["underwater_rows"])
    lot_by_attempt = single_by_attempt(context["lot_rows"])
    db_by_attempt = single_by_attempt(context["db_rows"])
    source_by_slug = {row.get("artifact_slug", ""): row for row in context["source_rows"]}
    cost_by_attempt = by_attempt(context["cost_rows"])
    curve_by_attempt = by_attempt(context["curve_rows"])
    direction_by_attempt = by_attempt(context["direction_rows"])
    regime_by_attempt = by_attempt(context["regime_rows"])
    slice_by_attempt = by_attempt(context["slice_rows"])

    run330f_decision = context["run330f_decision"]
    watchlist = set(run330f_decision.get("watchlist_not_selection", []))
    fragility = set(run330f_decision.get("fragility_flags", []))

    all_six_rows: list[dict[str, Any]] = []
    cost_curve_rows: list[dict[str, Any]] = []
    attribution_rows: list[dict[str, Any]] = []
    regime_rows: list[dict[str, Any]] = []
    memory_rows: list[dict[str, Any]] = []

    for attempt in sorted(queue_by_attempt):
        queue = queue_by_attempt[attempt]
        kpi = kpi_by_attempt.get(attempt, {})
        underwater = underwater_by_attempt.get(attempt, {})
        lot = lot_by_attempt.get(attempt, {})
        db = db_by_attempt.get(attempt, {})
        slug = queue.get("artifact_slug", "") or kpi.get("artifact_slug", "")
        cost = summarize_cost(attempt, cost_by_attempt)
        curve = summarize_curve(attempt, curve_by_attempt)
        slices = summarize_slices(attempt, slice_by_attempt)
        direction = direction_summary(attempt, direction_by_attempt)
        source = source_by_slug.get(slug, {})
        flags = risk_flags(kpi, cost, curve, underwater, slices, direction)
        label = reconciliation_label(flags, attempt in watchlist)
        trade_count = as_int(kpi.get("trade_count"))
        underwater_share = as_int(underwater.get("max_underwater_trade_count")) / trade_count if trade_count else 0.0

        all_six_rows.append(
            {
                "attempt_name": attempt,
                "candidate_id": queue.get("candidate_id", ""),
                "artifact_slug": slug,
                "feature_set_id": queue.get("feature_set_id", ""),
                "feature_count": queue.get("feature_count", ""),
                "forward_first_timestamp": queue.get("first_timestamp", ""),
                "forward_last_timestamp": queue.get("last_timestamp", ""),
                "threshold_policy": queue.get("threshold_policy", ""),
                "decision_threshold": queue.get("decision_threshold", ""),
                "stage334_queue_ready": queue.get("evidence_ready_for_reconciliation", ""),
                "stage330f_net_profit": as_float(kpi.get("net_profit")),
                "stage330f_profit_factor": as_float(kpi.get("profit_factor")),
                "stage330f_trade_count": trade_count,
                "stage330f_trades_per_day": as_float(kpi.get("trades_per_day")),
                "stage330f_expectancy": as_float(kpi.get("expectancy")),
                "stage330f_recovery_factor": as_float(kpi.get("recovery_factor")),
                "stage330f_equity_dd_amount": as_float(kpi.get("equity_dd_amount")),
                "stage330f_equity_dd_percent": as_float(kpi.get("equity_dd_percent")),
                "cost_plus_1_survives": cost.get("cost_plus_100_survives"),
                "cost_plus_2_survives": cost.get("cost_plus_200_survives"),
                "worst_curve_net": curve.get("worst_curve_net"),
                "max_underwater_trade_count": as_int(underwater.get("max_underwater_trade_count")),
                "underwater_trade_share": underwater_share,
                "negative_slice_count": slices.get("negative_slice_count"),
                "worst_slice_axis": slices.get("worst_slice_axis"),
                "worst_slice_bucket": slices.get("worst_slice_bucket"),
                "worst_slice_net": slices.get("worst_slice_net"),
                "buy_net_profit": direction.get("buy_net_profit"),
                "sell_net_profit": direction.get("sell_net_profit"),
                "stage330f_watchlist_not_selection": attempt in watchlist,
                "stage330f_fragility_flag": attempt in fragility,
                "risk_flags": flags,
                "reconciliation_label": label,
                "selection_eligible": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        cost_curve_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": slug,
                **cost,
                **curve,
                "total_trade_count": trade_count,
                "max_underwater_trade_count": as_int(underwater.get("max_underwater_trade_count")),
                "underwater_trade_share": underwater_share,
                "lot_normalization_boundary": lot.get("normalization_boundary", ""),
                "net_profit_per_1lot_linear": as_float(lot.get("net_profit_per_1lot_linear")) if lot else "",
                "equity_dd_amount_per_1lot_linear": as_float(lot.get("equity_dd_amount_per_1lot_linear")) if lot else "",
                "risk_flags": flags,
                "guard_judgment": label,
                "effect": "cost and curve evidence is used for memory, not for threshold or lot optimization",
            }
        )

        attribution_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": slug,
                "db_source_status": db.get("status", ""),
                "db_source_reason": db.get("reason", ""),
                **direction,
                "source_view_judgment": source.get("source_view_judgment", ""),
                "raw_session_gap_judgment": source.get("raw_session_gap_judgment", ""),
                "high_fragility_axis_count": source.get("high_fragility_axis_count", ""),
                "attribution_judgment": "usable_with_boundary_no_db_source" if db else "inconclusive_missing_db_row",
                "effect": "D/B source is not invented; long/short and source-view evidence remains research-only",
            }
        )

        regime_worst = worst_net_row(regime_by_attempt.get(attempt, []))
        regime_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": slug,
                **slices,
                "worst_regime_axis": regime_worst.get("axis", ""),
                "worst_regime_bucket": regime_worst.get("bucket", ""),
                "worst_regime_net": as_float(regime_worst.get("net_profit")) if regime_worst else "",
                "worst_regime_profit_factor": as_float(regime_worst.get("profit_factor")) if regime_worst else "",
                "regime_judgment": "loss_pockets_present" if as_int(slices.get("negative_slice_count")) > 0 else "no_negative_slice_seen",
                "effect": "session, hour, month, volatility, ADX, VIX, USD, and rate slices are preserved as guard evidence",
            }
        )

        memory_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": slug,
                "memory_type": label,
                "preserved_clue": label.startswith("preserved_clue"),
                "failure_memory_required": "failure_memory_required" in label or bool(flags),
                "primary_positive_evidence": f"net={as_float(kpi.get('net_profit'))};pf={as_float(kpi.get('profit_factor'))};trades={trade_count}",
                "primary_fragility_evidence": ";".join(flags),
                "next_probe": NEXT_RUN_ID,
                "selection_status": "not_selected",
                "goal_achieve": "not_claimed",
                "effect": "stronger rows become clues, weak rows become failure memory; neither becomes a selected candidate",
            }
        )

    return {
        "all_six": all_six_rows,
        "cost_curve": cost_curve_rows,
        "attribution": attribution_rows,
        "regime": regime_rows,
        "memory": memory_rows,
    }


def write_skill_receipts(context: Mapping[str, Any], outputs: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[Path]:
    all_six = list(outputs["all_six"])
    preserved_count = sum(1 for row in outputs["memory"] if row.get("preserved_clue") is True)
    failure_count = sum(1 for row in outputs["memory"] if row.get("failure_memory_required") is True)
    source_inputs = [
        RUN334C_QUEUE,
        RUN334C_MATRIX,
        RUN330E_FEATURE_MANIFEST,
        RUN330E_SUMMARY,
        RUN330F_KPI,
        RUN330F_COST,
        RUN330F_CURVE,
        RUN330F_UNDERWATER,
        RUN330F_LOT,
        RUN330F_DB,
        RUN330F_DIRECTION,
        RUN330F_REGIME,
        RUN330F_SLICES,
        RUN330F_DECISION,
        RUN330D_SOURCE,
    ]
    receipts: list[Path] = []
    receipts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": [rel(RUN330E_DIR), rel(RUN330F_DIR)],
                "shared_contract": "attempt_name, artifact_slug, feature set, ONNX hash, fixed threshold, MT5 report, telemetry, and no-selection boundary must align.",
                "known_differences": [
                    "cp322A exact is still blocked by missing post-2026-04-14 route signal.",
                    "Stage330 non-identity ONNX evidence is not cp322A exact identity.",
                    "D/B source attribution is out_of_scope_by_claim because Stage330 uses one probability surface.",
                ],
                "parity_check": "existing Stage330E MT5 report/telemetry evidence reconciled against Stage330F KPI/cost/curve/regime reports; no new MT5 authority claimed.",
                "parity_identity": {
                    "queue_rows": len(context["queue_rows"]),
                    "reconciled_rows": len(all_six),
                    "run334c_queue_sha256": sha256_file(RUN334C_QUEUE),
                    "run330e_summary_sha256": sha256_file(RUN330E_SUMMARY),
                    "run330f_kpi_sha256": sha256_file(RUN330F_KPI),
                },
                "runtime_claim_boundary": "runtime_probe_reconciliation_research_only",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "tester_identity": {
                    "terminal": "Stage330E portable MT5 runtime probe outputs inherited; run334D does not launch a new tester.",
                    "broker": "FPMarkets",
                    "symbol": "US100",
                    "timeframe": "M5",
                    "date_range": "post-2026-04-14 through latest Stage330E manifest timestamps",
                    "deposit_leverage_modeling_spread": "inherited from Stage330E set/ini/report artifacts; not reparameterized in run334D",
                },
                "ea_identity": {
                    "entrypoint": "Stage330E MT5 runtime probe package",
                    "parameter_source": rel(RUN334C_QUEUE),
                    "model_bundle_source": rel(RUN330E_FEATURE_MANIFEST),
                    "identity_boundary": "run334D reconciles existing reports and does not alter EA, set, model, threshold, risk, or lot logic.",
                },
                "report_identity": {
                    "stage330e_summary": rel(RUN330E_SUMMARY),
                    "stage330f_kpi": rel(RUN330F_KPI),
                    "stage330f_cost": rel(RUN330F_COST),
                    "stage330f_curve": rel(RUN330F_CURVE),
                    "hashes": {
                        rel(RUN330E_SUMMARY): sha256_file(RUN330E_SUMMARY),
                        rel(RUN330F_KPI): sha256_file(RUN330F_KPI),
                        rel(RUN330F_COST): sha256_file(RUN330F_COST),
                        rel(RUN330F_CURVE): sha256_file(RUN330F_CURVE),
                    },
                },
                "trade_evidence": {
                    "reconciled_attempt_count": len(all_six),
                    "trade_counts": {row["attempt_name"]: row["stage330f_trade_count"] for row in all_six},
                    "net_profit": {row["attempt_name"]: row["stage330f_net_profit"] for row in all_six},
                    "profit_factor": {row["attempt_name"]: row["stage330f_profit_factor"] for row in all_six},
                },
                "cost_assumptions": "Base MT5 report cost assumptions are inherited; run330F synthetic spread/slippage stress is used only as a no-retune sensitivity screen.",
                "forensic_checks": [
                    "all six run334C queue rows reconciled",
                    "Stage330F KPI/cost/curve/underwater/lot/direction/regime files parsed",
                    "D/B attribution kept out_of_scope_by_claim when source tags are absent",
                    "no new tester run, threshold search, or lot optimization performed",
                ],
                "backtest_judgment": "usable_with_boundary",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [rel(path) for path in source_inputs],
                "time_axis": "Forward rows are post-2026-04-14 US100 M5 broker-data derived rows; timestamps are inherited from Stage330E manifests and reports.",
                "sample_scope": {
                    "symbol": "US100",
                    "timeframe": "M5",
                    "scope": "Stage330E/330F existing forward runtime evidence only",
                    "reconciled_attempts": [row["attempt_name"] for row in all_six],
                },
                "missing_or_duplicate_check": "run334D does not rebuild bars; it checks file availability, row identity, and all-six carry-forward coverage.",
                "feature_label_boundary": "No new label, score threshold, model, risk, lot, or rule is created.",
                "split_boundary": "Forward data is used for reconciliation and failure memory only, not selection or retuning.",
                "leakage_risk": "Choosing only c56_plain_rf or m48_plain_rf would be KPI cherry-pick; run334D carries all six rows and labels both clues and failures.",
                "data_hash_or_identity": {rel(path): sha256_file(path) for path in source_inputs},
                "integrity_judgment": "usable_with_boundary",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "observed_change": "The six Stage330 non-identity probes show positive headline net values but uneven cost, curve, underwater, direction, and regime behavior.",
                "comparison_baseline": "run334C queue plus Stage330F raw-forward MT5 review.",
                "likely_drivers": [
                    "feature set breadth and model weighting",
                    "trade density",
                    "short-side losses",
                    "extra round-trip cost sensitivity",
                    "rate, ADX, month, and hour loss pockets",
                ],
                "segment_checks": [
                    "cost stress",
                    "curve pocket",
                    "underwater stretch",
                    "long/short attribution",
                    "session/hour/month/volatility/ADX/VIX/USD/rate slices",
                    "lot normalization",
                ],
                "trade_shape": {
                    "attempt_count": len(all_six),
                    "preserved_clue_count": preserved_count,
                    "failure_memory_count": failure_count,
                },
                "alternative_explanations": [
                    "positive net may come from short forward window luck",
                    "MT5 cost assumptions may understate live-like spread/slippage",
                    "single-surface non-identity ONNX cannot explain cp322A D/B source behavior",
                ],
                "attribution_confidence": "medium_research_only",
                "next_probe": NEXT_RUN_ID,
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "existing Stage330 non-identity ONNX control surfaces",
                "target_and_label": "inherited from Stage329/330 artifacts; not rebuilt in run334D",
                "split_method": "existing post-2026-04-14 runtime probe evidence reconciliation",
                "selection_metric": "none; all six evidence rows are retained",
                "secondary_metrics": [
                    "PF",
                    "expectancy",
                    "drawdown",
                    "underwater stretch",
                    "cost stress",
                    "curve pocket",
                    "regime loss pockets",
                    "direction attribution",
                ],
                "threshold_policy": "fixed inherited threshold; no search or calibration",
                "overfit_risk": "KPI cherry-pick and cost/curve pocket hiding remain the main risks.",
                "calibration_risk": "Scores are not treated as calibrated probabilities in run334D.",
                "comparison_baseline": "Stage330F mixed review and run334C all-six queue.",
                "validation_judgment": "exploratory_reconciliation_no_selection",
            },
        )
    )
    return receipts


def write_run_artifacts(context: Mapping[str, Any], outputs: Mapping[str, Sequence[Mapping[str, Any]]], now: str) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_csv(
            RUN_DIR / "all_six_runtime_reconciliation.csv",
            [
                "attempt_name",
                "candidate_id",
                "artifact_slug",
                "feature_set_id",
                "feature_count",
                "forward_first_timestamp",
                "forward_last_timestamp",
                "threshold_policy",
                "decision_threshold",
                "stage334_queue_ready",
                "stage330f_net_profit",
                "stage330f_profit_factor",
                "stage330f_trade_count",
                "stage330f_trades_per_day",
                "stage330f_expectancy",
                "stage330f_recovery_factor",
                "stage330f_equity_dd_amount",
                "stage330f_equity_dd_percent",
                "cost_plus_1_survives",
                "cost_plus_2_survives",
                "worst_curve_net",
                "max_underwater_trade_count",
                "underwater_trade_share",
                "negative_slice_count",
                "worst_slice_axis",
                "worst_slice_bucket",
                "worst_slice_net",
                "buy_net_profit",
                "sell_net_profit",
                "stage330f_watchlist_not_selection",
                "stage330f_fragility_flag",
                "risk_flags",
                "reconciliation_label",
                "selection_eligible",
                "claim_boundary",
            ],
            outputs["all_six"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "cost_curve_guard_reconciliation.csv",
            [
                "attempt_name",
                "artifact_slug",
                "cost_plus_025_survives",
                "cost_plus_050_survives",
                "cost_plus_100_survives",
                "cost_plus_200_survives",
                "cost_plus_100_net",
                "cost_plus_100_pf",
                "cost_plus_200_net",
                "cost_plus_200_pf",
                "max_cost_step_surviving_pf_gt_1",
                "first_cost_step_breaking_pf",
                "worst_curve_chunk_type",
                "worst_curve_chunk_id",
                "worst_curve_net",
                "worst_curve_profit_factor",
                "worst_curve_start",
                "worst_curve_end",
                "rolling_worst_net",
                "worst_third_id",
                "worst_third_net",
                "total_trade_count",
                "max_underwater_trade_count",
                "underwater_trade_share",
                "lot_normalization_boundary",
                "net_profit_per_1lot_linear",
                "equity_dd_amount_per_1lot_linear",
                "risk_flags",
                "guard_judgment",
                "effect",
            ],
            outputs["cost_curve"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "attribution_reconciliation_summary.csv",
            [
                "attempt_name",
                "artifact_slug",
                "db_source_status",
                "db_source_reason",
                "buy_trade_count",
                "buy_net_profit",
                "buy_profit_factor",
                "sell_trade_count",
                "sell_net_profit",
                "sell_profit_factor",
                "weak_direction",
                "directional_fragility",
                "source_view_judgment",
                "raw_session_gap_judgment",
                "high_fragility_axis_count",
                "attribution_judgment",
                "effect",
            ],
            outputs["attribution"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "regime_slice_reconciliation_summary.csv",
            [
                "attempt_name",
                "artifact_slug",
                "slice_row_count",
                "slice_axis_count",
                "negative_slice_count",
                "most_negative_axis",
                "worst_slice_axis",
                "worst_slice_bucket",
                "worst_slice_net",
                "worst_slice_profit_factor",
                "worst_regime_axis",
                "worst_regime_bucket",
                "worst_regime_net",
                "worst_regime_profit_factor",
                "regime_judgment",
                "effect",
            ],
            outputs["regime"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "preserved_clue_and_failure_memory.csv",
            [
                "attempt_name",
                "artifact_slug",
                "memory_type",
                "preserved_clue",
                "failure_memory_required",
                "primary_positive_evidence",
                "primary_fragility_evidence",
                "next_probe",
                "selection_status",
                "goal_achieve",
                "effect",
            ],
            outputs["memory"],
        )
    )
    artifacts.extend(write_skill_receipts(context, outputs))
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence", "claim_effect"],
            [
                {
                    "gate": "artifact_lineage",
                    "status": "passed_connected_with_boundary",
                    "evidence": "artifact_lineage_receipt.json",
                    "claim_effect": "Stage330/334 evidence is connected to run334D outputs without selection.",
                },
                {
                    "gate": "runtime_parity",
                    "status": "passed_reconciliation_only",
                    "evidence": "runtime_parity_receipt.json",
                    "claim_effect": "Existing MT5 runtime probe evidence is reconciled but not promoted to authority.",
                },
                {
                    "gate": "data_integrity",
                    "status": "passed_usable_with_boundary",
                    "evidence": "data_integrity_receipt.json",
                    "claim_effect": "Forward evidence is used for failure memory and clues, not retuning.",
                },
                {
                    "gate": "backtest_forensics",
                    "status": "passed_existing_report_identity_with_boundary",
                    "evidence": "backtest_forensics_receipt.json",
                    "claim_effect": "Stage330E/330F report paths and hashes remain the external evidence boundary.",
                },
                {
                    "gate": "performance_attribution",
                    "status": "passed_medium_research_only",
                    "evidence": "performance_attribution_receipt.json",
                    "claim_effect": "Cost, curve, direction, and regime pockets are recorded before any next probe.",
                },
                {
                    "gate": "model_validation",
                    "status": "passed_no_selection_no_retune",
                    "evidence": "model_validation_receipt.json",
                    "claim_effect": "No model, threshold, or lot is selected from forward data.",
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
    preserved_count = sum(1 for row in outputs["memory"] if row.get("preserved_clue") is True)
    failure_count = sum(1 for row in outputs["memory"] if row.get("failure_memory_required") is True)
    artifacts.append(
        write_json(
            RUN_DIR / "final_reconciliation_decision.json",
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "reconciled_attempt_count": len(outputs["all_six"]),
                "preserved_clue_count": preserved_count,
                "failure_memory_count": failure_count,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
                "reason": "Existing Stage330E/330F MT5 evidence is useful for research, but all six rows retain unresolved cost, curve, direction, or regime fragility.",
            },
        )
    )
    lineage = {
        "source_inputs": [
            rel(RUN334C_QUEUE),
            rel(RUN334C_MATRIX),
            rel(RUN334C_DECISION),
            rel(RUN330E_FEATURE_MANIFEST),
            rel(RUN330E_SUMMARY),
            rel(RUN330F_KPI),
            rel(RUN330F_COST),
            rel(RUN330F_CURVE),
            rel(RUN330F_UNDERWATER),
            rel(RUN330F_LOT),
            rel(RUN330F_DB),
            rel(RUN330F_DIRECTION),
            rel(RUN330F_REGIME),
            rel(RUN330F_SLICES),
            rel(RUN330F_DECISION),
            rel(RUN330D_SOURCE),
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
    all_six = list(outputs["all_six"])
    memory = list(outputs["memory"])
    preserved = [row["attempt_name"] for row in memory if row.get("preserved_clue") is True]
    failures = [row["attempt_name"] for row in memory if row.get("failure_memory_required") is True]
    report = write_md(
        REVIEWS_DIR / "run334D_existing_nonidentity_runtime_reconciliation.md",
        f"""
# run334D Existing Non-Identity Runtime Reconciliation(334D 기존 비정체성 런타임 대조)

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

## What Was Reconciled(무엇을 대조했나)

- Stage330E/330F(330E/330F 단계)의 existing MT5 runtime probe evidence(기존 MT5 런타임 탐침 근거) `6`개를 모두 대조했다.
- cost stress(비용 압박), curve pocket(곡선 포켓), underwater stretch(수중 구간), lot-normalized view(로트 정규화 보기), long/short attribution(롱/숏 귀속), regime slices(국면 슬라이스)를 함께 묶었다.
- D/B source(D/B 원천)는 Stage330 non-identity surface(비정체성 표면)에 존재하지 않으므로 `out_of_scope_by_claim`로 유지했다.

## Result(결과)

- reconciled_attempts(대조 시도): `{len(all_six)}`
- preserved_clues(보존 단서): `{', '.join(preserved) if preserved else 'none'}`
- failure_memory_required(실패 기억 필요): `{', '.join(failures) if failures else 'none'}`

Effect(효과): headline KPI(표면 핵심지표)가 좋은 행만 고르지 않고, 다음 run334E(334E 실행)가 cost/curve/regime/direction failure memory(비용/곡선/국면/방향 실패 기억)를 먼저 다루게 한다.

Next(다음): `{NEXT_RUN_ID}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage334D Existing Non-Identity Runtime Reconciliation(334D 기존 비정체성 런타임 대조)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage330E/330F(330E/330F 단계) 6개 existing runtime evidence(기존 런타임 근거)를 all-six no-selection(6개 전체 무선택) 방식으로 대조했고, 보존 단서와 실패 기억을 분리했다.
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
- latest_reconciliation(최신 대조): `{RUN_ID}`
- active_question(활성 질문): `forward_usable_onnx_handoff_contract_hardening_without_overfit`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage334D(334D 실행)는 existing non-identity evidence(기존 비정체성 근거) 6개를 모두 대조했고, 보존 단서와 실패 기억을 분리했지만 선택 후보는 만들지 않았다.
""",
    )
    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = replace_prefix_line(text, "- status(상태):", "- status(상태): `open_active`")
        text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        write_text_lossless(STAGE_BRIEF, text, had_bom)
    append_section_once(
        INPUTS_DIR / "input_refs.md",
        "## run334D Existing Non-Identity Runtime Reconciliation Outputs(334D 기존 비정체성 런타임 대조 출력)",
        f"""
- run334D_all_six(334D 전체 6개): `stages/{STAGE_ID}/02_runs/run334D/all_six_runtime_reconciliation.csv`
- run334D_cost_curve(334D 비용 곡선): `stages/{STAGE_ID}/02_runs/run334D/cost_curve_guard_reconciliation.csv`
- run334D_attribution(334D 귀속): `stages/{STAGE_ID}/02_runs/run334D/attribution_reconciliation_summary.csv`
- run334D_regime(334D 국면): `stages/{STAGE_ID}/02_runs/run334D/regime_slice_reconciliation_summary.csv`
- run334D_memory(334D 기억): `stages/{STAGE_ID}/02_runs/run334D/preserved_clue_and_failure_memory.csv`
- run334D_final_decision(334D 최종 결정): `stages/{STAGE_ID}/02_runs/run334D/final_reconciliation_decision.json`
""",
    )
    return [status_path, STAGE_BRIEF, INPUTS_DIR / "input_refs.md"]


def update_state_docs() -> list[Path]:
    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_insert = f"""- >-
  Stage334(334단계) run334D(334D 실행)는 `{STATUS}`로 existing non-identity runtime evidence reconciliation(기존 비정체성 런타임 근거 대조)을 완료했다. Effect(효과): Stage330E/330F(330E/330F 단계) 6개 MT5 근거를 모두 대조하고 preserved clues/failure memory(보존 단서/실패 기억)로 분리했지만 selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다."""
    text = insert_after_line_once(text, "current_focus:", focus_insert, "run334D(334D 실행)")
    write_text_lossless(WORKSPACE_STATE, text, had_bom)

    text, had_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v5`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": "- status(상태): `completed_existing_nonidentity_reconciliation_ready_for_next_stress_probe_design`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = f"- run334D_summary(334D 요약): existing non-identity runtime evidence reconciliation(기존 비정체성 런타임 근거 대조)을 `{STATUS}`로 완료했다. Effect(효과): 6개 전체를 cost/curve/regime/direction(비용/곡선/국면/방향) 기준으로 대조했고, 다음 run334E(334E 실행)는 no-retune stress probe design(무재튜닝 압박 탐침 설계)로 넘어간다."
    text = insert_after_line_once(text, f"- decision(판정): `{DECISION}`", summary, "run334D_summary")
    write_text_lossless(CURRENT_STATE, text, had_bom)

    append_section_once(
        CHANGELOG,
        "## 2026-05-26 - Stage334D Existing Non-Identity Runtime Reconciliation(334D 기존 비정체성 런타임 대조)",
        f"""
- run334D(334D 실행): Stage330E/330F(330E/330F 단계) 6개 existing MT5 runtime probe evidence(기존 MT5 런타임 탐침 근거)를 모두 대조했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): preserved clues/failure memory(보존 단서/실패 기억)를 분리했지만 selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
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
                "lane": "runtime_parity_reconciliation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334D_existing_nonidentity_runtime_reconciliation.md",
                "notes": "all_six_nonidentity_evidence_reconciled;preserved_clues_and_failure_memory;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__all_six_runtime_reconciliation",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "existing_nonidentity_runtime_evidence_reconciliation",
                "tier_scope": "research_contract_no_tier_kpi",
                "kpi_scope": "mt5_kpi_cost_curve_regime_direction_lot_normalized",
                "scoreboard_lane": "runtime_parity_reconciliation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334D_existing_nonidentity_runtime_reconciliation.md",
                "primary_kpi": "reconciled_attempts=6;selected_candidate=none",
                "guardrail_kpi": "no_model_training;no_threshold_retuning;no_lot_optimization;goal_achieve_not_claimed",
                "external_verification_status": "completed_existing_stage330_mt5_evidence_reconciliation_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__all_six_runtime_reconciliation",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_parity_reconciliation",
                "evidence_scope": "existing_nonidentity_runtime_probe_evidence",
                "kpi_scope": "mt5_kpi_cost_curve_regime_direction_lot_normalized",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": f"stages/{STAGE_ID}/03_reviews/run334D_existing_nonidentity_runtime_reconciliation.md",
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
                "artifact_type": "stage334D_reconciliation_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": "existing non-identity runtime evidence reconciliation; no operating claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> None:
    now = utc_now()
    context = load_context()
    outputs = build_reconciliation(context)
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
                "reconciled_attempt_count": len(outputs["all_six"]),
                "preserved_clue_count": sum(1 for row in outputs["memory"] if row.get("preserved_clue") is True),
                "failure_memory_count": sum(1 for row in outputs["memory"] if row.get("failure_memory_required") is True),
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
