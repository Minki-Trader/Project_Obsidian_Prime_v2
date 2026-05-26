from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN_ID = "run330D_regime_attribution_v1"
RUN_NUMBER = "run330D"
PARENT_RUN_ID = "run330C_forward_mt5_or_score_curve_review_v1"
NEXT_ACTION = "run330E_mt5_runtime_probe_or_block_v1"

STATUS = "completed_regime_source_attribution_no_forward_decision"
JUDGMENT = "regime_source_attribution_completed_research_only_runtime_gap_remains"
DECISION = "stage330D_regime_source_pressure_runtime_probe_or_block_next"
CLAIM_BOUNDARY = (
    "research_development_only_regime_source_attribution_no_forward_threshold_tuning_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN330C_DIR = STAGE_DIR / "02_runs" / "run330C"
RUN330B_DIR = STAGE_DIR / "02_runs" / "run330B"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage330D_regime_source_attribution.md"


AXES = [
    ("session", "session_slice"),
    ("hour", "hour"),
    ("month", "month"),
    ("volatility", "volatility_regime"),
    ("adx", "adx_regime"),
    ("vix", "vix_regime"),
    ("usd", "usd_regime"),
    ("rate", "rate_regime"),
    ("direction", "direction"),
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    if path.exists():
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    else:
        fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    index = {tuple(str(row.get(column, "")) for column in key_columns): pos for pos, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {field: csv_value(row.get(field, "")) for field in fieldnames}
        if key in index:
            existing[index[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(existing)
    return path


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def safe_div(value: float | None, denom: float | None) -> float | None:
    if value is None or denom in (None, 0):
        return None
    return value / denom


def profit_factor(values: Sequence[float]) -> float | None:
    gross_profit = sum(value for value in values if value > 0)
    gross_loss = -sum(value for value in values if value < 0)
    if gross_loss == 0:
        return None if gross_profit == 0 else math.inf
    return gross_profit / gross_loss


def max_drawdown(values: Sequence[float]) -> float:
    equity = 0.0
    peak = 0.0
    worst = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        worst = max(worst, peak - equity)
    return worst


def aggregate(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(tuple(row.get(key, "") for key in keys), []).append(row)
    output: list[dict[str, Any]] = []
    for key, group_rows in grouped.items():
        values = [float(row.get("net_profit_normalized", 0.0)) for row in group_rows]
        gross_profit = sum(value for value in values if value > 0)
        gross_loss = -sum(value for value in values if value < 0)
        output.append(
            {
                **dict(zip(keys, key)),
                "trade_count": len(group_rows),
                "net_profit": sum(values),
                "gross_profit": gross_profit,
                "gross_loss": gross_loss,
                "profit_factor": profit_factor(values),
                "expectancy": safe_div(sum(values), len(values)),
                "win_rate": safe_div(sum(1 for value in values if value > 0), len(values)),
                "max_drawdown": max_drawdown(values),
            }
        )
    return output


def load_proxy_trades() -> list[dict[str, Any]]:
    rows = read_csv_rows(RUN330C_DIR / "score_proxy_trade_records.csv")
    output: list[dict[str, Any]] = []
    for row in rows:
        row["source_scope"] = f"score_proxy_{row.get('view_id', '')}"
        row["net_profit_normalized"] = to_float(row.get("proxy_net_profit")) or 0.0
        row["runtime_source"] = "score_proxy_not_mt5"
        row["axis_adx"] = row.get("adx_regime", "")
        output.append(row)
    return output


def load_mt5_trades() -> list[dict[str, Any]]:
    rows = read_csv_rows(RUN330C_DIR / "session_mt5_reference_trade_records.csv")
    output: list[dict[str, Any]] = []
    for row in rows:
        row["source_scope"] = "session_mt5_reference"
        row["view_id"] = row.get("view_id") or "old_session_parity"
        row["net_profit_normalized"] = to_float(row.get("net_profit")) or 0.0
        row["runtime_source"] = "mt5_session_reference_not_raw_forward"
        row["adx_regime"] = row.get("adx_bucket", "")
        output.append(row)
    return output


def build_unified_regime_rows(all_trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis, column in AXES:
        usable = [dict(row, bucket=row.get(column, "")) for row in all_trades if row.get(column, "") != ""]
        for record in aggregate(usable, ["source_scope", "runtime_source", "artifact_slug", "candidate_id", "view_id", "axis", "bucket"]):
            record["axis"] = axis
            record["claim_boundary"] = CLAIM_BOUNDARY
            rows.append(record)
    return rows


def build_fragility_rows(regime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str], list[Mapping[str, Any]]] = {}
    for row in regime_rows:
        grouped.setdefault(
            (
                str(row.get("source_scope")),
                str(row.get("artifact_slug")),
                str(row.get("view_id")),
                str(row.get("axis")),
            ),
            [],
        ).append(row)
    output: list[dict[str, Any]] = []
    for (source_scope, slug, view_id, axis), rows in grouped.items():
        nets = [to_float(row.get("net_profit")) or 0.0 for row in rows]
        total = sum(nets)
        best = max(rows, key=lambda row: to_float(row.get("net_profit")) or -math.inf)
        worst = min(rows, key=lambda row: to_float(row.get("net_profit")) or math.inf)
        negative_count = sum(1 for value in nets if value < 0)
        concentration = safe_div(to_float(best.get("net_profit")), total) if total and total > 0 else None
        judgment = "balanced_or_inconclusive"
        if negative_count and (to_float(worst.get("net_profit")) or 0.0) <= -25:
            judgment = "regime_loss_pocket"
        if concentration is not None and concentration >= 0.75 and len(rows) > 1:
            judgment = "one_bucket_concentration"
        if negative_count and concentration is not None and concentration >= 0.75:
            judgment = "loss_pocket_and_one_bucket_concentration"
        output.append(
            {
                "source_scope": source_scope,
                "artifact_slug": slug,
                "view_id": view_id,
                "axis": axis,
                "bucket_count": len(rows),
                "total_net_profit": total,
                "best_bucket": best.get("bucket"),
                "best_bucket_net": best.get("net_profit"),
                "best_bucket_trade_count": best.get("trade_count"),
                "worst_bucket": worst.get("bucket"),
                "worst_bucket_net": worst.get("net_profit"),
                "worst_bucket_profit_factor": worst.get("profit_factor"),
                "negative_bucket_count": negative_count,
                "best_bucket_net_share_of_positive_total": concentration,
                "fragility_judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def by_key(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[str, ...], Mapping[str, Any]]:
    return {tuple(str(row.get(key, "")) for key in keys): row for row in rows}


def build_source_view_rows(
    kpi_rows: Sequence[Mapping[str, str]],
    gap_rows: Sequence[Mapping[str, str]],
    cost_rows: Sequence[Mapping[str, str]],
    curve_rows: Sequence[Mapping[str, str]],
    mt5_rows: Sequence[Mapping[str, str]],
    fragility_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    kpi = by_key(kpi_rows, ["artifact_slug", "view_id"])
    cost = {
        (row["artifact_slug"], row["view_id"], row["extra_cost_per_round_trip_account_ccy"]): row
        for row in cost_rows
    }
    mt5 = {row["artifact_slug"]: row for row in mt5_rows}
    gap = {row["artifact_slug"]: row for row in gap_rows}
    worst_curve: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in curve_rows:
        key = (row["artifact_slug"], row["view_id"])
        if key not in worst_curve or (to_float(row.get("net_profit")) or 0.0) < (to_float(worst_curve[key].get("net_profit")) or 0.0):
            worst_curve[key] = row
    frag_by_key: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for row in fragility_rows:
        if not str(row.get("source_scope", "")).startswith("score_proxy_"):
            continue
        frag_by_key.setdefault((str(row.get("artifact_slug")), str(row.get("view_id"))), []).append(row)

    output: list[dict[str, Any]] = []
    for slug in sorted({row["artifact_slug"] for row in kpi_rows}):
        raw = kpi.get((slug, "raw_forward"), {})
        session = kpi.get((slug, "old_session_parity"), {})
        mt5_row = mt5.get(slug, {})
        gap_row = gap.get(slug, {})
        raw_cost1 = cost.get((slug, "raw_forward", "1.0"), {})
        session_cost1 = cost.get((slug, "old_session_parity", "1.0"), {})
        raw_worst = worst_curve.get((slug, "raw_forward"), {})
        session_worst = worst_curve.get((slug, "old_session_parity"), {})
        frag_rows = frag_by_key.get((slug, "raw_forward"), []) + frag_by_key.get((slug, "old_session_parity"), [])
        high_fragility_axes = sum(1 for row in frag_rows if row.get("fragility_judgment") != "balanced_or_inconclusive")
        output.append(
            {
                "artifact_slug": slug,
                "candidate_id": raw.get("candidate_id") or session.get("candidate_id"),
                "raw_proxy_trade_count": raw.get("trade_count"),
                "raw_proxy_net_profit": raw.get("net_profit"),
                "raw_proxy_profit_factor": raw.get("profit_factor"),
                "raw_proxy_dd": raw.get("max_drawdown"),
                "old_session_proxy_trade_count": session.get("trade_count"),
                "old_session_proxy_net_profit": session.get("net_profit"),
                "old_session_proxy_profit_factor": session.get("profit_factor"),
                "session_mt5_trade_count": mt5_row.get("trade_count"),
                "session_mt5_net_profit": mt5_row.get("net_profit"),
                "session_mt5_profit_factor": mt5_row.get("profit_factor"),
                "raw_session_gap_judgment": gap_row.get("gap_judgment"),
                "raw_session_signal_per_day_ratio": gap_row.get("raw_session_signal_per_day_ratio"),
                "exclusive_raw_signal_rate": gap_row.get("exclusive_raw_signal_rate"),
                "raw_cost_plus1_survives": raw_cost1.get("survives_pf_gt_1"),
                "session_cost_plus1_survives": session_cost1.get("survives_pf_gt_1"),
                "raw_worst_curve_net": raw_worst.get("net_profit"),
                "raw_worst_curve_chunk": raw_worst.get("chunk_id"),
                "session_worst_curve_net": session_worst.get("net_profit"),
                "high_fragility_axis_count": high_fragility_axes,
                "source_view_judgment": source_view_judgment(gap_row, raw_cost1, raw_worst, high_fragility_axes),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def source_view_judgment(
    gap_row: Mapping[str, Any],
    raw_cost1: Mapping[str, Any],
    raw_worst: Mapping[str, Any],
    high_fragility_axes: int,
) -> str:
    if gap_row.get("gap_judgment") == "raw_session_gap_high_pressure":
        return "raw_forward_density_pressure_blocks_forward_pass"
    if raw_cost1.get("survives_pf_gt_1") == "False":
        return "cost_fragility_blocks_forward_pass"
    if (to_float(raw_worst.get("net_profit")) or 0.0) <= -50:
        return "curve_pocket_fragility_blocks_forward_pass"
    if high_fragility_axes >= 4:
        return "multi_regime_fragility_review_required"
    return "watchlist_not_selection"


def build_directional_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = aggregate(trades, ["source_scope", "runtime_source", "artifact_slug", "candidate_id", "view_id", "direction"])
    totals = aggregate(trades, ["source_scope", "artifact_slug", "view_id"])
    total_by_key = by_key(totals, ["source_scope", "artifact_slug", "view_id"])
    for row in rows:
        total = total_by_key.get((row["source_scope"], row["artifact_slug"], row["view_id"]), {})
        row["net_share_of_source_view"] = safe_div(to_float(row.get("net_profit")), to_float(total.get("net_profit")))
        row["direction_judgment"] = "direction_loss_pocket" if (to_float(row.get("net_profit")) or 0.0) < 0 else "direction_positive_or_mixed"
        row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def build_month_hour_session_rows(fragility_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        row
        for row in fragility_rows
        if row.get("axis") in {"month", "hour", "session"} and str(row.get("source_scope", "")).startswith("score_proxy_")
    ]


def build_handoff_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap_id": "raw_forward_mt5_missing",
            "status": "missing_required_for_forward_pass",
            "evidence_path": rel(RUN330C_DIR / "runtime_parity_receipt.json"),
            "effect": "Raw-forward score proxy cannot be treated as MT5 tester output.",
        },
        {
            "gap_id": "db_source_unavailable",
            "status": "out_of_scope_by_claim",
            "evidence_path": rel(RUN330C_DIR / "db_attribution_report.csv"),
            "effect": "Stage330 non-identity surfaces do not reproduce cp322A D/B source attribution.",
        },
        {
            "gap_id": "tail_gap_in_forward_feature_frames",
            "status": "carried_from_run330B",
            "evidence_path": rel(RUN330B_DIR / "forward_data_availability_audit.csv"),
            "effect": "Forward data is usable for pressure review but not enough for final forward pass.",
        },
        {
            "gap_id": "session_mt5_reference_only",
            "status": "reference_not_authority",
            "evidence_path": rel(RUN330C_DIR / "session_mt5_reference_kpi_report.csv"),
            "effect": "Old-session MT5 positivity remains separated from raw-forward judgment.",
        },
    ]


def build_decision_payload(source_rows: Sequence[Mapping[str, Any]], fragility_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    blocking = [row for row in source_rows if "blocks_forward_pass" in str(row.get("source_view_judgment", ""))]
    high_fragility = [row for row in fragility_rows if row.get("fragility_judgment") != "balanced_or_inconclusive"]
    c56_watch = [
        row
        for row in source_rows
        if str(row.get("artifact_slug", "")).startswith("c56")
        and "blocks_forward_pass" not in str(row.get("source_view_judgment", ""))
    ]
    reason = "raw_forward_density_cost_or_regime_fragility_requires_runtime_probe_or_block"
    if not blocking and c56_watch:
        reason = "c56_watchlist_survives_attribution_but_runtime_gap_prevents_forward_pass"
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "selected_candidate": "none",
        "blocking_source_view_count": len(blocking),
        "high_fragility_axis_count": len(high_fragility),
        "watchlist_not_selection_count": len(c56_watch),
        "reason": reason,
        "next_action": NEXT_ACTION,
    }


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "T06_regime_attribution",
            "status": "completed_score_proxy_and_session_mt5_reference",
            "evidence_path": rel(RUN_DIR / "regime_attribution_unified.csv"),
            "effect": "Regime pockets are explicit before any forward decision.",
        },
        {
            "gate_name": "T07_long_short_and_source_attribution",
            "status": "completed_source_view_and_directional_attribution",
            "evidence_path": rel(RUN_DIR / "source_view_attribution_matrix.csv"),
            "effect": "Raw/session/source and long/short fragility are separated.",
        },
        {
            "gate_name": "runtime_raw_forward_mt5",
            "status": "not_completed_next_run_required",
            "evidence_path": rel(RUN_DIR / "handoff_gap_audit.csv"),
            "effect": "Missing raw-forward MT5 remains visible and blocks Forward Passed.",
        },
    ]


def infer_artifact_type(path: Path) -> str:
    if path.suffix.lower() == ".json":
        return "json_receipt"
    if path.suffix.lower() == ".md":
        return "review_report"
    if path.suffix.lower() == ".py":
        return "pipeline_script"
    return "csv_report"


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    inputs = [
        RUN330C_DIR / "score_proxy_trade_records.csv",
        RUN330C_DIR / "session_mt5_reference_trade_records.csv",
        RUN330C_DIR / "score_curve_proxy_kpi_report.csv",
        RUN330C_DIR / "score_cost_stress_report.csv",
        RUN330C_DIR / "score_curve_pocket_report.csv",
        RUN330C_DIR / "raw_session_curve_gap_report.csv",
        RUN330B_DIR / "forward_data_availability_audit.csv",
    ]
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "generated_at_utc": generated_at_utc,
        "inputs": [{"path": rel(path), "sha256": sha256_file(path)} for path in inputs],
        "artifacts": [
            {"path": rel(path), "sha256": sha256_file(path), "artifact_type": infer_artifact_type(path)}
            for path in artifacts
            if path.exists()
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_outputs(generated_at_utc: str) -> tuple[list[Path], dict[str, Any]]:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    proxy_trades = load_proxy_trades()
    mt5_trades = load_mt5_trades()
    all_trades = [*proxy_trades, *mt5_trades]
    regime_rows = build_unified_regime_rows(all_trades)
    fragility_rows = build_fragility_rows(regime_rows)
    directional_rows = build_directional_rows(all_trades)
    source_rows = build_source_view_rows(
        read_csv_rows(RUN330C_DIR / "score_curve_proxy_kpi_report.csv"),
        read_csv_rows(RUN330C_DIR / "raw_session_curve_gap_report.csv"),
        read_csv_rows(RUN330C_DIR / "score_cost_stress_report.csv"),
        read_csv_rows(RUN330C_DIR / "score_curve_pocket_report.csv"),
        read_csv_rows(RUN330C_DIR / "session_mt5_reference_kpi_report.csv"),
        fragility_rows,
    )
    month_hour_session_rows = build_month_hour_session_rows(fragility_rows)
    handoff_rows = build_handoff_gap_rows()
    decision_payload = build_decision_payload(source_rows, fragility_rows)

    artifacts: list[Path] = []
    artifacts.append(write_csv(RUN_DIR / "regime_attribution_unified.csv", list(regime_rows[0].keys()), regime_rows))
    artifacts.append(write_csv(RUN_DIR / "regime_fragility_matrix.csv", list(fragility_rows[0].keys()), fragility_rows))
    artifacts.append(write_csv(RUN_DIR / "source_view_attribution_matrix.csv", list(source_rows[0].keys()), source_rows))
    artifacts.append(write_csv(RUN_DIR / "directional_fragility_report.csv", list(directional_rows[0].keys()), directional_rows))
    artifacts.append(write_csv(RUN_DIR / "month_hour_session_pressure_report.csv", list(month_hour_session_rows[0].keys()), month_hour_session_rows))
    artifacts.append(write_csv(RUN_DIR / "handoff_gap_audit.csv", list(handoff_rows[0].keys()), handoff_rows))
    artifacts.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gate_rows()))
    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [
                    rel(RUN330C_DIR / "score_proxy_trade_records.csv"),
                    rel(RUN330C_DIR / "session_mt5_reference_trade_records.csv"),
                ],
                "time_axis": "Trade open/close timestamps are UTC-like strings carried from run330C score proxy and Stage329F MT5 reference.",
                "sample_scope": "2026-04-14+ forward raw/session proxy plus old-session MT5 reference.",
                "missing_or_duplicate_check": "Run330C coverage audit is inherited; run330D performs attribution only.",
                "feature_label_boundary": "No new labels, thresholds, features, or model training are introduced.",
                "split_boundary": "Latest forward remains read-only; Stage329F MT5 is reference only.",
                "leakage_risk": "Attribution could tempt selection of c56 watchlist; result judgment keeps no selection.",
                "data_hash_or_identity": sha256_file(RUN330C_DIR / "score_proxy_trade_records.csv"),
                "integrity_judgment": "usable_with_boundary_attribution_only",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "observed_change": "run330D decomposes run330C proxy and MT5 reference by regime, source view, and direction.",
                "comparison_baseline": PARENT_RUN_ID,
                "likely_drivers": "raw/session density, session-only MT5 reference, direction skew, month/hour/session pockets, volatility/ADX/VIX/USD/rate regimes",
                "segment_checks": "session, hour, month, volatility, ADX, VIX, USD, rate, direction, source view",
                "trade_shape": "source_view_attribution_matrix.csv and directional_fragility_report.csv",
                "alternative_explanations": "score proxy is not MT5; raw-forward MT5 output is still missing",
                "attribution_confidence": "medium_for_proxy_attribution_low_for_runtime_authority",
                "next_probe": NEXT_ACTION,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": RUN_ID,
                "evidence_available": "regime/source/direction attribution reports and inherited run330C score proxy/cost/curve evidence",
                "evidence_missing": "raw-forward MT5 tester output, runtime handoff parity, final forward decision",
                "judgment_label": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "Attribution found where the proxy is fragile, but it is not a pass or a failure without runtime proof.",
            },
        )
    )
    artifacts.append(write_json(RUN_DIR / "final_regime_attribution_decision.json", decision_payload))
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "forward_passed",
                "forward_failed",
                "goal_achieve",
                "selected_candidate",
                "next_action",
                "claim_boundary",
            ],
            [{**decision_payload, "run_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY}],
        )
    )
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
                "next_action": NEXT_ACTION,
                "external_verification_status": "out_of_scope_by_claim_attribution_only_raw_mt5_next",
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(Path(__file__))
    artifacts.extend(write_reports(source_rows, fragility_rows, directional_rows, decision_payload))
    artifacts.append(write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    return artifacts, decision_payload


def write_reports(
    source_rows: Sequence[Mapping[str, Any]],
    fragility_rows: Sequence[Mapping[str, Any]],
    directional_rows: Sequence[Mapping[str, Any]],
    decision_payload: Mapping[str, Any],
) -> list[Path]:
    report_path = REVIEWS_DIR / "run330D_regime_source_attribution_review.md"
    decision_path = DECISION_DOC
    source_lines = "\n".join(
        f"| {row['artifact_slug']} | {row['source_view_judgment']} | {csv_value(row.get('raw_proxy_net_profit'))} | {csv_value(row.get('raw_cost_plus1_survives'))} | {csv_value(row.get('raw_worst_curve_net'))} | {csv_value(row.get('raw_session_gap_judgment'))} |"
        for row in source_rows
    )
    worst_fragility = sorted(
        fragility_rows,
        key=lambda row: (0 if row.get("fragility_judgment") != "balanced_or_inconclusive" else 1, to_float(row.get("worst_bucket_net")) or 0.0),
    )[:10]
    fragility_lines = "\n".join(
        f"| {row['artifact_slug']} | {row['view_id']} | {row['axis']} | {row['worst_bucket']} | {csv_value(row.get('worst_bucket_net'))} | {row['fragility_judgment']} |"
        for row in worst_fragility
    )
    direction_losses = [row for row in directional_rows if row.get("direction_judgment") == "direction_loss_pocket"]
    report = f"""
# Run330D Regime Source Attribution Review(330D 국면 원천 귀속 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Source View Read(원천 보기 판독)

| artifact(산출물) | judgment(판정) | raw net(원본 순손익) | cost +1 survives(비용 +1 생존) | worst curve(최악 곡선) | gap(간극) |
|---|---|---:|---|---:|---|
{source_lines}

## Worst Regime Pockets(최악 국면 포켓)

| artifact(산출물) | view(보기) | axis(축) | bucket(구간) | worst net(최악 순손익) | judgment(판정) |
|---|---|---|---|---:|---|
{fragility_lines}

## Read(판독)

- blocking source views(차단 원천 보기): `{decision_payload.get('blocking_source_view_count')}`
- high fragility axes(고취약 축): `{decision_payload.get('high_fragility_axis_count')}`
- c56 watchlist not selection(c56 관찰 목록, 선택 아님): `{decision_payload.get('watchlist_not_selection_count')}`
- direction loss pockets(방향 손실 포켓): `{len(direction_losses)}`

Effect(효과): c56(코어56) 쪽은 watchlist(관찰 목록)에 남지만, m48/u42(raw-forward density pressure, 원본 전진 밀도 압력)와 raw-forward MT5 missing(원본 전진 MT5 누락)이 남아 Forward Passed(전진 통과)는 없다.

## Key Files(주요 파일)

- regime attribution(국면 귀속): `{rel(RUN_DIR / 'regime_attribution_unified.csv')}`
- fragility matrix(취약성 행렬): `{rel(RUN_DIR / 'regime_fragility_matrix.csv')}`
- source/view attribution(원천/보기 귀속): `{rel(RUN_DIR / 'source_view_attribution_matrix.csv')}`
- directional fragility(방향 취약성): `{rel(RUN_DIR / 'directional_fragility_report.csv')}`
- handoff gaps(인계 공백): `{rel(RUN_DIR / 'handoff_gap_audit.csv')}`

## Next(다음)

`{NEXT_ACTION}`
"""
    decision_doc = f"""
# Stage330D Regime Source Attribution Decision(330D 국면 원천 귀속 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Reason(이유)

run330D(330D 실행)는 run330C(330C 실행)의 score proxy(점수 대리검증)를 session/hour/month/volatility/ADX/VIX/USD/rate/direction(세션/시간/월/변동성/ADX/VIX/USD/금리/방향)으로 분해했다. Effect(효과): 어떤 숫자가 국면 포켓인지 드러냈지만, raw-forward MT5(원본 전진 MT5)가 없으므로 최종 forward decision(전진 결정)은 아직 없다.

- blocking source views(차단 원천 보기): `{decision_payload.get('blocking_source_view_count')}`
- high fragility axes(고취약 축): `{decision_payload.get('high_fragility_axis_count')}`
- next_action(다음 행동): `{NEXT_ACTION}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return [write_md(report_path, report), write_md(decision_path, decision_doc)]


def update_selection_status() -> Path:
    text, had_bom = read_text_lossless(SELECTION_STATUS)
    replacements = {
        "- stage_status(": "- stage_status(단계 상태): `open_regime_source_attribution_completed`",
        "- latest_completed_run(": f"- latest_completed_run(최신 완료 실행): `{RUN_ID}`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_ACTION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- effect(": "- effect(효과): run330D(330D 실행)는 국면/방향/원천 귀속을 만들었지만, raw-forward MT5가 없어 선택 후보와 Forward Passed(전진 통과)는 없다.",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    return write_text_lossless(SELECTION_STATUS, text, had_bom)


def update_current_truth() -> list[Path]:
    updated: list[Path] = []
    state_text, state_bom = read_text_lossless(WORKSPACE_STATE)
    state_text = replace_prefix_line(state_text, "current_run_id:", f"current_run_id: {NEXT_ACTION}")
    focus_marker = "current_focus:\n"
    focus_entry = (
        "current_focus:\n"
        "- >-\n"
        "  Stage330(330단계) run330D(330D 실행)는 `completed_regime_source_attribution_no_forward_decision`로 regime/source/direction attribution(국면/원천/방향 귀속)을 완료했다. Effect(효과): Forward Passed/Failed(전진 통과/실패) 없이 run330E(330E 실행)의 raw-forward MT5 runtime probe or block(원본 전진 MT5 런타임 탐침 또는 차단)으로 넘긴다.\n"
    )
    if focus_marker in state_text and "run330D(330D 실행)는 `completed_regime_source_attribution_no_forward_decision`" not in state_text:
        state_text = state_text.replace(focus_marker, focus_entry, 1)
    if "stage330D_regime_source_attribution:" not in state_text:
        state_text = state_text.rstrip() + f"""

stage330D_regime_source_attribution:
  run_id: {RUN_ID}
  status: {STATUS}
  decision: {DECISION}
  next_action: {NEXT_ACTION}
  selected_candidate: none
  forward_passed: not_claimed
  forward_failed: not_claimed
  goal_achieve: not_claimed
  effect: regime_source_direction_attribution_completed_without_raw_forward_mt5_or_selection
"""
    updated.append(write_text_lossless(WORKSPACE_STATE, state_text, state_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_run(", f"- current_run(현재 실행): `{NEXT_ACTION}`")
    current_text = replace_prefix_line(current_text, "- status(", "- status(상태): `stage330_run330D_regime_source_attribution_completed_runtime_probe_next`")
    current_text = replace_prefix_line(current_text, "- decision(", f"- decision(판정): `{DECISION}`")
    current_text = replace_prefix_line(current_text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    summary = (
        "- run330D_summary(330D 요약): regime/source/direction attribution(국면/원천/방향 귀속)을 `completed_regime_source_attribution_no_forward_decision`로 닫았다. "
        "Effect(효과): 국면 포켓과 원천 취약성을 분리했지만 raw-forward MT5(원본 전진 MT5)가 없어 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 없다."
    )
    if "run330D_summary(330D 요약)" not in current_text:
        current_text = current_text.replace("- run330C_summary", summary + "\n- run330C_summary", 1)
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    stage_block = f"""
## run330D_regime_source_attribution_summary(330D 국면 원천 귀속 요약)

- run(실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): regime/source/direction attribution(국면/원천/방향 귀속)을 만들었고, raw-forward MT5(원본 전진 MT5)가 없어 선택 후보와 Forward Passed(전진 통과)는 없다.
"""
    updated.append(append_if_missing(STAGE_BRIEF, "run330D_regime_source_attribution_summary", stage_block))
    changelog_entry = f"- 2026-05-26: Stage330(330단계) `{RUN_ID}` regime/source attribution(국면/원천 귀속)을 완료했다. 효과(effect, 효과): c56 watchlist(관찰 목록)와 m48/u42 raw density pressure(원본 밀도 압력)를 분리하고 Goal Achieve(목표 달성)는 주장하지 않는다."
    updated.append(append_if_missing(CHANGELOG, RUN_ID, changelog_entry))
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run330D_regime_source_attribution_review.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "regime_source_attribution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": "regime_source_direction_attribution;raw_forward_mt5_missing;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__regime_source_attribution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "regime_source_attribution",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "regime_source_direction_attribution",
                "tier_scope": "latest_forward_raw_session_proxy_and_session_mt5_reference",
                "kpi_scope": "regime_net_pf_trade_count_direction_source",
                "scoreboard_lane": "performance_attribution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "regime_bucket_net_pf",
                "guardrail_kpi": "source_view_judgment;handoff_gap_audit",
                "external_verification_status": "out_of_scope_by_claim_attribution_only_raw_mt5_next",
                "notes": "No candidate selection, no Forward Passed/Failed, no runtime authority.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__regime_source_attribution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "regime_source_attribution(국면 원천 귀속)",
                "tier_scope": "latest forward raw/session proxy and MT5 reference(최신 전진 원본/세션 대리검증과 MT5 참고)",
                "scoreboard": "performance_attribution(성과 귀속)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selection;no_forward_decision;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        if not path.exists():
            continue
        artifact_rows.append(
            {
                "artifact_id": f"run330D_{path.stem}",
                "artifact_type": infer_artifact_type(path),
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": "Run330D regime/source attribution artifact; no Forward Passed/Failed claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage330D regime/source attribution review.")
    parser.add_argument("--generated-at-utc", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated_at_utc = args.generated_at_utc or utc_now()
    artifacts, decision_payload = write_outputs(generated_at_utc)
    artifacts.extend([update_selection_status(), *update_current_truth()])
    update_registers(generated_at_utc, artifacts)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "artifact_count": len([path for path in artifacts if path.exists()]),
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
